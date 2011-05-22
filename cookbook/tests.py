from django.test import TestCase
from core.models import Food, Unit, Amount, Preparation
from cookbook.models import Ingredient

class CookbookTest (TestCase):
    """Initialization shared by all test cases
    """
    def setUp(self):
        self.flour = Food.get(name='flour')
        self.cup = Unit.get(name='cup')


class IngredientParsingTest (CookbookTest):
    def test_whole_numbers(self):
        """Parse ingredients with integer quantities.
        """
        ingredient = Ingredient.parse("1 cup flour")
        self.failUnlessEqual(ingredient.amount.quantity, 1.0)

        ingredient = Ingredient.parse("2 cups flour")
        self.failUnlessEqual(ingredient.amount.quantity, 2.0)


    def test_simple_fractions(self):
        """Parse ingredients with simple fraction quantities.
        """
        ingredient = Ingredient.parse("1/2 cup flour")
        self.failUnlessEqual(ingredient.amount.quantity, 0.5)

        ingredient = Ingredient.parse("3/4 cup flour")
        self.failUnlessEqual(ingredient.amount.quantity, 0.75)


    def test_mixed_fractions(self):
        """Parse ingredients with mixed fraction quantities.
        """
        ingredient = Ingredient.parse("1 1/2 cup flour")
        self.failUnlessEqual(ingredient.amount.quantity, 1.5)

        ingredient = Ingredient.parse("2 3/4 cups flour")
        self.failUnlessEqual(ingredient.amount.quantity, 2.75)


    def test_decimals(self):
        """Parse ingredients with decimal quantities.
        """
        ingredient = Ingredient.parse("0.5 cup flour")
        self.failUnlessEqual(ingredient.amount.quantity, 0.5)

        ingredient = Ingredient.parse("3.25 cups flour")
        self.failUnlessEqual(ingredient.amount.quantity, 3.25)


    def test_preparation(self):
        """Parse ingredients with a preparation specified.
        """
        ingredient = Ingredient.parse("2 cups diced carrot")
        self.failUnlessEqual(ingredient.preparation.name, 'diced')

        ingredient = Ingredient.parse("4.5 cups sifted flour")
        self.failUnlessEqual(ingredient.preparation.name, 'sifted')


