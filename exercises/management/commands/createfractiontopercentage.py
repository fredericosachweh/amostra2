# -*- encoding: utf-8 -*-
from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create fraction to percentage conversion exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'fracao-para-porcentagem'
    description = u'{0}/{1} (fração para porcentagem)'

    def split_terms(self, term):
        """
        Tell a term like 3/100.
        """
        terms = term.strip().split('/')
        term1, term2 = [int(t) for t in terms]
        if not term2 == 100:
            raise ValueError('Term 2 is not 100.')
        return (term1, term2)

    def generate_operations(self):
        """
        Fractions from 1/100 until limit/100 (100 is fixed).
        """
        for i in range(1, self.limit + 1):
            yield (i, 100)

    def get_result(self, term1, term2):
        """
        Sets a placeholder for subclasses defined a new result schema.
        """
        return term1

    def create_exercise(self, term1, term2):
        desc = self.description.format(term1, term2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=desc, filter1=term1)

        if not created:
            return  # avoid duplicate exercise

        for n, term in enumerate((term1, term2)):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=n,
                                                  group='term{0}'.format(n + 1),
                                                  char_value=str(term)))

        result = self.get_result(term1, term2)
        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          value=result))
        return exercise
