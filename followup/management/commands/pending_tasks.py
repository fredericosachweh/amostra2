from datetime import timedelta
from django.utils.timezone import now

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import base
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from utils import EmailFromTemplate


class Command(base.BaseCommand):
    help = _("Sends e-mails to everyone with tasks from the current week.")

    def handle(self, verbosity, *args, **options):
        translation.activate('pt-BR')
        next_week = now() + timedelta(days=(7 - now().isoweekday() - 1))
        users = User.objects.prefetch_related('followup_tasks') \
            .filter(
                followup_tasks__is_done=False,
                followup_tasks__due_date__gt=now,
                followup_tasks__due_date__lt=next_week
            )

        for user in users:
            email = EmailFromTemplate(
                subject=_('New task for this week'),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
                template_name='followup/current_week_tasks',
                context={'user': user},
            )
            email.send()
        translation.deactivate()
