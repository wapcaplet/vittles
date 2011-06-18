from django.test import TestCase
from datetime import datetime
from core.models import Unit, FoodGroup
from cookbook.models import Recipe
from diet.models import Meal, DietPlan, TargetServing

class DietStringTest (TestCase):
    """Test correct string formatting of diet models.
    """
    fixtures = [
        'test_food',
        'test_unit',
        'test_equivalence',
        'test_recipe',
    ]

    def test_meal_string(self):
        pancakes = Recipe.get(name='Pancakes')
        meal, created = Meal.objects.get_or_create(
            kind='breakfast', recipe=pancakes, date=datetime.today())
        self.assertEqual(str(meal), 'Breakfast: Pancakes')


    def test_diet_plan_string(self):
        plan, created = DietPlan.objects.get_or_create(
            name='2000 Calorie Diet')
        self.assertEqual(str(plan), '2000 Calorie Diet')


    def test_target_serving_string(self):
        plan, created = DietPlan.objects.get_or_create(
            name='Food Pyramid')
        meat, created = FoodGroup.objects.get_or_create(
            name='meat')
        ounce = Unit.objects.get(name='ounce')
        serving, created = TargetServing.objects.get_or_create(
            diet_plan=plan,
            food_group=meat,
            quantity=8,
            unit=ounce,
        )
        self.assertEqual(str(serving), '8 ounces meat')


