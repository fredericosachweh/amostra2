from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = 'Create multiplication table exercises. Same as multiplication ' \
           'exercises but with a simples layout and just the result as answer.'
    matter = 'matematica'
    subject = 'multiplicacao'
    category = 'tabuada'
    description = '{0} * {1} (tabuada)'

    def split_terms(self, operation):
        return [int(t.strip()) for t in operation.split('*')]

    def generate_operations(self):
        for term1 in xrange(1, self.limit + 1):
            for term2 in xrange(1, self.limit + 1):
                yield (term1, term2)

    def create_exercise(self, term1, term2):
        description = self.description.format(term1, term2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, filter1=term1, filter2=term2)

        if not created:
            return  # avoid duplications

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term1',
                                              char_value=str(term1)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term2',
                                              char_value=str(term2)))

        product = term1 * term2
        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          value=product))

        return exercise
