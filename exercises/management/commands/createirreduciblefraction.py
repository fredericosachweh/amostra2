from decimal import Decimal as D
import fractions

from base import BaseCommand
from exercises import models
from utils.intervals import generate_one_dimension_fractions


class Command(BaseCommand):
    help = "Create irreducible fraction exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'fracoes-irredutiveis'

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

    def create_exercise(self, *args):
        if (args[0] / D(args[1])) != (args[2] / D(args[3])):
            raise ValueError('The fractions must be equivalent')

        filter1 = min(args)
        filter2 = max(args)

        description = '{0}/{1} = {2}/{3} (irred.)'.format(*args)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplicate the exercise

        for n, i in enumerate(args[0:2][::-1]):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=n,
                                                  group='term',
                                                  char_value=str(i)))

        for n, i in enumerate(args[2:][::-1]):
            self.answers.append(models.Answer(exercise=exercise,
                                              type='exact',
                                              position=n,
                                              tabindex=2 - n,
                                              group='missing',
                                              value=i))

        return exercise
