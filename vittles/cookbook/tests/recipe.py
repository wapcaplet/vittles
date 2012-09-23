from django.test import TestCase
from core.models import Food, Unit, FoodNutrition
from cookbook.models import Recipe, IngredientCategory

class RecipeTest (TestCase):
    fixtures = [
        'test_food',
        'test_unit',
        'test_equivalence',
        'test_food_nutrition',
        'test_nutrition',
        'test_recipe',
    ]
    def setUp(self):
        # Foods
        self.egg = Food.objects.get(name='egg')
        self.flour = Food.objects.get(name='all-purpose flour')
        self.butter = Food.objects.get(name='butter')
        self.salt = Food.objects.get(name='salt')
        # Units
        self.cup = Unit.objects.get(name='cup')
        self.ounce = Unit.objects.get(name='ounce')
        self.teaspoon = Unit.objects.get(name='teaspoon')
        # Recipe
        self.pancakes = Recipe.objects.get(name='Pancakes')


class RecipeNutritionTest (RecipeTest):
    def setUp(self):
        super(RecipeNutritionTest, self).setUp()
        # Add an egg and 1 cup of flour to the pancakes recipe
        self.pancakes.ingredients.create(quantity=1, food=self.egg)
        self.pancakes.ingredients.create(quantity=1, unit=self.cup, food=self.flour)
        self.pancakes.save()

        self.egg_NI = FoodNutrition.objects.get(
            food=self.egg, quantity=1, unit=None)
        self.flour_NI = FoodNutrition.objects.get(
            food=self.flour, quantity=1, unit=self.cup)
        self.butter_NI = FoodNutrition.objects.get(
            food=self.butter, quantity=1, unit=self.ounce)


    def test_recipe_nutrition_after_adding_ingredient(self):
        """Recalculate RecipeNutrition after adding an Ingredient.
        """
        # Before recalculation - only egg and flour
        total_NI = self.egg_NI + self.flour_NI
        self.assertTrue(self.pancakes.nutrition.is_equal(total_NI))

        # Add 1 oz. butter to recipe
        self.pancakes.ingredients.create(quantity=1, unit=self.ounce, food=self.butter)
        self.pancakes.save()

        # Ensure that butter nutrition is now included in the total
        total_NI = self.egg_NI + self.flour_NI + self.butter_NI
        self.assertTrue(self.pancakes.nutrition.is_equal(total_NI))


    def test_recipe_nutrition_after_changing_servings(self):
        """Recalculate RecipeNutrition after changing number of servings.
        """
        # If the recipe serves 2, nutrition information should be halved
        self.pancakes.num_portions = 2.0
        self.pancakes.save()
        total_NI = (self.egg_NI + self.flour_NI) * 0.5
        self.assertTrue(self.pancakes.nutrition.is_equal(total_NI))

        # If the recipe serves 4, nutrition information should be quartered
        self.pancakes.num_portions = 4.0
        self.pancakes.save()
        total_NI = (self.egg_NI + self.flour_NI) * 0.25
        self.assertTrue(self.pancakes.nutrition.is_equal(total_NI))


class RecipeIngredientTest (RecipeTest):
    def test_recipe_ingredient_groups(self):
        """Group Recipe ingredients by IngredientCategory.
        """
        # Wet and dry ingredient groups
        wet = IngredientCategory.get(name='Wet Works')
        dry = IngredientCategory.get(name='Dry Goods')

        wet_egg = self.pancakes.ingredients.create(
            category=wet, quantity=1, food=self.egg)
        wet_butter = self.pancakes.ingredients.create(
            category=wet, quantity=1, unit=self.ounce, food=self.butter)

        dry_salt = self.pancakes.ingredients.create(
            category=dry, quantity=1, unit=self.teaspoon, food=self.salt)
        dry_flour = self.pancakes.ingredients.create(
            category=dry, quantity=1, unit=self.cup, food=self.flour)

        all_groups = self.pancakes.ingredient_groups()

        # Ensure there are two groups
        self.assertEqual(len(all_groups), 2)
        wet_group, dry_group = all_groups

        # Ensure correct name for each group
        self.assertEqual(wet_group[0], u'Wet Works')
        self.assertEqual(dry_group[0], u'Dry Goods')

        # Ensure correct length of ingredient list in each group
        self.assertEqual(len(wet_group[1]), 2)
        self.assertEqual(len(dry_group[1]), 2)

        # Ensure correct ingredients in both groups
        self.assertTrue(wet_egg in wet_group[1])
        self.assertTrue(wet_butter in wet_group[1])
        self.assertTrue(dry_salt in dry_group[1])
        self.assertTrue(dry_flour in dry_group[1])

