import optparse
from decimal import Decimal as D

from django.core.management import CommandError

from _decimals import DecimalMixin
from base import BaseCommand
from exercises import models


class Command(DecimalMixin, BaseCommand):
    help = "Create multiplication of decimal per dozens exercises."
    matter = 'matematica'
    subject = 'multiplicacao'
    category = 'multiplicacao-decimal-por-dezena-centena-e-milhar'
    description = '{0} * {1} (por dezena)'

    option_list = BaseCommand.option_list + DecimalMixin.option_list + (
        optparse.make_option('--dozen-limit',
            action='store', type='int', dest='dozen_limit',
            help='What will be the limit for the multiplicator dozen?'),
    )

    def handle(self, *args, **kwargs):
        self.dozen_limit = kwargs['dozen_limit']
        if not self.dozen_limit:
            if not kwargs['operation']:
                raise CommandError('You must specify the dozen limit.')
            else:
                self.dozen_limit = None
        try:
            self.set_decimal_places(*args, **kwargs)
        except CommandError, e:
            if not kwargs['operation']:
                raise e
            else:
                self.decimal_places = None
        return super(Command, self).handle(*args, **kwargs)

    def split_terms(self, operation):
        """ Returns decimal numbers converted from strings like 9,99. """
        return [self.format_number(t) for t in operation.split('*')]

    def get_dozens(self):
        dozen = self.dozen_limit
        times = [1]
        while 1:
            if dozen < 10:
                break

            dozen = dozen / 10
            times.append(times[-1] * 10)
        return times[1:]

    def generate_operations(self):
        dozens = D(10) ** self.decimal_places
        start = 1
        limit = self.limit * dozens
        for term1 in xrange(start, limit + 1):
            for term2 in self.get_dozens():
                if term1 % 10 == 0:
                    continue  # avoid numbers like 1.10 or 2.300 or term2 not a dozen
                yield (term1 / dozens, term2)

    def get_tags(self):
        """
        Tells tag based on the given number of decimal places.
        """
        return '{}-casas'.format(self.decimal_places)

    def create_exercise(self, term1, term2):
        description = self.description.format(term1, term2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            tags=self.get_tags(),
            filter1=term1,
            filter2=term2
        )

        if not created:
            return  # avoid duplications

        self.create_exercise_data(exercise, term1, term2)
        return exercise

    def get_result(self, term1, term2):
        return '%g' % (term1 * term2)

    def create_exercise_data(self, exercise, term1, term2):
        str1, int1, dec1 = self.only_digits(term1)

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term1',
                                              char_value='{0},{1}'.format(int1, dec1)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=1,
                                              group='term2',
                                              char_value=term2))

        result = self.get_result(term1, term2)
        result_str, result_int, result_dec = self.only_digits(result)
        result_places = str(result)[::-1].find('.')

        for i, r in enumerate(result_str):
            self.answers.append(models.Answer(exercise=exercise,
                                              type='char',
                                              position=len(result_str) - i,
                                              tabindex=i + 1,
                                              group='result',
                                              value=r))

        tabindex = len(self.answers)
        last_answer = self.answers[0]
        result_length = last_answer.position
        for i in range(1, result_length):
            if i == result_places:
                comma = True
            else:
                comma = False

            self.answers.append(models.Answer(exercise=exercise,
                                              type='boolean',
                                              position=i,
                                              tabindex=tabindex + i,
                                              group='comma',
                                              value=comma))
