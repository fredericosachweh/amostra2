from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create addition exercises."
    matter = 'matematica'
    subject = 'adicao'
    category = 'soma-dois-andares'

    def split_terms(self, operation):
        return [int(t.strip()) for t in operation.split('+')]

    def generate_operations(self):
        for term1 in xrange(self.limit + 1):
            for term2 in xrange(self.limit + 1):
                yield (term1, term2)

    def get_tags(self):
        """
        The default integer addition creation don't need tags but there is room
        for subclasses (like decimal additions) implement custom tags.
        """
        return ''

    def create_exercise(self, term1, term2):
        description = '{0} + {1}'.format(term1, term2)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            tags=self.get_tags(),
            filter1=term1,
            filter2=term2)

        if not created:
            return  # avoid create the exercise again

        self.create_exercise_data(exercise, term1, term2)
        return exercise

    def create_exercise_data(self, exercise, term1, term2):
        # makes (315, 92) becomes (513, 29), as we run rtl
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

        size = max(len(str1), len(str2))
        if len(str2) < size:
            str2 = str2.ljust(size, '0')  # makes "29" be "290"
        if len(str1) < size:
            str1 = str1.ljust(size, '0')  # makes "29" be "290"

        result = ''
        support_str = ''
        support = 0
        tabindex = 1
        for n, (char1, char2) in enumerate(zip(str1, str2)):

            if n > 0:
                if support > 0:
                    type = 'digit'
                elif support == 0:
                    type = 'digit_or_blank'
                support_str = str(support) + support_str
                self.answers.append(models.Answer(exercise=exercise,
                                                  type=type,
                                                  position=n,
                                                  tabindex=tabindex-1,
                                                  group='support',
                                                  value=support))

            int1, int2 = int(char1), int(char2)

            res = int1 + int2 + support

            if res > 9:
                support = int(str(res)[0])
                res = int(str(res)[1])
            else:
                support = 0

            result = str(res) + result
            self.answers.append(models.Answer(exercise=exercise,
                                              type='digit',
                                              position=n,
                                              tabindex=tabindex,
                                              group='result',
                                              value=res))

            if n == (size - 1) and support > 0:
                result = str(support) + result
                self.answers.append(models.Answer(exercise=exercise,
                                                  type='digit',
                                                  position=n+1,
                                                  tabindex=tabindex+1,
                                                  group='result',
                                                  value=support))

            tabindex += 2
