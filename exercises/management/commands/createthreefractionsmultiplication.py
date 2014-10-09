import itertools

from base import BaseCommand
from exercises import models
from utils.intervals import generate_one_dimension_fractions


class Command(BaseCommand):
    help = "Create multiplication of 3 fractions exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'multiplicacao-3-fracoes'

    def split_terms(self, operation):
        """
        Breaks three fractions into a tuple like (t1, b1, t2, b2, t3, b3).
        """
        subterms = [t.strip() for t in operation.split('*')]
        terms = []
        for term in subterms:
            terms.extend([int(x) for x in term.split('/')])
        return terms

    def generate_operations(self):
        """
        Generates 3 fractions combinations.

        Returns a tuple like (t1, b1, t2, b2, t3, b3).
        """
        fractions = list(generate_one_dimension_fractions(self.limit))
        for terms in itertools.product(fractions, fractions, fractions):
            yield terms[0] + terms[1] + terms[2]

    def create_exercise(self, term1, base1, term2, base2, term3, base3):
        numerator = term1 * term2 * term3
        denominator = base1 * base2 * base3
        if numerator > denominator:
            tags = 'maior-que-1'
        else:
            tags = 'menor-igual-1'

        filter1 = max([term1, base1, term2, base2, term3, base3])
        filter2 = max([numerator, denominator])

        description = '{t1}/{b1} * {t2}/{b2} * {t3}/{b3}'.format(
            t1=term1, t2=term2, t3=term3, b1=base1, b2=base2, b3=base3)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            tags=tags,
            filter1=filter1,
            filter2=filter2
        )

        if not created:
            return  # avoid duplicate the exercise

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
                                              position=1,
                                              group='term2',
                                              char_value=str(term2)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term2',
                                              char_value=str(base2)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=1,
                                              group='term3',
                                              char_value=str(term3)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term3',
                                              char_value=str(base3)))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=1,
                                          tabindex=1,
                                          group='result',
                                          value=numerator))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=2,
                                          group='result',
                                          value=denominator))
