from decimal import Decimal as D
from django.test import TestCase

from utils.templatetags.utils_extras import cut_zeros
from utils import intervals


class UnitTestCase(TestCase):
    """
    Utilitaries tests.
    """
    def test_cut_zeros_tag(self):
        """
        Tests the cut_zeros template tag returns proper results.
        """
        self.assertEqual(cut_zeros(D('1.0')), '1')
        self.assertEqual(cut_zeros(D('14.030000')), '14,03')
        self.assertEqual(cut_zeros(D('10.0')), '10')

    def test_fraction_one_dimension(self):
        """
        Tests the generation of a list of fractions until such limit.
        """
        limit = 6
        expected_terms = [
            '1/2',
            '1/3', '2/3',
            '1/4', '2/4', '3/4',
            '1/5', '2/5', '3/5', '4/5',
            '1/6', '2/6', '3/6', '4/6', '5/6',
        ]
        obtained_terms = intervals.generate_one_dimension_fractions(limit)
        joined_terms = ['/'.join([str(a), str(b)]) for a, b in obtained_terms]
        self.assertEqual(expected_terms, joined_terms)
