from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from clients.models import Client


class FollowupManager(models.Manager):
    def tasks(self, qs=None):
        """ Searches for followup items that are tasks. """
        if not qs:
            qs = self.all()
        return self.exclude(due_date=None).exclude(responsible=None)

    def pending(self):
        """ Shows future tasks or not done tasks. """
        return self.filter(
            (models.Q(due_date__isnull=False) & models.Q(is_done=False)) |
            models.Q(due_date__gt=timezone.now())
        )

    def pending_for_user(self, user):
        """ Shows future or not done tasks for authors or responsibles. """
        qs = self.pending()
        return qs.filter(models.Q(author=user) | models.Q(responsible=user))


class Followup(models.Model):
    """
    The followup can represent history entries or tasks, when sets a due date
    and a responsible.
    """
    client = models.ForeignKey(Client, verbose_name=_('client'))
    author = models.ForeignKey(
        User, verbose_name=_('author'),
        related_name='followup_entries', blank=True, null=True
    )
    content = models.TextField(_('content'))
    created_at = models.DateTimeField(_('date'), default=timezone.now)

    due_date = models.DateTimeField(_('due date'), blank=True, null=True)
    responsible = models.ForeignKey(
        User, verbose_name=_('responsible'),
        related_name='followup_tasks', blank=True, null=True
    )
    is_done = models.BooleanField(default=False)

    # reference date for ordering is the due_date or the created_at
    ref_date = models.DateTimeField(_('ref date'), editable=False)

    objects = FollowupManager()

    def __unicode__(self):
        return self.content

    def save(self, *args, **kwargs):
        self.ref_date = self.due_date or self.created_at
        super(Followup, self).save(*args, **kwargs)

    def is_task(self):
        return bool(self.due_date) and bool(self.responsible)

    class Meta:
        verbose_name = _('followup')
        verbose_name_plural = _('followup')
        ordering = ('-ref_date',)


class Task(Followup):
    class Meta:
        proxy = True
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def is_late(self):
        return self.deadline <= timezone.now()
