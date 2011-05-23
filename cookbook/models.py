import re
from fractions import Fraction
from django.db import models
from core.models import ModelWrapper, Food, Preparation, Unit
from core.helpers import format_food_unit, fraction_to_float

class Ingredient (ModelWrapper):
    """A quantity of food used in a recipe.
    """
    quantity    = models.FloatField()
    unit        = models.ForeignKey(Unit, blank=True, null=True)
    preparation = models.ForeignKey(Preparation, null=True, blank=True)
    food        = models.ForeignKey(Food)
    optional    = models.BooleanField(default=False)

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
        # TODO:
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


class Recipe (ModelWrapper):
    """Instructions for preparing a meal.
    """
    name        = models.CharField(max_length=100)
    directions  = models.TextField(blank=True, null=True)
    preheat     = models.CharField(max_length=5, blank=True, null=True)
    servings    = models.IntegerField(blank=True, null=True)
    #ingredients = models.ManyToManyField(Ingredient, related_name='recipes', blank=True)

    def __unicode__(self):
        if self.servings:
            return "%s (%s servings)" % (self.name, self.servings)
        else:
            return self.name


class IngredientList (ModelWrapper):
    """A group of ingredients for part of a recipe.

    For example, a cake recipe may have one group for the batter, and another
    group for the icing. Or, a recipe may call for mixing dry ingredients
    separately from the wet ingredients before combining them.
    """
    name = models.CharField(max_length=100, default='Ingredients')
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredient_lists')
    recipe = models.ForeignKey(Recipe, related_name='ingredient_lists')

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.recipe)


