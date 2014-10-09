# -*- encoding: utf-8 -*-
import optparse

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create a tile area."
    matter = 'matematica'
    subject = 'area'
    category = 'area-dos-quadrados'
    description = u'área de {t} quadrados de {a}{u}²'

    option_list = BaseCommand.option_list + (
        optparse.make_option('--tilearea-limit',
            action='store', type='int', dest='tilearea_limit',
            help='What will be the area of each tile of the image?'),
    )

    UNITIES = [
        {'unity': 'm', 'name': 'metro', 'power': 1E0},
        {'unity': 'dam', 'name': u'decâmetro', 'power': 1E1},
        {'unity': 'hm', 'name': u'hectômetro', 'power': 1E2},
        {'unity': 'km', 'name': u'quilômetro', 'power': 1E3},
        {'unity': 'dm', 'name': u'decímetro', 'power': 1E-1},
        {'unity': 'cm', 'name': u'centímetro', 'power': 1E-2},
        {'unity': 'mm', 'name': u'milímetro', 'power': 1E-3},
    ]

    def handle(self, *args, **kwargs):
        self.tilearea_limit = kwargs.get('tilearea_limit', None)
        if not kwargs['operation'] and not self.tilearea_limit:
            raise Exception('You must specify the tilearea range limit')
        return super(Command, self).handle(*args, **kwargs)

    def split_terms(self, operation):
        """
        Split terms like "9:5" to create a tile objects.
        """
        subterms = [t.strip() for t in operation.split(':')]
        tiles = subterms[0]
        tilearea = subterms[1]
        unity = 'cm'  # defaults to cm for sample
        return (int(tiles), int(tilearea), unity)

    def get_tilearea_range(self):
        return xrange(1, self.tilearea_limit + 1)

    def generate_operations(self):
        for i in xrange(2, self.limit + 1):
            for j in self.get_tilearea_range():
                for unity in self.UNITIES:
                    yield (i, j, unity['unity'])

    def get_result(self, tiles, tilearea):
        return tiles * tilearea

    def create_exercise(self, tiles, tilearea, unity):
        # check if tilearea is defined, if not set 1
        if not tilearea:
            tilearea = 1

        result = self.get_result(tiles, tilearea)
        filter1 = result
        filter2 = tilearea

        description = self.description.format(t=tiles, a=tilearea, u=unity)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplicate the exercise

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term1',
                                              char_value=str(tiles)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term2',
                                              char_value=str(tilearea)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='unity',
                                              char_value=unity))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          value=result))

        return exercise
