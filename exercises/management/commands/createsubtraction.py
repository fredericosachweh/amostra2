from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create subtraction exercises."
    matter = 'matematica'
    subject = 'subtracao'
    category = 'subtracao'

    def split_terms(self, operation):
        return [int(t.strip()) for t in operation.split('-')]

    def generate_operations(self):
        for term1 in range(self.limit + 1):
            for term2 in range(term1):
                yield (term1, term2)

    def get_tags(self):
        """
        The default integer subtraction creation don't need tags but there is room
        for subclasses (like decimal subtraction) implement custom tags.
        """
        return ''

    def create_exercise(self, term1, term2):
        description = '{0} - {1}'.format(term1, term2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            tags=self.get_tags(),
            filter1=term1,
            filter2=term2)

        if not created:
            return  # avoid duplications

        # makes (153, 34) becomes (351, 43), as we run rtl
        self.create_exercise_data(exercise, term1, term2)
        return exercise

    def create_exercise_data(self, exercise, term1, term2):
        str1, str2 = str(term1)[::-1], str(term2)[::-1]

        # create each line1 number
        line1 = ''
        for n, c in enumerate(str1):
            line1 = c + line1
            self.questions.append(models.Question(exercise=exercise,
                                             type='char',
                                             position=n,
                                             group='line1',
                                             char_value=c))

        # create each line2 number
        line2 = ''
        for n, c in enumerate(str2):
            line2 = c + line2
            self.questions.append(models.Question(exercise=exercise,
                                             type='char',
                                             position=n,
                                             group='line2',
                                             char_value=c))

        str2 = str2.ljust(len(str1), '0')  # makes "43" be "430"

        # assumes that in the first iter, we didn't have to borrow
        had_to_borrow = False
        cannot_borrow = False

        # negative tabindex takes the support from the tab sequence. The user
        # must rely on a mouse click
        support_tabindex = -1

        # run through both lines at same time
        result = ''
        for n, (char1, char2) in enumerate(zip(str1, str2)):
            int1, int2 = int(char1), int(char2)

            # if we had to borrow in the last iter, this term must give
            # one unity and we must create an exact digit answer for it
            if had_to_borrow:
                int1 = int1 - 1
                if int1 < 0:
                    int1 = 9
                    cannot_borrow = True # term was 0, we must keep borrowing
                else:
                    cannot_borrow = False
                self.answers.append(models.Answer(exercise=exercise,
                                             type='digit',
                                             position=n,
                                             tabindex=support_tabindex,
                                             group='support',
                                             value=int1))
            elif n > 0:
                # otherwise, just create an optional answer that accepts zero
                # or blank value, but only for the seconds term and forward
                self.answers.append(models.Answer(exercise=exercise,
                                             type='digit_or_blank',
                                             tabindex=support_tabindex,
                                             position=n,
                                             group='support',
                                             value=0))

            res = int1 - int2

            # if res is negative, we must borrow a unity from the
            # neightbor that makes the first number grow by ten
            # we also take note of the borrow to cut the next term
            if res < 0:
                res = int1 + 10 - int2
                had_to_borrow = True  # borrow from the next iter
            else:
                if cannot_borrow:
                    had_to_borrow = True
                else:
                    had_to_borrow = False
            result = str(res) + result
            self.answers.append(models.Answer(exercise=exercise,
                                         type='digit',
                                         position=n,
                                         tabindex=n + 1,
                                         group='result',
                                         value=res))
