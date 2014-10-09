import datetime
from django.utils import timezone

from django.core.management import base
from django.utils.translation import ugettext_lazy as _

from clients.models import Contract


class Command(base.BaseCommand):
    help = _('Generate payment for the current month for all contracts with '
             'classes, using the 1st day as ref_date')

    def handle(self, **options):
        today = timezone.now()
        ref_date = datetime.date(today.year, today.month, 1)

        contracts = Contract.objects.filter(klass__isnull=False).distinct()
        for contract in contracts:
            payment, created = contract.payment_set.get_or_create(
                ref_date__month=ref_date.month, ref_date__year=ref_date.year,
                defaults={
                    'due_date': datetime.date(today.year, today.month, contract.payment_day),
                    'ref_date': ref_date
                }
            )
            if created:
                for klass in contract.klass_set.all():
                    klass.klasspayment_set.create(payment=payment,
                                                  current_cost=klass.cost)
