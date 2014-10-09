from base import BaseCommand
from exercises import models

from utils.polygons import REGULAR_POLYGONS


class Command(BaseCommand):
    help = "Create regular polygons to name exercises."
    matter = 'matematica'
    subject = 'figuras-geometricas'
    category = 'figuras-geometricas-planas-para-nome'
    description = u'{0} (nome de fig. geom.)'
    bulk_create_answers = False

    def split_terms(self, term):
        return (int(term),)

    def generate_operations(self):
        """
        Max limit is len(REGULAR_POLYGONS).
        """
        for polygon, value in REGULAR_POLYGONS.items()[:self.limit]:
            yield (polygon,)

    def make_choices(self, term):
        limit = (int(term) / 10 + 1) * 10
        for polygon, value in REGULAR_POLYGONS.items()[:limit]:
            if polygon == int(term):
                continue
            yield polygon

    def create_exercise(self, term):
        if term not in REGULAR_POLYGONS:
            raise ValueError('There is no polygon with {0} '
                             'sides available'.format(term))

        desc = self.description.format(term)
        exercise, created = self.category.exercise_set.get_or_create(
            description=desc, filter1=term)

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
