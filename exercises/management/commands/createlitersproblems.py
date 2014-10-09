from createmetersproblems import Command as BaseCommand


class Command(BaseCommand):
    help = "Create volume problems exercises."
    category = 'problemas-litros'

    UNITIES = [
        {'unity': 'l', 'name': 'litro', 'power': 1E0},
        {'unity': 'dal', 'name': u'decalitro', 'power': 1E1},
        {'unity': 'hl', 'name': u'hectolitro', 'power': 1E2},
        {'unity': 'kl', 'name': u'quilolitro', 'power': 1E3},
        {'unity': 'dl', 'name': u'decilitro', 'power': 1E-1},
        {'unity': 'cl', 'name': u'centilitro', 'power': 1E-2},
        {'unity': 'ml', 'name': u'mililitro', 'power': 1E-3},
    ]
