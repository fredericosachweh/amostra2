import itertools

from base import BaseCommand
from exercises import models
from utils.intervals import generate_one_dimension_fractions


class Command(BaseCommand):
    help = "Create multiplication of fraction by integer"
    matter = 'matematica'
    subject = 'fracoes'
    category = 'multiplicacao-fracao-por-inteiro'
    terms_separator = '*'

    def split_terms(self, operation):
        subterms = [t.strip() for t in operation.split(self.terms_separator)]
        term1 = subterms[0]
        term2, base2 = [t.strip() for t in subterms[1].split('/')]
        return (int(term1), int(term2), int(base2))

    def generate_operations(self):
        """
        Generate terms like 2 * 1/2, 2 * 1/3, LIMIT * 3/LIMIT and so on.
        """
        fractions = list(generate_one_dimension_fractions(self.limit))
        interval = xrange(2, self.limit + 1)
        for term1, (term2, base2) in itertools.product(interval, fractions):
            if term2 == base2:
                continue
            yield term1, term2, base2

    def create_exercise(self, term1, term2, base2):
        # tag the exercise to separate additions where the result is under or
        # above one
        missing1 = term1 * term2
        missing2 = base2

        filter1 = min([term1, term2, base2])
        filter2 = max([term1, term2, base2])

        description = '{t1} * {t2}/{b2}'.format(t1=term1,
            t2=term2, b2=base2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplicate the exercise

        self.create_variation(exercise, term1, term2, base2, missing1, missing2)

        return exercise

    def create_variation(self, exercise, term1, term2, base2, missing1,  missing2):
        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term1',
                                              char_value=str(term1)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=1,
                                              group='term2',
                                              char_value=str(term2)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term2',
                                              char_value=str(base2)))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=1,
                                          tabindex=1,
                                          group='missing',
                                          value=missing1))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=2,
                                          group='missing',
                                          value=missing2))
