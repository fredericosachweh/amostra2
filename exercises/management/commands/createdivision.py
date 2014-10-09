import optparse

from base import BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create division exercises."
    matter = 'matematica'
    subject = 'divisao'
    category = 'divisao'

    option_list = BaseCommand.option_list + (
        optparse.make_option('--divisor-limit',
            action='store', type='int', dest='divisor_limit',
            help='What will be the limit for the divisor range?'),
        optparse.make_option('--without-rest',
            action='store_true', dest='without_rest', default=False,
            help='Only results without rest?'),
    )

    def handle(self, *args, **kwargs):
        self.divisor_limit = kwargs.get('divisor_limit', None)
        self.without_rest = kwargs.get('without_rest', False)
        if not kwargs['operation'] and not self.divisor_limit:
            raise Exception('You must specify the divisor range limit')
        return super(Command, self).handle(*args, **kwargs)

    def split_terms(self, operation):
        return [int(t.strip()) for t in operation.split('/')]

    def generate_operations(self):
        for divided in xrange(1, self.limit + 1):
            divisor_limit = min([self.divisor_limit, divided])
            for divisor in xrange(1, divisor_limit + 1):
                if divisor > divided:
                    continue
                if self.without_rest and divided % divisor:
                    continue
                yield (divided, divisor)

    def get_tags(self, divided, divisor):
        """ Tells if there would be rest or not in the integer division. """
        if divided % divisor:
            return 'com-resto'
        else:
            return 'sem-resto'

    def create_exercise(self, divided, divisor):
        description = '{0} / {1}'.format(divided, divisor)
        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            filter1=divided,
            filter2=divisor,
            tags=self.get_tags(divided, divisor)
        )

        if not created:
            return  # avoid duplicate the exercise

        self.create_exercise_data(exercise, divided, divisor)
        return exercise

    def get_divided_digit(self, digit):
        """
        Converts to integer a char representing a digit from the divided.

        Open room for subclasses deal with decimal numbers as example.
        """
        return int(digit)

    def create_exercise_data(self, exercise, divided, divisor):
        if not isinstance(divisor, int):
            divisor = int(divisor)

        for n, c in enumerate(str(divided)[::-1]):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=n,
                                                  group='divided',
                                                  char_value=str(c)))

        for n, c in enumerate(str(divisor)[::-1]):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=n,
                                                  group='divisor',
                                                  char_value=str(c)))

        divided_digits = list(str(divided))
        rest = 0
        iteration = 0
        down_delta = 0
        while 1:
            try:
                char = divided_digits.pop(0)
                digit = self.get_divided_digit(char) + rest * 10
            except IndexError:
                break
            result = digit / divisor
            rest = digit % divisor

            if not self.answers and result == 0:
                continue  # ignore trailing zeros before start the result

            if result == 0:
                down_delta += 1
                self.questions.append(models.Question(
                    exercise=exercise,
                    type='char',
                    position=down_delta,
                    group='move{0}'.format(iteration - down_delta),
                    char_value=' '
                ))
            else:
                down_delta = 0

            self.answers.append(models.Answer(exercise=exercise,
                                              type='digit',
                                              position=len(divided_digits),
                                              tabindex=len(self.answers) + 1,
                                              group='quotient',
                                              value=result))

            # XXX products, rests and lowered digits are created in crescent
            # order instead of the default decrecent. This way, the templates
            # must iter through it from the end to the first

            if result > 0:
                width = len(str(digit))

                product = result * divisor
                for n, c in enumerate(str(product).rjust(width, '0')):
                    self.answers.append(models.Answer(
                        exercise=exercise,
                        type='digit_or_blank',
                        position=n,
                        tabindex=len(self.answers) + 1,
                        group='product{0}'.format(iteration),
                        value=int(c)
                    ))

                rests = []
                for n, c in enumerate(str(rest).rjust(width, '0')):
                    rests.append(models.Answer(
                        exercise=exercise,
                        type='digit_or_blank',
                        position=n,
                        tabindex=len(self.answers) + width - n,
                        group='rest{0}'.format(iteration),
                        value=int(c)
                    ))
                self.answers.extend(rests)

            try:
                # The next digit "lowered" side to rest
                down = self.get_divided_digit(divided_digits[0])
            except IndexError:
                continue

            self.answers.append(models.Answer(
                exercise=exercise,
                type='digit',
                position=0 + down_delta,
                tabindex=len(self.answers) + 1,
                group='down{0}'.format(iteration - down_delta),
                value=int(down)
            ))

            iteration += 1
