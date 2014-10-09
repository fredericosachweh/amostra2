import calendar
from datetime import datetime
from decimal import Decimal as D

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.dateformat import format as date_format
from django.utils.translation import ugettext_lazy as _

from clients.models import Contract, Klass
from utils import EmailFromTemplate


class PaymentManager(models.Manager):
    def all_with_visits(self):
        """
        Adds classes visits and opens count to each instance.

        The instances are already annotated with classes cost sum.
        """
        qs = self.annotate(opens=models.Count('open', distinct=True),
                           visits=models.Count('visit', distinct=True))
        return qs


class Payment(models.Model):
    contract = models.ForeignKey(Contract, verbose_name=_('contract'))
    created_at = models.DateField(_('create at'), default=timezone.now)
    ref_date = models.DateField(_('reference date'))
    due_date = models.DateField(_('expiry date'))
    payment_date = models.DateField(_('payment date'), blank=True, null=True)
    was_paid = models.BooleanField(_('was paid'), default=False, editable=False)
    klasses = models.ManyToManyField(
        Klass, verbose_name=_('classes'), through='KlassPayment')
    cost = models.DecimalField(
        _('cost'), max_digits=7, decimal_places=2, blank=True, null=True)
    invoice_file = models.FileField(_('invoice file'), upload_to='payments/payment/invoice_file', blank=True, null=True)
    objects = PaymentManager()

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    def __unicode__(self):
        klasses = [unicode(k) for k in self.klasses.all()]
        if len(klasses) > 1:
            in_klass = _('in the classes')
        else:
            in_klass = _('in the class')
        klass_names = ', '.join(klasses)
        instructions = _('Referring to use of Mainiti Software {in_klass} '
                         '{klasses}, at month {month} of {year}, by the '
                         'company {client}.')
        return instructions.format(in_klass=in_klass,
                                   klasses=klass_names,
                                   client=self.contract.client,
                                   month=date_format(self.ref_date, 'F'),
                                   year=date_format(self.ref_date, 'Y'))

    @models.permalink
    def get_absolute_url(self):
        return ('payments:payment-detail', (), {'pk': self.pk})

    def save(self, *args, **kwargs):
        """
        Updates the was_paid flag based in the existence of a payment date.
        Also sets the ref_date as the creation date when not specified.
        """
        if self.payment_date:
            self.was_paid = True
        else:
            self.was_paid = False

        if not self.ref_date:
            self.ref_date = self.created_at
        return super(Payment, self).save(*args, **kwargs)

    @property
    def client(self):
        return self.contract.client

    def is_expired(self):
        """ Tells when a payment is expired and can't be paid anymore. """
        return self.due_date < timezone.now().date()


def update_contract_status(sender, instance, **kwargs):
    """
    Set contracts payment status based on payment saved or deleted.

    Each time a payment is saved or deleted, if any payment is pending until
    the last day of the current month, the contract is marked as pending too.
    """
    today = timezone.now()
    first_weekday, last_day = calendar.monthrange(today.year, today.month)
    last_date = datetime(today.year, today.month, last_day, 23, 59)

    pending_payments = instance.contract.payment_set.filter(
        ref_date__lte=last_date, was_paid=False)
    instance.contract.pending_payment = bool(pending_payments.exists())
    instance.contract.save(update_fields=['pending_payment'])
models.signals.post_save.connect(update_contract_status, sender=Payment)
models.signals.post_delete.connect(update_contract_status, sender=Payment)

def send_payment_email(sender, instance, **kwargs):
    """
    Send email once when first define an invoice.
    """
    try:
        old_instance = Payment.objects.get(pk=instance.pk)
        old_invoice = old_instance.invoice_file
    except Payment.DoesNotExist:
        old_invoice = None
    if instance.invoice_file and instance.invoice_file != old_invoice:
        managers = instance.contract.client.managers.all()
        email = EmailFromTemplate(
            subject=_('Invoice from Mainiti'),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[m.email for m in managers],
            template_name='payments/invoice_email',
            context={'payment': instance},
        )
        email.send()
models.signals.pre_save.connect(send_payment_email, sender=Payment)


class Visit(models.Model):
    """Counts how many times a payment shown his details for an user."""
    payment = models.ForeignKey(Payment, verbose_name=_('payment'))
    created_at = models.DateField(_('create at'), default=timezone.now)

    class Meta:
        verbose_name = _('visit of payment')
        verbose_name_plural = _('visits of payments')


class Open(models.Model):
    """Counts how many times a payment was exported to PDF for printing."""
    payment = models.ForeignKey(Payment, verbose_name=_('payment'))
    created_at = models.DateField(_('create at'), default=timezone.now)

    class Meta:
        verbose_name = _('opening of payment')
        verbose_name_plural = _('opening of payments')


class KlassPayment(models.Model):
    """
    Joins the Klass with the Payment storing the class current_cost.

    Each time a class have his current_cost updated, it would updates the
    future klass payments to adjust the payments cost.
    """
    klass = models.ForeignKey(Klass, verbose_name=_('class'))
    payment = models.ForeignKey(Payment, verbose_name=_('payment'))
    created_at = models.DateField(_('create at'), default=timezone.now)
    update_at = models.DateField(_('update_at'), default=timezone.now)
    current_cost = models.DecimalField(_('current cost'),
                                       max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = _('payment value of class')
        verbose_name_plural = _('payments values of classes')

    def save(self, *args, **kwargs):
        """
        Defines the updated at var to a now() each time is saved and caches the
        klass cost a first time.
        """
        if self.pk:
            self.update_at = timezone.now()

        if not self.pk:
            self.current_cost = self.klass.cost
        return super(KlassPayment, self).save(*args, **kwargs)


def set_payment_cost(sender, instance, **kwargs):
    """
    Denormalizes the payment cost after save or delete a klass payment.

    If payment value lower than settings.PAYMENT_MIN change due_date to next
    month.
    """
    payment = instance.payment
    aggr = payment.klasspayment_set.aggregate(cost=models.Sum('current_cost'))
    full_cost = aggr['cost']
    if not full_cost:
        payment.cost = None
    else:
        today = payment.ref_date
        weekday, days_in_month = calendar.monthrange(today.year, today.month)
        month_range = (days_in_month - today.day + 1) / D(days_in_month)
        cost = full_cost * month_range
        if cost >= settings.MINIMAL_PAYMENT_COST:
            payment.cost = full_cost * month_range
        else:
            ref_date = datetime(today.year + (today.month / 12),
                                ((today.month % 12) + 1), 1)

            payment.ref_date = ref_date
            payment.cost = full_cost

    payment.save(update_fields=['cost', 'ref_date'])
models.signals.post_save.connect(set_payment_cost, sender=KlassPayment)
models.signals.post_delete.connect(set_payment_cost, sender=KlassPayment)
