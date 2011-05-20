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


