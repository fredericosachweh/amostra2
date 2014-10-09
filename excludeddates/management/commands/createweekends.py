import datetime

from django.core.management.base import BaseCommand
from django.utils.dateformat import format
from django.utils.dateparse import parse_date

from excludeddates import models


class Command(BaseCommand):
    def get_weekends(self, first_date):
        """
        Gives a list of SystemDate instances starting from the given date and
        cycling through sundays and saturdays until the end of the year.
        """
        date = first_date
        while 1:
            yield models.SystemDate(date=date)

            if date.isoweekday() == 7:
                period = 6
            elif date.isoweekday() == 6:
                period = 1
            else:
                raise ValueError('The first date must be a weekend.')
            date = date + datetime.timedelta(days=period)

            if date.year != first_date.year:
                break

    def handle(self, date_str, *args, **kwargs):
        # finds the first sunday near the ref date
        ref = parse_date(date_str)
        date = ref - datetime.timedelta(days=ref.isoweekday())

        # create all dates with one hit!
        models.SystemDate.objects.bulk_create(self.get_weekends(date))
