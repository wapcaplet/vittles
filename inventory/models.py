from django.db import models
from core.models import ModelWrapper, Food, Amount

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
    amount = models.ForeignKey(Amount)
    food = models.ForeignKey(Food)

    def __unicode__(self):
        return "%s %s" % (self.amount, self.food)

