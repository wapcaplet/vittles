from django.test import TestCase
from core.models import Food, Unit, Preparation
from cookbook.models import Portion, IngredientCategory, RecipeCategory, Recipe, Ingredient

class CookbookStringTest (TestCase):
    """Test correct string formatting of cookbook models.
    """
    fixtures = [
        'test_food',
        'test_unit',
        'test_equivalence',
        'test_recipe',
    ]

    def test_portion_string(self):
        """Format Portion as a string.
        """
        portion, created = Portion.objects.get_or_create(name='slice')
        self.assertEqual(str(portion), 'slice')


    def test_ingredient_category_string(self):
        """Format IngredientCategory as a string.
        """
        category, created = IngredientCategory.objects.get_or_create(name='dry goods')
        self.assertEqual(str(category), 'dry goods')


    def test_recipe_category_string(self):
        """Format RecipeCategory as a string.
        """
        category, created = RecipeCategory.objects.get_or_create(name='desserts')
        self.assertEqual(str(category), 'desserts')


    def test_recipe_string(self):
        """Format Recipe as a string.
        """
        # One portion
        portion, created = Portion.objects.get_or_create(name='loaf')
        recipe, created = Recipe.objects.get_or_create(
            name = 'Banana Bread',
            num_portions = 1,
            portion = portion)
        self.assertEqual(str(recipe), 'Banana Bread (1 loaf)')

        # Multiple portions
        portion, created = Portion.objects.get_or_create(name='cupcake')
        recipe, created = Recipe.objects.get_or_create(
            name = 'Chocolate Cupcakes',
            num_portions = 12,
            portion = portion)
        self.assertEqual(str(recipe), 'Chocolate Cupcakes (12 cupcakes)')


    def test_ingredient_string(self):
        """Format Ingredient as a string.
        """
        pancakes = Recipe.objects.get(name='Pancakes')
        egg = Food.objects.get(name='egg')
        butter = Food.objects.get(name='butter')
        ounce = Unit.objects.get(name='ounce')
        beaten, created = Preparation.objects.get_or_create(name='beaten')
        melted, created = Preparation.objects.get_or_create(name='melted')

        # quantity == 1
        eggs = Ingredient(recipe=pancakes, quantity=1, food=egg)
        self.assertEqual(str(eggs), '1 egg')
        # quantity > 1
        eggs.quantity = 2
        self.assertEqual(str(eggs), '2 eggs')
        # with preparation
        eggs.preparation = beaten
        self.assertEqual(str(eggs), '2 eggs, beaten')
        # with preparation, and optional
        eggs.optional = True
        self.assertEqual(str(eggs), '2 eggs, beaten (optional)')

        # Ingredient with units
        # quantity == 1
        ounces_butter = Ingredient(recipe=pancakes, quantity=1, unit=ounce, food=butter)
        self.assertEqual(str(ounces_butter), '1 ounce butter')
        # quantity > 1
        ounces_butter.quantity = 8
        self.assertEqual(str(ounces_butter), '8 ounces butter')
        # optional
        ounces_butter.optional = True
        self.assertEqual(str(ounces_butter), '8 ounces butter (optional)')
        # optional, with preparation
        ounces_butter.preparation = melted
        self.assertEqual(str(ounces_butter), '8 ounces butter, melted (optional)')


