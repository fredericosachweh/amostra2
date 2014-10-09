# -*- coding:utf-8 -*-
import textwrap
from pyboleto.pdf import BoletoPDF

from django.conf import settings
from django.http import HttpResponse
from django.utils.formats import date_format
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from payments import models
from payments.billet import BoletoCaixa
from utils.views import LoginRequiredMixin


class ManagedPaymentsMixin(object):
    """
    A Mixin that offers a list of payments whose the logged in user is manager.
    """
    def get_queryset(self):
        return models.Payment.objects.filter(
            contract__pk=self.kwargs['contract_pk']).order_by('-due_date')


class PaymentListView(LoginRequiredMixin, ManagedPaymentsMixin, generic.ListView):
    paginate_by = 12
    template_name = 'payments/payment_list.html'


class PaymentDetailView(generic.DetailView):
    """Shows detailed information about the Payment before print the billet."""
    model = models.Payment

    def get_context_data(self, **kwargs):
        context = super(PaymentDetailView, self).get_context_data(**kwargs)
        if not self.request.user.is_staff:
            self.object.visit_set.create()  # register how many visits
        return context

    def get_template_names(self):
        if self.request.user.is_authenticated():
            return ['payments/billing.html', ]
        else:
            return ['payments/billing_not_logged.html', ]


def print_payment(request, pk):
    """Generates the billet for payment as PDF for printing."""
    payment = models.Payment.objects.get(pk=pk)
    client = payment.contract.client

    # Set billet mainiti's data
    billet = BoletoCaixa()
    billet.carteira = settings.CEDENTE_CARTEIRA
    billet.conta_cedente = settings.CEDENTE_CONTA
    billet.agencia_cedente = settings.CEDENTE_AGENCIA
    billet.cedente = settings.CEDENTE
    billet.cedente_documento = settings.CEDENTE_DOCUMENTO
    billet.cedente_cidade = settings.CEDENTE_CIDADE
    billet.cedente_uf = settings.CEDENTE_UF
    billet.cedente_logradouro = settings.CEDENTE_LOGRADOURO
    billet.cedente_bairro = settings.CEDENTE_BAIRRO
    billet.cedente_cep = settings.CEDENTE_CEP

    # Set billet instructions
    billet.demonstrativo = textwrap.wrap(unicode(payment), 90)
    instructions = _('Do not accept payment after due date.')
    billet.instrucoes = textwrap.wrap(instructions, 90)

    # Set billet client's data
    billet.data_documento = now()
    billet.data_processamento = now()
    billet.data_documento = now()
    billet.data_vencimento = payment.due_date
    billet.nosso_numero = str(payment.id)
    billet.numero_documento = str(payment.id)
    billet.valor = payment.cost
    billet.valor_documento = payment.cost
    billet.sacado_nome = client.name
    billet.sacado_documento = client.cnpj
    billet.sacado_cidade = client.city
    billet.sacado_uf = client.state
    billet.sacado_endereco = client.address
    billet.sacado_bairro = client.quarter
    billet.sacado_cep = client.postal_code

    response = HttpResponse(mimetype='application/pdf')
    billet_file = BoletoPDF(response)
    billet_file.drawBoleto(billet)
    billet_file.save()

    if not request.user.is_staff:
        payment.open_set.create()  # regiter how many opens

    name = _('billet-{0}.pdf')
    name = name.format(date_format(payment.due_date, 'SHORT_DATE_FORMAT'))
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(name)
    return response
