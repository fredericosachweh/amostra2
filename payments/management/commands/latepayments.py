from django.conf import settings
from django.core.management import base
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from utils import EmailFromTemplate
from clients.models import Klass


class Command(base.BaseCommand):
    help = _("Sends e-mails to managers with klass with late payments")

    def handle(self, verbosity, *args, **options):
        translation.activate('pt-BR')
        klasses = Klass.objects.late_payment()
        managers_email = [email[1] for email in settings.MANAGERS]
        email = EmailFromTemplate(
            subject=_('Klasses with late payments'),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=managers_email,
            template_name='payments/late_payments_email',
            context={'klasses': klasses},
        )
        email.send()
        translation.deactivate()
