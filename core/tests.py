from django.test import TestCase
from vittles.core.models import Food, Unit, Equivalence, FoodNutritionInfo
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

    def test_convert_volume_to_grams(self):
        # Without food, assume 1.0 g/ml
        self.failUnlessEqual(to_grams(self.ml), 1.0)
        self.failUnlessEqual(to_grams(self.cup), 1.0 * 236.6)
        # With food, use its density
        self.failUnlessEqual(to_grams(self.ml, self.syrup), 1.2)
        self.failUnlessEqual(to_grams(self.ml, self.powder), 0.5)
        self.failUnlessEqual(to_grams(self.cup, self.syrup), 1.2 * 236.6)
        self.failUnlessEqual(to_grams(self.cup, self.powder), 0.5 * 236.6)

    def test_convert_weight_to_ml(self):
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


class NutritionTest (CoreTest):
    """Initialization shared by all test cases
    """
    def setUp(self):
        self.gram = Unit.get(name='gram', kind='weight')
        self.kilogram = Unit.get(name='kilogram', kind='weight')
        kilograms_to_grams = Equivalence.get(
            unit=self.kilogram,
            to_quantity=1000,
            to_unit=self.gram,
        )

    def assert_nutrition_info_equals(self, nutrition_info, **attrs):
        """Assert that the given `NutritionInfo` has attributes matching `attrs`.
        """
        for name, expect in attrs.iteritems():
            actual = nutrition_info.__getattribute__(name)
            self.assertEqual(nutrition_info.__getattribute__(name), expect,
                            "Expected %s == %s, got %s instead" % (name, expect, actual))

    def test_convert_nutrition_info(self):
        butter = Food.get(name='butter', grams_per_ml=0.97)
        nutrition = FoodNutritionInfo(
            quantity     = 10,
            unit         = self.gram,
            food         = butter,
            calories     = 100,
            fat_calories = 80,
            fat          = 50,
            carb         = 20,
            sodium       = 10,
            protein      = 5,
            cholesterol  = 0,
        )

        one_kilo = nutrition.for_amount(1, self.kilogram)
        self.assert_nutrition_info_equals(
            one_kilo,
            quantity     = 1.0,
            unit         = self.kilogram,
            calories     = 10000,
            fat_calories = 8000,
            fat          = 5000,
            carb         = 2000,
            sodium       = 1000,
            protein      = 500,
            cholesterol  = 0,
        )

        five_grams = nutrition.for_amount(5, self.gram)
        self.assert_nutrition_info_equals(
            five_grams,
            quantity     = 5,
            unit         = self.gram,
            calories     = 50,
            fat_calories = 40,
            fat          = 25,
            carb         = 10,
            sodium       = 5,
            protein      = 2.5,
            cholesterol  = 0,
        )


    def test_convert_nutrition_info_weight_to_volume(self):
        # Test data
        butter = Food.get(name='butter', grams_per_ml=0.97)
        cup = Unit.get(name='cup', kind='volume')
        ml = Unit.get(name='milliliter', kind='volume')
        ml_per_cup = Equivalence.get(
            unit=cup,
            to_quantity=236.6,
            to_unit=ml,
        )
        butter_nutrition = FoodNutritionInfo(
            food         = butter,
            quantity     = 14.0,
            unit         = self.gram,
            calories     = 100,
            fat_calories = 100,
            fat          = 11,
            carb         = 0,
            sodium       = 90,
            protein      = 0,
            cholesterol  = 30,
        )

        # Multiplier for a 1-gram serving size
        gram_serving = 1.0 / (1.0 * 14.0)          # 14.0 g/serving
        # Number of grams in target amount
        target_grams = 0.97 * 236.6                # 0.97 g/ml, 236.6 g/cup
        # Expected nutrition multiplier for a 1-cup amount
        servings_per_cup = gram_serving * target_grams

        # Ensure the amount calculated matches the 1-cup amount
        butter_nutrition_cup = butter_nutrition.for_amount(1, cup)
        self.assert_nutrition_info_equals(
            butter_nutrition_cup,
            quantity     = 1.0,
            unit         = cup,
            calories     = servings_per_cup * 100,
            fat_calories = servings_per_cup * 100,
            fat          = servings_per_cup * 11,
            carb         = servings_per_cup * 0,
            sodium       = servings_per_cup * 90,
            protein      = servings_per_cup * 0,
            cholesterol  = servings_per_cup * 30,
        )


    def test_convert_nutrition_info_volume_to_weight(self):
        peanut_butter = Food.get(name='peanut butter', grams_per_ml=0.76)
        tbs = Unit.get(name='tablespoon', kind='volume')
        ml = Unit.get(name='milliliter', kind='volume')
        ml_per_tbs = Equivalence.get(
            unit=tbs,
            to_quantity=14.8,
            to_unit=ml,
        )
        peanut_butter_nutrition = FoodNutritionInfo(
            food         = peanut_butter,
            quantity     = 2.0,
            unit         = tbs,
            calories     = 180,
            fat_calories = 110,
            fat          = 12,
            carb         = 12,
            sodium       = 110,
            protein      = 7,
            cholesterol  = 0,
        )

        gram_serving = 1.0 / (14.8 * 0.76 * 2.0)   # 14.8 ml/tbs, 0.76 g/ml, 2.0 tbs/serving
        target_grams = 1000.0
        servings_per_kg = gram_serving * target_grams

        peanut_butter_nutrition_kg = peanut_butter_nutrition.for_amount(1, self.kilogram)
        self.assert_nutrition_info_equals(
            peanut_butter_nutrition_kg,
            quantity     = 1.0,
            unit         = self.kilogram,
            calories     = servings_per_kg * 180,
            fat_calories = servings_per_kg * 110,
            fat          = servings_per_kg * 12,
            carb         = servings_per_kg * 12,
            sodium       = servings_per_kg * 110,
            protein      = servings_per_kg * 7,
            cholesterol  = servings_per_kg * 0,
        )


    def test_normalize_nutrition_info(self):
        butter = Food.get(name='butter', grams_per_ml=0.97)
        butter_nutrition = FoodNutritionInfo(
            food         = butter,
            quantity     = 14.0,
            unit         = self.gram,
            calories     = 100,
            fat_calories = 100,
            fat          = 11,
            carb         = 0,
            sodium       = 90,
            protein      = 0,
            cholesterol  = 30,
        )

        butter_nutrition.normalize()
        self.assert_nutrition_info_equals(
            butter_nutrition,
            food         = butter,
            quantity     = 1.0,
            unit         = self.gram,
            calories     = 7.14,
            fat_calories = 7.14,
            fat          = 0.79,
            carb         = 0.0,
            sodium       = 6.43,
            protein      = 0.0,
            cholesterol  = 2.14,
        )




from vittles.core.utils import \
        float_to_fraction, fraction_to_float, pluralize, format_food_unit

__test__ = {
    'float_to_fraction': float_to_fraction,
    'fraction_to_float': fraction_to_float,
    'format_food_unit': format_food_unit,
    'pluralize': pluralize,
}

