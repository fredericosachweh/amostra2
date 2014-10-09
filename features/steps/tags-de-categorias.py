# -*- coding: utf-8 -*-
import datetime

from django.core.management import call_command
from django.contrib.auth.models import User
from django.utils import timezone

from lettuce import step, world
from nose.tools import assert_equals, assert_in

from exercises import models


@step(u'existem categorias previamente cadastradas')
def load_categories(step):
    call_command('loaddata', 'exercises_categories.json')


@step(u'exercícios de "([^"]*)" \(([^)(]*)\) abaixo')
def create_exercise(step, category, command):
    category = models.Category.objects.get(name=category)
    for data in step.hashes:
        call_command(command,
                     operation=data[u'Operação'],
                     terms=int(data[u'Termos']))


@step(u'programa com uma bateria com (\d+) exercícios de expressões de adição')
def create_sample_program(step, count):
    program = world.program = models.Program.objects.create(
        matter=models.Matter.objects.get(slug='matematica'),
        name='Sample program'
    )
    module = program.module_set.create(name='Sample module', position=1)
    battery = module.battery_set.create(name='Sample battery', position=1)
    world.category_usage = battery.categoryusage_set.create(
        category=models.Category.objects.get(slug='adicao-subtracao-em-ordem-3-termos'),
        exercises_count=count,
        random_sorting=False,
        filter1_lower=0,
        filter1_upper=10,
        filter2_lower=0,
        filter2_upper=10,
    )


@step(u'esta bateria filtra a tag "([^"]*)"')
def set_category_tag(step, tag):
    world.category_usage.tags = tag
    world.category_usage.save()


@step(u'der início ao programa')
def start_program(step):
    today = timezone.now().date()
    world.usage = models.ProgramUsage.objects.create(
        klass=models.Klass.objects.get(),
        program=world.program,
        start_date=today,
        end_date=today + datetime.timedelta(days=10),
    )
    modules = list(world.program.module_set.values_list('pk', flat=True))
    world.usage.distribute_batteries(modules)

    user = User.objects.all()[0]
    schedule = world.usage.batteryschedule_set.get()
    world.user_battery = schedule.userbattery_set.create(user=user)


@step(u'seu único dia terá os exercícios abaixo:')
def check_exercises(step):
    qs = world.user_battery.exercises.order_by('description')
    found_exercises = list(qs.values_list('description', flat=True))
    expected_exercises = sorted([d[u'Exercício'] for d in step.hashes])
    assert_equals(found_exercises, expected_exercises)


@step(u'não poderei iniciar o programa, precisa de (\d+) exercícios mas só tem (\d+)')
def cant_start_program(step, expected, found):
    try:
        start_program(step)
    except ValueError, e:
        error = str(e)
        assert_in('There is not {0}'.format(expected), error)
        assert_in('Found {0}'.format(found), error)
