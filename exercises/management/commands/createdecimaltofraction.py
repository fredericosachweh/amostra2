# -*- encoding: utf-8 -*-
from decimal import Decimal as D

from createpercentagetofraction import Command as BaseCommand


class Command(BaseCommand):
    help = "Create decimal to fraction conversion exercises."
    category = 'decimal-para-fracao'
    description = u'{0} (decimal para fração)'

    def split_terms(self, term):
        return [D(term)]

    def generate_operations(self):
        """
        Generates samples from 0.01 up to Decimal(LIMIT/100).
        """
        for i in range(0, self.limit + 1):
            for n in range(i, 100):
                yield (i + (n / D(100)),)

    def get_result(self, term1):
        """
        Makes a decimal like 0.33 to be 33 to form the first fraction term..
        """
        return term1 * 100
