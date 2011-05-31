from django.db import models
from core.models import ModelWrapper, Food, Unit
from core.helpers import to_grams

class NutritionInfo (ModelWrapper):
    """Nutritional information for a food.
    """
    food         = models.ForeignKey(Food, null=True, blank=True, related_name='nutrition_infos')
    quantity     = models.FloatField(default=1)
    unit         = models.ForeignKey(Unit, null=True, blank=True)
    calories     = models.FloatField(default=0)
    fat_calories = models.FloatField(default=0)
    fat          = models.FloatField("Fat (g)", default=0)
    carb         = models.FloatField("Carb (g)", default=0)
    sodium       = models.FloatField("Sodium (mg)", default=0)
    protein      = models.FloatField("Protein (g)", default=0)
    cholesterol  = models.FloatField("Cholesterol (mg)", default=0)

    class Meta:
        ordering = ['food']
        verbose_name_plural = "Nutrition information"


    @classmethod
    def undefined(cls):
        """Return a special "undefined" `NutritionInfo` instance.
        """
        return NutritionInfo(quantity=0)


    def is_defined(self):
        return self.quantity > 0


    def __unicode__(self):
        if self.quantity == 0:
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
        """Return `NutritionInfo` for the given quantity and unit.
        """
        # If units are the same, scale by quantity alone
        if self.unit == to_unit:
            factor = float(to_quantity) / self.quantity
        else:
            # Scaling factor for a 1-gram serving size
            gram_serving = 1.0 / (to_grams(self.unit, self.food) * self.quantity)
            # Target quantity in grams
            target_grams = to_grams(to_unit, self.food) * to_quantity
            # Overall scaling factor to apply to all nutritional info
            factor = gram_serving * target_grams

        return NutritionInfo(
            quantity     = to_quantity,
            unit         = to_unit,
            calories     = factor * self.calories,
            fat_calories = factor * self.fat_calories,
            fat          = factor * self.fat,
            carb         = factor * self.carb,
            sodium       = factor * self.sodium,
            protein      = factor * self.protein,
            cholesterol  = factor * self.cholesterol
        )


    def normalize(self):
        """Adjust this `NutritionInfo` to have `quantity` of 1.0.
        """
        # Don't normalize undefined nutrition info
        if not self.is_defined():
            return

        scale = 1.0 / self.quantity
        self.quantity     = 1.0
        self.calories     = round(scale * self.calories, 2)
        self.fat_calories = round(scale * self.fat_calories, 2)
        self.fat          = round(scale * self.fat, 2)
        self.carb         = round(scale * self.carb, 2)
        self.sodium       = round(scale * self.sodium, 2)
        self.protein      = round(scale * self.protein, 2)
        self.cholesterol  = round(scale * self.cholesterol, 2)
        self.save()


    def __add__(self, other):
        """Add this `NutritionInfo` to another, and return the sum.
        The returned `NutritionInfo` has a quantity of 1, and no `Unit`.
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
        """Multiply this `NutritionInfo` by `factor`.
        """
        return NutritionInfo(
            quantity     = factor * self.quantity,
            unit         = self.unit,
            calories     = factor * self.calories,
            fat_calories = factor * self.fat_calories,
            fat          = factor * self.fat,
            carb         = factor * self.carb,
            sodium       = factor * self.sodium,
            protein      = factor * self.protein,
            cholesterol  = factor * self.cholesterol
        )

