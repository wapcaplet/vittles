from django.test import TestCase
from core.models import Unit, Food, FoodNutritionInfo
from cookbook.models import Recipe, Ingredient

class CookbookTest (TestCase):
    """Initialization shared by all test cases
    """
    def setUp(self):
        # Units
        self.cup = Unit.get(name='cup')
        self.ounce = Unit.get(name='ounce')

        # Foods
        self.egg = Food.get(name='egg')
        self.flour = Food.get(name='flour')
        self.butter = Food.get(name='butter')

        # Nutrition Infos
        self.egg_nutrition, created = FoodNutritionInfo.objects.get_or_create(
            food         = self.egg,
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
        self.flour_nutrition, created = FoodNutritionInfo.objects.get_or_create(
            food         = self.flour,
            quantity     = 1,
            unit         = self.cup,
            calories     = 400,
            fat_calories = 0,
            fat          = 0,
            carb         = 88,
            sodium       = 0,
            protein      = 12,
            cholesterol  = 0,
        )

        self.flour_nutrition, created = FoodNutritionInfo.objects.get_or_create(
            food         = self.butter,
            quantity     = 1,
            unit         = self.ounce,
            calories     = 200,
            fat_calories = 200,
            fat          = 22,
            carb         = 0,
            sodium       = 180,
            protein      = 0,
            cholesterol  = 60,
        )


    def assert_nutrition_info_equals(self, nutrition_info, **attrs):
        """Assert that the given `NutritionInfo` has attributes matching `attrs`.
        """
        for name, expect in attrs.iteritems():
            actual = nutrition_info.__getattribute__(name)
            self.assertEqual(nutrition_info.__getattribute__(name), expect,
                            "Expected %s == %s, got %s instead" % (name, expect, actual))


class RecipeTest (CookbookTest):
    def test_recipe_nutrition_info(self):
        pancakes = Recipe.get(name='Pancakes')
        pancakes.ingredients.create(quantity=1, food=self.egg)
        pancakes.ingredients.create(quantity=1, unit=self.cup, food=self.flour)
        pancakes.save()

        self.assert_nutrition_info_equals(
            pancakes.nutrition_info,
            calories     = 472,
            fat_calories = 20,
            fat          = 4.8,
            carb         = 88.4,
            sodium       = 71,
            protein      = 18.3,
            cholesterol  = 186,
        )

    def test_recipe_nutrition_info_recalculate(self):
        pancakes = Recipe.get(name='Pancakes')
        pancakes.ingredients.create(quantity=1, food=self.egg)
        pancakes.ingredients.create(quantity=1, unit=self.cup, food=self.flour)
        pancakes.save()

        # Before recalculation
        self.assert_nutrition_info_equals(
            pancakes.nutrition_info,
            calories     = 472,
            fat_calories = 20,
            fat          = 4.8,
            carb         = 88.4,
            sodium       = 71,
            protein      = 18.3,
            cholesterol  = 186,
        )

        # Add 1 oz. butter to recipe
        pancakes.ingredients.create(quantity=1, unit=self.ounce, food=self.butter)
        pancakes.save()

        self.assert_nutrition_info_equals(
            pancakes.nutrition_info,
            calories     = 672,
            fat_calories = 220,
            fat          = 26.8,
            carb         = 88.4,
            sodium       = 251,
            protein      = 18.3,
            cholesterol  = 246,
        )

