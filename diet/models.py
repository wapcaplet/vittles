from django.db import models
from core.models import ModelWrapper, Category, Unit
from core.utils import pluralize
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
    date           = models.DateField()
    kind           = models.CharField(max_length=20, choices=_meal_choices)
    recipe         = models.ForeignKey(Recipe)
    nutrition_info = models.ForeignKey(NutritionInfo, editable=False, null=True, blank=True)

    def __unicode__(self):
        string = u"%s" % self.get_kind_display()
        if self.recipe:
            string += ": %s" % self.recipe.name
        return string


class DietPlan (ModelWrapper):
    """Target intake of nutrition or food groups.
    """
    name           = models.CharField(max_length=100)
    description    = models.TextField(blank=True, null=True)
    nutrition_info = models.ForeignKey(NutritionInfo, null=True, blank=True)

    def __unicode__(self):
        return self.name


class TargetServing (ModelWrapper):
    """Target amount of a given food group as part of a diet plan.
    """
    diet_plan  = models.ForeignKey(DietPlan)
    food_group = models.ForeignKey(Category)
    quantity   = models.FloatField()
    unit       = models.ForeignKey(Unit)

    def __unicode__(self):
        return "%g %s %s" % (self.quantity, pluralize(self.unit), self.food_group)

