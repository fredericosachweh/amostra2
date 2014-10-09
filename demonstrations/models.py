import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from clients.models import Client


DEMONSTRATION_PERIOD = 5


class DemonstrationManager(models.Manager):
    def active(self):
        return self.all()


def five_days_from_now():
    return timezone.now().date() + datetime.timedelta(days=5)


class Demonstration(models.Model):
    """
    A demonstration is a trial solicitation from a client.
    """
    client = models.ForeignKey(Client, verbose_name=_('client'))
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    valid_until = models.DateField(_('valid until'), default=five_days_from_now)
    has_agreed = models.BooleanField(_('has agreed with terms?'), default=False)
    objects = DemonstrationManager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('demonstration')
        verbose_name_plural = _('demonstrations')

    def save(self, *args, **kwargs):
        if not self.valid_until:
            self.valid_until = self.created_at + \
                    datetime.timedelta(days=DEMONSTRATION_PERIOD)
        return super(Demonstration, self).save(*args, **kwargs)

    def is_expired(self):
        """ Tells if the valid_until didn't cross the current day. """
        now = timezone.now().date()
        return self.valid_until < now


    @models.permalink
    def get_absolute_url(self):
        return ('demonstrations:demo-start', (), {'pk': self.pk})


class CategoryUsage(models.Model):
    """
    Categories usage predefines what categories would be used in the
    demonstration and let a room for the exercise chance. Once the chance is
    done, the usage is done too.
    """
    demonstration = models.ForeignKey(Demonstration)
    category = models.ForeignKey('exercises.Category', related_name='demonstrations_category_usages')
    chance = models.ForeignKey('exercises.Chance', blank=True, null=True)
    position = models.IntegerField(_('position'))

    class Meta:
        ordering = ('position',)
        verbose_name = _('category usage')
        verbose_name_plural = _('categories usage')
