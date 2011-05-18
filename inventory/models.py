from django.db import models
from core.models import Unit, Food

class ShoppingList (models.Model):
    """A list of foods to shop for.
    """
    name = models.CharField(max_length=50)
    foods = models.ManyToManyField(Food)

    def __unicode__(self):
        return self.name


class Provision (models.Model):
    """A quantity of food on-hand.
    """
    quantity = models.FloatField(default=1, null=True)
    unit = models.ForeignKey(Unit, null=True)
    food = models.ForeignKey(Food)

    def __unicode__(self):
        return "%g %s %s" % (self.quantity, self.unit, self.food)

