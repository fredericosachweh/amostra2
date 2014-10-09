from createmultiplicationtable import Command as BaseCommand


class Command(BaseCommand):
    help= "Create multiplication per dozen exercises."
    category = 'multiplicacao-por-dezena'
    description = '{0} * {1} (por dezena)'

    def get_dozens(self):
        dozen = self.limit
        times = [1]
        while 1:
            if dozen < 10:
                break

            dozen = dozen / 10
            times.append(times[-1] * 10)
        return times[1:]

    def generate_operations(self):
        for term1 in xrange(1, self.limit + 1):
            for term2 in self.get_dozens():
                yield (term1, term2)
