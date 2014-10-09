# -*- encoding: utf-8 -*-
import itertools

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create polyhedron volume exercises."
    matter = 'matematica'
    subject = 'figuras-geometricas'
    category = 'volume-de-poliedros'
    description = u'{0} (volume de poliedros)'
    bulk_create_answers = False

    def split_terms(self, terms):
        """
        Splits a term like "1,2,3" into a list of width, height and depth.
        """
        return [int(i) for i in terms.split(',')]

    def generate_operations(self):
        """
        Generates options like (1, 1, 2) or (2, 2, 2) for width, height and depth.
        """
        interval = range(1, self.limit)
        axis = [interval] * 3
        for a, b, c in itertools.product(*axis):
            yield (a, b, c)

    def create_exercise(self, *args):
        if len(set(args)) == 1:
            polygon_type = 'cube'
            result = args[0] ** 3
        else:
            polygon_type = 'rectangular_prism'
            result = reduce(lambda x, y: x*y, args, 1)

        desc = self.description.format(
            'Volume({0})'.format(','.join([str(term) for term in args])))

        exercise, created = self.category.exercise_set.get_or_create(
            description=desc,
            filter1=max(args),
            filter2=min(args))

        if not created:
            return  # avoid duplicate exercise

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='type',
                                              char_value=polygon_type))

        for i, term in enumerate(args, start=1):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=(3 - i),
                                                  group='term',
                                                  char_value='{0}'.format(term)))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          value=result))

        return exercise
