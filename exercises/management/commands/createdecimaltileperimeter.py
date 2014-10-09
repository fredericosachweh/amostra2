# -*- encoding: utf-8 -*-
import math
from decimal import Decimal as D

from _decimals import DecimalMixin
from createtileperimeter import Command as BaseCommand


class Command(DecimalMixin, BaseCommand):
    help = "Create a decimal tile perimeter exercises."
    category = 'perimetro-dos-quadrados-decimal'
    description = u'perímetro decimal de {t} quadrados de {a}{u}²'

    option_list = BaseCommand.option_list + DecimalMixin.option_list

    def handle(self, *args, **kwargs):
        self.set_decimal_places(*args, **kwargs)
        return super(Command, self).handle(*args, **kwargs)

    def split_terms(self, operation):
        """
        Split terms like "9:5.5" to create a tile objects.
        """
        subterms = [t.strip() for t in operation.split(':')]
        tiles = subterms[0]
        tilearea = subterms[1]
        unity = 'cm'  # defaults to cm for sample
        return (int(tiles), D(tilearea), unity)

    def generate_operations(self):
        dozens = D(10) ** self.decimal_places
        limit = self.tilearea_limit * dozens
        for i in xrange(2, self.limit + 1):
            for n in xrange(1, limit):
                for unity in self.UNITIES:
                    if n % 10 == 0:
                        continue
                    yield (i, n / dozens, unity['unity'])

    def get_result(self, tiles, tileside):
        """
        Calculates the perimeter using the 2nd arg as the square side.

        Differs from the base tile perimeter exercise where the 2nd argument is
        the ref square area instead of side.
        """
        return self.get_unitary_perimeter(tiles) * tileside
