# -*- encoding: utf-8 -*-
import math

from createtilearea import Command as BaseCommand


class Command(BaseCommand):
    help = "Create a tile perimeter."
    category = 'perimetro-dos-quadrados'
    description = u'perímetro de {t} quadrados de {a}{u}²'

    def get_tilearea_range(self):
        """
        Returns only perfect squares as range for tilearea.
        """
        return [x ** 2 for x in xrange(1, self.tilearea_limit + 1)]

    def get_unitary_perimeter(self, tiles):
        """
        Calculates the perimeter assuming the side has 1 length unity.

        As we have side-by-side tiles disposed in a perfect square, just count
        the number of lines and columns to get perimeter.
        """
        columns = math.ceil(math.sqrt(tiles))
        lines = math.ceil(tiles / columns)
        return int((lines * 2) + (columns * 2))

    def get_result(self, tiles, tilearea):
        square_side = math.sqrt(tilearea)
        if square_side != int(square_side):
            raise ValueError('Square size must be a perfect square')

        return self.get_unitary_perimeter(tiles) * square_side
