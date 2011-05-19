from django.db import models


class Category (models.Model):
    """A classification for something.
    """
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('Category', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Food (models.Model):
    """Something edible.
    """
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Unit (models.Model):
    """A form of measurement.
    """
    name = models.CharField(max_length=50, unique=True)
    abbr = models.CharField(max_length=10, blank=True)

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


class Amount (models.Model):
    """A quantity of something, with units.
    """
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit)

    def __unicode__(self):
        return "%g %s" % (self.quantity, self.unit)


class Preparation (models.Model):
    """A method of preparing food for cooking or eating.
    """
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


