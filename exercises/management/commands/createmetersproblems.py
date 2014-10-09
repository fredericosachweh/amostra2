# -*- encoding: utf-8 -*-
import itertools

from django.utils import translation
from django.template.defaultfilters import floatformat

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create length problems exercises."
    matter = 'matematica'
    subject = 'unidades-de-medida'
    category = 'problemas-metros'

    UNITIES = [
        {'unity': 'm', 'name': 'metro', 'power': 1E0},
        {'unity': 'dam', 'name': u'decâmetro', 'power': 1E1},
        {'unity': 'hm', 'name': u'hectômetro', 'power': 1E2},
        {'unity': 'km', 'name': u'quilômetro', 'power': 1E3},
        {'unity': 'dm', 'name': u'decímetro', 'power': 1E-1},
        {'unity': 'cm', 'name': u'centímetro', 'power': 1E-2},
        {'unity': 'mm', 'name': u'milímetro', 'power': 1E-3},
    ]

    def get_unity(self, key):
        """
        Search unities list by unity symbol.
        """
        for u in self.UNITIES:
            if u['unity'] == key:
                return u

    def split_terms(self, operation):
        """
        Specify a quatriple of x, y, to unity, from unity. Keep from unity blank to use the base measurand.

        1,3,mm,m
        """
        terms = [x.strip() for x in operation.split(',')]
        if len(terms) == 4:
            term1, term2, to_unity, from_unity = terms
            to_unity = self.get_unity(to_unity)
            from_unity = self.get_unity(from_unity)
        else:
            term1, term2, to_unity = terms
            to_unity = self.get_unity(to_unity)
            from_unity = None
        return (int(term1), int(term2), to_unity, from_unity)

    def generate_operations(self):
        interval = range(1, self.limit + 1)
        axis = [
            interval,
            interval,
            self.UNITIES[1:],  # multiples
        ]
        for terms in itertools.product(*axis):
            if terms[0] == terms[1]:
                continue  # avoid convert x to x
            yield terms

    def create_exercise(self, term1, term2, to_unity, from_unity=None):
        if not from_unity:
            from_unity = self.UNITIES[0]  # base unity

        power = from_unity['power'] / to_unity['power']

        # direct order of unities
        conv1 = term1 * power
        conv2 = term2 * power
        self.create_variation(term1, term2, conv1, conv2,
                              from_unity, to_unity)

        # inverse order of unities
        conv1 = term1 / power
        conv2 = term2 / power
        from_unity, to_unity = to_unity, from_unity
        self.create_variation(term1, term2, conv1, conv2,
                              from_unity, to_unity)

    def create_variation(self, term1, term2, conv1, conv2, from_unity, to_unity):
        translation.activate('pt-BR')

        sterm1 = floatformat(term1, 6).rstrip('0').rstrip(',')
        sterm2 = floatformat(term2, 6).rstrip('0').rstrip(',')
        sconv1 = floatformat(conv1, 6).rstrip('0').rstrip(',')
        sconv2 = floatformat(conv2, 6).rstrip('0').rstrip(',')

        description = '{t1}{fu} = {c1}{tu} <> {t2}{fu} = {c2}{tu}'.format(
            t1=sterm1, t2=sterm2, c1=sconv1, c2=sconv2,
            fu=from_unity['unity'], tu=to_unity['unity']
        )

        # a tag tells if there is decimal values in the terms or there is only
        # integers
        if ',' in description:
            tags = 'decimal'
        else:
            tags = 'integer'

        exercise, created = self.category.exercise_set.get_or_create(
            description=description, tags=tags, filter1=int(term1), filter2=int(term2))

        if not created:
            return  # avoid duplications

        # We store strings, we need to store formatted numbers and a auxiliar
        # field to tell if the term is different from one and, in this case, if
        # applies pluralization of the unity name
        self.questions.append(models.Question(
            exercise=exercise, type='char', group='term1', char_value=sterm1))
        self.questions.append(models.Question(
            exercise=exercise, type='char', group='term1_plural', char_value=str(int(term1))))

        self.questions.append(models.Question(
            exercise=exercise, type='char', group='term2', char_value=sterm2))
        self.questions.append(models.Question(
            exercise=exercise, type='char', group='term2_plural', char_value=str(int(term2))))

        self.questions.append(models.Question(
            exercise=exercise, type='char', group='conv1', char_value=sconv1))
        self.questions.append(models.Question(
            exercise=exercise, type='char', group='conv1_plural', char_value=str(int(conv1))))

        # Saves the unities symbols and names
        self.questions.append(models.Question(
            exercise=exercise, type='char', group='from_unity', char_value=from_unity['unity']))
        self.questions.append(models.Question(
            exercise=exercise, type='char', group='from_name', char_value=from_unity['name']))

        self.questions.append(models.Question(
            exercise=exercise, type='char', group='to_unity', char_value=to_unity['unity']))
        self.questions.append(models.Question(
            exercise=exercise, type='char', group='to_name', char_value=to_unity['name']))

        # the answer is a decimal field
        self.answers.append(models.Answer(
            exercise=exercise, type='exact', tabindex=1, group='conv2', value=conv2))

        translation.deactivate()
