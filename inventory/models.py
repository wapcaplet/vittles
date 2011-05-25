from django.db import models
from vittles.core.models import ModelWrapper, Food, Unit
from vittles.core.helpers import format_food_unit

class ShoppingList (ModelWrapper):
    """A list of foods to shop for.
    """
    name = models.CharField(max_length=50)
    foods = models.ManyToManyField(Food)

    def __unicode__(self):
        return self.name


class Provision (ModelWrapper):
    """A quantity of food on-hand.
    """
    quantity    = models.FloatField()
    unit        = models.ForeignKey(Unit, blank=True, null=True)
    food        = models.ForeignKey(Food)

    def __unicode__(self):
        return format_food_unit(self.quantity, self.unit, self.food)

