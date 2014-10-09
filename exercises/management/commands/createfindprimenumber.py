# -*- encoding: utf-8 -*-
import random

from base import BaseCommand
from exercises import models
from utils import primes


class Command(BaseCommand):
    help = "Create exercises to find prime numbers."
    matter = 'matematica'
    subject = 'numeros-primos'
    category = 'encontre-numero-primo'
    description = u'encontre número primo {0}'
    bulk_create_answers = False

    def split_terms(self, term):
        term = int(term)
        if term > max(primes.PRIME_NUMBERS):
            raise ValueError('Max limit is %d.' % max(primes.PRIME_NUMBERS))
        if not term in primes.PRIME_NUMBERS:
            raise ValueError('{0} is not a prime number'.format(term))
        return (term,)

    def generate_operations(self):
        """
        Generates options for exercise.

        Create exercises where correct result is a prime number until limit.
        """
        for term in primes.PRIME_NUMBERS:
            if not term > self.limit:
                yield (term,)

    def create_exercise(self, term):
        desc = self.description.format(term)
        exercise, created = self.category.exercise_set.get_or_create(
            description=desc, filter1=term)

        if not created:
            return  # avoid duplicate exercise

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term',
                                              char_value=str(term)))

        # One correct answer and 9 possible incorrects
        choices_map = ['+{0}'.format(term)]
        numbers = [i for i in range(2, 109) if i not in primes.PRIME_NUMBERS]
        random.shuffle(numbers)
        for number in numbers[:29]:
            choices_map.append('-{0}'.format(number))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='radio',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          choices_map='\n'.join(choices_map),
                                          choices_sample=9))

        return exercise
