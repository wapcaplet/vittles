from django.test import TestCase
from core.models import Food, Unit, Equivalence, FoodNutritionInfo

class FoodNutritionTest (TestCase):
    """Test operations related to FoodNutritionInfo.
    """
    fixtures = ['test_unit', 'test_food', 'test_equivalence']

    def test_normalize_nutrition_info(self):
        gram = Unit.objects.get(name='gram')
        butter = Food.objects.get(name='butter')
        butter_nutrition = FoodNutritionInfo(
            food         = butter,
            quantity     = 14.0,
            unit         = gram,
            calories     = 100,
            fat_calories = 100,
            fat          = 11,
            carb         = 0,
            sodium       = 90,
            protein      = 0,
            cholesterol  = 30,
        )

        butter_nutrition.normalize()
        expected_total = FoodNutritionInfo(
            food         = butter,
            quantity     = 1.0,
            unit         = gram,
            calories     = 7.14,
            fat_calories = 7.14,
            fat          = 0.79,
            carb         = 0.0,
            sodium       = 6.43,
            protein      = 0.0,
            cholesterol  = 2.14,
        )
        self.assertTrue(butter_nutrition.is_equal(expected_total))


    def test_convert_nutrition_info(self):
        gram = Unit.objects.get(name='gram')
        kilogram = Unit.objects.get(name='kilogram')
        butter = Food.objects.get(name='butter')
        ten_grams_butter = FoodNutritionInfo(
            quantity     = 10,
            unit         = gram,
            food         = butter,
            calories     = 100,
            fat_calories = 80,
            fat          = 50,
            carb         = 20,
            sodium       = 10,
            protein      = 5,
            cholesterol  = 0,
        )

        one_kilo_butter = ten_grams_butter.for_amount(1, kilogram)
        expected_total = FoodNutritionInfo(
            quantity     = 1.0,
            unit         = kilogram,
            food         = butter,
            calories     = 10000,
            fat_calories = 8000,
            fat          = 5000,
            carb         = 2000,
            sodium       = 1000,
            protein      = 500,
            cholesterol  = 0,
        )
        self.assertTrue(one_kilo_butter.is_equal(expected_total))

        five_grams_butter = ten_grams_butter.for_amount(5, gram)
        expected_total = FoodNutritionInfo(
            quantity     = 5,
            unit         = gram,
            food         = butter,
            calories     = 50,
            fat_calories = 40,
            fat          = 25,
            carb         = 10,
            sodium       = 5,
            protein      = 2.5,
            cholesterol  = 0,
        )
        self.assertTrue(five_grams_butter.is_equal(expected_total))


    def test_convert_nutrition_info_weight_to_volume(self):
        # Test data
        gram = Unit.objects.get(name='gram')
        butter = Food.objects.get(name='butter')
        cup = Unit.objects.get(name='cup')
        ml = Unit.objects.get(name='milliliter')
        ml_per_cup = Equivalence.objects.get(unit=cup, to_unit=ml).to_quantity

        butter_nutrition = FoodNutritionInfo(
            food         = butter,
            quantity     = 14.0,
            unit         = gram,
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
        expected_total = FoodNutritionInfo(
            quantity     = 1.0,
            unit         = cup,
            food         = butter,
            calories     = servings_per_cup * 100,
            fat_calories = servings_per_cup * 100,
            fat          = servings_per_cup * 11,
            carb         = servings_per_cup * 0,
            sodium       = servings_per_cup * 90,
            protein      = servings_per_cup * 0,
            cholesterol  = servings_per_cup * 30,
        )
        self.assertTrue(butter_nutrition_cup.is_equal(expected_total))


    def test_convert_nutrition_info_volume_to_weight(self):
        kilogram = Unit.objects.get(name='kilogram')
        tbs = Unit.objects.get(name='tablespoon')
        ml = Unit.objects.get(name='milliliter')
        ml_per_tbs = Equivalence.objects.get(unit=tbs, to_unit=ml).to_quantity
        peanut_butter = Food.objects.get(name='peanut butter')

        two_tbs_peanut_butter = FoodNutritionInfo(
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

        one_kilo_peanut_butter = two_tbs_peanut_butter.for_amount(1, kilogram)
        expected_total = FoodNutritionInfo(
            quantity     = 1.0,
            unit         = kilogram,
            food         = peanut_butter,
            calories     = servings_per_kg * 180,
            fat_calories = servings_per_kg * 110,
            fat          = servings_per_kg * 12,
            carb         = servings_per_kg * 12,
            sodium       = servings_per_kg * 110,
            protein      = servings_per_kg * 7,
            cholesterol  = servings_per_kg * 0,
        )
        self.assertTrue(one_kilo_peanut_butter.is_equal(expected_total))



