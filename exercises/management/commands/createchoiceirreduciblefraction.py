# -*- encoding: utf-8 -*-
import fractions
from decimal import Decimal as D

from base import BaseCommand
from exercises import models
from utils.intervals import generate_one_dimension_fractions


class Command(BaseCommand):
    help = "Create figure to fraction convertion exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'escolha-da-fracao-irredutivel'
    bulk_create_answers = False

    def split_terms(self, operation):
        subterms = [t.strip() for t in operation.split('=')]
        term1, term2 = [t.strip() for t in subterms[0].split('/')]
        term3, term4 = [t.strip() for t in subterms[1].split('/')]
        return (int(term1), int(term2), int(term3), int(term4))

    def generate_operations(self):
        """
        Generates options for irreducible fractions exercises.

        Make fractions from 2/3 until N-1/N, ignoring any fraction
        without a simplified version.
        """
        interval = generate_one_dimension_fractions(self.limit, start=2)
        for term1, term2 in interval:
            simplified = fractions.Fraction(term1, term2)
            term3, term4 = (simplified.numerator, simplified.denominator)

            # Ignore equal fractions (that was not simplified)
            if term1 == term3 and term2 == term4:
                continue

            yield (term1, term2, term3, term4)

    def make_choices(self, term3, term4):
        """
        Generate 9 choices to complete choice_map.

        Generate choices with denominator greater that the numerator, sum of
        the n with the term3 or term4, if result is same a 1/4, denominator
        recept denominator multiplicated per n.
        The result is 3/6, 4/7, 5/8, 6/9, 7/10, 8/11, 9/12, 10/13, 11/14, 12/15,
        13/16, 14/17, 15/18, 16/19, 17/20, 18/21, 19/22, 20/23, 21/24.
        """
        ratio = float(term3) / float(term4)
        for i in range(2, 21):
            numerator = min(term3 + i, term4 + i)
            denominator = max(term3 + i, term4 + i)

            if float(numerator) / float(denominator) == ratio:
                denominator = denominator * i
            yield numerator, denominator

    def create_exercise(self, term1, term2, term3, term4):
        if (term1 / D(term2)) != (term3 / D(term4)):
            raise ValueError('The fractions must be equivalent')

        filter1 = min([term1, term2, term3, term4])
        filter2 = max([term1, term2, term3, term4])

        description = u'{0}/{1} = {2}/{3} (escolha da fração irred.)'.format(
                term1, term2, term3, term4)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplicate exercise

        for n, term in enumerate([term2, term1]):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=n,
                                                  group='fraction',
                                                  char_value=str(term)))

        choices_map = ['+{0}/{1}'.format(term3, term4)]
        for i, j in self.make_choices(term3, term4):
            choices_map.append('-{0}/{1}'.format(i, j))

        # give limit to 5 choices no matter how many was defined
        self.answers.append(models.Answer(exercise=exercise,
                                          type='radio',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          choices_map='\n'.join(choices_map),
                                          choices_sample=5))

        return exercise
