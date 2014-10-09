from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailFromTemplate(EmailMultiAlternatives):
    def __init__(self, subject='', from_email=None, to=None,
                 template_name=None, context={}, **kwargs):

        if template_name is None:
            raise TypeError('You must specify a template base name')

        context.update({
            'STATIC_URL': settings.STATIC_URL,
            'site': Site.objects.get_current(),
        })

        text_template = template_name + '.txt'
        text_content = render_to_string(text_template, context)
        super(EmailFromTemplate, self).__init__(subject, text_content, from_email, to, **kwargs)

        html_template = template_name + '.html'
        html_content = render_to_string(html_template, context)
        self.attach_alternative(content=html_content, mimetype='text/html')


def split_name(name):
    """
    Returns a tuple with the first and last name after split a full name.
    """
    try:
        first_name, last_name = name.split(' ', 1)
    except ValueError:
        first_name, last_name = name, ''
    return (first_name, last_name)
