import re
import itertools
import optparse

from createdecompositionintoprimefactors import Command as BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create a lowest commom multiple exercise."
    category = 'mmc'
    description = 'MMC({0})'
    split_regex = r'(LCM|MMC)\((.*)\)'

    option_list = BaseCommand.option_list + (
        optparse.make_option(
            '--terms',
            action='store', type='int', dest='terms',
            help='How many terms in the operation?'),
    )

    def handle(self, *args, **kwargs):
        self.terms = kwargs.get('terms', None)
        if not self.terms:
            raise Exception('You must specify how many terms')
        return super(Command, self).handle(*args, **kwargs)

    def split_terms(self, operation):
        """ A textual operation should be in form MMC(X, Y). """
        match = re.search(self.split_regex, operation, re.I)
        if not match:
            raise ValueError
        else:
            return [int(x) for x in match.group(2).split(',')]

    def generate_operations(self):
        interval = xrange(2, self.limit + 1)
        axis = [interval] * self.terms
        for terms in itertools.product(*axis):
            if len(set(terms)) != self.terms:
                continue  # ignore repeated numbers
            yield terms

    def get_tags(self):
        return '{0}-terms'.format(self.terms)  # identifies how many terms

    def create_result(self, exercise, numbers, divisors_and_steps):
        divisors = [divisor for divisor, steps in divisors_and_steps]
        result = reduce(lambda x, y: x * y, divisors)
        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=1,
                                          tabindex=len(self.answers) + 1,
                                          group='result',
                                          value=result))
