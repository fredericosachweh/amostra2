import re

from createadditionexpressions import Command as BaseCommand
from exercises import models


class Command(BaseCommand):
    help = "Create addition and subtraction exercises with potentiation and root extraction."
    subject = 'expressoes-potenciacao-radiciacao'
    split_term = r'([\^r+-])'

    def get_category_slug(self):
        return 'expressoes-potenciacao-radiciacao-adicao-subtracao'

    def split_terms(self, operation):
        terms = re.split(self.split_term, operation)
        terms = [t for t in terms if t]
        if operation[0].isdigit():
            terms.insert(0, '+')  # first plus sign
        signals = terms[::2]
        numbers = [int(i) for i in terms[1::2]]
        results = self.get_results(signals, numbers)
        return (terms, results)

    def check_root(self, number, exponent):
        result = round(number ** (1. / exponent))
        reverted_result = result ** exponent
        if number != reverted_result:
            raise ValueError('Result of the root extraction is not an exact value.')
        return result

    def get_results(self, signals, numbers):
        results = list()
        first_signal = signals[0]
        if first_signal == '-':
            numbers[0] = numbers[0] * -1
        exponent1 = numbers[1]
        exponent2 = numbers[4]
        number1 = numbers[0]
        number2 = numbers[2]
        number3 = numbers[3]
        number4 = numbers[-1]

        if signals[1] == '^':
            result1 = number1 ** exponent1
        else:
            result1 = self.check_root(number1, exponent1)
        results.append(result1)
        if signals[4] == '^':
            result2 = number3 ** exponent2
        else:
            result2 = self.check_root(number3, exponent2)
        results.append(result2)
        if signals[2] == '-':
            result3 = result1 - number2
        else:
            result3 = result1 + number2
        results.append(result3)
        if signals[3] == '-':
            result4 = result3 - result2
        else:
            result4 = result3 + result2
        results.append(result4)
        if signals[5] == '-':
            result5 = result4 - number4
        else:
            result5 = result4 + number4
        results.append(result5)
        return results

    def create_exercise(self, terms, results):
        description = ''.join([str(term) for term in terms])
        numbers = [int(i) for i in terms[1::2]]
        filter1 = min(numbers)
        filter2 = max(numbers)
        tags = list()
        if terms[0] == '-':
            tags.append('inicio-negat')
        else:
            tags.append('inicio-posit')
        if results[-1] < 0:
            tags.append('result-negat')
        else:
            tags.append('result-posit')

        exercise, created = self.category.exercise_set.get_or_create(
            description=description,
            filter1=filter1,
            filter2=filter2,
            tags=','.join(tags))

        if not created:
            return  # avoid create the exercise again

        for n, term in enumerate(terms):
            self.questions.append(models.Question(exercise=exercise,
                                                  type='char',
                                                  position=len(terms) - n,
                                                  group='exp',
                                                  char_value=term))

        for n, result in enumerate(results):
            self.answers.append(models.Answer(exercise=exercise,
                                              type=type,
                                              position=len(results) - n,
                                              tabindex=n+1,
                                              group='result',
                                              value=result))
