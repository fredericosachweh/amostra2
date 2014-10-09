import csv

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_comma_separated_integer_list
from django_localflavor_br import forms as br_forms, br_states

import models
from accounts.models import UserAccount
from exercises.models import Program, Module
from utils import split_name


class KlassSearchForm(forms.Form):
    """
    Searches a klass by his key to make login onto it.
    """
    klass = forms.CharField(label=_('Key'))

    def clean_klass(self):
        klass_key = self.cleaned_data['klass']
        try:
            klass = models.Klass.objects.get(key__iexact=klass_key)
        except models.Klass.DoesNotExist:
            raise forms.ValidationError(_('Klass key not found'))
        return klass


class ContractForm(forms.ModelForm):
    class Meta:
        model = models.Contract
        fields = ('client',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContractForm, self).__init__(*args, **kwargs)
        qs = models.Client.objects.filter(managers=user)
        self.fields['client'].queryset = qs
        self.fields['client'].empty_label = _('select a client...')


class KlassForm(forms.ModelForm):
    class Meta:
        model = models.Klass
        fields = ('name', 'teacher', 'end_date')

    def __init__(self, *args, **kwargs):
        contract = kwargs.pop('contract', None)
        super(KlassForm, self).__init__(*args, **kwargs)

        if contract is None:
            if self.instance.pk is None:
                raise ValueError('You must specify a contract or a saved instance')
            else:
                contract = self.instance.contract

        # the UserAccount is a proxy model that represents itself better than
        # the default django User model
        qs = UserAccount.objects.filter(involved_to_clients=contract.client)
        self.fields['teacher'].queryset = qs
        self.fields['teacher'].empty_label = _('select a teacher...')
        self.fields['teacher'].help_text = _('The class will be operated by a teacher but you can leave this field blank until the teacher is registered.')

        # adds a datepicker for the end_date
        self.fields['end_date'].widget = forms.TextInput(attrs={'data-datepicker': ''})


class TeacherUpdateForm(forms.Form):
    clients = forms.ModelMultipleChoiceField(queryset=models.Client.objects.none(),
                                             widget=forms.CheckboxSelectMultiple,
                                             required=True)

    def __init__(self, *args, **kwargs):
        manager = self.manager = kwargs.pop('manager')
        super(TeacherUpdateForm, self).__init__(*args, **kwargs)

        # if there is only one client for the manager, we don't need to
        # show a field to choose it...
        qs = manager.managed_clients.all()
        if qs.count() > 1:
            self.fields['clients'].queryset = qs
        else:
            del(self.fields['clients'])


class TeacherCreateForm(TeacherUpdateForm):
    name = forms.CharField(max_length=100, label=_('name'))
    email = forms.EmailField(label=_('e-mail'))

    def __init__(self, *args, **kwargs):
        super(TeacherCreateForm, self).__init__(*args, **kwargs)
        # forces the clients to be the last field
        if 'clients' in self.fields:
            self.fields.keyOrder.remove('clients')
            self.fields.keyOrder.append('clients')

    def clean_name(self):
        """ Returns the name as a tuple of first name and last name. """
        name = self.cleaned_data['name']
        return split_name(name)

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = models.Teacher.objects.filter(client__managers=self.manager,
                                           teacher__email=email)
        if qs.exists():
            raise forms.ValidationError(_('There is already a teacher with this email in your company.'))
        return email


class BaseKlassConfigForm(forms.Form):
    program = forms.ModelChoiceField(
        label=_('Program'),
        queryset=Program.objects.all(),
        widget=forms.RadioSelect,
        required=True
    )
    start_date = forms.DateField(
        label=_('Start date'),
        required=True,
        widget=forms.TextInput(attrs={'data-datepicker': ''})
    )
    end_date = forms.DateField(
        label=_('End date'),
        required=True,
        widget=forms.TextInput(attrs={'data-datepicker': ''})
    )
    modules = forms.CharField(
        label=_('Modules'),
        required=True,
        widget=forms.HiddenInput,
        validators=[validate_comma_separated_integer_list]
    )

    def __init__(self, *args, **kwargs):
        klass = self.klass = kwargs.pop('klass')
        super(BaseKlassConfigForm, self).__init__(*args, **kwargs)

        d = self.fields['end_date']
        d.initial = klass.end_date

        self.programs_choices = self.fields['program'].queryset
        self.modules_choices = Module.objects.all()

    def clean_modules(self):
        modules = self.cleaned_data['modules']
        return [int(x) for x in modules.split(',')]


class KlassRescheduleForm(BaseKlassConfigForm):
    pass


class KlassStartForm(BaseKlassConfigForm):
    students = forms.CharField(label=_('Students'), widget=forms.widgets.Textarea)

    def clean_students(self):
        """
        Ignore blanks lines and remove trailing spaces in the student name.
        Validates that the students count match the limit and that there is not
        repeated name.
        """
        names = [n.strip() for n in self.cleaned_data['students'].splitlines()]
        names = filter(None, names)  # remove blank lines
        if len(names) > self.klass.max_students:
            msg = _('You cannot set more than {0} students.')
            raise forms.ValidationError(msg.format(self.klass.max_students))

        seen = set()
        for name in names:
            if name in seen:
                msg = _('The name {0} appears more than once.')
                raise forms.ValidationError(msg.format(name))
            seen.add(name)

        return [split_name(n) for n in names if n]


class KlassPasswdForm(forms.ModelForm):
    class Meta:
        model = models.Klass
        fields = ('students',)


class KlassLoginForm(AuthenticationForm):
    """
    Offer the names of available students in the classroom to login and avoid
    login with a user outside the klass.
    """
    def __init__(self, *args, **kwargs):
        klass = kwargs.pop('klass')
        super(KlassLoginForm, self).__init__(*args, **kwargs)

        # TODO order by must come from the custom user model
        students = [(u.username, u.get_full_name()) for u in klass.students.all().order_by('first_name', 'last_name')]
        self.fields['username'] = forms.ChoiceField(label=_('Name'), choices=students, widget=forms.RadioSelect)


class PerformanceForm(forms.Form):
    start_date = forms.DateField(label=_('Start'))
    end_date = forms.DateField(label=_('End'))

    def __init__(self, *args, **kwargs):
        klass = kwargs.pop('klass')
        super(PerformanceForm, self).__init__(*args, **kwargs)

        self.fields['start_date'].initial = klass.program_usage.start_date
        self.fields['end_date'].initial = klass.program_usage.end_date


class ClientImportForm(forms.Form):
    csv_data = forms.FileField()

    keys = ('name', 'company_name', 'cnpj', 'phones', 'email', 'address', 'number',
            'complement', 'quarter', 'postal_code', 'city', 'state')

    def clean_csv_data(self):
        reader = csv.reader(self.cleaned_data['csv_data'])
        lines = []
        current_line = 0
        first_ignored = False
        for row in reader:
            current_line += 1
            if not first_ignored:
                first_ignored = True
                continue

            if len(row) != len(self.keys):
                s = _('Expected {exp} columns, found {fnd} at line {line}.')
                raise forms.ValidationError(s.format(exp=len(self.keys),
                                               fnd=len(row),
                                               line=current_line))

            data = dict(zip(self.keys, row))

            if data['name'] == '':
                raise forms.ValidationError(_('Name cannot be blank at line: {0}').format(current_line))

            if data['cnpj'] == '':
                data['cnpj'] = None  # blank CNPJ must be null for unique's integrity
            else:
                cnpj = br_forms.BRCNPJField()
                data['cnpj'] = ''.join([d for d in data['cnpj'] if d.isdigit()])
                try:
                    cnpj.clean(data['cnpj'])
                except forms.ValidationError:
                    raise forms.ValidationError(_('Error found on CNPJ at line: {0}.').format(current_line))
            if models.Client.objects.filter(cnpj__exact=data['cnpj']).exists():
                raise forms.ValidationError(_('CNPJ already exists at line: {0}.').format(current_line))

            data['email'] = data['email'].strip().lower()
            if data['email']:
                email_field = forms.EmailField()
                try:
                    email_field.clean(data['email'])
                except forms.ValidationError:
                    raise forms.ValidationError(_('Error found on the email at line: {0}.').format(current_line))

            # check if state its contained at state list
            state = data['state'].upper()
            choices = [k for k, v in br_states.STATE_CHOICES]
            if state and state not in choices:
                raise forms.ValidationError(_('State must be with 2 characters length at line: {0}.').format(current_line))
            else:
                data['state'] = state

            lines.append(data)

        return lines
