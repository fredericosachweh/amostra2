from django.contrib import messages
from django.db import transaction
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from clients import forms
from clients import models


class ClientsImportView(generic.FormView):
    """
    Imports suspect clients from a CSV list.
    """
    template_name = 'admin/clients/clients_import.html'
    form_class = forms.ClientImportForm

    @method_decorator(transaction.commit_on_success)
    def form_valid(self, form, **kwargs):
        csv_data = form.cleaned_data['csv_data']
        clients = []
        for data in csv_data:
            client = models.Client(**data)
            client.status = 'suspect'
            clients.append(client)

        models.Client.objects.bulk_create(clients)
        msg = _('{0} clients imported successfuly.')
        messages.success(self.request, msg.format(len(clients)))
        return redirect('admin:clients_client_changelist')

    def get_context_data(self, **kwargs):
        context = super(ClientsImportView, self).get_context_data(**kwargs)
        context['title'] = _('Import clients')
        return context


class InvoiceDataView(generic.DetailView):
    """
    Returns specific data for invoice
    """
    template_name = 'admin/clients/invoice_data.html'
    model = models.Client

    def get_context_data(self, **kwargs):
        context = super(InvoiceDataView, self).get_context_data(**kwargs)
        context['title'] = _('Invoice data')
        return context
