from django.test import TestCase
from vittles.core.models import Unit, Equivalence, Food
from vittles.nutrition.models import NutritionInfo

class NutritionTest (TestCase):
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


class NutritionInfoTest (NutritionTest):
    def assert_nutrition_info_equals(self, nutrition_info, **attrs):
        """Assert that the given `NutritionInfo` has attributes matching `attrs`.
        """
        for name, expect in attrs.iteritems():
            actual = nutrition_info.__getattribute__(name)
            self.assertEqual(nutrition_info.__getattribute__(name), expect,
                            "Expected %s == %s, got %s instead" % (name, expect, actual))


    def test_convert_nutrition_info(self):
        nutrition = NutritionInfo(
            serving_size = 10,
            serving_unit = self.gram,
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
            serving_size = 1.0,
            serving_unit = self.kilogram,
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
            serving_size = 5,
            serving_unit = self.gram,
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
        butter_nutrition = NutritionInfo(
            food         = butter,
            serving_size = 14.0,
            serving_unit = self.gram,
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
            serving_size = 1.0,
            serving_unit = cup,
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
        peanut_butter_nutrition = NutritionInfo(
            food         = peanut_butter,
            serving_size = 2.0,
            serving_unit = tbs,
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
            serving_size = 1.0,
            serving_unit = self.kilogram,
            calories     = servings_per_kg * 180,
            fat_calories = servings_per_kg * 110,
            fat          = servings_per_kg * 12,
            carb         = servings_per_kg * 12,
            sodium       = servings_per_kg * 110,
            protein      = servings_per_kg * 7,
            cholesterol  = servings_per_kg * 0,
        )


    def test_add_nutrition_info(self):
        nutrient_a = NutritionInfo(
            calories     = 50,
            fat_calories = 20,
            fat          = 5,
            carb         = 3,
            sodium       = 10,
            protein      = 0,
            cholesterol  = 40,
        )

        nutrient_b = NutritionInfo(
            calories     = 40,
            fat_calories = 30,
            fat          = 10,
            carb         = 0,
            sodium       = 30,
            protein      = 0,
            cholesterol  = 5,
        )

        nutrient_total = nutrient_a + nutrient_b
        self.assert_nutrition_info_equals(
            nutrient_total,
            calories     = 90,
            fat_calories = 50,
            fat          = 15,
            carb         = 3,
            sodium       = 40,
            protein      = 0,
            cholesterol  = 45,
        )


    def test_unknown_nutrition_info(self):
        # Any food with an unknown nutritional value returns a NutritionInfo
        # object with a quantity of 0
        meat = Food.get(name='mystery meat')
        nutrition = NutritionInfo.get(food=meat)
        self.assert_nutrition_info_equals(
            nutrition,
            serving_size = 1,
            serving_unit = None,
            calories     = 0,
            fat_calories = 0,
            fat          = 0,
            carb         = 0,
            sodium       = 0,
            protein      = 0,
            cholesterol  = 0,
        )

