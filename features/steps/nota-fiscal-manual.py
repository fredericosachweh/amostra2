# -*- coding:utf-8 -*-
import os
import datetime
import mock
import tempfile

from django.core.files import File
from django.core import mail

from lettuce import step, world
from nose.tools import assert_true, assert_false, assert_equals


@step(u'um pagamento para (\d{2})/(\d{2})/(\d{4})')
def create_payment(step, *due_date):
    due_date = [int(d) for d in due_date[::-1]]
    due_date = datetime.datetime(*due_date)
    payment = world.contract.payment_set.create(
        ref_date=due_date - datetime.timedelta(days=1),
        due_date=due_date
    )
    for klass in world.contract.klass_set.all():
        klass.klasspayment_set.create(payment=payment, current_cost=klass.cost)
    world.payment = payment


@step(u'gestor logar, acessar financeiro')
def access_payment(step):
    today = world.date_tuple
    with mock.patch('django.utils.timezone.now',
                    lambda: datetime.datetime(*today)):
        world.do_login('gestor', password='123456')
        assert_true(world.browser.is_text_present(u'Contratos'))

        # opens payment actions menu
        world.browser.find_link_by_text(u'Ações').last.click()
        world.browser.click_link_by_text(u'Financeiro')
        assert_true(world.browser.is_text_present(u'Financeiro'))


@step(u'não verá botão para imprimir nota na lista ou nos detalhes')
def check_invoice_unavailable(step):
    assert_false(world.browser.is_text_present('Nota'))      # at listing
    world.browser.click_link_by_text('Boleto')
    assert_true(world.browser.is_text_present('Pagamento'))
    assert_false(world.browser.is_text_present('Nota'))      # at details


@step(u'pagamento tem nota fiscal')
def attach_invoice(step):
    f = tempfile.NamedTemporaryFile(mode='w', delete=False)
    f.write('Conteudo da nota fical')
    f.close()
    world.uploaded_filename = filename = os.path.basename(f.name)
    world.payment.invoice_file.save(filename, File(open(f.name)))
    world.payment.save()


@step(u'verá botão para imprimir nota na lista e nos detalhes')
def check_invoice_available(step):
    """
    Check if there is a link to the invoice in the list and details.
    """
    listing_link = world.browser.find_link_by_href(world.payment.invoice_file.url)
    assert_equals('nota', listing_link.first.text)

    world.browser.click_link_by_text('Boleto')
    assert_true(world.browser.is_text_present('Pagamento'))

    details_link = world.browser.find_link_by_href(world.payment.invoice_file.url)
    assert_equals('nota', details_link.first.text)


@step(u'gerente terá recebido email com link para tal nota')
def check_invoice_email(step):
    email = mail.outbox[-1]
    email.body.index(world.payment.invoice_file.url)
