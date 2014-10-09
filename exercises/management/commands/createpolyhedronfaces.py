from base import BaseCommand

from exercises import models
from utils.polygons import POLYHEDRON_FACES


class Command(BaseCommand):
    help = "Create faces of polyhedron exercises."
    matter = 'matematica'
    subject = 'figuras-geometricas'
    category = 'faces-de-poliedros'
    repository = POLYHEDRON_FACES
    description = '{0} (faces de poliedro)'

    def split_terms(self, term):
        return (term,)

    def generate_operations(self):
        for key in self.repository.keys():
            yield (key,)

    def create_exercise(self, term):
        try:
            result = self.repository[term]
        except KeyError:
            raise ValueError('There is no polyhedron {0}'.format(term))

        description = self.description.format(term)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description)

        if not created:
            return  # avoid duplications

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term',
                                              char_value=term))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          value=result))

        return exercise
