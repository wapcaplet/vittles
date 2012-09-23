from django.test import TestCase
from nutrition.models import Nutrition

class NutritionOtherTest (TestCase):
    def test_nutrition_is_empty(self):
        """Check if Nutrition is empty.
        """
        empty_nutrient = Nutrition(
            calories     = 0,
            fat_calories = 0,
            fat          = 0,
            carb         = 0,
            sodium       = 0,
            protein      = 0,
            cholesterol  = 0,
        )
        self.assertTrue(empty_nutrient.is_empty())

        non_empty_nutrient = Nutrition(
            calories     = 0,
            fat_calories = 0,
            fat          = 0,
            carb         = 0,
            sodium       = 10,
            protein      = 0,
            cholesterol  = 0,
        )
        self.assertFalse(non_empty_nutrient.is_empty())

