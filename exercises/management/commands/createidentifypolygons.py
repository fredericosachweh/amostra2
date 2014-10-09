# -*- coding:utf-8 -*-
from django.utils import translation
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext

from base import BaseCommand
from exercises import models

from utils.polygons import SPECIAL_CASE_POLYGONS


class Command(BaseCommand):
    help = "Create identify polygons exercises."
    matter = 'matematica'
    subject = 'figuras-geometricas'
    category = 'figura-para-triangulo-ou-quadrilatero'
    description = u'{0} (identificar polígonos)'
    bulk_create_answers = False

    def split_terms(self, term):
        """
        Searches the SPECIAL_CASE_POLYGONS by the given value instead of key.
        """
        translation.activate('pt-BR')
        for polygon, value in SPECIAL_CASE_POLYGONS.items()[:self.limit]:
            if ugettext(value) == term:
                return (polygon, value)
        translation.deactivate()

    def generate_operations(self):
        """
        Max limit is len(REGULAR_POLYGONS).
        """
        for polygon, value in SPECIAL_CASE_POLYGONS.items()[:self.limit]:
            yield (polygon, value)

    def create_exercise(self, key, value):
        translation.activate('pt-BR')

        if key not in SPECIAL_CASE_POLYGONS:
            raise ValueError('There is no {0} polygon'.format(key))

        exercise, created = self.category.exercise_set.get_or_create(
            description=self.description.format(force_unicode(value)))

        if not created:
            return  # avoid duplicate exercise

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term',
                                              char_value=key))

        choices_map = [u'+{0}'.format(value)]
        for item in SPECIAL_CASE_POLYGONS.values():
            if item != value:
                choices_map.append(u'-{0}'.format(item))

        # give limit to 5 choices no matter how many was defined
        self.answers.append(models.Answer(exercise=exercise,
                                          type='radio',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          choices_map='\n'.join(choices_map),
                                          choices_sample=5))

        translation.deactivate()
        return exercise
