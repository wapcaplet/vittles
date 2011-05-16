from django.db import models
from core.models import Unit, Food

class Provision (models.Model):
    """A quantity of food available for use.
    """
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit)
    food = models.ForeignKey(Food)

    def __unicode__(self):
        return "%s %s %s" % \
                (self.quantity, self.unit, self.food)


class ShoppingList (models.Model):
    """A list of items to buy at the store.
    """
    pass
