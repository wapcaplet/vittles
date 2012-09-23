from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from diet.models import Meal

class DietViewTest (TestCase):
    fixtures = [
        'test_food',
        'test_unit',
        'test_equivalence',
        'test_food_nutrition',
        'test_nutrition',
        'test_recipe',
    ]
    def setUp(self):
        self.client = Client()


    def test_view_diet_index(self):
        """View diet index page.
        """
        response = self.client.get(reverse('diet_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diet/index.html')


    def test_view_diet_calendar(self):
        """View diet calendar page.
        """
        # Without date
        response = self.client.get(reverse('diet_meal_calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diet/meal_calendar.html')
        # With date
        url = reverse('diet_meal_calendar', args=['2011-06'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diet/meal_calendar.html')


    def test_view_diet_meal_add(self):
        """View page for adding a Meal.
        """
        url = reverse('diet_meal_add', args=['2011-06-01'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diet/add_meal.html')
        # Submit the form with a valid recipe
        params = {
            'date': '2011-06-01',
            'kind': 'breakfast',
            'recipe': '1',
        }
        response = self.client.post(url, params)
        # Ensure we were redirected back to the meal calendar
        self.assertEqual(response.status_code, 302)
        # Ensure a meal was created
        self.assertEqual(Meal.objects.count(), 1)

