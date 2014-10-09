import math


from django import template
from django.template.defaultfilters import floatformat
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def render_form(form):
    s = force_unicode(form.non_field_errors())
    for field in form.hidden_fields():
        s += force_unicode(field)
    for field in form.visible_fields():
        s += render_field(field)
    return mark_safe(s)


@register.filter
def render_field(field):
    templates = [
        'forms/{0}.html'.format(field.field.widget.__class__.__name__.lower()),
        'forms/field.html'
    ]
    return template.loader.render_to_string(templates, {'field': field})


@register.filter
def format_minutes(seconds):
    seconds = int(seconds)
    hours = seconds / 60 ** 2
    seconds = seconds % 60 ** 2
    minutes = seconds / 60
    seconds = seconds % 60

    output = '{0:02}:{1:02}'.format(minutes, seconds)
    if hours > 0:
        output = '{0:02}:'.format(hours) + output
    return output


@register.filter
def cut_zeros(n):
    """
    Format a number as string forcing several decimal places and cut extra
    right side zeros and the decimal point if necessary.
    """
    return floatformat(n, '17').rstrip('0').rstrip('.,')


@register.filter
def round_range(range, number):
    """Given a range, round it on a number."""
    index = range.index(number)
    start = index - 4
    if start < 0:
        start = 0
    end = index + 4 + 1
    if end > len(range):
        end = len(range)
    return range[start:end]


@register.simple_tag(takes_context=True)
def pagination_parameters(context):
    """Get parameters without the page index to build pagination links."""
    querydict = context['request'].GET.copy()
    if 'page' in querydict:
        del querydict['page']
    return querydict.urlencode()


@register.filter
def make_range(n):
    """
    Get value and find next perfect square

    e.g
    2 tiles have 2x2 blocks
    3 tiles have 2x2 blocks
    5 tiles have 3x3 blocks
    9 tiles have 3x3 blocks
    10 tiles have 4x4 blocks
    """
    n = range(int(n))
    return n

