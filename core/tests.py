from django.test import TestCase
from core.models import Unit, Equivalence, Amount, NoEquivalence

class ConversionTest (TestCase):
    def setUp(self):
        self.ounce = Unit.get(name='ounce')
        self.pound = Unit.get(name='pound')
        self.pound_to_ounces = Equivalence.get(
            unit=self.pound,
            to_quantity=16.0,
            to_unit=self.ounce,
        )
        self.two_pounds = Amount.get(quantity=2.0, unit=self.pound)
        self.four_ounces = Amount.get(quantity=4.0, unit=self.ounce)


    def test_pounds_to_ounces(self):
        """Convert a quantity when there is a direct equivalence.
        """
        ounces = self.two_pounds.convert(self.ounce)
        self.failUnlessEqual(ounces, 32.0)


    def test_ounces_to_pounds(self):
        """Convert a quantity when there is a reverse equivalence.
        """
        pounds = self.four_ounces.convert(self.pound)
        self.failUnlessEqual(pounds, 0.25)


    def test_missing_equivalence(self):
        """Raise an exception when no equivalence mapping is found.
        """
        quart = Unit.get(name='quart')
        self.assertRaises(NoEquivalence, self.two_pounds.convert, quart)


class AddAmountTest (TestCase):
    def setUp(self):
        self.ounce = Unit.get(name='ounce')
        self.pound = Unit.get(name='pound')
        self.pound_to_ounces = Equivalence.get(
            unit=self.pound,
            to_quantity=16.0,
            to_unit=self.ounce,
        )
        self.half_pound = Amount.get(quantity=0.5, unit=self.pound)
        self.two_pounds = Amount.get(quantity=2.0, unit=self.pound)
        self.four_ounces = Amount.get(quantity=4.0, unit=self.ounce)
        self.eight_ounces = Amount.get(quantity=8.0, unit=self.ounce)
        self.twelve_ounces = Amount.get(quantity=12.0, unit=self.ounce)


    def test_add_same_units(self):
        """Add two Amounts in the same units.
        """
        # Results in pounds
        self.failUnlessEqual(
            (self.two_pounds + self.half_pound).quantity, 2.5)
        self.failUnlessEqual(
            (self.half_pound + self.two_pounds).quantity, 2.5)
        # Results in ounces
        self.failUnlessEqual(
            (self.twelve_ounces + self.four_ounces).quantity, 16.0)
        self.failUnlessEqual(
            (self.four_ounces + self.twelve_ounces).quantity, 16.0)


    def test_subtract_same_units(self):
        """Subtract two Amounts in the same units.
        """
        # Results in pounds
        self.failUnlessEqual(
            (self.two_pounds - self.half_pound).quantity, 1.5)
        # Results in ounces
        self.failUnlessEqual(
            (self.twelve_ounces - self.four_ounces).quantity, 8.0)


    def test_add_different_units(self):
        """Add two Amounts in different units.
        """
        # Results in pounds
        self.failUnlessEqual(
            (self.two_pounds + self.four_ounces).quantity, 2.25)
        self.failUnlessEqual(
            (self.two_pounds + self.twelve_ounces).quantity, 2.75)
        self.failUnlessEqual(
            (self.half_pound + self.four_ounces).quantity, 0.75)
        self.failUnlessEqual(
            (self.half_pound + self.twelve_ounces).quantity, 1.25)
        # Results in ounces
        self.failUnlessEqual(
            (self.four_ounces + self.two_pounds).quantity, 36.0)
        self.failUnlessEqual(
            (self.twelve_ounces + self.two_pounds).quantity, 44.0)
        self.failUnlessEqual(
            (self.four_ounces + self.half_pound).quantity, 12.0)
        self.failUnlessEqual(
            (self.twelve_ounces + self.half_pound).quantity, 20.0)


    def test_subtract_different_units(self):
        """Subtract two Amounts in different units.
        """
        # Results in pounds
        self.failUnlessEqual(
            (self.two_pounds - self.four_ounces).quantity, 1.75)
        self.failUnlessEqual(
            (self.two_pounds - self.twelve_ounces).quantity, 1.25)
        self.failUnlessEqual(
            (self.half_pound - self.four_ounces).quantity, 0.25)
        # Results in ounces
        self.failUnlessEqual(
            (self.twelve_ounces - self.half_pound).quantity, 4.0)


    def test_multiply(self):
        """Multiply an Amount.
        """
        # Integer multiplier
        self.failUnlessEqual((self.two_pounds * 5).quantity, 10.0)
        self.failUnlessEqual((self.half_pound * 4).quantity, 2.0)
        self.failUnlessEqual((self.four_ounces * 3).quantity, 12.0)
        self.failUnlessEqual((self.twelve_ounces * 2).quantity, 24.0)
        # Fractional multiplier
        self.failUnlessEqual((self.two_pounds * 0.5).quantity, 1.0)
        self.failUnlessEqual((self.four_ounces * 0.1).quantity, 0.4)


    def test_equality_same_units(self):
        """Compare two Amounts in the same units for equality.
        """
        # Pounds
        self.assertTrue(self.two_pounds == self.two_pounds)
        self.assertTrue(self.half_pound == self.half_pound)
        self.assertTrue(self.four_ounces == self.four_ounces)
        self.assertTrue(self.twelve_ounces == self.twelve_ounces)
        # Ounces
        self.assertTrue(self.two_pounds != self.half_pound)
        self.assertTrue(self.half_pound != self.two_pounds)
        self.assertTrue(self.four_ounces != self.twelve_ounces)
        self.assertTrue(self.twelve_ounces != self.four_ounces)


    def test_equality_different_units(self):
        """Compare two Amounts in different units for equality.
        """
        self.assertTrue(self.half_pound == self.eight_ounces)
        self.assertTrue(self.eight_ounces == self.half_pound)

        self.assertTrue(self.half_pound != self.four_ounces)
        self.assertTrue(self.four_ounces != self.half_pound)


