# -*- encoding: utf-8 -*-
from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create hours to minutes and vice-versa exercises."
    matter = 'matematica'
    subject = 'medidas-de-tempo'
    category = 'hora-para-minuto'
    direct_description = '{0}h = {1}min'
    inverse_description = '{0}min = {1}h'

    def split_terms(self, term):
        """
        Specify how many hours. The term will generate 2 exercises: hours to
        minutes and minutes to hours.
        """
        return (term,)

    def generate_operations(self):
        for term in range(1, self.limit + 1):
            yield (term,)

    def create_exercise(self, term):
        hours = int(term)
        minutes = hours * 60
        self.create_variation(hours, minutes)
        self.create_variation(minutes, hours, inverse=True)

    def create_variation(self, term1, term2, inverse=False):
        if not inverse:
            description = self.direct_description
            filter1, filter2 = term1, term2
            tags = 'direct'
        else:
            description = self.inverse_description
            filter1, filter2 = term2, term1
            tags = 'inverse'
        description = description.format(term1, term2)

        exercise, created = self.category.exercise_set.get_or_create(
            description=description, tags=tags, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid create the exercise again

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term1',
                                              char_value=str(term1)))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=1,
                                          group='term2',
                                          value=term2))
