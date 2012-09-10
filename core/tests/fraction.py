from django.test import TestCase
from core.utils import fraction_to_float, float_to_fraction

class InflectionTest (TestCase):
    def setUp(self):
        self.quantities = [
            ('1/2', 0.5),
            ('1/3', 0.33),
            ('1/4', 0.25),
            ('1/8', 0.125),
            ('1/10', 0.1),

            ('1-1/4', 1.25),
            ('2-3/4', 2.75),
            ('9-1/3', 9.33),
        ]

    def test_float_to_fraction(self):
        """Convert floats into fractions."""
        for fraction, float in self.quantities:
            self.assertEqual(float_to_fraction(float), fraction)

    def test_fraction_to_float(self):
        """Convert fractions into floats."""
        for fraction, float in self.quantities:
            self.assertAlmostEqual(fraction_to_float(fraction), float, 2)

    def test_float_to_fraction_precision(self):
        """Convert floats into fractions with custom precision."""
        self.assertEqual(float_to_fraction(0.1875, 16), '3/16')
        self.assertEqual(float_to_fraction(0.1875, 8), '1/5')
        self.assertEqual(float_to_fraction(0.1875, 4), '1/4')

