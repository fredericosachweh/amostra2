import itertools

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create addition of fraction with same base exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'adicao-fracoes-mesmo-denominador'
    terms_separator = '+'

    def split_terms(self, operation):
        subterms = [t.strip() for t in operation.split(self.terms_separator)]
        term1, base1 = [t.strip() for t in subterms[0].split('/')]
        term2, base2 = [t.strip() for t in subterms[1].split('/')]
        if base1 != base2:
            raise ValueError('Set fractions with same base!')
        return (int(term1), int(term2), int(base1))

    def generate_operations(self):
        interval = xrange(1, self.limit + 1)
        axis = [interval] * 3
        for terms in itertools.product(*axis):
            yield terms

    def create_exercise(self, term1, term2, base):
        # tag the exercise to separate additions where the result is under or
        # above one
        addition = term1 + term2
        if addition > base:
            tags = 'maior-que-1'
        else:
            tags = 'menor-igual-1'

        filter1 = max([term1, term2])
        filter2 = base

        description = '{t1}/{b} + {t2}/{b}'.format(t1=term1, t2=term2, b=base)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, tags=tags, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplicate the exercise

        self.create_variation(exercise, term1, term2, addition, base)

        return exercise

    def create_variation(self, exercise, term1, term2, result, base):
        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=1,
                                              group='term1',
                                              char_value=str(term1)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term1',
                                              char_value=str(base)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=1,
                                              group='term2',
                                              char_value=str(term2)))

        self.questions.append(models.Question(exercise=exercise,
                                              type='char',
                                              position=0,
                                              group='term2',
                                              char_value=str(base)))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=1,
                                          tabindex=1,
                                          group='result',
                                          value=result))

        self.answers.append(models.Answer(exercise=exercise,
                                          type='exact',
                                          position=0,
                                          tabindex=2,
                                          group='result',
                                          value=base))
