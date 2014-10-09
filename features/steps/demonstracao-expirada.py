# -*- coding: utf-8 -*-
import datetime

from lettuce import step, world

from clients import factories


@step(u'demonstração válida até (\d{2})/(\d{2})/(\d{4})')
def create_dated_demo(step, day, month, year):
    manager = factories.UserFactory.create(username='gestor', password='123456')
    client = factories.ClientFactory.create(cnpj='28144144000130',
                                            managers=[manager])

    valid_until = datetime.date(int(year), int(month), int(day))
    world.demo = client.demonstration_set.create(valid_until=valid_until)
