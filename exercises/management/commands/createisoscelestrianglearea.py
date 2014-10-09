# -*- encoding: utf-8 -*-
from django.core.management.base import CommandError

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create area of isosceles triangle exercises."
    matter = 'matematica'
    subject = 'area'
    category = 'area-triangulos-isosceles'
    description = u'área triâng. isósceles base {b}, altura {h}'

    def split_terms(self, term):
        """
        Splits terms like (3, 5) into a pair (base, height).
        """
        terms = term.strip().split(',')
        term1, term2 = [int(i) for i in terms]
        if (term1 * term2) % 2 > 0:
            raise CommandError('The result is decimal.')
        return [term1, term2]

    def generate_operations(self):
        """
        Makes (base, height) from (1, 2) until (limit, limit - 1).
        """
        for i in range(2, self.limit + 1):
            for j in range(1, i + 1):
                if ((i * j) % 2) > 0:
                    continue
                if not j == i:
                    yield (j, i)

    def create_exercise(self, base, height):
        desc = self.description.format(b=base, h=height)
        filter1 = base
        filter2 = height

        exercise, created = self.category.exercise_set.get_or_create(
            description=desc, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplicate the exercise

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              group='base',
                                              char_value=str(base)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              group='height',
                                              char_value=str(height)))

        result = (base*height) / 2
        self.answers.append(models.Answer(exercise=exercise,
                                          type='char',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          value=result))
        return exercise
