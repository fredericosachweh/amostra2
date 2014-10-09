from django.utils.translation import ugettext_lazy as _

REGULAR_POLYGONS = {
    3: _('triangle'),
    4: _('quadrilateral'),
    5: _('pentagon'),
    6: _('hexagon'),
    7: _('heptagon'),
    8: _('octagon'),
    9: _('enneagon'),
    10: _('decagon'),
    11: _('hendecagon'),
    12: _('dodecagon'),
}

SOLIDS = {
    'cube': _('cube'),
    'rectangular_prism': _('rectangular prism'),
    'triangular_prism': _('triangular prism'),
    'quadrangular_prism': _('quadrangular prism'),
    'pentagonal_prism': _('pentagonal prism'),
    'triangular_pyramid': _('triangular pyramid'),
    'quadrangular_pyramid': _('quadrangular pyramid'),
    'pentagonal_pyramid': _('pentagonal pyramid'),
    'sphere': _('sphere'),
    'cylinder': _('cylinder'),
    'cone': _('cone'),
}

POLYHEDRON_FACES = {
    'cube': 6,
    'rectangular_prism': 6,
    'triangular_prism': 5,
    'quadrangular_prism': 6,
    'pentagonal_prism': 7,
    'triangular_pyramid': 4,
    'quadrangular_pyramid': 5,
    'pentagonal_pyramid': 6,
}

POLYHEDRON_EDGES = {
    'cube': 12,
    'rectangular_prism': 12,
    'triangular_prism': 9,
    'quadrangular_prism': 12,
    'pentagonal_prism': 15,
    'triangular_pyramid': 6,
    'quadrangular_pyramid': 8,
    'pentagonal_pyramid': 10,
}

POLYHEDRON_VERTICES = {
    'cube': 8,
    'rectangular_prism': 8,
    'triangular_prism': 6,
    'quadrangular_prism': 8,
    'pentagonal_prism': 10,
    'triangular_pyramid': 4,
    'quadrangular_pyramid': 5,
    'pentagonal_pyramid': 6,
}

SPECIAL_CASE_POLYGONS = {
    'equilateral_triangle': _('equilateral triangle'),
    'isosceles': _('isosceles triangle'),
    'scalene': _('scalene triangle'),
    'right_triangle': _('right triangle'),
    'square': _('square'),
    'rectangle': _('rectangle'),
    'rhombus': _('rhombus'),
    'trapezoid': _('trapezoid'),
    'parallelogram': _('parallelogram'),
}
