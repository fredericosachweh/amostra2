import itertools
from decimal import Decimal as D

from createdecimaladdition import Command as BaseCommand

from exercises import models


class Command(BaseCommand):
    help = "Create decimal addition with 3 addends exercises"
    category = 'soma-tres-andares-decimal'

    def generate_operations(self):
        dozens = D(10) ** self.decimal_places
        limit = self.limit * dozens
        interval = xrange(1, limit)
        print len(interval)
        for term1, term2, term3 in itertools.product(*[interval] * 3):
            if term1 % 10 == 0 or term2 % 10 == 0 or term3 % 10 == 0:
                continue  # avoid numbers like 1.10 or 2.300
            yield(term1 / dozens, term2 / dozens, term3 / dozens)

    def create_exercise(self, term1, term2, term3):
        filter1 = min([term1, term2, term3])
        filter2 = max([term1, term2, term3])

        description = '{0} + {1} + {2}'.format(term1, term2, term3)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            filter1=filter1,
            filter2=filter2)

        if not created:
            return  # avoid create the exercise again

        self.create_exercise_data(exercise, term1, term2, term3)

        return exercise

    def create_exercise_data(self, exercise, term1, term2, term3):
        f = '{:.%df}' % self.decimal_places  # .2f, .3f and so on
        int1, dec1 = f.format(term1).split('.')
        int2, dec2 = f.format(term2).split('.')
        int3, dec3 = f.format(term3).split('.')

        str1 = (int1 + dec1)[::-1]
        str2 = (int2 + dec2)[::-1]
        str3 = (int3 + dec3)[::-1]

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
        # create each line3 number
        line3 = ''
        for n, c in enumerate(str3):
            line3 = c + line3
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=n,
                                                  group='line3',
                                                  char_value=c))

        size = max(len(str1), len(str2), len(str3))
        if len(str1) < size:
            str1 = str1.ljust(size, '0')
        if len(str2) < size:
            str2 = str2.ljust(size, '0')
        if len(dec3) < size:
            str3 = str3.ljust(size, '0')

        result = ''
        support_str = ''
        support = 0
        tabindex = 1
        for n, (char1, char2, char3) in enumerate(zip(str1, str2, str3)):
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

            # convert lines to int
            int1, int2, int3 = int(char1), int(char2), int(char3)
            # calculares lines to build a result
            res = int1 + int2 + int3 + support

            # check is result is greater than 9, if true, first digit become support
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

            # The last support fall down as a result
            if n == (size - 1) and support > 0:
                result = str(support) + result
                self.answers.append(models.Answer(exercise=exercise,
                                                  type='digit',
                                                  position=n+1,
                                                  tabindex=tabindex+1,
                                                  group='result',
                                                  value=support))

            tabindex += 2
        for i in range(1, len(str1)):
            if i == self.decimal_places:
                comma = ','
            else:
                comma = ' '
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='comma1',
                                                  char_value=comma))
        for i in range(1, len(str2)):
            if i == self.decimal_places:
                comma = ','
            else:
                comma = ' '
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='comma2',
                                                  char_value=comma))

        for i in range(1, len(str3)):
            if i == self.decimal_places:
                comma = ','
            else:
                comma = ' '
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=i,
                                                  group='comma3',
                                                  char_value=comma))

        result = term1 + term2 + term3
        result_str = f.format(result).replace('.', '')  # makes 1.034 be 1034
        tabindex = len(self.answers)
        for i in range(1, len(result_str)):
            if i == self.decimal_places:
                comma = True
            else:
                comma = False

            self.answers.append(models.Answer(exercise=exercise,
                                              type='boolean',
                                              position=i,
                                              tabindex=tabindex+i,
                                              group='comma',
                                              value=comma))
