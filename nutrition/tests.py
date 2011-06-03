from django.test import TestCase
from core.models import Unit, Equivalence, Food
from nutrition.models import NutritionInfo

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


    #def test_unknown_nutrition_info(self):
        #unknown_nutrition = NutritionInfo.undefined()
        #self.assertFalse(unknown_nutrition.is_defined())


