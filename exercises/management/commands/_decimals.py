import optparse

from django.core.management import CommandError

from decimal import Decimal as D
from exercises import models


class DecimalMixin(object):
    option_list = (
        optparse.make_option('--decimal-places',
            action='store', type='int', dest='decimal_places',
            help='How many decimal places?'),
    )

    def set_decimal_places(self, *args, **kwargs):
        places = kwargs.get('decimal_places', None)
        if not places:
            raise CommandError('You must specify how many decimal places')
        else:
            self.decimal_places = int(places)

    def format_number(self, n):
        return D(n.strip().replace(',', '.'))

    def only_digits(self, value):
        """
        Returns a decimal number with the decimal point stripped.

        For instance, 1.25 would be 125. Also returns the integer and decimal
        parts.
        """
        try:
            integer, decimal = str(value).split('.')
        except ValueError:
            integer = str(value)
            decimal = ''
        joined = integer + decimal
        return joined, integer, decimal

    def generate_operations(self):
        dozens = D(10) ** self.decimal_places
        start = 1
        limit = self.limit * dozens
        for term1 in xrange(start, limit):
            for term2 in xrange(start, limit):
                if term1 % 10 == 0 or term2 % 10 == 0:
                    continue  # avoid numbers like 1.10 or 2.300
                yield (term1 / dozens, term2 / dozens)


class DecimalDivisionMixin(DecimalMixin):
    def get_divided_digit(self, digit):
        """
        Converts to integer a char representing a digit from the divided.

        Maps a blank space to a zero as it will represent decimal digits after
        the last unity.
        """
        if digit == " ":
            return 0
        else:
            return int(digit)

    def get_tags(self, divided, divisor):
        """
        Returns tags based on the given decimal places.

        Unlike other decimal operations, the decimal division exercises asserts
        that the operators and the result has the specified decimal places.
        """
        return '{}-casas'.format(self.decimal_places)

    def generate_decimal_operations(self):
        """
        Returns an generator of operations.

        It is used by the generate_operations and let the subclass use an
        specific implementation and still use the custom generate_operations
        logic.
        """
        raise NotImplementedError

    def generate_operations(self):
        """
        Generate division operations of decimal per decimal.

        Reuses the range of default division but ignores exercises that do not
        result the expected decimal places.
        """
        for divided, divisor in self.generate_decimal_operations():
            result = divided / D(divisor)
            decimal_places = abs(result.as_tuple().exponent)
            if decimal_places != self.decimal_places:
                continue
            yield (divided, divisor)

    def fill_divided_with_spaces(
            self, divided, result, divided_places, divisor_places):
        """
        Fills divided with spaces to make an integer result.

        The spaces are read as zeros and are placed according result decimal
        places to give an integer result with same digits of decimal result.

        Returns the filled divided and the number of decimal places of result
        (to be used to comma generation).
        """
        result_places = abs(result.as_tuple().exponent)
        spaces_to_fill = (len(divided) +
                          result_places -
                          divided_places +
                          divisor_places)
        divided_str = divided.ljust(spaces_to_fill, " ")
        return divided_str, result_places

    def make_comma_answers(self, exercise, result, decimal_places):
        # Place the comma according result.
        result_str = str(result).replace('.', '')  # makes 1.034 be 1034
        tabindex = len(self.answers)
        for i in range(1, len(result_str)):
            if i == decimal_places:
                comma = True
            else:
                comma = False

            self.answers.append(models.Answer(exercise=exercise,
                                              type='boolean',
                                              position=i,
                                              tabindex=tabindex+i,
                                              group='comma',
                                              value=comma))
