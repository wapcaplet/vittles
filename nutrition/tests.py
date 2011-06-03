from django.test import TestCase
from nutrition.models import NutritionInfo


class NutritionInfoTest (TestCase):
    def assert_nutrition_info_equals(self, nutrition_info, **attrs):
        """Assert that the given `NutritionInfo` has attributes matching `attrs`.
        """
        for name, expect in attrs.iteritems():
            actual = nutrition_info.__getattribute__(name)
            self.assertEqual(nutrition_info.__getattribute__(name), expect,
                            "Expected %s == %s, got %s instead" % (name, expect, actual))


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

        self.assert_nutrition_info_equals(
            nutrient * 2.0,
            calories     = 100,
            fat_calories = 40,
            fat          = 10,
            carb         = 6,
            sodium       = 20,
            protein      = 0,
            cholesterol  = 80,
        )

        self.assert_nutrition_info_equals(
            nutrient * 0.5,
            calories     = 25,
            fat_calories = 10,
            fat          = 2.5,
            carb         = 1.5,
            sodium       = 5,
            protein      = 0,
            cholesterol  = 20,
        )


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
        self.assert_nutrition_info_equals(
            nutrient_b,
            calories     = 50,
            fat_calories = 20,
            fat          = 5,
            carb         = 3,
            sodium       = 10,
            protein      = 0,
            cholesterol  = 40,
        )

