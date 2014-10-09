# -*- coding: utf-8 -*-
import datetime
import mock
from decimal import Decimal as D

from lettuce import step, world
from nose.tools import assert_equals, assert_in

from django.core import mail
from django.core.management import call_command


@step(u'contrato tem data preferida de pagamento como dia (\d{2}) de cada mês')
def payment_date(step, day):
    world.contract.payment_day = int(day)
    world.contract.save()


@step(u'comando para geração de pagamentos é executado')
@mock.patch('django.utils.timezone.now', lambda: datetime.datetime(*world.date_tuple))
def generate_payments(step):
    call_command('generatepayments')


@step(u'contrato terá pagamento em (\d{2})/(\d{2})/(\d{4}) no valor de ([\d,]+)')
def last_contract_payment(step, day, month, year, value):
    payment_date = datetime.date(int(year), int(month), int(day))
    value = D(value.replace(',', '.'))
    payments = world.contract.payment_set.filter(due_date=payment_date,
                                                 cost=value)
    assert_equals(payments.count(), 1)


@step(u'comando para aviso de inadimplentes é executado')
@mock.patch('django.utils.timezone.now', lambda: datetime.datetime(*world.date_tuple))
def late_payments(step):
    call_command('latepayments')


@step(u'os managers receberão um e-mail com os dados:')
def check_client_and_klass_in_body(step):
    for data in step.hashes:
        assert_in(data['Cliente'], mail.outbox[0].body)
        assert_in(data['Turma'], mail.outbox[0].body)
