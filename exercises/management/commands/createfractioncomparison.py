# -*- encoding: utf-8 -*-
import itertools
import random

from base import BaseCommand
from exercises import models
from utils.intervals import generate_one_dimension_fractions


class Command(BaseCommand):
    """
    Create fraction comparison exercises.

    Each generated exercise would do a greater than OR a lesser than comparison
    (randomically choosen).
    """
    help = 'Create fraction comparison exercises.'
    matter = 'matematica'
    subject = 'fracoes'
    category = 'comparacao-fracoes'
    description = u'{0}/{1} {op} {2}/{3}'
    operators = ('gt', 'lt')
    bulk_create_answers = False

    def split_terms(self, term):
        """Splits a term like "3/5, 2/5" to (a, b, c, d)."""
        pairs = [t.strip() for t in term.split(',')]
        if len(pairs) > 2:
            operator = pairs.pop(-1)
        else:
            operator = None

        terms = [[int(x) for x in t.split('/')] for t in pairs]
        items = terms[0] + terms[1]

        if operator:
            if not operator in self.operators:
                raise ValueError('{0} is not a valid operator'.format(operator))
            items.append(operator)
        return items

    def generate_operations(self):
        """Generates fractions from 1/2 until limit/limit."""
        fractions = list(generate_one_dimension_fractions(self.limit))
        for terms in itertools.product(fractions, fractions):
            yield terms[0] + terms[1]

    def create_fraction(self, exercise, group, terms):
        for n, term in enumerate(terms[::-1]):  # use reverse order
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=n,
                                                  group=group,
                                                  char_value=str(term)))

    def create_exercise(self, a, b, c, d, operator=None):
        terms = [a, b, c, d]
        if not operator:
            operator = random.choice(self.operators)

        desc = self.description.format(*terms, op=operator)
        exercise, created = self.category.exercise_set.get_or_create(
            description=desc, filter1=min(terms), filter2=max(terms))

        if not created:
            return  # avoid duplicate exercise

        self.create_fraction(exercise, 'fraction1', [a, b])
        self.create_fraction(exercise, 'fraction2', [c, d])

        comp = a / float(b) - c / float(d)

        # our comparison tells what is the greater fraction but, if the
        # operation is lesser than comparison, just invert the comparison term
        if operator == 'lt':
            comp = comp * -1
            operator_desc = 'menor'
        else:
            operator_desc = 'maior'

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='operator',
                                              char_value=operator_desc))

        choices = [
            ['-', u'{0}/{1}'.format(a, b)],
            ['-', u'{0}/{1}'.format(c, d)],
            ['-', u'São iguais ou equivalentes'],
        ]

        if comp == 0:
            choices[2][0] = '+'
        elif comp > 0:
            choices[0][0] = '+'
        else:
            choices[1][0] = '+'

        choices_map = '\n'.join([(a + b) for a, b in choices])

        # give exactly 3 choices
        self.answers.append(models.Answer(exercise=exercise,
                                          type='radio',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          choices_map=choices_map,
                                          choices_sample=3))
        return exercise
