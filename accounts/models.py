from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy


class UserAccount(User):
    """
    Proxy model to be used in place of the user model when the name of the user
    is preferred as unicode representation of the object.
    """
    class Meta:
        proxy = True

    def __unicode__(self):
        return self.get_full_name()

    @property
    def user(self):
        """
        Returns a mirror of the user account as an user instance.
        """
        user = User()
        user.__dict__ = self.__dict__
        return user


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        permissions = (
            ('act-as-manager', 'Can act as clients manager'),
            ('act-as-teacher', 'Can act as teacher'),
            ('act-as-student', 'Can act as student'),
        )

    def __unicode__(self):
        return unicode(self.user)


def create_profile(sender, instance, created, **kwargs):
    """
    Creates a new profile with default values when a user is created.
    """
    if created:
        instance.profile_set.create()
models.signals.post_save.connect(create_profile, sender=User)

#
# Adds 2 methods to the user instance to get all home routes depending on his
# groups and to get the home route or a desambiguation page
#

ROUTES = {
    'students': (_('Student'), 'student:user-battery-list'),
    'teachers': (_('Teacher'), 'teacher:klass-list'),
    'managers': (_('Manager'), 'manager:contract-list'),
}


def get_home_urls(user):
    """
    Returns the pair or group name and url of the user homepage depending of
    his profile type (group).
    """
    groups = user.groups.filter(name__in=['managers', 'teachers', 'students']). \
                         values_list('name', flat=True)
    return [(ROUTES[name][0], reverse_lazy(ROUTES[name][1])) for name in groups]


def get_home_url(user):
    """
    Returns the only one url for the user or returns a url for a
    desambiguation page.
    """
    user_urls = user.get_home_urls()
    if len(user_urls) == 1:
        return user_urls[0][1]
    else:
        return reverse_lazy('home-desambiguation')


User.add_to_class('get_home_urls', get_home_urls)
User.add_to_class('get_home_url', get_home_url)
