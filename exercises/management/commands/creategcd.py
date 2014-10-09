import fractions

from createlcm import Command as BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create a greatest common divisor exercise."
    category = 'mdc'
    description = 'MDC({0})'
    split_regex = r'(GCD|MDC)\((.*)\)'

    def get_terms_gcd(self, terms):
        """
        Returns the GDC for two or more terms.

        The fractions.gcd can operate only two terms, we combine the results as
        they get calculated through reduce.
        """
        return reduce(fractions.gcd, terms)

    def generate_operations(self):
        """
        Returns the same range as the MDC but ignore result=1.
        """
        for terms in super(Command, self).generate_operations():
            result = self.get_terms_gcd(terms)
            if result > 1:
                yield terms

    def create_result(self, exercise, numbers, divisors_and_steps):
        result = self.get_terms_gcd(numbers)
        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=1,
                                          tabindex=len(self.answers) + 1,
                                          group='result',
                                          value=result))
