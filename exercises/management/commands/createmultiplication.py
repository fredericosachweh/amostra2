from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create multiplication exercises."
    matter = 'matematica'
    subject = 'multiplicacao'
    category = 'multiplicacao'

    def split_terms(self, operation):
        return [int(t.strip()) for t in operation.split('*')]

    def generate_operations(self):
        for term1 in xrange(self.limit + 1):
            for term2 in xrange(self.limit + 1):
                yield (term1, term2)

    def get_tags(self, term1, term2):
        """
        The default integer multiplication creation don't need tags but there
        is room for subclasses (like decimal mult.) implement custom tags.
        """
        return ''

    def create_exercise(self, term1, term2):
        description = '{0} * {1}'.format(term1, term2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            tags=self.get_tags(term1, term2),
            filter1=term1,
            filter2=term2)

        if not created:
            return  # avoid duplications

        self.create_exercise_data(exercise, term1, term2)
        return exercise

    def create_exercise_data(self, exercise, term1, term2, sterm1=None, sterm2=None):
        if sterm1 is None:
            sterm1 = str(term1)
        if sterm2 is None:
            sterm2 = str(term2)

        result_width = max([len(sterm1), len(sterm2)])

        for i, c in enumerate(sterm1[::-1]):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='line1',
                                                  char_value=c))

        for i, c in enumerate(sterm2[::-1]):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='line2',
                                                  char_value=c))

            delta = len(self.answers)
            for j, d in enumerate(sterm1[::-1]):
                partial_group = 'partial{0}'.format(i + 1)
                support_group = 'support{0}'.format(i + 1)

                if j == 0:
                    dozen = 0  # first loop didn't set dozen yet
                subproduct = int(c) * int(d) + dozen

                if subproduct > 9:
                    dozen = subproduct / 10
                    unity = subproduct - dozen * 10
                else:
                    dozen = 0
                    unity = subproduct

                self.answers.append(models.Answer(exercise=exercise,
                                                  type='digit',
                                                  position=j,
                                                  tabindex=(j * 2 + 1) + delta,
                                                  group=partial_group,
                                                  value=unity))

                # the dozen part of subproduct becomes a support digit unless
                # in the last loop, where it becomes a partial result
                if (j + 1) == len(sterm1):
                    if dozen == 0:
                        break  # avoid a field to fill zero in the last loop

                    group = partial_group
                    position = j + 1
                else:
                    group = support_group
                    position = j

                if dozen == 0:
                    type = 'digit_or_blank'
                else:
                    type = 'digit'

                self.answers.append(models.Answer(exercise=exercise,
                                                  type=type,
                                                  position=position,
                                                  tabindex=(j * 2 + 2) + delta,
                                                  group=group,
                                                  value=dozen))

            width = j + 1 + i  # partial with + alignment
            if width > result_width:
                result_width = width

        if len(sterm2) > 1:
            delta = len(self.answers)
            product = str(term1 * term2)

            # fill the start of the result string with zeros to make it have the
            # same width of the largest subprodct and cache the original width
            # to compare and set these filled zeros as digit_or_blank
            original_width = len(product)
            if original_width < result_width:
                product = product.rjust(result_width, '0')

            for n, c in enumerate(product[::-1]):
                if (n + 1) > original_width:
                    # after the first non-zero, all digits must be exact, even
                    # another zeros in the muddle or end of number
                    type = 'digit_or_blank'
                else:
                    type = 'digit'
                self.answers.append(models.Answer(exercise=exercise,
                                                  type=type,
                                                  position=n,
                                                  tabindex=n + 1 + delta,
                                                  group='result',
                                                  value=int(c)))
