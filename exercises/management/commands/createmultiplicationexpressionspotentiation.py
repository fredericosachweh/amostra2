from createadditionexpressionspotentiation import Command as BaseCommand


class DecimalDivisionError(Exception):
    pass


class Command(BaseCommand):
    split_term = r'([\^r/*+-])'

    def get_category_slug(self):
        return 'expressoes-potenciacao-radiciacao-multiplicacao'

    def check_division(self, term1, term2):
        if term1 % term2:
            raise DecimalDivisionError
        return term1 / term2

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
        if signals[2] == '*':
            result3 = result1 * number2
        else:
            result3 = self.check_division(result1, number2)
        results.append(result3)
        if signals[5] == '*':
            result4 = result2 * number4
        else:
            result4 = self.check_division(result2, number4)
        results.append(result4)
        if signals[3] == '-':
            result5 = result3 - result4
        else:
            result5 = + result3 + result4
        results.append(result5)
        return results
