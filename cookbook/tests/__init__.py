from django.test import TestCase
from core.models import Unit, Food, FoodNutritionInfo
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


from django.test.client import Client
from django.core.urlresolvers import reverse

class CookbookIndexTest (TestCase):
    def setUp(self):
        self.context = Client()

    def test_cookbook_index(self):
        index = self.context.get(reverse('cookbook-index'))
        self.assertEqual(index.status_code, 200)

        # Test templates rendered
        #print('templates:')
        #print([t.name for t in index.templates])

        # Test view context
        #print('context:')
        #print(index.context['recipe_categories'])


