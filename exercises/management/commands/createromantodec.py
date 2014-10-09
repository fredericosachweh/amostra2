import roman

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create roman to decimal numbers exercises."
    matter = 'matematica'
    subject = 'numeros-romanos'
    category = 'romano-para-decimal'

    def split_terms(self, n):
        return (n.strip(),)

    def generate_operations(self):
        for n in range(1, self.limit + 1):
            yield (n,)

    def create_exercise(self, n):
        r = roman.toRoman(int(n))
        description = '{0} em decimais'.format(r)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, filter1=int(n))

        if not created:
            return  # avoid duplications

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='number',
                                              char_value=r))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          value=n))

        return exercise
