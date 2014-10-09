from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from utils.cardinals import fractional
from utils.polygons import REGULAR_POLYGONS, SOLIDS
from exercises import models

register = template.Library()


def convert_to_fraction(number):
    if isinstance(number, basestring):
        desc = number
    else:
        desc = number.description
    m, n = [int(x) for x in desc.split('/')]
    return m, n


@register.filter
def fraction_name(choice):
    m, n = convert_to_fraction(choice)
    return fractional(m, n)


@register.filter
def mixed_number(choice, base=None):
    """
    Converts a fraction like '10/6' onto a dict to represent
    the mixed number 1 4/6.
    """
    if base is None:
        m, n = convert_to_fraction(choice)
    else:
        m = int(choice)
        n = int(base)
    integer = m / n
    rest = m % n
    return {'integer': integer, 'term1': rest, 'term2': n}


@register.filter
def polygon_name(choice):
    if isinstance(choice, models.Choice):
        choice = choice.description
    return REGULAR_POLYGONS[int(choice)]


@register.filter
def solid_name(choice):
    if isinstance(choice, models.Choice):
        choice = choice.description
    return SOLIDS[choice]


@register.filter
def solid_figure(choice):
    if isinstance(choice, models.Choice):
        choice = choice.description
    return mark_safe('<img src="{0}images/polygons/{1}.svg" width="132"/>'.format(
        settings.STATIC_URL, choice))


@register.filter
def special_polygons(key):
    return mark_safe(u'<img src="{0}images/specialcasepolygons/{1}.svg" width="132"/>'.format(
            settings.STATIC_URL, key))
