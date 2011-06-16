from django.test import TestCase
from core.models import Food, FoodNutritionInfo
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



