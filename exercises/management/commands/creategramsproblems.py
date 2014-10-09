from createmetersproblems import Command as BaseCommand


class Command(BaseCommand):
    help = "Create mass problems exercises."
    category = 'problemas-gramas'

    UNITIES = [
        {'unity': 'g', 'name': 'grama', 'power': 1E0},
        {'unity': 'dag', 'name': u'decagrama', 'power': 1E1},
        {'unity': 'hg', 'name': u'hectograma', 'power': 1E2},
        {'unity': 'kg', 'name': u'quilograma', 'power': 1E3},
        {'unity': 'dg', 'name': u'decigrama', 'power': 1E-1},
        {'unity': 'cg', 'name': u'centigrama', 'power': 1E-2},
        {'unity': 'mg', 'name': u'miligrama', 'power': 1E-3},
    ]
