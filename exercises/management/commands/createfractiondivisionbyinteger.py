import itertools

from base import BaseCommand
from exercises import models
from utils.intervals import generate_one_dimension_fractions


class Command(BaseCommand):
    help = "Create division of fraction by integer"
    matter = 'matematica'
    subject = 'fracoes'
    category = 'divisao-fracao-por-inteiro'

    def split_terms(self, operation):
        """
        Splits operation in subterms.

        Receives a operation like '2/3 / 4' and splits the reversed string
        using '/' as separator to get ('4, '3/2'), then returns term1, base1
        and term2 (in the original expected order).
        """
        subterms = [t.strip() for t in operation[::-1].split('/', 1)]
        term2 = subterms[0]
        base1, term1 = [t.strip() for t in subterms[1].split('/')]
        return (int(term1), int(base1), int(term2))

    def generate_operations(self):
        """
        Combines a list of fractions with a list of integers.
        """
        fractions = list(generate_one_dimension_fractions(self.limit))
        interval = xrange(2, self.limit + 1)
        for terms in itertools.product(interval, fractions):
            term2 = terms[0]
            term1, base1 = terms[1]
            if term1 == base1:
                continue
            yield term1, base1, term2

    def create_exercise(self, term1, base1, term2):
        # calculates missing terms to answer

        missing1 = term1
        missing2 = base1
        missing3 = 1
        missing4 = term2
        missing5 = term1
        missing6 = base1 * term2

        filter1 = min([term1, base1, term2])
        filter2 = max([term1, base1, term2])

        description = '{t1}/{b1} / {t2}'.format(t1=term1,
            b1=base1, t2=term2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplicate the exercise

        self.create_variation(exercise, term1, base1, term2, missing1, missing2,
                              missing3, missing4, missing5, missing6)

        return exercise

    def create_variation(self, exercise, term1, base1, term2, missing1, missing2,
                         missing3, missing4, missing5, missing6):

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=1,
                                              group='term1',
                                              char_value=str(term1)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term1',
                                              char_value=str(base1)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term2',
                                              char_value=str(term2)))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=1,
                                          tabindex=1,
                                          group='partial1',
                                          value=missing1))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=2,
                                          group='partial1',
                                          value=missing2))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=1,
                                          tabindex=3,
                                          group='partial2',
                                          value=missing3))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=4,
                                          group='partial2',
                                          value=missing4))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=1,
                                          tabindex=5,
                                          group='result',
                                          value=missing5))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=6,
                                          group='result',
                                          value=missing6))
