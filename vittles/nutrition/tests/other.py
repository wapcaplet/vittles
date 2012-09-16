from django.test import TestCase
from nutrition.models import NutritionInfo

class NutritionInfoOtherTest (TestCase):
    def test_nutrition_info_is_empty(self):
        """Check if NutritionInfo is empty.
        """
        empty_nutrient = NutritionInfo(
            calories     = 0,
            fat_calories = 0,
            fat          = 0,
            carb         = 0,
            sodium       = 0,
            protein      = 0,
            cholesterol  = 0,
        )
        self.assertTrue(empty_nutrient.is_empty())

        non_empty_nutrient = NutritionInfo(
            calories     = 0,
            fat_calories = 0,
            fat          = 0,
            carb         = 0,
            sodium       = 10,
            protein      = 0,
            cholesterol  = 0,
        )
        self.assertFalse(non_empty_nutrient.is_empty())

