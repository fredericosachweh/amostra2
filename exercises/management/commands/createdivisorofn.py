# -*- encoding: utf-8 -*-
import optparse
import random

from django.core.management.base import CommandError

from base import BaseCommand
from exercises import models
from utils.primes import PRIME_NUMBERS


class Command(BaseCommand):
    help = "Create exercises to tell numbers divisors of N."
    matter = 'matematica'
    subject = 'divisao'
    category = 'divisor-de-n'
    description = u'{0} divisor de {1}'
    bulk_create_answers = False

    option_list = BaseCommand.option_list + (
        optparse.make_option('--divisor-limit',
            action='store', type='int', dest='divisor_limit',
            help='What will be the limit for the divisor range?'),
    )

    def handle(self, *args, **kwargs):
        self.divisor_limit = kwargs.get('divisor_limit', None)
        if not kwargs['operation'] and not self.divisor_limit:
            raise Exception('You must specify the divisor range limit')
        return super(Command, self).handle(*args, **kwargs)

    def make_not_divisors(self, divisor, divided):
        """
        Lists 21 numbers that are not divisors of divided.

        Uses numbers next to the specified divisor to the correct and wrong
        choices have the same magnitude.
        """
        not_divisors = []
        count = 1
        while len(not_divisors) < 21:
            forward = divisor + count
            if divided % forward != 0:
                not_divisors.append(forward)
            backward = divisor - count
            if backward > 1 and divided % backward != 0:
                not_divisors.append(backward)
            count += 1
        return not_divisors

    def is_prime(self, number):
        """
        Test known prime numbers and a low list of divisors.

        This can produce no primes only divisible by 13 (as an example), but it
        is enough for the application.
        """
        if number in PRIME_NUMBERS:
            return True
        for i in range(2, 11):
            if number % i:
                return False
        return True

    def split_terms(self, terms):
        terms = terms.split('/')
        divided = int(terms[0])
        divisor = int(terms[1])
        if self.is_prime(divided):
            raise CommandError('The divided "%s" is prime.' % divided)

        not_divisors = self.make_not_divisors(divisor, divided)
        return (divided, divisor, not_divisors)

    def generate_operations(self):
        for divided in range(2, self.limit + 1):
            if self.is_prime(divided):
                continue

            # Only one iterator to divisors individeds per divisor
            divisor_limit = min([self.divisor_limit + 1, divided])
            for divisor in range(2, divisor_limit):
                if divided % divisor == 0:
                    not_divisors = self.make_not_divisors(divisor, divided)
                    yield (divided, divisor, not_divisors)

    def create_exercise(self, divided, divisor, not_divisors):
        filter1 = divided
        filter2 = divisor

        desc = self.description.format(divided, divisor)
        exercise, created = self.category.exercise_set.get_or_create(
            description=desc, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplicate exercise

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term',
                                              char_value=str(divided)))

        # One correct answer and 9 possible incorrects
        choices_map = ['+{0}'.format(divisor)]
        random.shuffle(not_divisors)
        for not_divisor in not_divisors[:9]:
            choices_map.append('-{0}'.format(not_divisor))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='radio',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          choices_map='\n'.join(choices_map),
                                          choices_sample=5))

        return exercise
