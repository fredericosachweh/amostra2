from _decimals import DecimalMixin
from createmultiplication import Command as BaseCommand
from exercises import models


class Command(DecimalMixin, BaseCommand):
    help = "Create decimal multiplication exercises."
    category = 'multiplicacao-decimal'

    option_list = BaseCommand.option_list + DecimalMixin.option_list

    def handle(self, *args, **kwargs):
        places = kwargs.get('decimal_places', None)
        if not places and not kwargs['operation']:
            raise Exception('You must specify how many decimal places')
        else:
            if places:
                self.decimal_places = int(places)
            else:
                self.decimal_places = None
        return super(Command, self).handle(*args, **kwargs)

    def split_terms(self, operation):
        """ Returns decimal numbers converted from strings like 9,99. """
        return [self.format_number(t) for t in operation.split('*')]

    def get_tags(self, *args):
        """
        Tells tag based on the max number of decimal places.

        For instance, 22.5*1.46 would have 2 decimal places and a compatible
        tag name.
        """
        terms_places = [str(t)[::-1].find('.') for t in args]
        places = max(terms_places)
        return '{}-casas'.format(places)

    def create_exercise_data(self, exercise, term1, term2):
        str1, int1, dec1 = self.only_digits(term1)
        str2, int2, dec2 = self.only_digits(term2)
        super(Command, self).create_exercise_data(
            exercise, int(str1), int(str2), sterm1=str1, sterm2=str2)

        for i in range(1, len(str1)):
            if i == len(dec1):
                comma = ','
            else:
                comma = ' '
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='comma1',
                                                  char_value=comma))
        for i in range(1, len(str2)):
            if i == len(dec2):
                comma = ','
            else:
                comma = ' '
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='comma2',
                                                  char_value=comma))

        result = term1 * term2
        result_places = str(result)[::-1].find('.')
        tabindex = len(self.answers)

        # creates as many commas as result positions, the position is gotten
        # from the last answer that is necessary a result
        last_answer = self.answers[-1]
        if len(str2) > 1:
            assert last_answer.group == 'result'
        else:
            assert last_answer.group == 'partial1'
        result_length = last_answer.position + 1

        for i in range(1, result_length):
            if i == result_places:
                comma = True
            else:
                comma = False

            self.answers.append(models.Answer(exercise=exercise,
                                              type='boolean',
                                              position=i,
                                              tabindex=tabindex+i,
                                              group='comma',
                                              value=comma))
