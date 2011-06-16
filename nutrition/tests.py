from django.test import TestCase
from nutrition.models import NutritionInfo


class NutritionInfoTest (TestCase):
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

        actual_total = nutrient_a + nutrient_b
        expected_total = NutritionInfo(
            calories     = 90,
            fat_calories = 50,
            fat          = 15,
            carb         = 3,
            sodium       = 40,
            protein      = 0,
            cholesterol  = 45,
        )
        self.assertTrue(actual_total.is_equal(expected_total))


    def test_multiply_nutrition_info(self):
        nutrient = NutritionInfo(
            calories     = 50,
            fat_calories = 20,
            fat          = 5,
            carb         = 3,
            sodium       = 10,
            protein      = 0,
            cholesterol  = 40,
        )

        actual_total = nutrient * 2.0
        expected_total = NutritionInfo(
            calories     = 100,
            fat_calories = 40,
            fat          = 10,
            carb         = 6,
            sodium       = 20,
            protein      = 0,
            cholesterol  = 80,
        )
        self.assertTrue(actual_total.is_equal(expected_total))


        actual_total = nutrient * 0.5
        expected_total = NutritionInfo(
            calories     = 25,
            fat_calories = 10,
            fat          = 2.5,
            carb         = 1.5,
            sodium       = 5,
            protein      = 0,
            cholesterol  = 20,
        )
        self.assertTrue(actual_total.is_equal(expected_total))


    def test_nutrition_info_set_equal(self):
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

        nutrient_b.set_equal(nutrient_a)
        expected_total = NutritionInfo(
            calories     = 50,
            fat_calories = 20,
            fat          = 5,
            carb         = 3,
            sodium       = 10,
            protein      = 0,
            cholesterol  = 40,
        )
        self.assertTrue(nutrient_b.is_equal(expected_total))

