# -*- encoding: utf-8 -*-
from createfiguretoimproperfraction import Command as BaseCommand


class Command(BaseCommand):
    """
    This is the same command of create figure to improper fraction. The only
    difference is the exercise description and category name, that influences
    the template used.
    """
    help = "Create improper fraction to figure convertion exercises."
    category = 'fracao-impropria-para-figura'
    description = u'{0}/{1} (fração impr. para fig.)'
