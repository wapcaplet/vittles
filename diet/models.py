from django.db import models
from core.models import ModelWrapper
from nutrition.models import NutritionInfo
from cookbook.models import Recipe


class Meal (ModelWrapper):
    """Something eaten during the day.
    """
    _meal_choices = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('drink', 'Drink'),
    )
    kind           = models.CharField(max_length=20, choices=_meal_choices)
    recipe         = models.ForeignKey(Recipe, null=True, blank=True)
    date           = models.DateField()
    nutrition_info = models.ForeignKey(NutritionInfo, editable=False, null=True, blank=True)


class DietPlan (ModelWrapper):
    """Target intake of nutrition or food groups.
    """
    name         = models.CharField(max_length=100)
    description  = models.TextField(blank=True, null=True)
    calories     = models.FloatField(default=0)
    fat_calories = models.FloatField(default=0)
    fat          = models.FloatField("Fat (g)", default=0)
    carb         = models.FloatField("Carb (g)", default=0)
    sodium       = models.FloatField("Sodium (mg)", default=0)
    protein      = models.FloatField("Protein (g)", default=0)
    cholesterol  = models.FloatField("Cholesterol (mg)", default=0)


