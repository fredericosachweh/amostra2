from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django_localflavor_br import br_states, forms as br_forms

from followup.models import Followup
from demonstrations.models import Demonstration
import models


class TeacherInline(admin.TabularInline):
    model = models.Teacher
    raw_id_fields = ('teacher',)
    related_lookup_fields = {
        'fk': ('teacher',)
    }
    extra = 0


class ContractInline(admin.TabularInline):
    model = models.Contract
    fields = ('document', 'number', 'up_to_date')
    readonly_fields = ('number', 'up_to_date')
    extra = 0

    def up_to_date(self, obj):
        return not obj.pending_payment
    up_to_date.boolean = True


class PersonFormSet(forms.models.BaseInlineFormSet):
    """
    Using a formset into an inline so we can tamper with all forms data one
    time only
    """
    def clean(self):
        super(PersonFormSet, self).clean()

        all_roles = set(models.Role.objects.filter(mandatory=True) \
                                    .values_list('name', flat=True))
        for f in self.forms:
            person_roles = set(f.cleaned_data['roles'].values_list('name',
                                                                   flat=True))
            all_roles = all_roles.difference(person_roles)

        if all_roles:
            msg = _('You need at least one person performing the roles: {0}.')
            raise ValidationError(msg.format(', '.join(all_roles)))


class PersonInline(admin.TabularInline):
    model = models.Person
    fields = ('name', 'email', 'telephone', 'cellphone', 'roles')
    extra = 0
    formset = PersonFormSet


class FollowupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Defining readonly fields for inline followup. Using this form instead
        of get_readonly_fields which alters data for the whole Client.
        """
        super(FollowupForm, self).__init__(*args, **kwargs)
        self.fields['responsible'].queryset = User.objects.filter(is_staff=True)

        if self.instance and self.instance.pk:
            if not (self.instance.responsible and self.instance.due_date):
                self.fields['content'].widget.attrs['readonly'] = True

    def clean_content(self):
        """
        Prevents hacks when doing a POST.
        """
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.content
        else:
            return self.cleaned_data['content']


class FollowupInline(admin.TabularInline):
    model = Followup
    fields = ('content', 'created_at', 'author', 'due_date', 'responsible', 'is_done')
    form = FollowupForm
    readonly_fields = ('created_at', 'author', 'is_done',)
    extra = 0


class DemonstrationForm(forms.ModelForm):
    def has_changed(self):
        """
        Forces the form to be treated as changed everytime once all his fields
        are filled with defaults and can be saved without be "changed"
        effectively.
        """
        return True


class DemonstrationInline(admin.TabularInline):
    model = Demonstration
    fields = ('created_at', 'valid_until', 'send_link')
    readonly_fields = ('send_link',)
    extra = 0
    form = DemonstrationForm

    def send_link(self, instance):
        if instance.pk and not instance.is_expired():
            url = reverse('demonstrations:demo-send',
                          kwargs={'pk': instance.pk})
            return _('<a href="{0}">Send&nbsp;demonstration</a>').format(url)
        elif instance.is_expired():
            return _('Demonstration expired')
        else:
            return ''
    send_link.allow_tags = True


class ClientForm(forms.ModelForm):
    cnpj = br_forms.BRCNPJField(label=_('CNPJ Number'), required=False)
    state = forms.ChoiceField(
        label=_('State'),
        required=False,
        choices=(('', '------'),) + br_states.STATE_CHOICES
    )
    phones = forms.CharField(
        label=_('Phones'),
        required=False,
        widget=admin.widgets.AdminTextInputWidget
    )

    class Meta:
        model = models.Client

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = User.objects.filter(is_staff=True)

    def clean_cnpj(self):
        """
        Force the result to be None instead of a blank string to pass
        unique constraint.
        """
        cnpj = self.cleaned_data.get('cnpj', None)
        if not cnpj:
            cnpj = None
        return cnpj


class ClientAdmin(admin.ModelAdmin):
    inlines = (ContractInline, TeacherInline, PersonInline, FollowupInline, DemonstrationInline)
    raw_id_fields = ('managers',)
    list_display = ('name', 'cnpj', 'phones', 'email', 'state', 'city', 'status')
    list_filter = (
        'status', 'owner', 'external_source', 'city', 'state',
        'adm_structure', 'private_school_category'
    )
    search_fields = (
        'phones', 'email', 'name', 'company_name', 'cnpj', 'person__name',
        'person__email', 'person__telephone', 'person__cellphone'
    )
    related_lookup_fields = {
        'm2m': ('managers',)
    }
    readonly_fields = ('status', 'external_source', 'external_code')
    fieldsets = (
        (None, {'fields': (
            'name',
            'status',
            'company_name',
            'cnpj',
            'phones',
            'email',
            'site',
            ('adm_structure', 'private_school_category'),
        )}),
        (_('Address Information'), {'fields': (
            ('address', 'number', 'complement'),
            ('quarter', 'state', 'city'),
            'postal_code',
        )}),
        (None, {'fields': (
            'managers',
            'owner',
        )}),
        (None, {'fields': (
            'external_source',
            'external_code',
        )}),
    )
    form = ClientForm

    def save_formset(self, request, form, formset, change):
        """
        For the followup inline, sets the author as the current user of
        request, if not already set.
        """
        if not formset.model == Followup:
            return super(ClientAdmin, self).save_formset(request, form, formset, change)

        instances = formset.save(commit=False)
        for instance in instances:
            if instance.author is None:
                instance.author = request.user
            instance.save()
        formset.save_m2m()


class KlassInline(admin.TabularInline):
    model = models.Klass
    extra = 0
    raw_id_fields = ('teacher', 'students')
    related_lookup_fields = {
        'fk': ('teacher',),
        'm2m': ('students',)
    }


class ContractAdmin(admin.ModelAdmin):
    inlines = (KlassInline,)
    list_display = ('number', 'client', 'created_at', 'klasses_count', 'up_to_date')
    list_filter = ('payment_day', 'pending_payment')
    search_fields = ('number', 'client__name', 'client__email', 'client__company_name')
    raw_id_fields = ('client',)
    readonly_fields = ('number', 'created_at', 'up_to_date', 'klasses_count')

    def up_to_date(self, obj):
        return not obj.pending_payment
    up_to_date.boolean = True


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'mandatory',)


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Contract, ContractAdmin)
admin.site.register(models.Role, RoleAdmin)
