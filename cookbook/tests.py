from django.test import TestCase
from core.models import Food, Unit
from cookbook.models import Ingredient

class CookbookTest (TestCase):
    """Initialization shared by all test cases
    """
    def setUp(self):
        self.flour = Food.get(name='flour')
        self.cup = Unit.get(name='cup')


class IngredientParsingTest (CookbookTest):
    def _matches(self, ingredient,
                           quantity, unit_name, food_name, preparation_name=None):
        """Return True if an ingredient has attributes matching the given values.
        """
        if ingredient.quantity != quantity:
            return False
        if ingredient.unit and ingredient.unit.name != unit_name:
            return False
        if ingredient.preparation and ingredient.preparation.name != preparation_name:
            return False
        if ingredient.food.name != food_name:
            return False

        return True


    def test_whole_numbers(self):
        """Parse ingredients with integer quantities.
        """
        ingredient = Ingredient.parse("1 cup flour")
        self.assertTrue(
            self._matches(ingredient, 1.0, 'cup', 'flour'))

        ingredient = Ingredient.parse("2 cups flour")
        self.assertTrue(
            self._matches(ingredient, 2.0, 'cup', 'flour'))


    def test_simple_fractions(self):
        """Parse ingredients with simple fraction quantities.
        """
        ingredient = Ingredient.parse("1/2 cup flour")
        self.assertTrue(
            self._matches(ingredient, 0.5, 'cup', 'flour'))

        ingredient = Ingredient.parse("3/4 cup flour")
        self.assertTrue(
            self._matches(ingredient, 0.75, 'cup', 'flour'))


    def test_mixed_fractions(self):
        """Parse ingredients with mixed fraction quantities.
        """
        ingredient = Ingredient.parse("1 1/2 cup flour")
        self.assertTrue(
            self._matches(ingredient, 1.5, 'cup', 'flour'))

        ingredient = Ingredient.parse("2 3/4 cups flour")
        self.assertTrue(
            self._matches(ingredient, 2.75, 'cup', 'flour'))


    def test_decimals(self):
        """Parse ingredients with decimal quantities.
        """
        ingredient = Ingredient.parse("0.5 cup flour")
        self.assertTrue(
            self._matches(ingredient, 0.5, 'cup', 'flour'))

        ingredient = Ingredient.parse("3.25 cups flour")
        self.assertTrue(
            self._matches(ingredient, 3.25, 'cup', 'flour'))


    def test_preparation(self):
        """Parse ingredients with a preparation specified.
        """
        ingredient = Ingredient.parse("2 cups carrot, diced")
        self.assertTrue(
            self._matches(ingredient, 2.0, 'cup', 'carrot', 'diced'))

        ingredient = Ingredient.parse("4.5 cups flour, sifted")
        self.assertTrue(
            self._matches(ingredient, 4.5, 'cup', 'flour', 'sifted'))


    def test_empty_units(self):
        """Parse ingredients without units specified.
        """
        ingredient = Ingredient.parse("3 eggs")
        self.assertTrue(
            self._matches(ingredient, 3.0, None, 'egg'))

        ingredient = Ingredient.parse("25 peppercorns")
        self.assertTrue(
            self._matches(ingredient, 25.0, None, 'peppercorn'))


