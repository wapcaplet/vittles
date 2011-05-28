from django.db import models
from vittles.core.models import ModelWrapper, Food, Unit
from vittles.core.helpers import convert_amount

class NutritionInfo (ModelWrapper):
    """Nutritional information for a food.
    """
    food              = models.OneToOneField(Food, null=True, blank=True, related_name='nutrition_info')
    serving_size      = models.FloatField(default=1)
    serving_unit      = models.ForeignKey(Unit, null=True, blank=True)
    calories          = models.FloatField(default=0)
    fat_calories      = models.FloatField(default=0)
    fat               = models.FloatField(default=0, help_text="grams")
    carb              = models.FloatField(default=0, help_text="grams")
    sodium            = models.FloatField(default=0, help_text="milligrams")
    protein           = models.FloatField(default=0, help_text="grams")
    cholesterol       = models.FloatField(default=0, help_text="milligrams")

    class Meta:
        ordering = ['food']
        verbose_name_plural = "Nutrition information"


    @classmethod
    def undefined(cls):
        """Return a special "undefined" NutritionInfo instance.
        """
        return NutritionInfo(serving_size=0)


    def __unicode__(self):
        if self.serving_size == 0:
            return "Unknown nutrition"

        if self.food:
            string = "%s" % self.food
        else:
            string = "%i calories" % self.calories
        return string


    def full_string(self):
        string = "%i calories (%i from fat) " % (self.calories, self.fat_calories)
        string += "%ig fat, %ig carbs, " % (self.fat, self.carb)
        string += "%img sodium, %ig protein, " % (self.sodium, self.protein)
        string += "%img cholesterol" % self.cholesterol
        return string


    def for_amount(self, to_quantity, to_unit):
        """Return the nutritional information for the given quantity and unit.
        """
        factor = to_quantity / convert_amount(self.serving_size, self.serving_unit, to_unit)
        return NutritionInfo(
            serving_size = to_quantity,
            serving_unit = to_unit,
            calories     = factor * self.calories,
            fat_calories = factor * self.fat_calories,
            fat          = factor * self.fat,
            carb         = factor * self.carb,
            sodium       = factor * self.sodium,
            protein      = factor * self.protein,
            cholesterol  = factor * self.cholesterol
        )


    def __add__(self, other):
        """Add this NutritionInfo to another, and return the sum.
        The returned NutritionInfo has a quantity of 1, and no Unit.
        """
        return NutritionInfo(
            calories     = self.calories + other.calories,
            fat_calories = self.fat_calories + other.fat_calories,
            fat          = self.fat + other.fat,
            carb         = self.carb + other.carb,
            sodium       = self.sodium + other.sodium,
            protein      = self.protein + other.protein,
            cholesterol  = self.cholesterol + other.cholesterol,
        )


    def __mul__(self, factor):
        """Multiply this NutritionInfo by the given amount.
        """
        return NutritionInfo(
            serving_size = factor * self.serving_size,
            serving_unit = self.serving_unit,
            calories     = factor * self.calories,
            fat_calories = factor * self.fat_calories,
            fat          = factor * self.fat,
            carb         = factor * self.carb,
            sodium       = factor * self.sodium,
            protein      = factor * self.protein,
            cholesterol  = factor * self.cholesterol
        )

