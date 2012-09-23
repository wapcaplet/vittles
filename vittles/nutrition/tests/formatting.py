from django.test import TestCase
from nutrition.models import Nutrition

class NutritionStringTest (TestCase):
    def test_nutrition_string(self):
        """Format Nutrition as a string.
        """
        nutrient = Nutrition(
            calories     = 50,
            fat_calories = 20,
            fat          = 5,
            carb         = 3,
            sodium       = 10,
            protein      = 0,
            cholesterol  = 40,
        )
        self.assertEqual(str(nutrient), '50 calories')

        self.assertEqual(nutrient.full_string(),
            "50 calories (20 from fat) 5g fat, 3g carbs, 10mg sodium, 0g protein, 40mg cholesterol")

