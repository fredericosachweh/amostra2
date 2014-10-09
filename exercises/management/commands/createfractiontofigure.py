# -*- encoding: utf-8 -*-
from createfiguretofraction import Command as BaseCommand


class Command(BaseCommand):
    """
    This is the same command of create figure to fraction. The only difference
    is the exercise description and category name, that influences the template
    used.
    """
    help = "Create fraction to figure convertion exercises."
    category = 'fracao-para-figura'
    description = u'{0}/{1} (fração para fig.)'
