# -*- encoding: utf-8 -*-
import optparse
import random

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create exercises to tell numbers divisible by N."
    matter = 'matematica'
    subject = 'divisao'
    category = 'divisivel-por-n'
    description = u'{0} divisível por {1}'
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

    def make_indivisibles(self, divisor, divided):
        """
        Makes 21 numbers not divisible by divisor.

        Uses numbers next to the specified divived to the correct and wrong
        choices have the same magnitude.
        """
        indivisible = []
        count = 1
        while len(indivisible) < 21:
            forward = divided + count
            if forward % divisor != 0:
                indivisible.append(forward)
            backward = divided - count
            if backward > 1 and backward % divisor != 0:
                indivisible.append(backward)
            count += 1
        return indivisible

    def split_terms(self, terms):
        terms = terms.split('/')
        divided = int(terms[0])
        divisor = int(terms[1])
        if divided % divisor != 0:
            raise ValueError('{0} isn\'t divisor or {1}'.format(divisor,
                                                                divided))
        indivisibles = self.make_indivisibles(divisor, divided)
        return (divided, divisor, indivisibles)

    def generate_operations(self):
        """
        Generates options for exercise.

        Iter until limit defining the divisors and, for each divisor, iters
        between itself and the limit creating pair of (divided, divisor).
        """
        for divisor in range(2, self.divisor_limit + 1):
            # Only one iterator to indivisibles per divisor
            for divided in range(divisor, self.limit + 1):
                if (divided % divisor == 0):
                    indivisibles = self.make_indivisibles(divisor, divided)
                    yield (divided, divisor, indivisibles)

    def create_exercise(self, divided, divisor, indivisibles):
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
                                              char_value=str(divisor)))

        # One correct answer and 9 possible incorrects
        choices_map = ['+{0}'.format(divided)]
        random.shuffle(indivisibles)
        for indivisible in indivisibles[:9]:
            choices_map.append('-{0}'.format(indivisible))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='radio',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          choices_map='\n'.join(choices_map),
                                          choices_sample=5))

        return exercise
