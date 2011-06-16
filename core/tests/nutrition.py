from django.test import TestCase
from core.models import Food, Unit, Equivalence, FoodNutritionInfo

class FoodNutritionTest (TestCase):
    """Test operations related to FoodNutritionInfo.
    """
    fixtures = ['test_unit', 'test_food', 'test_equivalence']
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



