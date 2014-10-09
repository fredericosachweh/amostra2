import re
import itertools
import optparse

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create addition and subtraction exercises."
    matter = 'matematica'
    subject = 'expressoes-adicao-subtracao'

    option_list = BaseCommand.option_list + (
        optparse.make_option('--terms',
            action='store', type='int', dest='terms',
            help='How many terms in the operation?'),
    )

    def handle(self, *args, **kwargs):
        self.terms = kwargs.get('terms', None)
        if not self.terms:
            raise Exception('You must specify how many terms')
        return super(Command, self).handle(*args, **kwargs)

    def get_category_slug(self):
        return 'adicao-subtracao-em-ordem-{0}-termos'.format(self.terms)

    def split_terms(self, operation):
        terms = re.split(r'([+-])', operation)
        if operation[0].isdigit():
            yield 1  # first plus sign
        for t in terms:
            if t == '+':
                yield 1
            elif t == '-':
                yield -1
            elif t != '':
                yield int(t)

    def generate_operations(self):
        signal = [1, -1]  # plus or minus
        interval = range(0, self.limit + 1)
        axis = [signal, interval] * self.terms
        for terms in itertools.product(*axis):
            if terms.count(0) > 1:
                continue  # ignore more than one zero in the generation
            if terms[0] == 0 or terms[1] == 0:
                continue  # ignore an starting zero
            yield terms

    def get_description(self, pairs):
        first = True
        for signal, number in pairs:
            if signal == 1:
                if first:
                    yield ''
                else:
                    yield '+'
            elif signal == -1:
                yield '-'
            first = False
            yield str(number)

    def create_exercise(self, *terms):
        signals = terms[::2]
        numbers = terms[1::2]
        pairs = zip(signals, numbers)

        description_list = list(self.get_description(pairs))
        description = ''.join(description_list)

        if self.category.exercise_set.filter(description=description).exists():
            return  # ignore already existent exercises

        tags = []
        if description_list[0] == '-':
            tags.append('inicio-negat')
        else:
            tags.append('inicio-posit')

        # create a line as "-2+5-3", each digit is a question
        for n, term in enumerate(description_list):
            self.questions.append(models.Question(type='char',
                                                  position=len(description_list) - n,
                                                  group='exp',
                                                  char_value=term))

        curr_signal, curr_number = pairs.pop(0)
        for n, (next_signal, next_number) in enumerate(pairs):
            result = curr_signal * curr_number + next_signal * next_number
            self.answers.append(models.Answer(type=type,
                                              position=len(pairs) - n,
                                              tabindex=n+1,
                                              group='result',
                                              value=result))
            if result < 0:
                if not 'result-negat' in tags:
                    tags.append('result-negat')
                curr_signal = -1
            else:
                curr_signal = 1
            curr_number = abs(result)

        if not 'result-negat' in tags:
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
