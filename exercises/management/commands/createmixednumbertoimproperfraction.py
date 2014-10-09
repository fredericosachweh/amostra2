# -*- encoding: utf-8 -*-
from createimproperfractiontomixednumber import Command as BaseCommand


class Command(BaseCommand):
    """
    This is the same command of create improper fraction to mixed number. The
    only difference is the exercise description and category name, that
    influences the template used.
    """
    help = "Create mixed number to improper fraction conversion exercises."
    category = 'misto-para-fracao-impropria'
    description = u'{0}/{1} (misto para fração impr.)'
