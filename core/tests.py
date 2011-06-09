from django.test import TestCase
from vittles.core.models import Food, Unit, Equivalence, FoodNutritionInfo
from vittles.core.helpers import \
        NoEquivalence, convert_unit, to_grams, to_ml, convert_amount, add_amount, subtract_amount

class CoreTest (TestCase):
    """Initialization shared by all test cases
    """
    fixtures = [
        'test_food.yaml',
        'test_unit.yaml',
        'test_equivalence.yaml',
    ]


class ConvertUnitTest (CoreTest):
    def test_convert_unit(self):
        self.failUnlessEqual(convert_unit('pound', 'ounce'), 16)
        self.failUnlessEqual(convert_unit('ounce', 'pound'), 1.0 / 16)

    def test_convert_unit_without_equivalence(self):
        self.assertRaises(NoEquivalence, convert_unit, 'pound', 'quart')
        self.assertRaises(NoEquivalence, convert_unit, 'ounce', 'quart')


class ConvertDifferentUnitKindsTest (CoreTest):
    def test_convert_volume_to_grams(self):
        # Two foods with very different densities
        honey = Food.objects.get(name='honey')
        paprika = Food.objects.get(name='paprika')

        # Two units of volume
        ml = Unit.objects.get(name='milliliter')
        cup = Unit.objects.get(name='cup')
        ml_per_cup = Equivalence.objects.get(unit=cup, to_unit=ml).to_quantity

        # Convert units of volume into grams
        # Without food, assume 1.0 g/ml
        self.failUnlessEqual(to_grams(ml), 1.0)
        self.failUnlessEqual(to_grams(cup), 1.0 * ml_per_cup)
        # With food, use its density
        self.failUnlessEqual(to_grams(ml, honey), honey.grams_per_ml)
        self.failUnlessEqual(to_grams(ml, paprika), paprika.grams_per_ml)
        self.failUnlessEqual(to_grams(cup, honey), honey.grams_per_ml * ml_per_cup)
        self.failUnlessEqual(to_grams(cup, paprika), paprika.grams_per_ml * ml_per_cup)


    def test_convert_weight_to_ml(self):
        # Two foods with very different densities
        honey = Food.objects.get(name='honey')
        paprika = Food.objects.get(name='paprika')
        # Two units of weight
        gram = Unit.objects.get(name='gram')
        ounce = Unit.objects.get(name='ounce')
        g_per_oz = Equivalence.objects.get(unit=ounce, to_unit=gram).to_quantity

        # Convert units of weight into milliliters
        # Without food, assume 1.0 g/ml
        self.failUnlessEqual(to_ml(gram), 1.0)
        self.failUnlessEqual(to_ml(ounce), g_per_oz)
        # With food, use its density
        self.failUnlessEqual(to_ml(gram, honey), 1.0 / honey.grams_per_ml)
        self.failUnlessEqual(to_ml(gram, paprika), 1.0 / paprika.grams_per_ml)
        self.failUnlessEqual(to_ml(ounce, honey), g_per_oz / honey.grams_per_ml)
        self.failUnlessEqual(to_ml(ounce, paprika), g_per_oz / paprika.grams_per_ml)


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
        self.gram = Unit.objects.get(name='gram')
        self.kilogram = Unit.objects.get(name='kilogram')


    def assert_nutrition_info_equals(self, nutrition_info, **attrs):
        """Assert that the given `NutritionInfo` has attributes matching `attrs`.
        """
        for name, expect in attrs.iteritems():
            actual = nutrition_info.__getattribute__(name)
            self.assertEqual(nutrition_info.__getattribute__(name), expect,
                            "Expected %s == %s, got %s instead" % (name, expect, actual))


    def test_normalize_nutrition_info(self):
        butter = Food.objects.get(name='butter')
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


    def test_convert_nutrition_info(self):
        butter = Food.objects.get(name='butter')
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
        butter = Food.objects.get(name='butter')
        cup = Unit.objects.get(name='cup')
        ml = Unit.objects.get(name='milliliter')
        ml_per_cup = Equivalence.objects.get(unit=cup, to_unit=ml).to_quantity

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
        target_grams = butter.grams_per_ml * ml_per_cup
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
        peanut_butter = Food.objects.get(name='peanut butter')
        tbs = Unit.objects.get(name='tablespoon')
        ml = Unit.objects.get(name='milliliter')
        ml_per_tbs = Equivalence.objects.get(unit=tbs, to_unit=ml).to_quantity

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

        # 14.8 ml/tbs, 0.76 g/ml, 2.0 tbs/serving
        gram_serving = 1.0 / (ml_per_tbs * peanut_butter.grams_per_ml * 2.0)
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



from vittles.core.utils import \
        float_to_fraction, fraction_to_float, pluralize, format_food_unit

__test__ = {
    'float_to_fraction': float_to_fraction,
    'fraction_to_float': fraction_to_float,
    'format_food_unit': format_food_unit,
    'pluralize': pluralize,
}

