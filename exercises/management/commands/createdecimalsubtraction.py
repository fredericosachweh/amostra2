from decimal import Decimal as D

from _decimals import DecimalMixin
from createsubtraction import Command as BaseCommand
from exercises import models


class Command(DecimalMixin, BaseCommand):
    help = "Create decimal subtraction exercises."
    category = 'subtracao-decimal'

    option_list = BaseCommand.option_list + DecimalMixin.option_list

    def handle(self, *args, **kwargs):
        self.set_decimal_places(*args, **kwargs)
        return super(Command, self).handle(*args, **kwargs)

    def split_terms(self, operation):
        """ Returns decimal numbers converted from strings like 9,99. """
        return [self.format_number(t) for t in operation.split('-')]

    def generate_operations(self):
        dozens = D(10) ** self.decimal_places
        start = 1
        limit = self.limit * dozens
        for term1 in xrange(start, limit):
            for term2 in xrange(start, term1):
                if term1 % 10 == 0 or term2 % 10 == 0:
                    continue  # avoid numbers like 1.10 or 2.300
                yield (term1 / dozens, term2 / dozens)

    def get_tags(self):
        return '{}-casas'.format(self.decimal_places)

    def create_exercise_data(self, exercise, term1, term2):
        int1, dec1 = str(term1).split('.')
        int2, dec2 = str(term2).split('.')

        size = max(len(dec1), len(dec2))
        if len(dec2) < size:
            dec2 = dec2.ljust(size, '0')
        if len(dec1) < size:
            dec1 = dec1.ljust(size, '0')

        str1 = int1 + dec1
        str2 = int2 + dec2
        super(Command, self).create_exercise_data(exercise, int(str1), int(str2))

        decimal_places = max(len(dec1), len(dec2))
        for i in range(1, len(str1)):
            if i == decimal_places:
                comma = ','
            else:
                comma = ' '
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='comma1',
                                                  char_value=comma))
        for i in range(1, len(str2)):
            if i == decimal_places:
                comma = ','
            else:
                comma = ' '
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='comma2',
                                                  char_value=comma))

        result = str(int(str1) + int(str2))
        tabindex = len(self.answers)
        for i in range(1, len(result)):
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
