# -*- coding: utf-8 -*-
import datetime
import mock
from decimal import Decimal

from django.conf import settings
from django.core.urlresolvers import reverse

from lettuce import step, world
from lettuce.django import django_url
from nose.tools import assert_equals, assert_almost_equals, assert_true

from clients import factories



@step(u'Quando seguir os passos até finalizar a compra')
def access_final_purchase_step(step):
    """
    Run through each purchase step until purchase end.

    Process to the managers and teachers creation/warning and the payment
    creation. Mock up the django.utils.timezone.now function to simulate
    specific date events.
    """
    date_tuple = world.date_tuple
    with mock.patch('django.utils.timezone.now',
                    lambda: datetime.datetime(*date_tuple)):
        world.browser.visit(django_url(world.demo.get_absolute_url()))

        # 1st step: client data conference
        world.browser.click_link_by_text('Comprar agora')
        assert_true(world.browser.is_text_present(u'Confira seus dados'))

        # 2nd step: contract agree (predefined when created client)
        world.browser.click_link_by_text('Continuar')
        assert_true(world.browser.is_text_present('Leia o contrato'))

        # 3rd step: tell klasses and managers (predefined when created client)
        world.browser.find_by_xpath('//button[text()="Continuar"]').first.click()
        assert_true(world.browser.is_text_present(u'Defina quais as turmas'))

        # 4th step: when teachers, managers and payments would be created
        world.browser.find_by_xpath('//button[text()="Continuar"]').first.click()
        assert_true(world.browser.is_text_present(u'Compra finalizada'))


@step(u'terei um boleto de ([\d,]+) '
       'referente a (\d{2})/(\d{4}), '
       'vencendo em (\d{2})/(\d{2})/(\d{4})')
def check_billet_value_and_dates(step, value, ref_month, ref_year, day, month, year):
    cost = Decimal(value.replace(',', '.'))
    ref_month, ref_year = int(ref_month), int(ref_year)
    due_date = datetime.date(int(year), int(month), int(day))

    payment = world.contract.payment_set.get()
    assert_almost_equals(payment.cost, cost)
    assert_equals(payment.ref_date.month, ref_month)
    assert_equals(payment.ref_date.year, ref_year)
    assert_equals(payment.due_date, due_date)


@step(u'cliente não tem definido o CNPJ')
def unset_cnpj(step):
    world.client.cnpj = None
    world.client.save()


@step(u'acess(?:o|ar) (?:tal|a) demonstração')
def visit_demonstration(step):
    if hasattr(world, 'date_tuple'):
        date_tuple = world.date_tuple
    else:
        date_tuple = datetime.date.today().timetuple()[:3]
    with mock.patch('django.utils.timezone.now',
                    lambda: datetime.datetime(*date_tuple)):
        world.browser.visit(django_url(world.demo.get_absolute_url()))


@step(u'Dado um cliente com uma turma, prestes a fechar negócio')
def create_sample_client(step):
    """
    Creates sample data for tests.

    Creates a client with a manager, a teacher and a valid demonstration, with
    klasses, just ready to reach and procede the final purchase step.
    """
    # Creates a client with manager
    manager = factories.UserFactory.create(username='gestor', password='123456')
    client = factories.ClientFactory.create(cnpj='28144144000130',
                                            has_agreed=True,  # agreed with terms
                                            managers=[manager])
    world.client = client

    # Creates a teacher for the client
    world.teacher = factories.UserFactory.create(username='professor',
                                                 password='123456')
    client.teacher_set.create(teacher=world.teacher, is_confirmed=True)

    # isolates a far future date, considering we are testing with mocked dates
    # in 2014 year
    world.future_date = datetime.date(2014, 12, 31)

    # Creates a contract and a klass for contract and teacher for a far future
    # date, considering we are testing with mocked dates in 2014 year
    world.contract = client.contract_set.create(document=client.cnpj)
    world.klass = world.contract.klass_set.create(
        name='Sample class',
        teacher=world.teacher,
        end_date=world.future_date,
    )

    # creates a demonstration with a far future valid date
    world.demo = client.demonstration_set.create(valid_until=world.future_date)


@step(u'custo por turma é ([\d,]+)')
def klass_cost(step, value):
    settings.KLASS_COST = Decimal(value.replace(',', '.'))


@step(u'a turma se chama "([^"]+)"')
def rename_klass(step, name):
    world.klass.name = name
    world.klass.save()


@step(u'o nome do cliente é "([^"]*)"')
def rename_client(step, name):
    world.client.name = name
    world.client.save()


@step(u'professor logar e selecionar uma turma')
def access_some_klass(step):
    if hasattr(world, 'date_tuple'):
        date_tuple = world.date_tuple
    else:
        date_tuple = datetime.date.today().timetuple()[:3]
    with mock.patch('django.utils.timezone.now',
                    lambda: datetime.datetime(*date_tuple)):
        world.browser.visit(django_url(reverse('home')))
        world.do_login('professor', '123456')
        assert_true(world.browser.is_text_present(u'Programas e turmas'))
        world.browser.click_link_by_text('Iniciar')
