from django.db import models
from core.models import Unit, Food

class Provision (models.Model):
    """A quantity of food stored in a pantry.
    """
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit)
    food = models.ForeignKey(Food)

    def __unicode__(self):
        return "%s %s %s" % \
                (self.quantity, self.unit, self.food)

