from django import template


register = template.Library()


@register.assignment_tag
def next_batteries_schedules(klass, number=3):
    return klass.program_usage.batteryschedule_set.pending()[:number]
