from django.test import TestCase
from core.models import Unit, Equivalence, Food, FoodNutritionInfo
from nutrition.models import NutritionInfo
from cookbook.models import Recipe, Ingredient

class CookbookTest (TestCase):
    """Initialization shared by all test cases
    """
    def setUp(self):
        pass

    def assert_nutrition_info_equals(self, nutrition_info, **attrs):
        """Assert that the given `NutritionInfo` has attributes matching `attrs`.
        """
        for name, expect in attrs.iteritems():
            actual = nutrition_info.__getattribute__(name)
            self.assertEqual(nutrition_info.__getattribute__(name), expect,
                            "Expected %s == %s, got %s instead" % (name, expect, actual))


class RecipeTest (CookbookTest):
    def test_recipe_nutrition_info(self):
        # Units
        cup = Unit.get(name='cup')

        # Foods
        egg = Food.get(name='egg')
        flour = Food.get(name='flour')

        # Nutrition Infos
        egg_nutrition, created = FoodNutritionInfo.objects.get_or_create(
            food         = egg,
            quantity     = 1,
            unit         = None,
            calories     = 72,
            fat_calories = 20,
            fat          = 4.8,
            carb         = 0.4,
            sodium       = 71,
            protein      = 6.3,
            cholesterol  = 186,
        )
        flour_nutrition, created = FoodNutritionInfo.objects.get_or_create(
            food         = flour,
            quantity     = 1,
            unit         = cup,
            calories     = 400,
            fat_calories = 0,
            fat          = 0,
            carb         = 88,
            sodium       = 0,
            protein      = 12,
            cholesterol  = 0,
        )

        noodles = Recipe.get(name='Pancakes')
        noodles.ingredients.create(quantity=1, food=egg)
        noodles.ingredients.create(quantity=1, unit=cup, food=flour)
        noodles.save()

        self.assert_nutrition_info_equals(
            noodles.nutrition_info,
            calories     = 472,
            fat_calories = 20,
            fat          = 4.8,
            #carb         = 88.4,
            sodium       = 71,
            protein      = 18.3,
            cholesterol  = 186,
        )

