import random
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from utils.models import generate_random_passwords


CLIENT_STATUS = [
    ('suspect', _('Suspect')),
    ('prospect', _('Prospect')),
    ('lead', _('Lead')),
    ('active', _('Active')),
    ('frozen', _('Frozen')),
    ('inactive', _('Inactive')),
    ('suspended', _('Suspended')),
    ('cancelled', _('Cancelled')),
    ('removed', _('Removed')),
]


class Client(models.Model):
    name = models.CharField(_('name'), max_length=255)
    owner = models.ForeignKey(User, verbose_name=_('responsible'), related_name='owned_clients', blank=True, null=True)
    managers = models.ManyToManyField(User, verbose_name=_('managers'), related_name='managed_clients', blank=True)
    teachers = models.ManyToManyField(User, verbose_name=_('teachers'), related_name='involved_to_clients', blank=True, through='Teacher')
    company_name = models.CharField(_('company name'), max_length=255, blank=True)
    cnpj = models.CharField(_('CNPJ number'), max_length=19, blank=True, null=True, unique=True, default=None)
    phones = models.TextField(_('phones'), blank=True)
    email = models.EmailField(_('email'), blank=True)
    site = models.CharField(_('site'), max_length=255, blank=True)
    address = models.CharField(_('address'), max_length=255, blank=True)
    number = models.CharField(_('number'), max_length=50, blank=True)
    complement = models.CharField(_('complement'), max_length=150, blank=True)
    quarter = models.CharField(_('quarter'), max_length=150, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=10, blank=True)
    city = models.CharField(_('city'), max_length=255, blank=True)
    state = models.CharField(_('state'), max_length=2, blank=True)
    status = models.CharField(_('status'), max_length=20, choices=CLIENT_STATUS, default='suspect', editable=False)
    has_agreed = models.BooleanField(_('has agreed with contract?'), default=False)

    external_source = models.CharField(_('external source'), max_length=255, blank=True)
    external_code = models.CharField(_('external code'), max_length=255, blank=True)
    adm_structure = models.CharField(_('administrative structure'), max_length=255, blank=True)
    private_school_category = models.CharField(_('private school category'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    def __unicode__(self):
        return self.name

    def has_complete_data(self):
        """
        Returns False when there is any mandatory data missing.
        """
        return bool(self.cnpj)  # TODO for now, only the cnpj number is
                                # required, we need to define which fields are
                                # required too


def add_user_to_managers(sender, instance, action, **kwargs):
    """
    Adds the user to the managers group when the number of clients whose the
    user is related to as manager is more than zero.
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        if kwargs['pk_set'] is None:
            return  # FIXME it's running post_clear before post_add

        users = User.objects.filter(pk__in=kwargs['pk_set'])
        managers_group = Group.objects.get(name='managers')
        for user in users:
            clients = user.managed_clients.count()
            if clients > 0:
                user.groups.add(managers_group)
            else:
                user.groups.remove(managers_group)
models.signals.m2m_changed.connect(add_user_to_managers,
                                   sender=Client.managers.through)


def log_client_status_changes(sender, instance, **kwargs):
    try:
        old_instance = Client.objects.get(pk=instance.pk)
    except Client.DoesNotExist:
        return

    if instance.status != old_instance.status:
        content = _('Status changed from {0} to {1}.')
        instance.followup_set.create(
            content=content.format(old_instance.status, instance.status))
models.signals.pre_save.connect(log_client_status_changes, sender=Client)


class Contract(models.Model):
    """
    A contract represents a group of classes. Some client can have more than
    one contract so he can have separated bills and invoices.
    """
    client = models.ForeignKey(Client, verbose_name=_('client'))
    number = models.CharField(_('number'), max_length=8, unique=True, editable=False)
    created_at = models.DateTimeField(_('created at'), default=timezone.now, editable=False)
    document = models.CharField(_('document'), max_length=20, blank=True)
    klasses_count = models.IntegerField(_('classes count'), default=0, editable=False)
    payment_day = models.IntegerField(_('day of payment'), default=settings.PAYMENT_DAY)
    pending_payment = models.BooleanField(_('any pending payment?'), default=False, editable=False)

    class Meta:
        verbose_name = _('contract')
        verbose_name_plural = _('contracts')
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.number


def gen_contract_number(sender, instance, **kwargs):
    """ Generates an eight digits random string (to let text search). """
    if instance.pk is None:
        number = int(random.random() * 10 ** 8)
        instance.number = unicode(number)
models.signals.pre_save.connect(gen_contract_number, sender=Contract)


class Teacher(models.Model):
    """
    A teacher relates the client and the user. It is the "through" class of the
    m2m relationship.

    It also tells if the user has confirmed his relation with
    the client and how many classes the user teaches.
    """
    client = models.ForeignKey(Client)
    teacher = models.ForeignKey(User, verbose_name=_('teacher'))
    is_confirmed = models.BooleanField(_('is confirmed?'), default=True)

    class Meta:
        unique_together = ('client', 'teacher')
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')

    def __unicode__(self):
        return self.teacher.first_name


def add_user_to_clients(sender, instance, **kwargs):
    """
    Adds the user to the clients group when the number of clients whose the
    user is related to as teacher is more than zero.
    """
    clients = instance.teacher.involved_to_clients.count()
    teachers_group = Group.objects.get(name='teachers')
    if clients > 0:
        instance.teacher.groups.add(teachers_group)
    else:
        instance.teacher.groups.remove(teachers_group)
models.signals.post_save.connect(add_user_to_clients, sender=Teacher)
models.signals.pre_delete.connect(add_user_to_clients, sender=Teacher)


class KlassManager(models.Manager):
    def active(self):
        """
        Filter klasses currently running from up to date contracts.

        Up to date contracts are the ones with one or more payments but not
        pending.
        """
        today = timezone.now().date()
        qs = self.filter(end_date__gte=today,
                         contract__payment__isnull=False,
                         contract__pending_payment=False)
        return qs

    def late_payment(self):
        """
        Lists classes unaccessible by tearcher and students.

        Lists classes with more than one payment, with one of then late (case
        of continuated contract classes), or classes with only one unpaid (not
        even late) payment (case of new contract classes).
        """
        late_limit = timezone.now() - timedelta(days=settings.LATE_PAYMENT)
        qs = self.annotate(payment_count=models.Count('contract__payment'))
        qs = qs.filter(
            (models.Q(payment_count=1) &
             models.Q(payment__payment_date__isnull=True)) |
            (models.Q(payment_count__gt=1) &
             models.Q(payment__due_date__lte=late_limit) &
             models.Q(payment__payment_date__isnull=True))
        )
        return qs


class Klass(models.Model):
    contract = models.ForeignKey(Contract, verbose_name=_('contract'))
    name = models.CharField(_('name'), max_length=255)
    max_students = models.IntegerField(_('max students'), default=50)
    teacher = models.ForeignKey(User, verbose_name=_('teacher'), related_name='taught_klasses', blank=True, null=True)
    end_date = models.DateField(_('end date'), help_text=_('E.g.: the end of school year.'))
    students = models.ManyToManyField(User, verbose_name=_('students'), related_name='took_klasses')
    students_count = models.IntegerField(_('students count'), default=0, editable=False)
    password_list_printed_at = models.DateTimeField(_('password list printed' ' at'), blank=True, null=True, editable=False)

    key = models.CharField(_('key'), max_length=10, unique=True, db_index=True, editable=False)
    cost = models.DecimalField(_('cost'), max_digits=10, decimal_places=2, default=settings.KLASSES_COST)

    objects = KlassManager()

    class Meta:
        verbose_name = _('class')
        verbose_name_plural = _('classes')

    def __unicode__(self):
        return self.name

    @property
    def client(self):
        return self.contract.client


def generate_klass_key(sender, instance, **kwargs):
    if not instance.key:
        keys = generate_random_passwords(1, length=4)
        instance.key = keys[0]
models.signals.pre_save.connect(generate_klass_key, sender=Klass)


def count_contract_klasses(sender, instance, **kwargs):
    """
    Denormalize the classes count of a contract.
    """
    instance.contract.klasses_count = instance.contract.klass_set.count()
    instance.contract.save()
models.signals.post_save.connect(count_contract_klasses, sender=Klass)

#TODO pre-delete seems to be a mistake,
#the count would get the almost deleted class
models.signals.pre_delete.connect(count_contract_klasses, sender=Klass)


def count_klass_students(sender, instance, action, **kwargs):
    """
    Denormalize the students count of a klass.
    """
    if action in ['post_add', 'post_delete', 'post_clear']:
        instance.students_count = instance.students.count()
        instance.save()
models.signals.m2m_changed.connect(count_klass_students,
                                   sender=Klass.students.through
                                   )


def add_user_to_students(sender, instance, action, **kwargs):
    """
    Adds the user to the students group when the number of klasses whose the
    user is related to is more than zero.
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        if kwargs['pk_set'] is None:
            return  # FIXME it's running post_clear before post_add
        users = User.objects.filter(pk__in=kwargs['pk_set'])
        students_group = Group.objects.get(name='students')
        for user in users:
            klasses = user.took_klasses.count()
            if klasses > 0:
                user.groups.add(students_group)
            else:
                user.groups.remove(students_group)
models.signals.m2m_changed.connect(add_user_to_students,
                                   sender=Klass.students.through
                                   )


class Role(models.Model):
    name = models.CharField(_('name'), max_length=100)
    mandatory = models.BooleanField(_('mandatory'), default=False,
        help_text=_('Mark this to force at least one person in this role when saving a client.'))

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __unicode__(self):
        return self.name


class Person(models.Model):
    client = models.ForeignKey(Client, verbose_name=_('client'), blank=True, null=True)
    name = models.CharField(_('name'), max_length=255)
    email = models.EmailField(_('e-mail'), max_length=254, blank=True)
    telephone = models.CharField(_('telephone'), max_length=14, blank=True)
    cellphone = models.CharField(_('cellphone'), max_length=14, blank=True)
    roles = models.ManyToManyField(Role, verbose_name=_('roles'), related_name='participating_roles', blank=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    @property
    def fancy_name(self):
        roles = ', '.join([r.name for r in self.roles.all()])
        if roles:
            roles = '(' + roles + ')'
        return u'{0} <{1}> {2}'.format(self.name, self.email, roles)
