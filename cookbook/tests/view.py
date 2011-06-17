from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from cookbook.models import Recipe

class CookbookIndexTest (TestCase):
    fixtures = [
        'test_food',
        'test_unit',
        'test_equivalence',
        'test_food_nutrition_info',
        'test_nutrition_info',
        'test_recipe',
        'test_recipe_nutrition_info',
    ]
    def setUp(self):
        self.context = Client()


    def test_view_cookbook_index(self):
        index = self.context.get(reverse('cookbook-index'))
        self.assertEqual(index.status_code, 200)
        # Index template is rendered
        template_names = [t.name for t in index.templates]
        self.assertTrue('cookbook/index.html' in template_names)
        # One recipe category is shown
        self.assertEqual(len(index.context['recipe_categories']), 1)


    def test_view_cookbook_recipe(self):
        pancakes = Recipe.objects.get(name='Pancakes')
        recipe = self.context.get(pancakes.get_absolute_url())
        self.assertEqual(recipe.status_code, 200)
        # Ensure context is correct
        self.assertEqual(recipe.context['recipe'], pancakes)
        self.assertEqual(recipe.context['nutrition_info'], pancakes.nutrition_info)


