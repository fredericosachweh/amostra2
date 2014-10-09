from django.db import models

from clients.models import Client, Klass
from demonstrations.models import Demonstration
from followup.models import Followup
from payments.models import Payment


def set_client_status(sender, instance, **kwargs):
    """
    The client status would be:

    removed: manually removed; TODO
    cancelled: manually cancelled; TODO
    inactive: has only inactive klasses (klasses ended);
    frozen: has active klasses from pending contracts;
    active: has active klasses (klasses not ended, from up to date contracts);
    lead: has created only one payment but didn't paid it;
    prospect: has at least one task or demonstration created;
    suspect: any other case;
    """
    client = instance.client
    active_klasses = Klass.objects.active().filter(contract__client=client)
    if active_klasses.exists():
        status = 'active'
    else:
        payments = Payment.objects.filter(contract__client=client)
        payments_count = payments.count()
        if payments_count == 1 and not payments[0].was_paid:
            status = 'lead'
        elif payments_count > 1:
            if payments.filter(was_paid=False).exists():
                status = 'frozen'
            else:
                status = 'inactive'
        else:
            demonstrations = client.demonstration_set.all()
            tasks = client.followup_set.tasks()
            if demonstrations.exists() or tasks.exists():
                status = 'prospect'
            else:
                status = 'suspect'
    Client.objects.filter(pk=client.pk).update(status=status)
models.signals.post_save.connect(set_client_status, sender=Klass)
models.signals.post_delete.connect(set_client_status, sender=Klass)
models.signals.post_save.connect(set_client_status, sender=Demonstration)
models.signals.post_delete.connect(set_client_status, sender=Demonstration)
models.signals.post_save.connect(set_client_status, sender=Followup)
models.signals.post_delete.connect(set_client_status, sender=Followup)
models.signals.post_save.connect(set_client_status, sender=Payment)
models.signals.post_delete.connect(set_client_status, sender=Payment)
