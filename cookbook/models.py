import re
from django.db import models
from vittles.core.models import ModelWrapper, Food, Preparation, Unit
from vittles.core.utils import format_food_unit, fraction_to_float


class Portion (ModelWrapper):
    """Serving or portion names for recipe yields.
    Examples: muffin, roll, loaf, serving.
    """
    name = models.CharField(max_length=50, unique=True)
    plural = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class IngredientCategory (ModelWrapper):
    """A category of ingredients within a recipe.
    Examples: dry, wet, icing, filling, or sauce.
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Ingredient categories'

    def __unicode__(self):
        return self.name


class RecipeCategory (ModelWrapper):
    """A category of recipe.
    Examples: entree, dessert, side dish.
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Recipe categories'

    def __unicode__(self):
        return self.name


class Recipe (ModelWrapper):
    """Instructions for preparing a meal.
    """
    name         = models.CharField(max_length=100)
    directions   = models.TextField(blank=True, null=True)
    preheat      = models.CharField(max_length=5, blank=True, null=True)
    num_portions = models.IntegerField("Yield", blank=True, null=True)
    portion      = models.ForeignKey(Portion, blank=True, null=True)
    source       = models.CharField(max_length=100, blank=True, null=True)
    rating       = models.IntegerField(blank=True, null=True)
    category     = models.ForeignKey(RecipeCategory, blank=True, null=True)

    def __unicode__(self):
        string = "%s" % self.name
        if self.num_portions:
            string += " (%s)" % self.servings()
        return string


    def servings(self):
        """Return a string indicating the yield or serving size of this recipe.
        """
        string = "%d" % self.num_portions
        if self.portion:
            if self.num_portions > 1:
                string += " %s" % self.portion.plural
            else:
                string += " %s" % self.portion.name
        return string


    def directions_paragraphs(self):
        """Return the Recipe directions, split into a list of paragraphs.
        """
        return [line for line in self.directions.splitlines()
                if line.strip() != '']


    def ingredient_groups(self):
        """Return a list of ``(category, [ingredients])`` for this recipe.
        ``category`` is ``None`` for any ingredients without a defined category.
        """
        ingredients = self.ingredients.all()
        categories = set(ingred.category for ingred in ingredients)
        groups = []
        for category in categories:
            if category:
                category = category.name
            groups.append((category, ingredients.filter(category__name=category)))
        return groups


class Ingredient (ModelWrapper):
    """A quantity of food used in a recipe.
    """
    recipe      = models.ForeignKey(Recipe, related_name='ingredients')
    category    = models.ForeignKey(IngredientCategory, blank=True, null=True)
    quantity    = models.FloatField()
    unit        = models.ForeignKey(Unit, blank=True, null=True)
    preparation = models.ForeignKey(Preparation, blank=True, null=True)
    food        = models.ForeignKey(Food)
    optional    = models.BooleanField(default=False)

    class Meta:
        ordering = ['category', 'food']

    def __unicode__(self):
        string = format_food_unit(self.quantity, self.unit, self.food)
        if self.preparation:
            string += ", %s" % self.preparation
        if self.optional:
            string += " (optional)"
        return string


    @classmethod
    def parse(cls, text):
        """Parse the given text, and return an Ingredient instance.
        `text` is expected to be in this format:

            <quantity> <unit> <food>, <preparation> (optional)

        """
        # TODO: How on earth to handle spaces in both unit and food names?
        pattern = re.compile(
            """
            ^
            (?P<quantity>[\d\./ ]+)         # Integer, decimal, or mixed fraction
            [ ]+                            # At least one space
            ((?P<unit>\w+)[ ]+)?            # Optional unit name
            (?P<food>\w+)                   # Food name
            (,[ ]+(?P<preparation>\w+))?    # Optional preparation name
            $
            """, re.X)
        match = pattern.match(text)

        if not match:
            raise ValueError("Could not parse ingredient from: '%s'" % text)

        parts = match.groupdict()

        quantity = fraction_to_float(parts['quantity'])

        # If quantity is > 1, some de-pluralization may be needed
        # FIXME: Make this work with funky pluralizations like "potatoes"
        if quantity > 1.0:
            if parts['unit']:
                parts['unit'] = parts['unit'].rstrip('s')
            else:
                parts['food'] = parts['food'].rstrip('s')

        # Look up unit if one was given
        if parts['unit']:
            unit = Unit.get(name=parts['unit'])
        else:
            unit = None

        # Look up preparation if one was given
        if parts['preparation']:
            preparation = Preparation.get(name=parts['preparation'])
        else:
            preparation = None

        food = Food.get(name=parts['food'])
        return Ingredient.get(quantity=quantity, unit=unit, preparation=preparation, food=food)


