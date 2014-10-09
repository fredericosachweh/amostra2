# -*- coding: utf-8 -*-
from decimal import Decimal

from django.conf import settings

from lettuce import step


@step(u'custo por turma é ([\d,]+)')
def check_klasses_cost(step, value):
    value = Decimal(value.replace(',', '.'))
    settings.KLASSES_COST = value


@step(u'o limite de pagamento mínimo é ([\d,]+)')
def set_minimal_payment_limit(step, value):
    value = Decimal(value.replace(',', '.'))
    settings.MINIMAL_PAYMENT_COST = value
