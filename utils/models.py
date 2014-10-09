from django.contrib.auth.models import User
from django.db import models


def id_as_username(prefix='user'):
    m = User.objects.all().aggregate(id=models.Max('id'))
    id = m.get('id', 0) + 1
    return '{prefix}{id}'.format(prefix=prefix, id=id)


class MultiDict(object):
    """
    Given a queryset or a list, group it by the group attribute of each item
    but still preserv the original list navigation, giving a bidimensional
    access.
    """
    def __init__(self, initial, group_callback=None):
        self.items_list = []
        self.items_dict = {}
        for item in initial:
            if group_callback is not None:
                group = group_callback(item)
            else:
                group = item.group
            self.add(item, group)

    def __unicode__(self):
        return unicode(self.items_list) + '\n' + unicode(self.items_dict)

    def __len__(self):
        return len(self.items_list)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.items_list[key]
        else:
            return self.items_dict[key]

    def add(self, item, key):
        self.items_list.append(item)
        if not key in self.items_dict:
            self.items_dict[key] = [item]
        else:
            self.items_dict[key].append(item)

    def get(self, key, default):
        if key in self.items_dict:
            return self[key]
        else:
            return default


class MultiDictManager(models.Manager):
    """
    Converts a resulting list to a bidimensional mapping object that can be
    accessed as a list or as a dictionary of lists grouped together by the
    *group* field.
    """
    def as_dict(self):
        return MultiDict(self.all())


def generate_random_passwords(quantity, length=5, flat=False):
    """
    Generates the given random passwords quantity using django's own password
    generator but with only lowecase letters and digits not ambiguous.
    """
    passwords = []
    for i in xrange(quantity):
        passwords.append(User.objects.make_random_password(
            length=length,
            allowed_chars='abcdefghjkmnpqrstuvwxyz23456789'
        ))
    if quantity == 1 and flat:
        return passwords[0]
    else:
        return passwords
