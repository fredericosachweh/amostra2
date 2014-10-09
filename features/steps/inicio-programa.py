# -*- coding: utf-8 -*-

from django.core.management import call_command

from lettuce import step, world
from lettuce.django import django_url
from nose.tools import assert_true

from exercises.models import Program


@step(u'Dado um programa exemplo com (\d+) baterias')
def create_sample_program(step, batteries):
    call_command('loaddata', 'exercises_categories.json')
    call_command('loaddata', 'exercises_programs.json')
    program = Program.objects.get(pk=1)
    program.batteries_count = int(batteries)
    program.save()
    world.program = program


@step(u'verei o programa exemplo com (\d+) dias')
def check_batteries_number(step, batteries):
    assert_true(world.browser.is_text_present(world.program.name))
    assert_true(world.browser.is_text_present(u'{0} dias'.format(batteries)))


@step(u'verei o conteúdo programático do programa exemplo')
def content_programatic(step):
    assert_true(world.browser.is_text_present(u'Conteúdo programático'))
    assert_true(world.browser.is_text_present(u'Soma'))
