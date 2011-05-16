from django.db import models
from core.models import Unit, Food

class Pantry (models.Model):
    """A place where food may be stored.
    Could be generic, or a specific location (cupboard, freezer, etc.)
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Provision (models.Model):
    """A quantity of food stored in a pantry.
    """
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit)
    food = models.ForeignKey(Food)
    pantry = models.ForeignKey(Pantry)

    def __unicode__(self):
        return "%s %s %s" % \
                (self.quantity, self.unit, self.food)

