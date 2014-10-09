from django.db import models
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _
from clients.models import Client, Teacher


# any date would have any of these states based on how many times it
# appears in the three different dates list (system, manager, teacher)
DATE_STATES = {
    0: 'included',
    1: 'excluded',
    2: 're-included',
    3: 're-excluded',
}


class BaseDate(models.Model):
    """
    A excluded date is a date to be ignored when allocating classes.

    The date can be excluded in 3 repositories:

    * Weekend and holidays (default, by admin team)
    * School vacations (by manager)
    * Teacher impediments (by himself)

    If the date appears once in any list, will be excluded. If it appears
    twice, it is re-included, otherwise, it is re-excluded.
    """
    date = models.DateField(_('date'))

    class Meta:
        abstract = True
        ordering = ('date',)

    def __unicode__(self):
        return date_format(self.date)


class SystemDate(BaseDate):
    """
    Dates excluded by the administration team (e.g. weekends and holidays).
    """
    class Meta:
        verbose_name = _('system excluded date')
        verbose_name_plural = _('system excluded dates')


class ClientDate(BaseDate):
    """
    Dates excluded by the manager of the client (e.g. school vacations).
    """
    client = models.ForeignKey(Client, verbose_name=_('client'))

    class Meta:
        unique_together = ('date', 'client')
        verbose_name = _('client excluded date')
        verbose_name_plural = _('client excluded dates')


class TeacherDate(BaseDate):
    """
    Dates excluded by the teacher of a class (e.g. class council).
    """
    teacher = models.ForeignKey(Teacher, verbose_name=_('teacher'))

    class Meta:
        unique_together = ('date', 'teacher')
        verbose_name = _('teacher excluded date')
        verbose_name_plural = _('teacher excluded dates')
