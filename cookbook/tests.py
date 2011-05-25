from django.test import TestCase
from vittles.core.models import Food, Unit
from vittles.cookbook.models import Ingredient

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


    def assert_correct_parsing(self, text, quantity, unit_name,
                               food_name, preparation_name=None):
        """Assert that the given text is parsed correctly as an Ingredient,
        with attributes matching those given.
        """
        ingredient = Ingredient.parse(text)
        self.assertTrue(
            self._matches(
                ingredient,
                quantity,
                unit_name,
                food_name,
                preparation_name
            )
        )


    def test_whole_number_quantities(self):
        self.assert_correct_parsing("1 cup flour", 1.0, 'cup', 'flour')
        self.assert_correct_parsing("2 cups flour", 2.0, 'cup', 'flour')


    def test_simple_fraction_quantities(self):
        self.assert_correct_parsing("1/2 cup flour", 0.5, 'cup', 'flour')
        self.assert_correct_parsing("3/4 cup flour", 0.75, 'cup', 'flour')


    def test_mixed_fraction_quantities(self):
        self.assert_correct_parsing("1 1/2 cup flour", 1.5, 'cup', 'flour')
        self.assert_correct_parsing("2 3/4 cups flour", 2.75, 'cup', 'flour')


    def test_decimal_quantities(self):
        self.assert_correct_parsing("0.5 cup flour", 0.5, 'cup', 'flour')
        self.assert_correct_parsing("3.25 cups flour", 3.25, 'cup', 'flour')


    def test_ingredient_with_preparation(self):
        self.assert_correct_parsing(
            "2 cups carrot, diced", 2.0, 'cup', 'carrot', 'diced')
        self.assert_correct_parsing(
            "4.5 cups flour, sifted", 4.5, 'cup', 'flour', 'sifted')


    def test_empty_units(self):
        self.assert_correct_parsing(
            "3 eggs", 3.0, None, 'egg')
        self.assert_correct_parsing(
            "25 peppercorns", 25.0, None, 'peppercorn')


    def test_empty_units_with_preparation(self):
        self.assert_correct_parsing(
            "3 eggs, beaten", 3.0, None, 'egg', 'beaten')

