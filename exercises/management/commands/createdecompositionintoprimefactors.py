from base import BaseCommand
from exercises import models
from utils.primes import PRIME_NUMBERS


class Command(BaseCommand):
    help = "Create decomposition into prime factors exercise."
    subject = 'numeros-primos'
    matter = 'matematica'
    category = 'decomposicao-em-fatores-primos'
    description = 'Decomp. do {0} em primos'

    def divide_by_prime(self, x, prime):
        if x % prime == 0:
            return x // prime
        else:
            return x

    def split_terms(self, operation):
        """
        Returns a clean integer passed as argument.

        Returns it as a list to conform with the create_exercise method that
        also works for many combined terms.
        """
        return [int(operation)]

    def generate_operations(self):
        interval = xrange(2, self.limit + 1)
        for term in interval:
            if term in PRIME_NUMBERS:
                continue
            yield [term]

    def get_tags(self):
        return ''

    def create_exercise(self, *numbers):
        involved_numbers = ', '.join([str(n) for n in numbers])
        description = self.description.format(involved_numbers)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            filter1=min(numbers),
            filter2=max(numbers),
            tags=self.get_tags()
        )

        if not created:
            return  # avoid duplications

        divisors_and_steps = self.get_divisors(exercise, *numbers)
        self.create_result(exercise, numbers, divisors_and_steps)
        return exercise

    def get_divisors(self, exercise, *numbers):
        """
        Decomposes one or more numbers into [common] divisors.

        Attends a decomposition exercise but can also attend a lower common
        divisor.
        """
        for n, number in enumerate(numbers[::-1]):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=n,
                                                  group='numbers',
                                                  char_value=str(number)))

        primes = list(PRIME_NUMBERS)
        lines = []

        line = list(numbers[:])  # copied
        end = [1] * len(line)  # [1, 1, 1, ...]
        while line != end:
            prime = primes[0]
            new_line = [self.divide_by_prime(x, prime) for x in line]
            if new_line == line:
                primes.pop(0)  # ignore this prime as it doesn't divide any number
            else:
                line = new_line
                lines.append((prime, line))

        for i, (divisor, steps) in enumerate(lines[::-1]):
            divisor_tabindex = (len(numbers) + 1) * (len(lines) - i - 1) + 1
            self.answers.append(models.Answer(exercise=exercise,
                                              type='exact',
                                              position=i,
                                              tabindex=divisor_tabindex,
                                              group='divisors',
                                              value=divisor))

            for j, step in enumerate(steps[::-1]):
                position = j + len(numbers) * i
                tabindex = divisor_tabindex + len(numbers) - j
                self.answers.append(models.Answer(exercise=exercise,
                                                  type='exact',
                                                  position=position,
                                                  tabindex=tabindex,
                                                  group='steps',
                                                  value=step))
        return lines

    def create_result(self, exercise, numbers, divisors_and_steps):
        """
        Handle the divisors to create a result.

        Not used for decomposition exercises but useful for lower common
        divisors.
        """
        pass
