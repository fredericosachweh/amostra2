import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from demonstrations import forms, models
from payments.models import Payment
from utils import split_name, EmailFromTemplate
from utils.models import id_as_username, generate_random_passwords
from utils.views import PdfMixin, MultipleFormsView


class DemonstrationMixin(object):
    @cached_property
    def demonstration(self):
        return get_object_or_404(models.Demonstration, pk=self.kwargs['pk'])


class StartView(generic.DetailView):
    """
    Shows the client data to be confirmed by the user.
    """
    template_name = 'demonstrations/purchase/start.html'
    model = models.Demonstration

    def get(self, request, *args, **kwargs):
        if not self.get_object().client.has_complete_data():
            return redirect('demonstrations:purchase:client-update', pk=kwargs['pk'])
        return super(StartView, self).get(request, *args, **kwargs)


class ClientUpdateView(DemonstrationMixin, generic.UpdateView):
    """
    Offers a way to the client update his data after conference.
    """
    form_class = forms.ClientUpdateForm
    template_name = 'demonstrations/purchase/client_update.html'

    def get_object(self):
        return self.demonstration.client

    def get_success_url(self):
        messages.success(self.request, _('Client update successful'))
        return reverse('demonstrations:purchase:start',
                       kwargs={'pk': self.demonstration.pk})


class ContractAgreeView(DemonstrationMixin, generic.UpdateView):
    """
    Shows the contract to the user and, after his agree, creates a new contract
    instance for the client document.
    """
    template_name = 'demonstrations/purchase/contract_agree.html'
    form_class = forms.ContractAgreeForm

    def get_object(self):
        return self.demonstration.client

    def get_success_url(self):
        self.demonstration.client.contract_set.get_or_create(
            document=self.demonstration.client.cnpj)
        return reverse('demonstrations:purchase:klasses-create',
                       kwargs={'pk': self.demonstration.pk})


class ContractPrintView(PdfMixin, DemonstrationMixin, generic.TemplateView):
    template_name = 'demonstrations/purchase/contract_print.html'
    print_header_title = _('Service agreement contract')


class KlassesCreateView(DemonstrationMixin, MultipleFormsView):
    """
    Let the user create classes for the only one contract.
    """
    template_name = 'demonstrations/purchase/klasses_create.html'
    form_classes = {
        'managers': forms.ManagerFormSet,
        'klasses': forms.KlassFormSet,
    }

    @cached_property
    def contract(self):
        """
        Returns the client's contract, assumes there will be only one.
        """
        return self.demonstration.client.contract_set.get()

    def get_forms_kwargs(self):
        kwargs = super(KlassesCreateView, self).get_forms_kwargs()
        kwargs['klasses'].update({
            'prefix': 'klasses',
            'queryset': self.contract.klass_set.all()
        })
        kwargs['managers'].update({
            'prefix': 'managers',
            'queryset': self.demonstration.client.managers.all()
        })
        return kwargs

    @method_decorator(transaction.commit_on_success)
    def forms_valid(self, forms):
        self.create_managers(forms['managers'])
        self.create_klasses(forms['klasses'])
        self.create_payment()
        return redirect('demonstrations:purchase:payment',
                        pk=self.demonstration.pk)

    def create_managers(self, form):
        """
        Creates specified managers, reusing then if already exists.

        Sets a random password for the just created users and sends an
        invitation email for each manager, reused or created (in this case,
        with his password).
        """
        for f in form:
            user = f.save(commit=False)
            if not user.username:
                user.username = id_as_username(prefix='user')
            if not user.pk:
                password = generate_random_passwords(1, flat=True)
                user.set_password(password)
            else:
                password = None
            user.save()
            self.demonstration.client.managers.add(user)

            # warn each user that he was invited as a manager
            email = EmailFromTemplate(
                subject=_('Welcome to Mainiti'),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
                template_name='demonstrations/purchase/manager_created_email',
                context={'user': user,
                         'password': password,
                         'client': self.demonstration.client},
            )
            email.send()

    def create_teacher(self, name, email):
        """
        Creates and returns users not found by email, otherwise, reuse them.

        Returns the user instance and the password used when created, or None
        if the password wasn't set because the user already exists.
        """
        try:
            user = User.objects.get(email=email)
            password = None
        except User.DoesNotExist:
            first_name, last_name = split_name(name)
            user = User(
                username=id_as_username(prefix='teacher'),
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            password = generate_random_passwords(1, flat=True)
            user.set_password(password)
            user.save()
        return user, password

    def create_klasses(self, form):
        """
        Create the specified klasses.

        The classes will end in the last day of year with the specified
        teacher (reusing it if already exists).
        """
        self.klasses = []  # stores created klasses to be attached to payments

        teachers = {}  # stores teachers as they are created to be reused
        now = timezone.now()
        end_date = datetime.date(now.year, 12, 31)
        for f in form:
            klass = f.save(commit=False)
            klass.contract = self.contract
            klass.end_date = end_date

            name = f.cleaned_data['teacher_name']
            email = f.cleaned_data['teacher_email']
            if email in teachers:
                teacher, password = teachers[email]
            else:
                teacher, password = self.create_teacher(name, email)
                teachers[teacher.email] = (teacher, password)

            klass.teacher = teacher
            klass.save()

            self.klasses.append(klass)

            # Also glue the user instance with the client through Teacher M2M
            qs = self.demonstration.client.teacher_set.filter(teacher=teacher)
            if not qs.exists():
                self.demonstration.client.teacher_set.create(teacher=teacher,
                                                             is_confirmed=True)

        # warn each user that he was invited as a teacher
        for user, password in teachers.values():
            email = EmailFromTemplate(
                subject=_('Welcome to Mainiti'),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
                template_name='managers/clients/teacher_created_email',
                context={'user': user,
                         'password': password,
                         'clients': [self.demonstration.client]},
            )
            email.send()

    def create_payment(self):
        """
        Creates a proportional payment for the client for the current month.

        If the payment is greater than a limit, create it, otherwise, create a
        full month payment referring the next month.
        """
        today = timezone.now().date()
        due_date = today + datetime.timedelta(days=1)

        try:
            payment = self.contract.payment_set.get()
            previous_cost = payment.cost
            previous_due_date = payment.due_date
        except Payment.DoesNotExist:
            payment = self.contract.payment_set.create(due_date=due_date,
                                                       ref_date=due_date)
            for klass in self.klasses:
                payment.klasspayment_set.create(klass=klass)
        else:
            # Updates the due_date and ref_date of the payment if it is expired
            if payment.is_expired():
                payment.due_date = payment.ref_date = due_date
                payment.save()

            # Adds any new class to the payment
            in_payment_klasses = list(payment.klasses.all())
            for klass in self.klasses:
                if klass in in_payment_klasses:
                    in_payment_klasses.remove(klass)
                else:
                    payment.klasspayment_set.create(klass=klass)

            # Removes any unwanted klass
            if in_payment_klasses:
                qs = payment.klasspayment_set.filter(
                    klass__in=in_payment_klasses)
                qs.delete()

            payment = self.contract.payment_set.get()
            if payment.cost != previous_cost or payment.due_date != previous_due_date:
                messages.warning(
                    self.request,
                    _('The payment was updated, make sure you '
                      'print the new version!')
                )


class PaymentView(generic.DetailView):
    template_name = 'demonstrations/purchase/payment.html'
    model = models.Demonstration

    def get_context_data(self, **kwargs):
        contract = self.object.client.contract_set.get()
        context = super(PaymentView, self).get_context_data(**kwargs)
        context['klasses'] = contract.klass_set.count()
        context['payment'] = contract.payment_set.get()
        return context
