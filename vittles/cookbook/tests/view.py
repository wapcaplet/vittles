from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from cookbook.models import Recipe

class CookbookViewTest (TestCase):
    fixtures = [
        'test_food',
        'test_unit',
        'test_equivalence',
        'test_food_nutrition',
        'test_nutrition',
        'test_recipe',
        'test_recipe_nutrition',
    ]
    def setUp(self):
        self.client = Client()


    def test_view_cookbook_index(self):
        """View the Cookbook index page.
        """
        response = self.client.get(reverse('cookbook_index'))
        self.assertEqual(response.status_code, 200)
        # Index template is rendered
        self.assertTemplateUsed(response, 'cookbook/index.html')
        # One recipe category is shown
        self.assertEqual(len(response.context['recipe_categories']), 1)


    def test_view_cookbook_recipe(self):
        """View a Recipe page.
        """
        pancakes = Recipe.objects.get(name='Pancakes')
        url = reverse('cookbook_show_recipe', kwargs={'recipe_id': pancakes.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Recipe template is rendered
        self.assertTemplateUsed(response, 'cookbook/recipe.html')
        # Ensure context is correct
        self.assertEqual(response.context['recipe'], pancakes)
        self.assertEqual(response.context['nutrition'], pancakes.nutrition)


    def test_view_cookbook_nonexistent_recipe(self):
        """View a nonexistent Recipe.
        """
        url = reverse('cookbook_show_recipe', kwargs={'recipe_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

