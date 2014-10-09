import itertools

from createthreefractionsadditionsamebase import Command as BaseCommand


class Command(BaseCommand):
    help = "Create subtraction of 3 fractions with same base exercises."
    category = 'subtracao-3-fracoes-mesmo-denominador'
    terms_separator = '-'

    def generate_operations(self):
        interval = xrange(1, self.limit + 1)
        axis = [interval] * 4
        for terms in itertools.product(*axis):
            if (terms[0] - terms[1] - terms[2]) < 1:
                continue  # ignore result 0 or negative
            yield terms

    def create_exercise(self, term1, term2, term3, base):
        # tag the exercise to separate additions where the result is under or
        # above one
        subtraction = term1 - term2 - term3
        if subtraction > base:
            tags = 'maior-que-1'
        else:
            tags = 'menor-igual-1'

        filter1 = max([term1, term2, term3])
        filter2 = base

        description = '{t1}/{b} - {t2}/{b} - {t3}/{b}'.format(t1=term1, t2=term2, t3=term3, b=base)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, tags=tags, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplicate the exercise

        self.create_variation(exercise, term1, term2, term3, subtraction, base)

        return exercise
