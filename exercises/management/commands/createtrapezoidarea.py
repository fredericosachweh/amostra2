# -*- encoding: utf-8 -*-
import math
import random
from decimal import Decimal as D

from django.core.management.base import CommandError

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create area of trapezoid exercises."
    matter = 'matematica'
    subject = 'area'
    category = 'area-trapezios'
    description = u'área trapézio base maior {b1}, base menor {b2}, altura {h}'
    min_pct = 60
    max_pct = 80

    def get_result(self, larger_base, shorter_base, height):
        result = ((larger_base + shorter_base) * height) / 2.
        if result - int(result) > 0:
            raise CommandError('The result must be integer')
        return result

    def get_shorter_base(self, larger_base, shorter_base_pct):
        return int(math.ceil(larger_base * (shorter_base_pct / D(100))))

    def split_terms(self, term):
        """
        Splits comma sep. integers into (greater_base, height, percentage).

        The percentage is used to get the short_base from larger_base and must
        be between min and max percentages configured through class attributes.
        """
        terms = term.strip().split(',')
        larger_base, height, shorter_base_pct = [int(i) for i in terms]

        # Percentage to create term3
        if not (self.min_pct <= shorter_base_pct <= self.max_pct):
            msg = 'Shorter base % must be between {0}% and {1}%.'.format(
                    self.min_pct, self.max_pct)
            raise CommandError(msg)

        shorter_base = self.get_shorter_base(larger_base, shorter_base_pct)

        result = self.get_result(larger_base, shorter_base, height)
        return (larger_base, shorter_base, height, result)

    def generate_operations(self):
        """
        Makes a list of (larger_base, shorter_base, height, result).

        Starts the larger base from 5 to make a sane shorted base. Ignore too
        large or too taller trapezoids.
        """
        for larger_base in xrange(5, self.limit + 1):
            for height in xrange(3, self.limit + 1):
                pct = random.randint(self.min_pct, self.max_pct)
                shorter_base = self.get_shorter_base(larger_base, pct)
                try:
                    result = self.get_result(larger_base, shorter_base, height)
                except CommandError:
                    continue

                # Ignore bases 3x larger than height and vice versa
                rate = larger_base / float(height)
                if rate > 3 or rate ** -1 > 3:
                    continue
                yield (larger_base, shorter_base, height, result)

    def create_exercise(self, larger_base, shorter_base, height, result):
        exercise, created = self.category.exercise_set.get_or_create(
            description=self.description.format(b1=larger_base,
                                                b2=shorter_base,
                                                h=height),
            filter1=larger_base,
            filter2=height
        )

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              group='base1',
                                              char_value=str(larger_base)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              group='height',
                                              char_value=str(height)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              group='base2',
                                              char_value=str(shorter_base)))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='char',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          value=result))
        return exercise
