from decimal import Decimal as D

from _decimals import DecimalDivisionMixin
from createdivision import Command as BaseCommand


class Command(DecimalDivisionMixin, BaseCommand):
    help = "Create division exercises of two integers with decimal result."
    matter = 'matematica'
    subject = 'divisao'
    category = 'divisao-resposta-decimal'

    option_list = BaseCommand.option_list + DecimalDivisionMixin.option_list

    def handle(self, *args, **kwargs):
        self.set_decimal_places(*args, **kwargs)
        return super(Command, self).handle(*args, **kwargs)

    def generate_decimal_operations(self):
        return BaseCommand.generate_operations(self)

    def create_exercise_data(self, exercise, divided, divisor):
        result = divided / D(divisor)
        sdivided, decimal_places = self.fill_divided_with_spaces(
            divided=str(divided),
            result=result,
            divided_places=0,
            divisor_places=0
        )

        super(Command, self).create_exercise_data(exercise, sdivided, divisor)

        self.make_comma_answers(exercise, result, decimal_places)
