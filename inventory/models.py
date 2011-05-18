from django.db import models
from core.models import Unit, Food

class Place (models.Model):
    """A place where provisions may be located
    (pantry, freezer, shopping list etc.)
    """
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Provision (models.Model):
    """A quantity of food on a shopping list or in a pantry.
    """
    quantity = models.FloatField(blank=True, null=True)
    unit = models.ForeignKey(Unit, null=True)
    food = models.ForeignKey(Food)
    place = models.ForeignKey(Place, null=True, related_name='provisions')

    def __unicode__(self):
        desc = "%g %s %s" % (self.quantity, self.unit, self.food)
        if self.place:
            desc += " (%s)" % self.place
        return desc

