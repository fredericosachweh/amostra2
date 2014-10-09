# -*- encoding: utf-8 -*-
import math

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create square root exercises."
    matter = 'matematica'
    subject = 'radiciacao'
    category = 'raiz-quadrada'

    def split_terms(self, operation):
        return [int(operation)]

    def generate_operations(self):
        """
        Gives numbers starting from 4, the first perfect square of 2.
        """
        for term in xrange(4, self.limit + 1):
            sqrt = math.sqrt(term)
            orig = pow(sqrt, 2)
            if orig != term:
                continue
            yield (term, sqrt)

    def create_exercise(self, term, sqrt=None):
        if sqrt is None:
            # Check if this is a perfect square root.
            sqrt = math.sqrt(term)
            orig = pow(sqrt, 2)
            if orig != term:
                raise ValueError('Square root must be perfect!')

        description = u'raíz quadrada de {0}'.format(term)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            filter1=term,
            filter2=term)

        if not created:
            return  # avoid create the exercise again

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term',
                                              char_value=term))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          group='result',
                                          value=int(sqrt)))

        return exercise
