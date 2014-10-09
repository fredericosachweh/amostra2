import datetime

from django.utils.timezone import now
from decimal import Decimal as D

from django.conf import settings
from django.test import TransactionTestCase

from clients import factories
from payments.billet import BoletoCaixa


class PaymentsTestCase(TransactionTestCase):
    fixtures = (
        'auth_groups.json',
    )

    def setUp(self):
        self.first_date = datetime.date(2014, 1, 1)
        self.end_date = datetime.date(2014, 1, 30)
        self.current_date = datetime.date(2014, 1, 15)
        self.days_left = 31 - 15 + 1  # we know 2014 january has 31 days
        self.future_date = self.current_date + datetime.timedelta(days=7)

        self.client = factories.ClientFactory.create()
        self.contract = self.client.contract_set.create(document='1234')
        self.klass1 = self.contract.klass_set.create(name='Test class #1',
                                                     end_date=self.future_date)
        self.klass2 = self.contract.klass_set.create(name='Test class #2',
                                                     end_date=self.future_date)

    def create_payment(self, date):
        payment = self.contract.payment_set.create(ref_date=date,
                                                   due_date=self.future_date)
        payment.klasspayment_set.create(klass=self.klass1)
        payment.klasspayment_set.create(klass=self.klass2)
        return payment

    def test_payment_full_cost_in_first_date(self):
        """
        Tests that in the 1st day of month, payment cost is full klass cost.
        """
        payment = self.create_payment(self.first_date)
        self.assertEqual(payment.cost, settings.KLASSES_COST * 2)

    def test_payment_partial_cost_in_current_date(self):
        """
        Tests partial payments.

        Asserts that in the middle of month, the payment cost will be the
        proportional to the days left in the month, including the current date.
        """
        payment = self.create_payment(self.current_date)
        partial_rate = self.days_left / D(31)
        self.assertEqual(payment.cost, settings.KLASSES_COST * 2 * partial_rate)

    def test_klass_cost_change(self):
        """
        Tests that if the class cost changes, the payment gets updated.
        """
        payment = self.create_payment(self.first_date)
        self.assertEqual(payment.cost, settings.KLASSES_COST * 2)

        kp = payment.klasspayment_set.all()[0]
        kp.current_cost += 10
        kp.save()

        payment = self.contract.payment_set.get()  # reload instance
        self.assertEqual(payment.cost, settings.KLASSES_COST * 2 + 10)

    def test_klass_remove(self):
        """
        Tests that if the class cost are removed, the payment gets updated.
        """
        payment = self.create_payment(self.first_date)
        self.assertEqual(payment.cost, settings.KLASSES_COST * 2)

        kp = payment.klasspayment_set.all()[0]
        kp.delete()

        payment = self.contract.payment_set.get()  # reload instance
        self.assertEqual(payment.cost, settings.KLASSES_COST)

    def test_validate_nosso_numero(self):
        payment = self.create_payment(self.first_date)

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
        billet.data_documento = now()
        billet.data_processamento = now()
        billet.data_documento = now()
        billet.data_vencimento = payment.due_date
        billet.nosso_numero = str(payment.id)
        billet.numero_documento = str(payment.id)
        billet.valor = payment.cost
        billet.valor_documento = payment.cost
        billet.sacado_nome = self.client.name
        billet.sacado_documento = self.client.cnpj
        billet.sacado_cidade = self.client.city
        billet.sacado_uf = self.client.state
        billet.sacado_endereco = self.client.address
        billet.sacado_bairro = self.client.quarter
        billet.sacado_cep = self.client.postal_code

        self.assertEqual(billet.nosso_numero, '{0}000000000000000{1}'.format(
            settings.BILLET_PREFIX, payment.id))

    def test_payment_due_date(self):
        payment = self.create_payment(self.end_date)

        self.assertEqual(payment.ref_date.date(), datetime.date(2014, 2, 1))
        self.assertEqual(payment.cost, 140)
