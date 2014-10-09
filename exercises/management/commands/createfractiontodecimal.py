# -*- encoding: utf-8 -*-
from decimal import Decimal as D
from createfractiontopercentage import Command as BaseCommand


class Command(BaseCommand):
    help = "Create fraction to decimal convertion exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'fracao-para-decimal'
    description = u'{0}/{1} (fração para decimal)'

    def get_result(self, term1, term2):
        return term1 / D(term2)
