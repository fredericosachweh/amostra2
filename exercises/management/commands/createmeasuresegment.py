# -*- encoding: utf-8 -*-
from django.core.management.base import CommandError
from django.utils.datastructures import SortedDict

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create measure segment exercises."
    matter = 'matematica'
    subject = 'geometria'
    category = 'reta-e-segmento'

    SEGMENTS = {
        'r': SortedDict([
            ('a', 0),
            ('b', 4),
            ('c', 6),
            ('d', 9),
            ('e', 10),
        ]),
        's': SortedDict([
            ('a', 0),
            ('b', 3),
            ('c', 4),
            ('d', 8),
            ('e', 10),
        ])
    }

    def split_terms(self, term):
        """
        Gets (a, b, r) and check they are valid points and straight.

        The first two terms are points in a straight and the third argument is
        one of the available straights.
        """
        point_a, point_b, straight = term.strip().split(',')
        if straight not in self.SEGMENTS:
            choices = ', '.join(self.SEGMENTS.keys())
            msg = 'Unknown straight {0}. Choices are {1}'
            raise CommandError(msg.format(straight, choices))

        points = self.SEGMENTS[straight]
        choices = ', '.join(points.keys())
        msg = 'Unknown point {0}. Choices are {1}'
        if point_a not in points:
            raise CommandError(msg.format(point_a, choices))
        if point_b not in points:
            raise CommandError(msg.format(point_b, choices))

        if point_a == point_b:
            raise CommandError('The points cannot be the same.')

        return (point_a, point_b, straight)

    def generate_operations(self):
        """
        Combine each straight points and yields (a, b, r).

        For each point in the straight, iters forward over the next points,
        never backward.
        """
        for straight, segments in self.SEGMENTS.items():
            for i, point_a in enumerate(segments.keys()):
                forward_segments = segments.keys()[i+1:]
                for point_b in forward_segments:
                    yield (point_a, point_b, straight)

    def create_exercise(self, point_a, point_b, straight):
        position_a = self.SEGMENTS[straight][point_a]
        position_b = self.SEGMENTS[straight][point_b]

        description = '{a}{b} (medida de segmentos, reta {r})'.format(
            a=point_a.upper(), b=point_b.upper(), r=straight)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, filter1=position_a, filter2=position_b)

        if not created:
            return  # avoid duplicate the exercise

        for n, point in enumerate([point_a, point_b]):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  group='points',
                                                  position=2 - n,
                                                  char_value=point))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              group='straight',
                                              char_value=straight))

        # Creates all points sequentially to render the straight in template
        segments = self.SEGMENTS[straight].values()
        for n, segment in enumerate(segments):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  group='segments',
                                                  position=len(segments) - n,
                                                  char_value=str(segment)))

        result = abs(position_a - position_b)
        self.answers.append(models.Answer(exercise=exercise,
                                          type='char',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          value=result))
        return exercise
