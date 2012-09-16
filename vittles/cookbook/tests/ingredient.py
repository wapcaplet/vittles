from django.test import TestCase
from core.models import Food, Unit, FoodNutritionInfo
from cookbook.models import Recipe, Ingredient

class IngredientNutritionTest (TestCase):
    fixtures = [
        'test_food',
        'test_unit',
        'test_equivalence',
        'test_food_nutrition_info',
        'test_nutrition_info',
        'test_recipe',
    ]

    def test_ingredient_nutrition_info_recalculation(self):
        """Recalculate IngredientNutritionInfo on save.
        """
        egg = Food.objects.get(name='egg')
        pancakes = Recipe.objects.get(name='Pancakes')
        # Create an ingredient
        eggs = Ingredient(recipe=pancakes, quantity=2, food=egg)
        eggs.save()

        egg_NI = FoodNutritionInfo.objects.get(food=egg, quantity=1, unit=None)

        # Nutrition info should equal 2 eggs
        total_NI = egg_NI * 2.0
        self.assertTrue(eggs.nutrition_info.is_equal(total_NI))

        # Make it 3 eggs
        eggs.quantity = 3
        eggs.save()

        # Ensure nutrition reflects 3 eggs now
        total_NI = egg_NI * 3.0
        self.assertTrue(eggs.nutrition_info.is_equal(total_NI))


    def test_ingredient_nutrition_info_recalculation_from_different_unit(self):
        """Recalculate IngredientNutritionInfo with different units on save.
        """
        pancakes = Recipe.objects.get(name='Pancakes')
        # A food that we don't have nutrition info for yet
        nuts, created = Food.objects.get_or_create(name='nuts')
        tablespoon = Unit.objects.get(name='tablespoon')
        teaspoon = Unit.objects.get(name='teaspoon')
        # NutritionInfo in terms of a different unit
        nuts_NI, created = FoodNutritionInfo.objects.get_or_create(
            food=nuts, quantity=1, unit=teaspoon, calories=50)
        # Create an ingredient
        tablespoon_nuts = Ingredient(recipe=pancakes, quantity=1, unit=tablespoon, food=nuts)
        tablespoon_nuts.save()
        # Ensure correct nutrition was calculated
        self.assertTrue(tablespoon_nuts.nutrition_info.is_equal(nuts_NI * 3.0))

