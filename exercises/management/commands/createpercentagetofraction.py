# -*- encoding: utf-8 -*-
from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create percentage to fraction convesion exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'porcentagem-para-fracao'
    description = u'{0} (porcentagem para fração)'

    def split_terms(self, term):
        return [int(term)]

    def generate_operations(self):
        for i in range(1, self.limit + 1):
            yield (i,)

    def get_result(self, term1):
        """
        Sets a placeholder for subclasses defined a new result schema.

        If this case, return the term itself to make 33% be 33/100.
        """
        return term1

    def create_exercise(self, term1):
        desc = self.description.format(term1)
        exercise, created = self.category.exercise_set.get_or_create(
            description=desc, filter1=term1)

        if not created:
            return  # avoid duplicate exercise

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='question',
                                              char_value=str(term1)))

        result = self.get_result(term1)
        for n, result in enumerate((100, result)):
            self.answers.append(models.Answer(exercise=exercise,
                                              type='exact',
                                              position=n,
                                              tabindex=2 - n,
                                              group='result',
                                              value=result))

        return exercise
