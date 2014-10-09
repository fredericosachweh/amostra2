# -*- encoding: utf-8 -*-
from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create criteria of divisible exercises."
    matter = 'matematica'
    subject = 'divisao'
    category = 'criterios-divisibilidade'
    description = u'critério divis. {0}'
    bulk_create_answers = False

    NUMBERS = [
        {'number': 2, 'description': u'Quando ele termina em um algarismo par, ou seja, quando termina em 0, 2, 4, 6 ou 8.'},
        {'number': 3, 'description': u'Quando a soma dos valores absolutos dos seus algarismos é divisível por 3.'},
        {'number': 4, 'description': u'Quando termina em 00 ou quando o número formado pelos dois últimos algarismos da direita for divisível por 4.'},
        {'number': 5, 'description': u'Quando ele termina em 0 ou 5.'},
        {'number': 6, 'description': u'Quando é divisível por 2 e por 3.'},
        {'number': 8, 'description': u'Quando termina em 000, ou quando o número formado pelos três últimos algarismos da direita for divisível por 8.'},
        {'number': 9, 'description': u'Quando a soma dos valores absolutos dos seus algarismos for divisível por 9.'},
        {'number': 10, 'description': u'Quando ele termina em 0.'},
        {'number': 12, 'description': u'Quando é divisível por 3 e por 4.'},
    ]

    def split_terms(self, term):
        return (int(term),)

    def generate_operations(self):
        """
        Max limit is 12.
        """
        for term in self.NUMBERS:
            if term['number'] > self.limit:
                continue
            yield (term['number'],)

    def make_choices(self, term):
        for choice in self.NUMBERS:
            yield choice

    def create_exercise(self, term):
        desc = self.description.format(term)
        exercise, created = self.category.exercise_set.get_or_create(
            description=desc, filter1=term)

        if not created:
            return  # avoid duplicate exercise

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='number',
                                              char_value='{0}'.format(term)))

        choices_map = []
        for choice in self.make_choices(term):
            if choice['number'] == term:
                choices_map.append(u'+{0}'.format(choice['description']))
            else:
                choices_map.append(u'-{0}'.format(choice['description']))

        # give limit to 5 choices no matter how many was defined
        self.answers.append(models.Answer(exercise=exercise,
                                          type='radio',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          choices_map='\n'.join(choices_map),
                                          choices_sample=5))

        return exercise
