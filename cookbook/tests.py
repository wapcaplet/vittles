from django.test import TestCase
from core.models import Unit, Food, FoodNutritionInfo
from cookbook.models import Recipe, Ingredient

class CookbookTest (TestCase):
    """Initialization shared by all test cases
    """
    fixtures = [
        'test_food.yaml',
        'test_unit.yaml',
        'test_equivalence.yaml',
    ]

    def setUp(self):
        # Units
        self.cup = Unit.objects.get(name='cup')
        self.ounce = Unit.objects.get(name='ounce')

        # Foods
        self.egg = Food.objects.get(name='egg')
        self.flour = Food.objects.get(name='all-purpose flour')
        self.butter = Food.objects.get(name='butter')

        # Nutrition Infos
        self.egg_nutrition_info, created = FoodNutritionInfo.objects.get_or_create(
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
        self.flour_nutrition_info, created = FoodNutritionInfo.objects.get_or_create(
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

        self.butter_nutrition_info, created = FoodNutritionInfo.objects.get_or_create(
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


class IngredientNutritionTest (CookbookTest):
    def test_ingredient_nutrition_info_recalculation(self):
        pancakes = Recipe.get(name='Pancakes')
        eggs = Ingredient(
            recipe   = pancakes,
            quantity = 2,
            food     = self.egg,
        )
        eggs.save()

        egg = self.egg_nutrition_info

        # Before recalculation
        self.assert_nutrition_info_equals(
            eggs.nutrition_info,
            calories     = 2 * egg.calories,
            fat_calories = 2 * egg.fat_calories,
            fat          = 2 * egg.fat,
            carb         = 2 * egg.carb,
            sodium       = 2 * egg.sodium,
            protein      = 2 * egg.protein,
            cholesterol  = 2 * egg.cholesterol,
        )

        # Add another egg
        eggs.quantity = 3
        eggs.save()

        # Ensure nutrition reflects 3 eggs now
        self.assert_nutrition_info_equals(
            eggs.nutrition_info,
            calories     = 3 * egg.calories,
            fat_calories = 3 * egg.fat_calories,
            fat          = 3 * egg.fat,
            carb         = 3 * egg.carb,
            sodium       = 3 * egg.sodium,
            protein      = 3 * egg.protein,
            cholesterol  = 3 * egg.cholesterol,
        )


class RecipeTest (CookbookTest):
    def test_recipe_nutrition_info_recalculation(self):
        pancakes = Recipe.get(name='Pancakes')
        pancakes.ingredients.create(quantity=1, food=self.egg)
        pancakes.ingredients.create(quantity=1, unit=self.cup, food=self.flour)
        pancakes.save()

        egg = self.egg_nutrition_info
        flour = self.flour_nutrition_info
        butter = self.butter_nutrition_info

        # Before recalculation
        self.assert_nutrition_info_equals(
            pancakes.nutrition_info,
            calories     = egg.calories     + flour.calories,
            fat_calories = egg.fat_calories + flour.fat_calories,
            fat          = egg.fat          + flour.fat,
            carb         = egg.carb         + flour.carb,
            sodium       = egg.sodium       + flour.sodium,
            protein      = egg.protein      + flour.protein,
            cholesterol  = egg.cholesterol  + flour.cholesterol,
        )

        # Add 1 oz. butter to recipe
        pancakes.ingredients.create(quantity=1, unit=self.ounce, food=self.butter)
        pancakes.save()

        # Ensure that butter nutrition is now included
        self.assert_nutrition_info_equals(
            pancakes.nutrition_info,
            calories     = egg.calories     + flour.calories     + butter.calories,
            fat_calories = egg.fat_calories + flour.fat_calories + butter.fat_calories,
            fat          = egg.fat          + flour.fat          + butter.fat,
            carb         = egg.carb         + flour.carb         + butter.carb,
            sodium       = egg.sodium       + flour.sodium       + butter.sodium,
            protein      = egg.protein      + flour.protein      + butter.protein,
            cholesterol  = egg.cholesterol  + flour.cholesterol  + butter.cholesterol,
        )


from django.test.client import Client

class CookbookIndexTest (TestCase):
    def setUp(self):
        self.context = Client()

    def test_cookbook_index(self):
        index = self.context.get('/cookbook/')
        self.assertEqual(index.status_code, 200)

        # Test templates rendered
        #print('templates:')
        #print([t.name for t in index.templates])

        # Test view context
        #print('context:')
        #print(index.context['recipe_categories'])


