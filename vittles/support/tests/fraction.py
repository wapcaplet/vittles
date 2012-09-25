from django.test import TestCase
from support.utils import fraction_to_float, float_to_fraction

class FractionTest (TestCase):
    def setUp(self):
        self.less_than_one = [
            ('1/2', 0.5),
            ('1/3', 0.33),
            ('1/4', 0.25),
            ('1/8', 0.125),
            ('1/10', 0.1),
        ]
        self.greater_than_one = [
            ('1-1/4', 1.25),
            ('2-3/4', 2.75),
            ('9-1/3', 9.33),
        ]

    def test_float_to_fraction_lt_one(self):
        """Convert floats < 1.0 into simple fraction strings."""
        for fraction, float in self.less_than_one:
            self.assertEqual(float_to_fraction(float), fraction)

    def test_float_to_fraction_gt_one(self):
        """Convert floats > 1.0 into mixed fraction strings."""
        for fraction, float in self.greater_than_one:
            self.assertEqual(float_to_fraction(float), fraction)

    def test_float_to_fraction_whole_number(self):
        """Convert whole-number floats into simple integer strings."""
        whole_numbers = [
            ('1', 1.0),
            ('2', 2.0),
            ('3', 3.0),
        ]
        for fraction, float in whole_numbers:
            self.assertEqual(float_to_fraction(float), fraction)


    def test_fraction_to_float_lt_one(self):
        """Convert fraction strings < 1.0 into floats."""
        for fraction, float in self.less_than_one:
            self.assertAlmostEqual(fraction_to_float(fraction), float, 2)

    def test_fraction_to_float_gt_one(self):
        """Convert fraction strings > 1.0 into floats."""
        for fraction, float in self.greater_than_one:
            self.assertAlmostEqual(fraction_to_float(fraction), float, 2)

    def test_fraction_to_float_whole_number(self):
        """Convert fraction strings equalling whole numbers into floats."""
        whole_numbers = [
            ('1/1', 1.0),
            ('3/3', 1.0),
            ('2/1', 2.0),
            ('6/2', 3.0),
            ('12/4', 3.0),
        ]
        for fraction, float in whole_numbers:
            self.assertAlmostEqual(fraction_to_float(fraction), float, 2)

    def test_float_to_fraction_denominators(self):
        """Convert floats into fraction strings with limit on denominator."""
        self.assertEqual(float_to_fraction(0.1875, 16), '3/16')
        self.assertEqual(float_to_fraction(0.1875, 8), '1/5')
        self.assertEqual(float_to_fraction(0.1875, 4), '1/4')

