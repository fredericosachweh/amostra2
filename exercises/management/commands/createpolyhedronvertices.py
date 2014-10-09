# -*- encoding: utf-8 -*-
from createpolyhedronfaces import Command as BaseCommand
from utils.polygons import POLYHEDRON_VERTICES


class Command(BaseCommand):
    help = "Create polyhedron vertices exercises."
    matter = 'matematica'
    subject = 'figuras-geometricas'
    category = 'vertices-de-poliedros'
    repository = POLYHEDRON_VERTICES
    description = u'{0} (vértices de poliedro)'
