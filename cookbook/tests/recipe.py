from django.test import TestCase
from core.models import Food, Unit, FoodNutritionInfo
from cookbook.models import Recipe

class RecipeTest (TestCase):
    fixtures = [
        'test_food',
        'test_unit',
        'test_equivalence',
        'test_food_nutrition_info',
        'test_nutrition_info',
        'test_recipe',
    ]

    def test_recipe_nutrition_info_recalculation(self):
        # Foods
        egg = Food.objects.get(name='egg')
        flour = Food.objects.get(name='all-purpose flour')
        butter = Food.objects.get(name='butter')
        # Units
        cup = Unit.objects.get(name='cup')
        ounce = Unit.objects.get(name='ounce')
        # Add an egg and 1 cup of flour to the pancakes recipe
        pancakes = Recipe.objects.get(name='Pancakes')
        pancakes.ingredients.create(quantity=1, food=egg)
        pancakes.ingredients.create(quantity=1, unit=cup, food=flour)
        pancakes.save()

        egg_NI = FoodNutritionInfo.objects.get(food=egg, quantity=1, unit=None)
        flour_NI = FoodNutritionInfo.objects.get(food=flour, quantity=1, unit=cup)
        butter_NI = FoodNutritionInfo.objects.get(food=butter, quantity=1, unit=ounce)

        # Before recalculation
        total_NI = egg_NI + flour_NI
        self.assertTrue(pancakes.nutrition_info.is_equal(total_NI))

        # Add 1 oz. butter to recipe
        pancakes.ingredients.create(quantity=1, unit=ounce, food=butter)
        pancakes.save()

        # Ensure that butter nutrition is now included in the total
        total_NI = egg_NI + flour_NI + butter_NI
        self.assertTrue(pancakes.nutrition_info.is_equal(total_NI))

        # Make the recipe have two servings instead of one
        pancakes.num_portions = 2.0
        pancakes.save()

        # Ensure the nutrition information is now halved
        total_NI = (egg_NI + flour_NI + butter_NI) * 0.5
        self.assertTrue(pancakes.nutrition_info.is_equal(total_NI))

