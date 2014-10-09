from django.core.management import base
from django.db.models import Count, Max

from exercises import models


class Command(base.BaseCommand):
    def handle(self, verbosity, *args, **options):
        self.verbosity = int(verbosity)
        qs = models.Category.objects.select_related('subject', 'matter')
        qs = qs.prefetch_related('sites') \
               .annotate(exercises=Count('exercise'),
                         upper_limit1=Max('exercise__filter1'),
                         upper_limit2=Max('exercise__filter2'))
        for c in qs:
            print ('%s (%d)' % (c.name, c.pk)).ljust(50), \
                  ('%d' % (c.exercises or 0)).rjust(10), \
                  ('%d' % (c.upper_limit1 or 0)).rjust(10), \
                  ('%d' % (c.upper_limit2 or 0)).rjust(10)

