from django.test import TestCase
from core.helpers import NoEquivalence, add_amount, subtract_amount

class AmountTest (TestCase):
    fixtures = ['test_unit', 'test_food', 'test_equivalence']

class AddAmountTest (AmountTest):
    """Test adding two amounts together.
    """
    def test_add_same_units(self):
        """Add two amounts having the same units.
        """
        # Results in pounds
        self.failUnlessEqual(add_amount(2.0, 'pound', 0.5, 'pound'), 2.5)
        self.failUnlessEqual(add_amount(0.5, 'pound', 2.0, 'pound'), 2.5)
        # Results in ounces
        self.failUnlessEqual(add_amount(12.0, 'ounce', 4.0, 'ounce'), 16.0)
        self.failUnlessEqual(add_amount(4.0, 'ounce', 12.0, 'ounce'), 16.0)


    def test_add_different_units(self):
        """Add two amounts having different units.
        """
        # Results in pounds
        self.failUnlessEqual(add_amount(2, 'pound', 4, 'ounce'), 2.25)
        self.failUnlessEqual(add_amount(2, 'pound', 12, 'ounce'), 2.75)
        self.failUnlessEqual(add_amount(0.5, 'pound', 4, 'ounce'), 0.75)
        self.failUnlessEqual(add_amount(0.5, 'pound', 12, 'ounce'), 1.25)
        # Results in ounces
        self.failUnlessEqual(add_amount(4, 'ounce', 2, 'pound'), 36.0)
        self.failUnlessEqual(add_amount(12, 'ounce', 2, 'pound'), 44.0)
        self.failUnlessEqual(add_amount(4, 'ounce', 0.5, 'pound'), 12.0)
        self.failUnlessEqual(add_amount(12, 'ounce', 0.5, 'pound'), 20.0)


    def test_add_units_without_equivalence(self):
        """NoEquivalence when adding amounts with different units.
        """
        self.assertRaises(NoEquivalence, add_amount, 2.0, 'pound', 3.0, 'quart')


class SubtractAmountTest (AmountTest):
    """Test subtracting one amount from another.
    """
    def test_subtract_same_units(self):
        """Subtract amounts having the same units.
        """
        # Results in pounds
        self.failUnlessEqual(subtract_amount(2, 'pound', 0.5, 'pound'), 1.5)
        # Results in ounces
        self.failUnlessEqual(subtract_amount(12, 'ounce', 4, 'ounce'), 8.0)


    def test_subtract_different_units(self):
        """Subtract amounts having different units.
        """
        # Results in pounds
        self.failUnlessEqual(subtract_amount(2, 'pound', 4, 'ounce'), 1.75)
        self.failUnlessEqual(subtract_amount(2, 'pound', 12, 'ounce'), 1.25)
        self.failUnlessEqual(subtract_amount(0.5, 'pound', 4, 'ounce'), 0.25)
        # Results in ounces
        self.failUnlessEqual(subtract_amount(12, 'ounce', 0.5, 'pound'), 4.0)


    def test_subtract_units_without_equivalence(self):
        """NoEquivalence subtracting amounts with different units.
        """
        self.assertRaises(NoEquivalence, subtract_amount, 2.0, 'pound', 3.0, 'quart')



