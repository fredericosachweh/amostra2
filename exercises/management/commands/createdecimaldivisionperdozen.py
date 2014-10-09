from createdecimalmultiplicationperdozen import Command as BaseCommand


class Command(BaseCommand):
    help = "Create division of decimal per dozens exercises."
    subject = 'divisao'
    category = 'divisao-de-decimal-por-dezena-centena-e-milhar'

    def split_terms(self, operation):
        """ Returns decimal numbers converted from strings like 9,99. """
        return [self.format_number(t) for t in operation.split('/')]

    def get_result(self, term1, term2):
        return term1 / term2

    def create_exercise(self, term1, term2):
        description = '{0} / {1} (por dezena)'.format(term1, term2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            tags=self.get_tags(),
            filter1=term1,
            filter2=term2
        )

        if not created:
            return  # avoid duplications

        self.create_exercise_data(exercise, term1, term2)
        return exercise
