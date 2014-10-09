# -*- coding: utf-8 -*-
import datetime
import mock

from django.core import mail
from django.core.management import call_command
from django.core.urlresolvers import reverse

from lettuce import step, world
from nose.tools import assert_equals, assert_in

from followup import models
from clients import factories


@step(u'usuário qualquer com tarefa para (\d{2})/(\d{2})/(\d{4})')
def create_sample_user(step, *task_date):
    task_date = [int(d) for d in task_date[::-1]]
    today = datetime.datetime(*task_date)
    client = factories.ClientFactory.create(cnpj='28144144000130')
    admin_staff = factories.UserFactory.create(username='admin_staff',
                                               email='manager@user.com')

    world.task = models.Task.objects.create(
        client=client,
        responsible=admin_staff,
        author=admin_staff,
        due_date=today
    )


@step(u'executar o comando para enviar tarefas por e-mail')
def send_tasks_weekly(step, *task_date):
    date_tuple = world.date_tuple
    with mock.patch('django.utils.timezone.now',
                    lambda: datetime.datetime(*date_tuple)):
        call_command('pending_tasks')


@step(u'Então usuário qualquer irá receber um aviso por e-mail')
def check_message_destinatary(step):
    assert_equals(mail.outbox[0].to, ['manager@user.com'])
    assert_equals(mail.outbox[0].subject, 'Novas tarefas para esta semana')


@step(u'E corpo do email terá link para tarefa')
def check_link_in_message_body(step):
    url = reverse('admin:followup_task_change', args=(world.task.pk,))
    assert_in(url, mail.outbox[0].body)
