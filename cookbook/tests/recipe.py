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
    def setUp(self):
        # Foods
        self.egg = Food.objects.get(name='egg')
        self.flour = Food.objects.get(name='all-purpose flour')
        self.butter = Food.objects.get(name='butter')
        # Units
        self.cup = Unit.objects.get(name='cup')
        self.ounce = Unit.objects.get(name='ounce')
        # Add an egg and 1 cup of flour to the pancakes recipe
        self.pancakes = Recipe.objects.get(name='Pancakes')
        self.pancakes.ingredients.create(quantity=1, food=self.egg)
        self.pancakes.ingredients.create(quantity=1, unit=self.cup, food=self.flour)
        self.pancakes.save()

        self.egg_NI = FoodNutritionInfo.objects.get(
            food=self.egg, quantity=1, unit=None)
        self.flour_NI = FoodNutritionInfo.objects.get(
            food=self.flour, quantity=1, unit=self.cup)
        self.butter_NI = FoodNutritionInfo.objects.get(
            food=self.butter, quantity=1, unit=self.ounce)


    def test_recipe_nutrition_info_after_adding_ingredient(self):
        # Before recalculation - only egg and flour
        total_NI = self.egg_NI + self.flour_NI
        self.assertTrue(self.pancakes.nutrition_info.is_equal(total_NI))

        # Add 1 oz. butter to recipe
        self.pancakes.ingredients.create(quantity=1, unit=self.ounce, food=self.butter)
        self.pancakes.save()

        # Ensure that butter nutrition is now included in the total
        total_NI = self.egg_NI + self.flour_NI + self.butter_NI
        self.assertTrue(self.pancakes.nutrition_info.is_equal(total_NI))


    def test_recipe_nutrition_info_after_changing_servings(self):
        # If the recipe serves 2, nutrition information should be halved
        self.pancakes.num_portions = 2.0
        self.pancakes.save()
        total_NI = (self.egg_NI + self.flour_NI) * 0.5
        self.assertTrue(self.pancakes.nutrition_info.is_equal(total_NI))

        # If the recipe serves 4, nutrition information should be quartered
        self.pancakes.num_portions = 4.0
        self.pancakes.save()
        total_NI = (self.egg_NI + self.flour_NI) * 0.25
        self.assertTrue(self.pancakes.nutrition_info.is_equal(total_NI))

