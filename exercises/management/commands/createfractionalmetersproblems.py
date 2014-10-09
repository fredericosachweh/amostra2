# -*- encoding: utf-8 -*-

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create fractional problems exercises (meters)."
    matter = 'matematica'
    subject = 'unidades-de-medida'
    category = 'problemas-fracionarios-metros'

    UNITIES = [
        {'unity': 'km', 'name': u'quilômetros', 'power': 1E3},
        {'unity': 'hm', 'name': u'hectômetros', 'power': 1E2},
        {'unity': 'dam', 'name': u'decâmetros', 'power': 1E1},
        {'unity': 'm', 'name': u'metros', 'power': 1E0},
        {'unity': 'dm', 'name': u'decímetros', 'power': 1E-1},
        {'unity': 'cm', 'name': u'centímetros', 'power': 1E-2},
        {'unity': 'mm', 'name': u'milímetros', 'power': 1E-3},
    ]

    def get_unity(self, key=None, power=None):
        """
        Search unities list by unity symbol or power.
        """
        for u in self.UNITIES:
            if key and u['unity'] == key:
                return u
            if power and u['power'] == power:
                return u

    def split_terms(self, operation):
        terms = [x.strip() for x in operation.split(',')]
        term1, from_unity = terms
        from_unity = self.get_unity(key=from_unity)
        return (term1, from_unity)

    def generate_operations(self):
        for n in range(1, self.limit + 1):
            values = map(lambda x: x/10.0+n, range(0, 10))
            for value in values:
                for type in self.UNITIES[1:]:
                    yield [value, type]

    def create_exercise(self, term1, from_unity):
        term1 = float(term1)
        str1 = str(term1).replace('.', '')

        # First exercise
        to_unity = self.get_unity(power=from_unity['power'] / 10)
        term2 = int(str1)
        if to_unity:
            self.create_variation(term1, term2, from_unity, to_unity)

        # Second exercise
        to_unity = self.get_unity(power=from_unity['power'] / 100)
        term2 = int(str1) * 10
        if to_unity:
            self.create_variation(term1, term2, from_unity, to_unity)

    def create_variation(self, term1, term2, from_unity, to_unity):
        str1 = str(term1).replace('.', ',')

        description = '{t1}{fu} = {t2}{tu}'.format(
            t1=str1, t2=term2, fu=from_unity['unity'], tu=to_unity['unity']
        )

        # a tag tells if there is decimal values in the terms or there is only
        # integers
        if ',' in description:
            tags = 'decimal'
        else:
            tags = 'integer'

        exercise, created = self.category.exercise_set.get_or_create(
            description=description, tags=tags, filter1=term1, filter2=term2)

        if not created:
            return  # avoid duplications

        self.questions.append(models.Question(
            exercise=exercise, type='char', group='question', char_value=str1))
        self.questions.append(models.Question(
            exercise=exercise, type='char', group='question_type', char_value=from_unity['name']))
        self.questions.append(models.Question(
            exercise=exercise, type='char', group='result_type', char_value=to_unity['name']))

        self.answers.append(models.Answer(
            exercise=exercise, type='char', tabindex=1, group='result', value=term2))
