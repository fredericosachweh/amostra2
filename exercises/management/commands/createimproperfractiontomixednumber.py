# -*- encoding: utf-8 -*-
from createfiguretoimproperfraction import Command as BaseCommand


class Command(BaseCommand):
    """
    This is the same command of create figure to improper fraction. The only
    difference is the exercise description and category name, that influences
    the template used.
    """
    help = "Create improper fraction to mixed number."
    category = 'fracao-impropria-para-misto'
    description = u'{0}/{1} (fração impr. para misto)'

    def split_terms(self, term):
        terms = super(Command, self).split_terms(term)
        if terms[0] % terms[1] == 0:
            raise ValueError('The corresponding mixed number cannot be an integer')
        return terms

    def generate_operations(self):
        for m, n in super(Command, self).generate_operations():
            if m % n == 0:
                continue  # ignore mixed numbers that are integers
            yield (m, n)

    def make_choices(self, term1, term2):
        for m, n in super(Command, self).make_choices(term1, term2):
            if m % n == 0:
                continue  # ignore mixed numbers that are integers
            yield (m, n)
