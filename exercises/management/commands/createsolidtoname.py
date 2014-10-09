# -*- encoding: utf-8 -*-
from base import BaseCommand
from exercises import models

from utils.polygons import SOLIDS


class Command(BaseCommand):
    help = "Create geometric solid to name exercises."
    matter = 'matematica'
    subject = 'figuras-geometricas'
    category = 'solidos-geometricos-para-nome'
    description = u'{0} (sólido geom. para nome)'
    bulk_create_answers = False

    def split_terms(self, term):
        return (term,)

    def generate_operations(self):
        """
        Max limit is len(SOLIDS).
        """
        for polygon, value in SOLIDS.items()[:self.limit]:
            yield (polygon,)

    def make_choices(self, term):
        for polygon, value in SOLIDS.items():
            if polygon == term:
                continue
            yield polygon

    def create_exercise(self, term):
        desc = self.description.format(term)
        exercise, created = self.category.exercise_set.get_or_create(
            description=desc)

        if not created:
            return  # avoid duplicate exercise

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term',
                                              char_value='{0}'.format(term)))

        choices_map = ['+{0}'.format(term)]
        for polygon in self.make_choices(term):
            choices_map.append('-{0}'.format(polygon))

        # give limit to 5 choices no matter how many was defined
        self.answers.append(models.Answer(exercise=exercise,
                                          type='radio',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          choices_map='\n'.join(choices_map),
                                          choices_sample=5))

        return exercise
