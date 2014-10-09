from decimal import Decimal as D

from _decimals import DecimalDivisionMixin
from createdivision import Command as BaseCommand
from exercises import models


class Command(DecimalDivisionMixin, BaseCommand):
    help = "Create division exercises of decimal per decimal."
    matter = 'matematica'
    subject = 'divisao'
    category = 'divisao-decimal'

    option_list = BaseCommand.option_list + DecimalDivisionMixin.option_list

    def handle(self, *args, **kwargs):
        self.set_decimal_places(*args, **kwargs)
        return super(Command, self).handle(*args, **kwargs)

    def split_terms(self, operation):
        """ Returns decimal numbers converted from strings like 9,99. """
        return [self.format_number(t) for t in operation.split('/')]

    def generate_decimal_operations(self):
        return DecimalDivisionMixin.generate_operations(self)

    def create_exercise_data(self, exercise, divided, divisor):
        # Use the divided and divisor as integers fixed to give a result with
        # the same digits of the decimal result, but integer.
        str1, int1, dec1 = self.only_digits(divided)
        str2, int2, dec2 = self.only_digits(divisor)

        result = divided / D(divisor)
        str1_, decimal_places = self.fill_divided_with_spaces(
            divided=str1,
            result=result,
            divided_places=len(dec1),
            divisor_places=len(dec2)
        )

        super(Command, self).create_exercise_data(exercise, str1_, str2)

        for i in range(1, len(str1_)):
            if i == self.decimal_places + len(str1_) - len(str1):
                comma = ','
            else:
                comma = ' '
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='comma_divided',
                                                  char_value=comma))

        for i in range(1, len(str2)):
            if i == self.decimal_places:
                comma = ','
            else:
                comma = ' '
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='comma_divisor',
                                                  char_value=comma))

        self.make_comma_answers(exercise, result, decimal_places)
