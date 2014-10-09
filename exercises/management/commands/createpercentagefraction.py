# -*- encoding: utf-8 -*-
from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create percentage fractions exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'fracao-de-porcentagem'
    description = u'{0}/100 (matriz)'

    def split_terms(self, term):
        """
        Returns the term, an integer between 1 and 100 read as a percentage.
        """
        term = int(term)
        assert 1 <= term <= 100
        return (term,)

    def generate_operations(self):
        """
        Generates operations from 1 to 100.
        """
        assert self.limit <= 100
        for i in range(1, self.limit + 1):
            yield (i,)

    def create_exercise(self, term):
        desc = self.description.format(term)
        exercise, created = self.category.exercise_set.get_or_create(
            description=desc, filter1=term)

        if not created:
            return  # avoid duplicate exercise

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='percentage',
                                              char_value=str(term)))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          value=term))

        return exercise
