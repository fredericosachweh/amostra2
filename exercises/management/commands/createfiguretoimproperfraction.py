# -*- encoding: utf-8 -*-
from createfiguretofraction import Command as BaseCommand


class Command(BaseCommand):
    help = "Create figure to improper fraction exercises."
    category = 'figura-para-fracao-impropria'
    description = u'{0}/{1} (fig. para fração impr.)'

    def split_terms(self, term):
        terms = super(Command, self).split_terms(term)
        if terms[0] <= terms[1]:
            raise ValueError('The term is not an improper fraction')
        return terms

    def generate_operations(self):
        """
        Fractions from 3/2 until (2 * limit) / limit.
        """
        for i in range(2, self.limit + 1):
            for j in range(i+1, i*2 + 1):
                yield (j, i)

    def make_choices(self, term1, term2):
        """
        If term1/term2 is 9/5, generates choices from 5/4 to 8/4, 6/5 to 10/5
        and 7/6 to 12/6, excluding 9/5 and any number proportional to it.
        """
        ratio = float(term1) / float(term2)
        for i in (term2 - 1, term2, term2 + 1):
            if i < 2:
                continue  # avoid choices like 1/1 or 1/0
            for j in range(i+1, 2*i + 1):
                if float(j) / float(i) == ratio:
                    continue  # avoid equivalent fractions
                yield j, i
