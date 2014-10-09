# -*- encoding: utf-8 -*-
from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create figure to fraction convertion exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'figura-para-fracao'
    description = u'{0}/{1} (fig. para fração)'
    bulk_create_answers = False

    def split_terms(self, term):
        """
        Tell a term like 3/5.
        """
        terms = term.strip().split('/')
        return [int(t) for t in terms]

    def generate_operations(self):
        """
        Fractions from 1/2 until limit/limit.
        """
        for i in range(2, self.limit + 1):
            for j in range(1, i + 1):
                yield (j, i)

    def make_choices(self, term1, term2):
        """
        If term1/term2 is 3/5, generates choices from 1/4 to 4/4, 1/5 to 5/5
        and 1/6 to 6/6, excluding 3/5 and any number proportional to it.
        """
        ratio = float(term1) / float(term2)
        for i in (term2 - 1, term2, term2 + 1):
            if i < 2:
                continue  # avoid choices like 1/1 or 1/0
            for j in range(1, i + 1):
                if float(j) / float(i) == ratio:
                    continue  # avoid equivalent fractions
                yield j, i

    def create_exercise(self, term1, term2):
        desc = self.description.format(term1, term2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=desc, filter1=term1, filter2=term2)

        if not created:
            return  # avoid duplicate exercise

        for n, term in enumerate((term2, term1)):  # use reverse order
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=n,
                                                  group='fraction',
                                                  char_value=str(term)))

        choices_map = ['+{0}/{1}'.format(term1, term2)]
        for i, j in self.make_choices(term1, term2):
            choices_map.append('-{0}/{1}'.format(i, j))

        # give limit to 5 choices no matter how many was defined
        self.answers.append(models.Answer(exercise=exercise,
                                          type='radio',
                                          position=0,
                                          tabindex=1,
                                          group='result',
                                          choices_map='\n'.join(choices_map),
                                          choices_sample=5))

        return exercise
