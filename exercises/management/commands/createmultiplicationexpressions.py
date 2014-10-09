import re
import itertools
import math
import optparse

from base import BaseCommand
from exercises import models


class DecimalDivisionError(Exception):
    pass


class Command(BaseCommand):
    help = "Create multiplication and division expressions exercises."
    matter = 'matematica'
    subject = 'expressoes-multiplicacao-divisao'

    option_list = BaseCommand.option_list + (
        optparse.make_option('--terms',
            action='store', type='int', dest='terms',
            help='How many terms in the operation?'),
        optparse.make_option('--addition-limit',
            action='store', type='int', dest='addition_limit',
            help='Limit for a standalone addition or subtraction operation.')
    )

    def handle(self, *args, **kwargs):
        self.terms = kwargs.get('terms', None)
        if not self.terms:
            if kwargs['operation']:
                terms = re.split(r'([*/+-])', kwargs['operation'])
                self.terms = int(math.ceil(len(terms) / 2.))
            else:
                raise ValueError('You must specify how many terms')

        self.addition_limit = kwargs.get('addition_limit', None)
        if self.terms % 2 and not kwargs['operation'] and not self.addition_limit:
            raise ValueError('You must specify the standalone addition or subtraction limit.')
        return super(Command, self).handle(*args, **kwargs)

    def get_category_slug(self):
        return 'multiplicacao-divisao-{0}-termos'.format(self.terms)

    def split_terms(self, operation):
        terms = filter(None, re.split(r'([*/+-])', operation))
        for t in terms:
            if t in '+-*/':
                yield t
            elif t != '':
                yield int(t)

    def check_divisions(self, terms):
        """
        Discover the divisions in a terms list and check if the previous term
        is divisible by the next term.
        """
        start = 0
        while 1:
            try:
                index = terms.index('/', start)
                if terms[index - 1] % terms[index + 1]:
                    raise DecimalDivisionError
                start = index + 1
            except ValueError:
                break

    def generate_operations(self):
        interval = range(0, self.limit + 1)
        axis = []
        if self.terms % 2:
            axis.extend([range(0, self.addition_limit + 1), '+-'])

        for i in range(self.terms / 2):
            if i > 0:
                axis.append('+-')
            axis.extend([interval, '*/', interval])

        for n, terms in enumerate(itertools.product(*axis)):
            integers = [d for d in terms if isinstance(d, int)]
            if len(set(integers)) == 1:
                continue  # avoid digit repetitions (a * a + a * a)

            try:
                self.check_divisions(terms)
            except (DecimalDivisionError, ZeroDivisionError):
                continue

            # for odd number of terms, there will be an stand alone number that
            # will be in the start or in the end of operation in a cyclic way
            if self.terms % 2 and n % 2:
                # make (a + b * c) becomes (b * c + a)
                terms = terms[2:] + terms[:2][::-1]

            yield terms

    def create_exercise(self, *terms):
        description = ''.join([unicode(item) for item in terms])
        if self.category.exercise_set.filter(description=description).exists():
            return  # avoid duplications

        tags = []

        # assumes there will be no zero as first term of a division or a
        # multiplication
        zero_is_mult = False
        has_divisions = False
        starts_negative = False
        returns_negative = False

        products = []
        for n, term in enumerate(terms):
            self.questions.append(models.Question(type='char',
                                                  position=len(terms) - n,
                                                  group='line',
                                                  char_value=unicode(term)))

            if term in ['*', '/']:
                if terms[n-1] == 0:
                    zero_is_mult = True
                if term == '*':
                    partial = terms[n-1] * terms[n+1]
                else:
                    partial = terms[n-1] / terms[n+1]
                    has_divisions = True
                try:
                    if terms[n-2] == '-':
                        signal = -1
                    else:
                        signal = 1
                except IndexError:
                    signal = 1
                products.append(signal * partial)

        for n, product in enumerate(products):
            self.answers.append(models.Answer(type='exact',
                                              position=len(products) - n,
                                              tabindex=n+1,
                                              group='product',
                                              value=abs(product)))

        numbers = [x for x in terms if isinstance(x, int)]

        # adds the standalone addition or subtraction to the list of product
        # results that will make additions
        if len(numbers) % 2:
            if terms[-2] in '+-':
                if terms[-2] == '+':
                    signal = 1
                else:
                    signal = -1
                products.append(signal * terms[-1])
            else:
                if isinstance(terms[0], basestring):
                    if terms[0] == '+':
                        signal = 1
                    else:
                        signal = -1
                        starts_negative = True
                    products.insert(0, signal * terms[1])
                else:
                    products.insert(0, terms[0])

        curr_term = products.pop(0)
        for n, next_term in enumerate(products):
            addition = curr_term + next_term
            self.answers.append(models.Answer(type='exact',
                                              position=len(products) - n,
                                              tabindex=len(self.answers) + 1,
                                              group='addition',
                                              value=addition))
            curr_term = addition
            if addition < 0:
                returns_negative = True

        if len(numbers) % 2:
            # the numbers are used to define what is the min and max digit in the
            # operation but it ignores the number of the standalone addition or
            # subtraction as this number can have a different range from the others
            if terms[-2] in '+-':
                numbers = numbers[:-1]
            else:
                numbers = numbers[1:]

        if zero_is_mult:
            tags.append('com-zero')
        else:
            tags.append('sem-zero')
        if has_divisions:
            tags.append('com-divisao')
        else:
            tags.append('sem-divisao')
        if starts_negative:
            tags.append('inicio-negat')
        else:
            tags.append('inicio-posit')
        if returns_negative:
            tags.append('result-negat')
        else:
            tags.append('result-posit')
        exercise = self.category.exercise_set.create(description=description,
                                                     tags=','.join(tags),
                                                     filter1=min(numbers),
                                                     filter2=max(numbers))
        for answer in self.answers:
            answer.exercise = exercise

        for question in self.questions:
            question.exercise = exercise

        return exercise
