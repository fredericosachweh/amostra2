# -*- coding: utf-8 -*-
import datetime
import mock

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

from lettuce import step, world
from lettuce.django import django_url
from nose.tools import assert_equals, assert_true

from clients import factories
from exercises.models import Program, BatterySchedule


@step(u'contrato não tem pagamentos')
def contract_doesnt_have_payments(step):
    assert_equals(world.contract.payment_set.count(), 0)


@step(u'prazo para pagamento estar atrasado é de (\d+) dias')
def set_payment_late(step, days):
    days = int(days)
    settings.LATE_PAYMENT = days


def create_klass_payment(payment):
    for klass in world.contract.klass_set.all():
        klass.klasspayment_set.create(payment=payment, current_cost=klass.cost)


@step(u'contrato tem pagamentos quitados em (\d{2})/(\d{4}) e (\d{2})/(\d{4})')
def create_paid_payments(step, first_month, first_year, second_month, second_year):
    dates = [
        (first_year, first_month),
        (second_year, second_month),
    ]
    for year, month in dates:
        ref_date = datetime.date(int(year), int(month), 1)
        due_date = datetime.date(int(year), int(month), settings.PAYMENT_DAY)
        payment = world.contract.payment_set.create(
            ref_date=ref_date,
            due_date=due_date,
            payment_date=due_date + datetime.timedelta(days=1)
        )
        create_klass_payment(payment)

    assert_true(world.contract.payment_set.count, 2)


@step(u'novo pagamento é gerado para este contrato a vencer em (\d{2})/(\d{2})/(\d{4})')
def create_pending_payment(step, *due_date):
    due_date = [int(d) for d in due_date[::-1]]
    due_date = datetime.datetime(*due_date)
    payment = world.contract.payment_set.create(
        ref_date=due_date - datetime.timedelta(days=1),
        due_date=due_date
    )
    create_klass_payment(payment)
    assert_true(world.contract.payment_set.count(), 3)


@step(u'pagamento de (\d{2})/(\d{2})/(\d{4}) for quitado')
def make_payment_paid(step, day, month, year):
    due_date = datetime.date(int(year), int(month), int(day))
    payment = world.contract.payment_set.get(due_date=due_date)
    payment.payment_date = timezone.now()
    payment.save()


@step(u'turma for iniciada dia (\d{2})/(\d{2})/(\d{4}) num programa exemplo com um aluno')
def start_klass(step, *start_date):
    call_command('loaddata', 'exercises_categories.json')
    call_command('loaddata', 'exercises_programs.json')
    start_date = [int(d) for d in start_date[::-1]]
    start_date = datetime.datetime(*start_date)

    program = Program.objects.get()
    klass = world.contract.klass_set.get()
    program_usage = program.programusage_set.create(
        klass=klass, start_date=start_date, end_date=world.future_date
    )
    modules = list([i.id for i in program.module_set.all()])
    program_usage.distribute_batteries(modules)

    # Creates a student for the klass
    student = factories.UserFactory.create(username='aluno', password='123456')
    world.student = student
    klass.students.add(student)
    assert_true(klass.students.count(), 1)


@step(u'aluno logar')
def access_as_student(step):
    date_tuple = world.date_tuple
    with mock.patch('django.utils.timezone.now',
                    lambda: datetime.datetime(*date_tuple)):
        klass = world.contract.klass_set.get()
        world.do_login_as_student(klass.key, '123456')


@step('houver tarefa para hoje')
def check_today_has_batteries(step):
    """
    Gets the only one battery schedule for the mocked today.

    Do not use clever methods as we only need to know there is the expected
    battery for today.
    """
    date_tuple = world.date_tuple
    with mock.patch('django.utils.timezone.now',
                    lambda: datetime.datetime(*date_tuple)):
        today = timezone.now()
        battery_schedule = BatterySchedule.objects.filter(date=today)
        assert_equals(battery_schedule.filter(date=today).count(), 1)


@step(u'verei uma tarefa para o dia')
def check_battery_is_visible(step):
    link = world.browser.find_link_by_text('Iniciar')
    assert_equals(len(link), 1)


@step(u'não verei nenhuma tarefa para o dia')
def check_battery_is_not_visible(step):
    assert_true(world.browser.is_text_present(u'suas tarefas estão em dia'))
    assert_true(world.browser.is_text_present(u'não tem tarefas para fazer hoje'))
