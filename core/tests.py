from django.test import TestCase
from core.models import Unit, Equivalence, Amount, NoEquivalence

class ConversionTest (TestCase):
    def setUp(self):
        self.ounce = Unit.get(name='ounce')
        self.pound = Unit.get(name='pound')
        self.quart = Unit.get(name='quart')
        self.equiv = Equivalence.get(
            unit=self.pound,
            to_quantity=16.0,
            to_unit=self.ounce,
        )
        self.two_pounds = Amount.get(quantity=2.0, unit=self.pound)


    def test_pounds_to_ounces(self):
        """Correctly convert from one quantity to another.
        """
        ounces = self.two_pounds.convert(self.ounce)
        self.failUnlessEqual(ounces, 32.0)


    def test_missing_equivalence(self):
        """Raise an exception when no equivalence mapping is found.
        """
        self.assertRaises(NoEquivalence, self.two_pounds.convert, self.quart)


