import itertools

from base import BaseCommand
from exercises import models
from utils.lcm import lcm
from utils.intervals import generate_one_dimension_fractions


class Command(BaseCommand):
    help = "Create subtraction of fraction with different base exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'subtracao-fracoes-denominadores-diferentes'
    terms_separator = '-'

    def split_terms(self, operation):
        subterms = [t.strip() for t in operation.split(self.terms_separator)]
        term1, base1 = [t.strip() for t in subterms[0].split('/')]
        term2, base2 = [t.strip() for t in subterms[1].split('/')]
        if base1 == base2:
            raise ValueError('Set fractions with different base!')
        return (int(term1), int(term2), int(base1), int(base2))

    def generate_operations(self):
        """
        Combines two dimensions of terms.

        Avoids terms with same base and avoid negative result subtractions.
        """
        fractions = list(generate_one_dimension_fractions(self.limit))
        for terms in itertools.product(fractions, fractions):
            term1, base1, term2, base2 = terms[0] + terms[1]
            if base1 == base2:
                continue

            if (term1/float(base1)) <= (term2/float(base2)):
                continue  # avoid zero or negative

            yield term1, term2, base1, base2

    def create_exercise(self, term1, term2, base1, base2):
        # tag the exercise to separate additions where the result is under or
        # above one
        filter1 = min([term1, term2, base1, base2])
        filter2 = max([term1, term2, base1, base2])

        # missing1 and missing5 is the lcm denominator because we don't
        # simplify the fraction
        missing1 = missing5 = lcm((base1, base2))
        missing2 = missing1 / base1 * term1
        missing3 = missing1 / base2 * term2

        if missing2 <= missing3:
            raise ValueError('Can\'t generate a zero or negative result.')

        missing4 = missing2 - missing3

        description = '{t1}/{b1} - {t2}/{b2}'.format(t1=term1, t2=term2, b1=base1, b2=base2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplicate the exercise

        self.create_variation(exercise, term1, term2, base1, base2,
                            missing1, missing2, missing3, missing4, missing5)

        return exercise

    def create_variation(self, exercise, term1, term2, base1, base2,
                         missing1, missing2, missing3, missing4, missing5):
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

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=1,
                                          group='missing1',
                                          value=missing1))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=2,
                                          group='missing2',
                                          value=missing2))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=3,
                                          group='missing3',
                                          value=missing3))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=4,
                                          group='missing4',
                                          value=missing4))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=5,
                                          group='missing5',
                                          value=missing5))

