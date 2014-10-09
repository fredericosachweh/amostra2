from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

import models
from clients.models import Client


def mark_payment_as_paid(modeladmin, request, queryset):
    """
    Action to mark payments as paid.

    Iter each item in queryset to trigger pre_save and post_save signals that
    affects contracts data.
    """
    payment_date = now()
    for item in queryset:
        item.payment_date = payment_date
        item.save()
mark_payment_as_paid.short_description = _('Mark selected payments as paid')


class ClientFilter(admin.SimpleListFilter):
    """
    Filter a payment list by contract's clients.
    """
    parameter_name = 'client'
    title = _('Client')

    def lookups(self, request, model_admin):
        return Client.objects.all().values_list('pk', 'name')

    def queryset(self, request, queryset):
        if self.value() is not None:
            client_pk = self.value()
            queryset = queryset.filter(contract__client__pk=client_pk)
        return queryset


class OpenInline(admin.TabularInline):
    model = models.Open
    extra = 0


class VisitInline(admin.TabularInline):
    model = models.Visit
    extra = 0


class KlassPaymentInline(admin.TabularInline):
    model = models.KlassPayment
    extra = 0


class PaymentAdmin(admin.ModelAdmin):
    inlines = (KlassPaymentInline, OpenInline, VisitInline)
    list_display = ('get_number', 'due_date', 'get_client', 'contract',
                    'was_paid', 'payment_date', 'get_cost', 'get_open_and_visit',
                    'get_invoice_data')
    list_filter = ('was_paid', ClientFilter)
    date_hierarchy = 'payment_date'
    search_fields = ('=id', 'contract__number',)
    readonly_fields = ('was_paid',)
    actions = (mark_payment_as_paid,)

    def queryset(self, request):
        return models.Payment.objects.all_with_visits()

    def get_client(self, obj):
        return obj.contract.client
    get_client.short_description = _('client')

    def get_number(self, obj):
        return '%08d' % obj.pk
    get_number.short_description = _('number')

    def get_cost(self, obj):
        return obj.cost
    get_cost.short_description = _('cost')

    def get_open_and_visit(self, obj):
        return '{visits}/{opens}'.format(opens=obj.opens, visits=obj.visits)
    get_open_and_visit.short_description = _('open/visit')

    def get_invoice_data(self, obj):
        url = reverse('invoice-data', kwargs={'pk': obj.contract.client.pk})
        return '<a href="{0}">Dados do cliente</a>'.format(url)
    get_invoice_data.allow_tags = True

admin.site.register(models.Payment, PaymentAdmin)
