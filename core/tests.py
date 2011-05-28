from django.test import TestCase
from vittles.core.models import Food, Unit, Equivalence
from vittles.core.helpers import \
        NoEquivalence, convert_unit, to_grams, to_ml, convert_amount, add_amount, subtract_amount

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


class ConvertUnitTest (CoreTest):
    def test_convert_unit(self):
        self.failUnlessEqual(convert_unit('pound', 'ounce'), 16)
        self.failUnlessEqual(convert_unit('ounce', 'pound'), 1.0 / 16)

    def test_convert_unit_without_equivalence(self):
        self.assertRaises(NoEquivalence, convert_unit, 'pound', 'quart')
        self.assertRaises(NoEquivalence, convert_unit, 'ounce', 'quart')


class ConvertDifferentUnitKindsTest (CoreTest):
    def setUp(self):
        self.ml = Unit.get(name='milliliter', kind='volume')
        self.cup = Unit.get(name='cup', kind='volume')
        self.gram = Unit.get(name='gram', kind='weight')
        self.ounce = Unit.get(name='ounce', kind='weight')

        self.syrup = Food.get(name='syrup', grams_per_ml=1.2)
        self.powder = Food.get(name='powder', grams_per_ml=0.5)

        self.cup_to_ml = Equivalence.get(
            unit=self.cup,
            to_quantity=236.6,
            to_unit=self.ml,
        )
        self.ounce_to_gram = Equivalence.get(
            unit=self.ounce,
            to_quantity=28.35,
            to_unit=self.gram,
        )

    def test_convert_volume_to_weight(self):
        # Without food, assume 1.0 g/ml
        self.failUnlessEqual(to_grams(self.ml), 1.0)
        self.failUnlessEqual(to_grams(self.cup), 1.0 * 236.6)
        # With food, use its density
        self.failUnlessEqual(to_grams(self.ml, self.syrup), 1.2)
        self.failUnlessEqual(to_grams(self.ml, self.powder), 0.5)
        self.failUnlessEqual(to_grams(self.cup, self.syrup), 1.2 * 236.6)
        self.failUnlessEqual(to_grams(self.cup, self.powder), 0.5 * 236.6)

    def test_convert_weight_to_volume(self):
        # Without food, assume 1.0 g/ml
        self.failUnlessEqual(to_ml(self.gram), 1.0)
        self.failUnlessEqual(to_ml(self.ounce), 28.35)
        # With food, use its density
        self.failUnlessEqual(to_ml(self.gram, self.syrup), 1.0 / 1.2)
        self.failUnlessEqual(to_ml(self.gram, self.powder), 1.0 / 0.5)
        self.failUnlessEqual(to_ml(self.ounce, self.syrup), 28.35 / 1.2)
        self.failUnlessEqual(to_ml(self.ounce, self.powder), 28.35 / 0.5)


class ConvertAmountTest (CoreTest):
    def test_convert_amount(self):
        self.failUnlessEqual(convert_amount(2, 'pound', 'ounce'), 32)
        self.failUnlessEqual(convert_amount(4, 'ounce', 'pound'), 0.25)

    def test_convert_amount_without_equivalence(self):
        self.assertRaises(NoEquivalence, convert_amount, 2, 'pound', 'quart')
        self.assertRaises(NoEquivalence, convert_amount, 2, 'ounce', 'quart')


class AddAmountTest (CoreTest):
    def test_add_same_units(self):
        # Results in pounds
        self.failUnlessEqual(add_amount(2.0, 'pound', 0.5, 'pound'), 2.5)
        self.failUnlessEqual(add_amount(0.5, 'pound', 2.0, 'pound'), 2.5)
        # Results in ounces
        self.failUnlessEqual(add_amount(12.0, 'ounce', 4.0, 'ounce'), 16.0)
        self.failUnlessEqual(add_amount(4.0, 'ounce', 12.0, 'ounce'), 16.0)


    def test_add_different_units(self):
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
        self.assertRaises(NoEquivalence, add_amount, 2.0, 'pound', 3.0, 'quart')


class SubtractAmountTest (CoreTest):
    def test_subtract_same_units(self):
        # Results in pounds
        self.failUnlessEqual(subtract_amount(2, 'pound', 0.5, 'pound'), 1.5)
        # Results in ounces
        self.failUnlessEqual(subtract_amount(12, 'ounce', 4, 'ounce'), 8.0)


    def test_subtract_different_units(self):
        # Results in pounds
        self.failUnlessEqual(subtract_amount(2, 'pound', 4, 'ounce'), 1.75)
        self.failUnlessEqual(subtract_amount(2, 'pound', 12, 'ounce'), 1.25)
        self.failUnlessEqual(subtract_amount(0.5, 'pound', 4, 'ounce'), 0.25)
        # Results in ounces
        self.failUnlessEqual(subtract_amount(12, 'ounce', 0.5, 'pound'), 4.0)


    def test_subtract_units_without_equivalence(self):
        self.assertRaises(NoEquivalence, subtract_amount, 2.0, 'pound', 3.0, 'quart')


from vittles.core.utils import \
        float_to_fraction, fraction_to_float, pluralize, format_food_unit

__test__ = {
    'float_to_fraction': float_to_fraction,
    'fraction_to_float': fraction_to_float,
    'format_food_unit': format_food_unit,
    'pluralize': pluralize,
}

