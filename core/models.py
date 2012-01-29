from django.db import models
from core import utils, helpers
from nutrition.models import NutritionInfo
# For list_filter_range
from core import filters

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
        verbose_name_plural = 'Food Groups'


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

    def has_nutrition_info(self):
        """Return True if this `Food` has `FoodNutritionInfo`, False otherwise.
        """
        return self.nutrition_infos.count() > 0


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


class FoodNutritionInfo (NutritionInfo):
    """Nutritional information for a Food.
    """
    food     = models.ForeignKey(Food, related_name='nutrition_infos')
    quantity = models.FloatField(default=1)
    unit     = models.ForeignKey(Unit, null=True, blank=True)

    def for_amount(self, to_quantity, to_unit):
        """Return a `FoodNutritionInfo` for the given quantity and unit.
        """
        # If units are the same, scale by quantity alone
        if self.unit == to_unit:
            factor = float(to_quantity) / self.quantity
        else:
            # Scaling factor for a 1-gram serving size
            gram_serving = 1.0 / (helpers.to_grams(self.unit, self.food) * self.quantity)
            # Target quantity in grams
            target_grams = helpers.to_grams(to_unit, self.food) * to_quantity
            # Overall scaling factor to apply to all nutritional info
            factor = gram_serving * target_grams

        return FoodNutritionInfo(
            food         = self.food,
            quantity     = to_quantity,
            unit         = to_unit,
            calories     = factor * self.calories,
            fat_calories = factor * self.fat_calories,
            fat          = factor * self.fat,
            carb         = factor * self.carb,
            sodium       = factor * self.sodium,
            protein      = factor * self.protein,
            cholesterol  = factor * self.cholesterol
        )


    def normalize(self):
        """Adjust this `NutritionInfo` to have `quantity` of 1.0.
        """
        # FIXME: Catch possibility of self.quantity == 0
        scale = 1.0 / self.quantity
        self.quantity     = 1.0
        self.calories     = round(scale * self.calories, 2)
        self.fat_calories = round(scale * self.fat_calories, 2)
        self.fat          = round(scale * self.fat, 2)
        self.carb         = round(scale * self.carb, 2)
        self.sodium       = round(scale * self.sodium, 2)
        self.protein      = round(scale * self.protein, 2)
        self.cholesterol  = round(scale * self.cholesterol, 2)
        self.save()


    def is_equal(self, other):
        """Return True if this `FoodNutritionInfo` is equal to another,
        False otherwise.
        """
        return all([
            self.quantity == other.quantity,
            self.unit == other.unit,
            self.food == other.food,
        ]) and super(FoodNutritionInfo, self).is_equal(other)


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

