import optparse

from decimal import Decimal as D
from createdecimaldivision import Command as BaseCommand


class Command(BaseCommand):
    help = "Create division of decimal per integer exercises."
    category = 'divisao-decimal-por-inteiro'

    def generate_decimal_operations(self):
        dozens = D(10) ** self.decimal_places
        start = 1
        limit = self.limit * dozens
        for term1 in xrange(start, limit + 1):
            for term2 in xrange(start, self.divisor_limit + 1):
                if term1 % 10 == 0:
                    continue  # avoid numbers like 1.10 or 2.300
                yield (term1 / dozens, term2)
