import math
import roman

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create decimal to roman numbers exercises."
    matter = 'matematica'
    subject = 'numeros-romanos'
    category = 'decimal-para-romano'
    bulk_create_answers = False

    def split_terms(self, n):
        return (n.strip(),)

    def generate_operations(self):
        for n in range(1, self.limit + 1):
            yield (n,)

    def create_exercise(self, n):
        n = int(n)
        description = '{0} em romanos'.format(n)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, filter1=n)

        if not created:
            return  # avoid duplicate exercise

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='number',
                                              char_value=str(n)))

        # get the numbers between the dozens around the current number, they
        # will be randomized at execution
        limit = int(math.ceil(n/10.)) * 10 + 1
        choices = range(limit - 10, limit)

        # choices exercises are written through a choices_map variable
        choices_map = []
        for c in choices:
            if c == n:
                flag = '+'
            else:
                flag = '-'
            r = roman.toRoman(c)
            choices_map.append(flag + r)

        # give 10 choices but limit to 5 answers when running the exercise
        self.answers.append(models.Answer(exercise=exercise,
                                          type='radio',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          choices_map='\n'.join(choices_map),
                                          choices_sample=5))

        return exercise
