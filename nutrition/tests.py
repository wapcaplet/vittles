from django.test import TestCase
from vittles.core.models import Unit, Equivalence, Food
from vittles.nutrition.models import NutritionInfo

class NutritionTest (TestCase):
    """Initialization shared by all test cases
    """
    def setUp(self):
        self.gram = Unit.get(name='gram')
        self.kilogram = Unit.get(name='kilogram')
        kilograms_to_grams = Equivalence.get(
            unit=self.kilogram,
            to_quantity=1000,
            to_unit=self.gram,
        )


class NutritionInfoTest (NutritionTest):
    def assert_nutrition_info_equals(self, nutrition_info, **attrs):
        for name, value in attrs.iteritems():
            self.assertEqual(nutrition_info.__getattribute__(name), value)


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

        one_kilo = nutrition.for_amount(1.0, self.kilogram)
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

        five_grams = nutrition.for_amount(5.0, self.gram)
        self.assert_nutrition_info_equals(
            five_grams,
            serving_size = 5.0,
            serving_unit = self.gram,
            calories     = 50,
            fat_calories = 40,
            fat          = 25,
            carb         = 10,
            sodium       = 5,
            protein      = 2.5,
            cholesterol  = 0,
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
        # object with a quantity of 1, and 0 for all other fields.
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

