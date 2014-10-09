from createpolyhedronfaces import Command as BaseCommand
from utils.polygons import POLYHEDRON_EDGES


class Command(BaseCommand):
    help = "Create polyhedron edges exercises."
    matter = 'matematica'
    subject = 'figuras-geometricas'
    category = 'arestas-de-poliedros'
    repository = POLYHEDRON_EDGES
    description = '{0} (arestas de poliedro)'
