# -*- encoding: utf-8 -*-
import calendar
import datetime
import mock
from decimal import Decimal as D

from django.conf import settings
from django.core import mail
from django.utils import timezone
from splinter.request_handler.status_code import HttpResponseError

from utils.tests.base import BaseTestCase


def now_plus_1_day():
    return datetime.datetime.now() + datetime.timedelta(days=1)


def now_plus_3_days():
    return datetime.datetime.now() + datetime.timedelta(days=3)


class IntegrationTestCase(BaseTestCase):
    fixtures = BaseTestCase.fixtures + [
        'exercises_categories.json',
        'exercises_sample.json.bz2',
        'flatpages_sample.json',
    ]

    def setUp(self):
        super(IntegrationTestCase, self).setUp()

        self.client.cnpj = '28144144000130'
        self.client.save()

        date = timezone.now() + datetime.timedelta(days=7)
        self.demo = self.client.demonstration_set.create(valid_until=date)

    def test_purchase(self):
        """
        Tests that a client with complete data can finish a purchase.
        """
        self.browser.visit(self.live_server_url + self.demo.get_absolute_url())
        self.assertTrue(self.browser.is_text_present(u'Inicie sua demonstração'))

        self.browser.click_link_by_text('Comprar agora')
        self.assertTrue(self.browser.is_text_present(u'Confira seus dados'))

        self.browser.click_link_by_text('Continuar')
        self.assertTrue(self.browser.is_text_present('Leia o contrato'))

        self.browser.find_by_xpath('//button[text()="Continuar"]').first.click()
        self.assertTrue(self.browser.is_text_present(u'Você precisa concordar com o contrato!'))

        self.browser.check("has_agreed")
        self.browser.find_by_xpath('//button[text()="Continuar"]').first.click()

        self.assertTrue(self.browser.is_text_present(u'Defina quais as turmas'))

        # The manager is already here
        manager_email_field = self.browser.find_by_name('managers-0-email').first
        self.assertEqual(manager_email_field.value, self.manager.email)

        # The teacher must be attached
        self.browser.click_link_by_text('Adicionar turma')
        self.browser.fill('klasses-0-name', u'4ºA')
        self.browser.fill('klasses-0-teacher_name', u'João da Silva')
        self.browser.fill('klasses-0-teacher_email', u'joao@email.com')

        self.browser.find_by_xpath('//button[text()="Continuar"]').first.click()
        self.assertTrue(self.browser.is_text_present(u'Compra finalizada'))

        # There will be 2 emails: one for the manager and one for the teacher
        self.assertEqual(len(mail.outbox), 2)

        # The only one manager was reused. He gets the first email and, as
        # already registered, do not get his credentials in the message's body
        manager = self.client.managers.get()
        self.assertEqual(manager, self.manager)
        self.assertEqual(mail.outbox[0].subject, 'Bem-vindo ao Mainiti')
        self.assertNotIn(manager.email, mail.outbox[0].body)

        # The only one teacher was newly created and gets the second email with
        # his credentials
        teacher = self.client.teacher_set.get()
        self.assertEqual(teacher.teacher.email, 'joao@email.com')
        self.assertEqual(mail.outbox[1].subject, 'Bem-vindo ao Mainiti')
        self.assertIn('joao@email.com', mail.outbox[1].body)

        # The only one contract was implicit created
        contract = self.client.contract_set.get()
        self.assertEqual(contract.document, self.client.cnpj)

        # A new payment was created for tomorrow
        payment = contract.payment_set.get()
        tomorrow = timezone.now().date() + datetime.timedelta(days=1)
        self.assertEqual(payment.due_date, tomorrow)
        self.assertEqual(payment.ref_date, tomorrow)

        # The klass has a cost equal to the default cost
        kp = payment.klasspayment_set.get()
        self.assertEqual(kp.current_cost, settings.KLASSES_COST)

        # The payment cost is proportional to the days left after
        # due date/tomorrow
        today = timezone.now().date()
        first_weekday, days_in_month = calendar.monthrange(today.year,
                                                           today.month)
        payment_rate = (days_in_month - today.day) / D(days_in_month)
        self.assertAlmostEqual(payment.cost,
                               kp.current_cost * payment_rate,
                               places=2)

    def test_purchase_renew_payment(self):
        """
        Tests that after reach the last step of a purchase and after a few
        days, if I go back to purchase, the payment is updated.
        """
        self.test_purchase()

        self.browser.visit(self.live_server_url + self.demo.get_absolute_url())
        self.browser.click_link_by_text('Comprar agora')
        self.assertTrue(self.browser.is_text_present(u'Confira seus dados'))

        self.browser.click_link_by_text('Continuar')
        self.assertTrue(self.browser.is_text_present('Leia o contrato'))

        self.browser.find_by_xpath('//button[text()="Continuar"]').first.click()
        self.assertTrue(self.browser.is_text_present(u'Defina quais as turmas'))

        original_due_date = timezone.now().date() + datetime.timedelta(days=1)
        with mock.patch('django.utils.timezone.now', now_plus_3_days):
            self.browser.find_by_xpath('//button[text()="Continuar"]').first.click()
            self.assertTrue(self.browser.is_text_present(u'Compra finalizada'))
            self.assertTrue(self.browser.is_text_present(u'pagamento foi atualizado'))

        contract = self.client.contract_set.get()
        payment = contract.payment_set.get()

        # The payment was expired, a new payment date was set 3 days after
        self.assertEqual(payment.due_date,
                         original_due_date + datetime.timedelta(days=3))

    def test_purchase_add_klass(self):
        """
        Tests that after reach the last step of a purchase, restart the process
        and add a new klass, the payment value is updated.
        """
        self.test_purchase()

        contract = self.client.contract_set.get()
        payment = contract.payment_set.get()
        original_cost = payment.cost

        self.browser.visit(self.live_server_url + self.demo.get_absolute_url())
        self.browser.click_link_by_text('Comprar agora')
        self.assertTrue(self.browser.is_text_present(u'Confira seus dados'))

        self.browser.click_link_by_text('Continuar')
        self.assertTrue(self.browser.is_text_present('Leia o contrato'))

        self.browser.find_by_xpath('//button[text()="Continuar"]').first.click()
        self.assertTrue(self.browser.is_text_present(u'Defina quais as turmas'))

        # Adds a new klass
        self.browser.click_link_by_text('Adicionar turma')
        self.browser.fill('klasses-1-name', u'4ºB')
        self.browser.fill('klasses-1-teacher_name', u'João da Silva')
        self.browser.fill('klasses-1-teacher_email', u'joao@email.com')

        self.browser.find_by_xpath('//button[text()="Continuar"]').first.click()
        self.assertTrue(self.browser.is_text_present(u'Compra finalizada'))
        self.assertTrue(self.browser.is_text_present(u'pagamento foi atualizado'))

        # The payment has tow klasses and his value now refers both
        payment = contract.payment_set.get()
        self.assertEqual(payment.klasses.count(), 2)
        self.assertEqual(payment.klasses.count(), 2)
        self.assertEqual(payment.cost, original_cost * 2)
