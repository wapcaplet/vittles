from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class NoEquivalence (Exception):
    pass


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


class Category (ModelWrapper):
    """A classification for something.
    """
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('Category', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Food (ModelWrapper):
    """Something edible.
    """
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Unit (ModelWrapper):
    """A form of measurement.
    """
    name = models.CharField(max_length=50, unique=True)
    abbr = models.CharField(max_length=10, blank=True)

    def __unicode__(self):
        return self.name


class Equivalence (ModelWrapper):
    """Maps one unit to another.
    """
    unit = models.ForeignKey(Unit)
    to_quantity = models.FloatField()
    to_unit = models.ForeignKey(Unit, related_name='+')

    def __unicode__(self):
        return "1 %s equals %g %s(s)" % (self.unit, self.to_quantity, self.to_unit)


class Preparation (ModelWrapper):
    """A method of preparing food for cooking or eating.
    """
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Amount (ModelWrapper):
    """A quantity of something, with units.
    """
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit)

    def __unicode__(self):
        return "%g %s" % (self.quantity, self.unit)


    def convert(self, to_unit):
        """Convert this amount to a given unit, and return the equivalent
        quantity in that unit. Requires that an `Equivalence` be defined
        for the relevant units; if no `Equivalence` is found, raise a
        `NoEquivalence` exception.
        """
        # If units are the same, no conversion is necessary
        if self.unit == to_unit:
            return self.quantity
        # Otherwise, try to find a direct mapping between units
        try:
            equivalence = Equivalence.objects.get(unit=self.unit, to_unit=to_unit)
        except ObjectDoesNotExist:
            # OK, see if there's a mapping in the other direction
            try:
                equivalence = Equivalence.objects.get(unit=to_unit, to_unit=self.unit)
            except ObjectDoesNotExist:
                raise NoEquivalence("Cannot convert '%s' to '%s'" % (self.unit, to_unit))
            else:
                return self.quantity / equivalence.to_quantity
        else:
            return self.quantity * equivalence.to_quantity


    def __add__(self, other_amount):
        """Add this Amount to another Amount, and return a new Amount in the
        same units as this one.
        """
        new_quantity=self.quantity + other_amount.convert(self.unit)
        return Amount(unit=self.unit, quantity=new_quantity)


    def __sub__(self, other_amount):
        """Subtract another Amount from this Amount, and return a new Amount in
        the same units as this one.
        """
        new_quantity=self.quantity - other_amount.convert(self.unit)
        return Amount(unit=self.unit, quantity=new_quantity)


    def __mul__(self, factor):
        """Multiply this Amount by a numeric value, and return a new Amount
        in the same units as this one.
        """
        return Amount(unit=self.unit, quantity=self.quantity * factor)


    def __eq__(self, other_amount):
        """Return True if this Amount is equal to another Amount, False otherwise.
        """
        return self.quantity == other_amount.convert(self.unit)


    def __ne__(self, other_amount):
        """Return False if this Amount is equal to another Amount, True otherwise.
        """
        return self.quantity != other_amount.convert(self.unit)


    def __gt__(self, other_amount):
        """Return True if this Amount is greater than another Amount, False otherwise.
        """
        return self.quantity > other_amount.convert(self.unit)


    def __lt__(self, other_amount):
        """Return True if this Amount is less than another Amount, False otherwise.
        """
        return self.quantity < other_amount.convert(self.unit)


