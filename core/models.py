from django.db import models
from core import utils

class ModelWrapper (models.Model):
    """Abstract base class for models.
    Adds functionality to the Django builtin `Model` class.
    """
    class Meta:
        abstract = True

    @classmethod
    def get(cls, **attributes):
        """Wrapper for `Model.objects.get_or_create`, returning an instance
        with the given attributes, creating one if none exist. Does not bother
        returning the `created` parameter like `get_or_create` does. Intended
        to make it easier to get an instance with the given attributes, if you
        don't care so much whether it already existed or had to be created.
        """
        obj, created = cls.objects.get_or_create(**attributes)
        return obj


class FoodGroup (ModelWrapper):
    """A classification for something.
    """
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('FoodGroup', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'


class Food (ModelWrapper):
    """Something edible.
    """
    name         = models.CharField(max_length=50, unique=True)
    food_group   = models.ForeignKey(FoodGroup, null=True, blank=True)
    grams_per_ml = models.FloatField(default=1.0)

    # Use range-based flitering for grams_per_ml
    grams_per_ml.list_filter_range = [0.5, 1.0]

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Unit (ModelWrapper):
    """A form of measurement.
    """
    _kind_choices = (
        ('weight', 'Weight'),
        ('volume', 'Volume'),
        ('individual', 'Individual'),
    )
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10, blank=True)
    kind = models.CharField(max_length=10, choices=_kind_choices)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Equivalence (ModelWrapper):
    """Maps one unit to another.
    """
    unit = models.ForeignKey(Unit)
    to_quantity = models.FloatField()
    to_unit = models.ForeignKey(Unit, related_name='+')

    def __unicode__(self):
        if self.to_quantity > 1.0:
            to_unit = utils.pluralize(self.to_unit)
        else:
            to_unit = self.to_unit
        return u"1 %s = %g %s" % (self.unit, self.to_quantity, to_unit)


class Preparation (ModelWrapper):
    """A method of preparing food for cooking or eating.
    """
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

