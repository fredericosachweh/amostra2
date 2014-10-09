import optparse

from decimal import Decimal as D
from createdecimalmultiplication import Command as BaseCommand


class Command(BaseCommand):
    help = "Create multiplication of decimal per integer exercises."
    category = 'multiplicacao-decimal-por-inteiro'

    option_list = BaseCommand.option_list + (
        optparse.make_option('--integer-limit',
            action='store', type='int', dest='integer_limit',
            help='What will be the limit for the integer range?'),
    )

    def handle(self, *args, **kwargs):
        self.integer_limit = kwargs.get('integer_limit', None)
        if not kwargs['operation'] and not self.integer_limit:
            raise Exception('You must specify the integer range limit')
        return super(Command, self).handle(*args, **kwargs)

    def generate_operations(self):
        dozens = D(10) ** self.decimal_places
        start = 1
        limit = self.limit * dozens
        for term1 in xrange(start, limit + 1):
            for term2 in xrange(start, self.integer_limit + 1):
                if term1 % 10 == 0:
                    continue  # avoid numbers like 1.10 or 2.300
                yield (term1 / dozens, term2)
