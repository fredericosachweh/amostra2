from _decimals import DecimalMixin
from createaddition import Command as BaseCommand
from exercises import models


class Command(DecimalMixin, BaseCommand):
    help = "Create decimal addition exercises."
    category = 'soma-dois-andares-decimal'

    option_list = BaseCommand.option_list + DecimalMixin.option_list

    def handle(self, *args, **kwargs):
        self.set_decimal_places(*args, **kwargs)
        return super(Command, self).handle(*args, **kwargs)

    def split_terms(self, operation):
        """ Returns decimal numbers converted from strings like 9,99. """
        return [self.format_number(t) for t in operation.split('+')]

    def get_tags(self):
        return '{}-casas'.format(self.decimal_places)

    def create_exercise_data(self, exercise, term1, term2):
        f = '{:.%df}' % self.decimal_places  # .2f, .3f and so on
        int1, dec1 = f.format(term1).split('.')
        int2, dec2 = f.format(term2).split('.')

        size = max(len(dec1), len(dec2))
        if len(dec2) < size:
            dec2 = dec2.ljust(size, '0')
        if len(dec1) < size:
            dec1 = dec1.ljust(size, '0')

        str1 = int1 + dec1
        str2 = int2 + dec2

        # creates the integer addition
        super(Command, self).create_exercise_data(exercise, int(str1), int(str2))

        for i in range(1, len(str1)):
            if i == self.decimal_places:
                comma = ','
            else:
                comma = ' '
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='comma1',
                                                  char_value=comma))
        for i in range(1, len(str2)):
            if i == self.decimal_places:
                comma = ','
            else:
                comma = ' '
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='comma2',
                                                  char_value=comma))

        result = term1 + term2
        result_str = f.format(result).replace('.', '')  # makes 1.034 be 1034
        tabindex = len(self.answers)
        for i in range(1, len(result_str)):
            if i == self.decimal_places:
                comma = True
            else:
                comma = False

            self.answers.append(models.Answer(exercise=exercise,
                                              type='boolean',
                                              position=i,
                                              tabindex=tabindex+i,
                                              group='comma',
                                              value=comma))
