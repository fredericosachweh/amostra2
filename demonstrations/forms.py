from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_localflavor_br import forms as br_forms

import models
from clients.models import Client, Person, Klass


class PersonForDemonstrationForm(forms.ModelForm):
    client_name = forms.CharField(label=_('Entity name'))

    class Meta:
        model = Person
        exclude = ('roles', 'client')

    def __init__(self, *args, **kwargs):
        super(PersonForDemonstrationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder.remove('client_name')
        self.fields.keyOrder.insert(0, 'client_name')
        self.fields['email'].required = True
        self.fields['telephone'].required = True


class DemonstrationSendForm(forms.Form):
    emails = forms.MultipleChoiceField(
        label=_('Persons'),
        widget=forms.CheckboxSelectMultiple
    )
    greeting = forms.CharField(
        label=_('Greeting'),
        widget=forms.Textarea,
        required=False
    )

    def __init__(self, emails, *args, **kwargs):
        super(DemonstrationSendForm, self).__init__(*args, **kwargs)
        self.fields['emails'].choices = emails
        self.fields['emails'].initial = [email for email, name in emails]


class DemonstrationStartForm(forms.ModelForm):
    class Meta:
        model = models.Demonstration
        fields = ('has_agreed',)

    def __init__(self, *args, **kwargs):
        super(DemonstrationStartForm, self).__init__(*args, **kwargs)
        self.fields['has_agreed'].label = _('I read and agree with terms')

    def clean_has_agreed(self):
        has_agreed = self.cleaned_data['has_agreed']
        if not has_agreed:
            raise forms.ValidationError(_('You must agree with the terms!'))
        return has_agreed


class ClientUpdateForm(forms.ModelForm):
    """
    Form to the client update his own data.
    """
    cnpj = br_forms.BRCNPJField(label=_('CNPJ Number'), required=True)

    class Meta:
        model = Client
        fields = ('name', 'company_name', 'cnpj', 'phones', 'address', 'number',
                  'complement', 'quarter', 'city', 'state', 'postal_code')


class ContractAgreeForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('has_agreed',)

    def __init__(self, *args, **kwargs):
        super(ContractAgreeForm, self).__init__(*args, **kwargs)
        self.fields['has_agreed'].label = _('I read and agree with contract')

    def clean_has_agreed(self):
        has_agreed = self.cleaned_data['has_agreed']
        if not has_agreed:
            raise forms.ValidationError(_('You must agree with the contract!'))
        return has_agreed


class AtLeastOneFormSet(forms.models.BaseModelFormSet):
    """
    Validates that the user adds at least one valid and changed form.
    """
    # TODO use min_num and validate_min from future django releases
    def clean(self):
        if any(self.errors):
            return  # pass away individual forms errors

        for form in self.initial_forms:
            if not form.is_valid() or not (self.can_delete and form.cleaned_data.get('DELETE')):
                return
        for form in self.extra_forms:
            if form.has_changed():
                return
        raise forms.ValidationError(_('Add at least one entry'))


class KlassForm(forms.ModelForm):
    teacher_name = forms.CharField(label=_('Teacher name'))
    teacher_email = forms.EmailField(label=_('Teacher email'))

    class Meta:
        model = Klass
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(KlassForm, self).__init__(*args, **kwargs)
        if self.instance.teacher:
            self.fields['teacher_name'].initial = self.instance.teacher.get_full_name()
            self.fields['teacher_email'].initial = self.instance.teacher.email


KlassFormSet = forms.models.modelformset_factory(
    Klass, extra=0, form=KlassForm, formset=AtLeastOneFormSet
)


class ManagerForm(forms.ModelForm):
    """
    Form to ask the name and email of the manager of a new client.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(ManagerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True


ManagerFormSet = forms.models.modelformset_factory(
    User, extra=0, form=ManagerForm, formset=AtLeastOneFormSet
)
