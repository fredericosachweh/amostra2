from createhourstominutes import Command as BaseCommand


class Command(BaseCommand):
    help = "Create minutes to seconds and vice-versa exercises."
    category = 'minuto-para-segundo'
    direct_description = '{0}min = {1}s'
    inverse_description = '{0}s = {1}min'
