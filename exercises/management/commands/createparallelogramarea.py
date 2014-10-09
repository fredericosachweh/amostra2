# -*- encoding: utf-8 -*-
import math
import random
from decimal import Decimal as D

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create area of parallelogram exercises."
    matter = 'matematica'
    subject = 'area'
    category = 'area-paralelogramos'
    description = u'área paralelogramo base {b}, altura {h}'
    min_percentage = 15
    max_percentage = 30

    def get_result(self, base, height):
        return base * height

    def split_terms(self, term):
        """
        Splits terms like (3, 5) into a pair (base, height).
        """
        terms = term.strip().split(',')
        base, height = [int(i) for i in terms]
        return (base, height)

    def generate_operations(self):
        """
        Makes (base, height) from (5, 3) until (limit, limit).

        The base starts from 5 to have a sane value to randomize and make a
        displacement/inclination of the paralelogram.

        Ignore too large or too taller parallelograms.
        """
        for base in range(5, self.limit + 1):
            for height in range(3, self.limit + 1):
                # Ignore bases 3x larger than height and vice versa
                rate = base / float(height)
                if rate > 3 or rate ** -1 > 3:
                    continue
                yield (base, height)

    def create_exercise(self, base, height):
        exercise, created = self.category.exercise_set.get_or_create(
            description=self.description.format(b=base, h=height),
            filter1=base,
            filter2=height,
        )

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              group='base',
                                              char_value=str(base)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              group='height',
                                              char_value=str(height)))

        # Displacement makes an inclination in the standard rectangle, making
        # it a parallelogram
        percentage = random.randint(self.min_percentage, self.max_percentage)
        displacement = int(math.ceil(base * (percentage / D(100))))
        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              group='displacement',
                                              char_value=str(displacement)))

        result = self.get_result(base, height)
        self.answers.append(models.Answer(exercise=exercise,
                                          type='char',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          value=result))
        return exercise
