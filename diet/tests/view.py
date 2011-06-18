from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class DietViewTest (TestCase):
    def setUp(self):
        self.context = Client()


    def test_view_diet_index(self):
        response = self.context.get(reverse('diet-index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diet/index.html')


    def test_view_diet_calendar(self):
        # Without date
        response = self.context.get(reverse('diet-meal-calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diet/meal_calendar.html')
        # With date
        response = self.context.get(reverse('diet-meal-calendar', args=['2011-06']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diet/meal_calendar.html')


    def test_view_diet_meal_add(self):
        response = self.context.get(reverse('diet-meal-add', args=['2011-06-01']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diet/add_meal.html')

