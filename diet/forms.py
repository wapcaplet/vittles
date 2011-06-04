from django.forms import ModelForm
from diet.models import DietPlan, Meal

class MealForm (ModelForm):
    class Meta:
        model = Meal

class DietPlanForm (ModelForm):
    class Meta:
        model = DietPlan

