from django.db import models


class Food (models.Model):
    """Something edible.
    """
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Unit (models.Model):
    """A form of measurement.
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Equivalence (models.Model):
    """Maps one unit to another.
    """
    unit = models.ForeignKey(Unit)
    to_quantity = models.FloatField()
    to_unit = models.ForeignKey(Unit, related_name='+')

    def __unicode__(self):
        return "1 %s equals %g %s(s)" % (self.unit, self.to_quantity, self.to_unit)

