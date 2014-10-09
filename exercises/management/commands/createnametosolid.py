# -*- encoding: utf-8 -*-
from createsolidtoname import Command as BaseCommand


class Command(BaseCommand):
    help = "Create name to geometric solid exercises."
    category = 'nome-para-solidos-geometricos'
    description = u'{0} (nome para sólido geom.)'
