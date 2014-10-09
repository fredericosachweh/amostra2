import itertools
from decimal import Decimal as D

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create equivalent fraction exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'fracoes-equivalentes'

    def split_terms(self, operation):
        subterms = [t.strip() for t in operation.split('=')]
        term1, term2 = [int(t.strip()) for t in subterms[0].split('/')]
        term3, term4 = [int(t.strip()) for t in subterms[1].split('/')]
        return (term1, term2, term3, term4)

    def generate_operations(self):
        interval = xrange(1, self.limit + 1)
        axis = [interval] * 3
        for terms in itertools.product(*axis):
            a, b, c = terms
            d = c * b / D(a)
            if d != int(d):
                continue  # only integer denominator
            if a == b:
                continue  # avoid a/a == c/c
            yield a, b, c, d

    def create_exercise(self, *args):
        if (args[0] / D(args[1])) != (args[2] / D(args[3])):
            raise ValueError('The fractions must be equivalent')

        filter1 = min(args)
        filter2 = max(args)

        description = '{0}/{1} = {2}/{3}'.format(*args)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplicate the exercise

        for n, i in enumerate(args[0:3], start=1):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=n,
                                                  group='term%d' % n,
                                                  char_value=str(i)))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=1,
                                          tabindex=1,
                                          group='missing4',
                                          value=args[3]))

        return exercise
