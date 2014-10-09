import itertools

from createfractionadditionsamebase import Command as BaseCommand


class Command(BaseCommand):
    help = "Create subtraction of fraction with same base exercises."
    matter = 'matematica'
    subject = 'fracoes'
    category = 'subtracao-mesmo-denominador'
    terms_separator = '-'

    def generate_operations(self):
        interval = xrange(1, self.limit + 1)
        axis = [interval] * 3
        for term1, term2, base in itertools.product(*axis):
            if term2 >= term1:
                continue  # avoid zero or negative results
            yield (term1, term2, base)

    def create_exercise(self, term1, term2, base):
        # tag the exercise to separate additions where the result is under or
        # above one
        subtraction = term1 - term2
        if term1 > base or term2 > base:
            tags = 'maior-que-1'
        else:
            tags = 'menor-igual-1'

        filter1 = max([term1, term2])
        filter2 = base

        description = '{t1}/{b} - {t2}/{b}'.format(t1=term1, t2=term2, b=base)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description, tags=tags, filter1=filter1, filter2=filter2)

        if not created:
            return  # avoid duplications

        self.create_variation(exercise, term1, term2, subtraction, base)

        return exercise
