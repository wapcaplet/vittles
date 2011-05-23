from django.test import TestCase
from core.models import Unit, Equivalence
from core.helpers import convert_amount, add_amount, subtract_amount, NoEquivalence

class CoreTest (TestCase):
    """Initialization shared by all test cases
    """
    def setUp(self):
        ounce = Unit.get(name='ounce')
        pound = Unit.get(name='pound')
        self.pound_to_ounces = Equivalence.get(
            unit=pound,
            to_quantity=16.0,
            to_unit=ounce,
        )


class ConvertAmountTest (CoreTest):
    def test_direct_equivalence_conversion(self):
        pound = Unit.get(name='pound')
        ounce = Unit.get(name='ounce')
        self.failUnlessEqual(convert_amount(2, pound, ounce), 32.0)


    def test_reverse_equivalence_conversion(self):
        pound = Unit.get(name='pound')
        ounce = Unit.get(name='ounce')
        self.failUnlessEqual(convert_amount(4, ounce, pound), 0.25)


    def test_convert_units_without_equivalence(self):
        pound = Unit.get(name='pound')
        quart = Unit.get(name='quart')
        self.assertRaises(NoEquivalence, convert_amount, 2, pound, quart)


class AddAmountTest (CoreTest):
    def test_add_same_units(self):
        pound = Unit.get(name='pound')
        ounce = Unit.get(name='ounce')
        # Results in pounds
        self.failUnlessEqual(add_amount(2.0, pound, 0.5, pound), 2.5)
        self.failUnlessEqual(add_amount(0.5, pound, 2.0, pound), 2.5)
        # Results in ounces
        self.failUnlessEqual(add_amount(12.0, ounce, 4.0, ounce), 16.0)
        self.failUnlessEqual(add_amount(4.0, ounce, 12.0, ounce), 16.0)


    def test_add_different_units(self):
        pound = Unit.get(name='pound')
        ounce = Unit.get(name='ounce')
        # Results in pounds
        self.failUnlessEqual(add_amount(2, pound, 4, ounce), 2.25)
        self.failUnlessEqual(add_amount(2, pound, 12, ounce), 2.75)
        self.failUnlessEqual(add_amount(0.5, pound, 4, ounce), 0.75)
        self.failUnlessEqual(add_amount(0.5, pound, 12, ounce), 1.25)
        # Results in ounces
        self.failUnlessEqual(add_amount(4, ounce, 2, pound), 36.0)
        self.failUnlessEqual(add_amount(12, ounce, 2, pound), 44.0)
        self.failUnlessEqual(add_amount(4, ounce, 0.5, pound), 12.0)
        self.failUnlessEqual(add_amount(12, ounce, 0.5, pound), 20.0)


    def test_add_units_without_equivalence(self):
        pound = Unit.get(name='pound')
        quart  = Unit.get(name='quart')
        self.assertRaises(NoEquivalence, add_amount, 2.0, pound, 3.0, quart)


class SubtractAmountTest (CoreTest):
    def test_subtract_same_units(self):
        pound = Unit.get(name='pound')
        ounce = Unit.get(name='ounce')
        # Results in pounds
        self.failUnlessEqual(subtract_amount(2, pound, 0.5, pound), 1.5)
        # Results in ounces
        self.failUnlessEqual(subtract_amount(12, ounce, 4, ounce), 8.0)


    def test_subtract_different_units(self):
        pound = Unit.get(name='pound')
        ounce = Unit.get(name='ounce')
        # Results in pounds
        self.failUnlessEqual(subtract_amount(2, pound, 4, ounce), 1.75)
        self.failUnlessEqual(subtract_amount(2, pound, 12, ounce), 1.25)
        self.failUnlessEqual(subtract_amount(0.5, pound, 4, ounce), 0.25)
        # Results in ounces
        self.failUnlessEqual(subtract_amount(12, ounce, 0.5, pound), 4.0)


    def test_subtract_units_without_equivalence(self):
        pound = Unit.get(name='pound')
        quart = Unit.get(name='quart')
        self.assertRaises(NoEquivalence, subtract_amount, 2.0, pound, 3.0, quart)


from helpers import float_to_fraction, fraction_to_float, format_food_unit

__test__ = {
    'float_to_fraction': float_to_fraction,
    'fraction_to_float': fraction_to_float,
    'format_food_unit': format_food_unit,
}

