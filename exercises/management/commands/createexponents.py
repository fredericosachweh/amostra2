import optparse
import itertools

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create exponentation exercises."
    matter = 'matematica'
    subject = 'exponenciacao'
    category = 'potenciacao-de-inteiros'

    option_list = BaseCommand.option_list + (
        optparse.make_option('--exponent-limit',
            action='store', type='int', dest='exponent_limit',
            help='What is the exponent limit?'),
    )

    def handle(self, *args, **kwargs):
        self.exponent_limit = kwargs.get('exponent_limit', None)
        if not self.exponent_limit:
            if not kwargs['operation']:
                raise ValueError('You must specify the exponent limit')
        return super(Command, self).handle(*args, **kwargs)

    def split_terms(self, operation):
        subterms = [t.strip() for t in operation.split('^')]
        term1 = subterms[0]
        term2 = subterms[1]
        return (int(term1), int(term2))

    def generate_operations(self):
        """
        Generates exponent choices like 1^2, 2^0, 3^7 or 5^3.

        Seek until reach self.limit ^ self.exponent_limit. Calculates the
        result to stay under the database field limit and pass the result
        forward to avoid recalculate in the exercise creation.
        """
        numbers = xrange(1, self.limit + 1)
        exponents = xrange(0, self.exponent_limit + 1)
        for i, j in itertools.product(numbers, exponents):
            result = pow(i, j)  # Evaluate the exponents
            if result >= 10**8:
                continue  # Ignore exercises above models limit
            yield (i, j, result)

    def create_exercise(self, term1, term2, result=None):
        """
        Creates exponent exercises.

        Calculates the intermediary steps so the student may tell the final
        result and as many steps as the exponent number. E.g.:

        2^4 = 2 * 2 * 2 * 2 = 16

        Accepts the result as argument or calculates the result otherwise.
        """
        if result is None:
            result = pow(term1, term2)  # Evaluate the exponents

        if term1 % 10 == 0:
            tags = 'dezena'
        else:
            tags = 'unidade'

        description = '{0}^{1}'.format(term1, term2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            filter1=term1,
            filter2=term2,
            tags=tags
        )

        if not created:
            return  # avoid create the exercise again

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term1',
                                              char_value=term1))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term2',
                                              char_value=term2))

        if term2 > 1:
            for i, n in enumerate(range(term2)[::-1]):
                self.answers.append(models.Answer(exercise=exercise,
                                                  type='exact',
                                                  position=i,
                                                  tabindex=n+1,
                                                  group='partial',
                                                  value=term1))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=len(self.answers) + 1,
                                          group='result',
                                          value=result))
