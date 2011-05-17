from django.db import models
from core.models import Unit, Food

class Place (models.Model):
    """A place where provisions may be located
    (pantry, freezer, shopping list etc.)
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Provision (models.Model):
    """A quantity of food on a shopping list or in a pantry.
    """
    quantity = models.FloatField(blank=True)
    unit = models.ForeignKey(Unit, null=True)
    food = models.ForeignKey(Food)
    place = models.ForeignKey(Place, null=True)

    def __unicode__(self):
        desc = "%g %s %s" % (self.quantity, self.unit, self.food)
        if self.place:
            desc += " (%s)" % self.place
        return desc

