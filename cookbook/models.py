import re
from fractions import Fraction
from django.db import models
from core.models import ModelWrapper, Food, Amount, Preparation, Unit

class Ingredient (ModelWrapper):
    """A quantity of food used in a recipe.
    """
    amount      = models.ForeignKey(Amount)
    preparation = models.ForeignKey(Preparation, null=True, blank=True)
    food        = models.ForeignKey(Food)

    def __unicode__(self):
        if self.preparation:
            return "%s %s %s" % \
                    (self.amount, self.preparation, self.food)
        else:
            return "%s %s" % \
                    (self.amount, self.food)

    @classmethod
    def parse(cls, text):
        """Parse the given text, and return an Ingredient instance.
        `text` is expected to be in this format:

            <quantity> <unit> <preparation> <food>

        """
        # TODO:
        pattern = re.compile(
            """
            ^
            (?P<quantity>[\d\./ ]+)         # Integer, decimal, or mixed fraction
            [ ]+                            # At least one space
            ((?P<unit>\w+)[ ]+)?            # Optional unit name
            ((?P<preparation>\w+)[ ]+)?     # Optional preparation name
            (?P<food>\w+)                   # Food name
            $
            """, re.X)
        match = pattern.match(text)

        if not match:
            raise ValueError("Could not parse ingredient from: '%s'" % text)

        parts = match.groupdict()

        # Split the quantity on spaces, and accumulate fractions
        quantity = 0.0
        for numpart in parts['quantity'].split(' '):
            quantity += float(Fraction(numpart))

        # If quantity is > 1, some de-pluralization may be needed
        # FIXME: Make this work with funky pluralizations like "potatoes"
        if quantity > 1.0:
            if parts['unit']:
                parts['unit'] = parts['unit'].rstrip('s')
            else:
                parts['food'] = parts['food'].rstrip('s')

        # If a unit was given, look it up
        if parts['unit']:
            parts['unit'] = Unit.get(name=parts['unit'])

        amount = Amount.get(quantity=quantity, unit=parts['unit'])

        # Include preparation if there is one
        if parts['preparation']:
            preparation = Preparation.get(name=parts['preparation'])
        else:
            preparation = None

        food = Food.get(name=parts['food'])
        return Ingredient.get(amount=amount, preparation=preparation, food=food)


class Recipe (ModelWrapper):
    """Instructions for preparing a meal.
    """
    name        = models.CharField(max_length=100)
    directions  = models.TextField()
    servings    = models.IntegerField(blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes', blank=True)

    def __unicode__(self):
        if self.servings:
            return "%s (%s servings)" % (self.name, self.servings)
        else:
            return self.name


class IngredientGroup (ModelWrapper):
    """A group of ingredients for part of a recipe.

    For example, a cake recipe may have one group for the batter, and another
    group for the icing. Or, a recipe may call for mixing dry ingredients
    separately from the wet ingredients before combining them.
    """
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredient_groups')
    recipe = models.ForeignKey(Recipe, related_name='ingredient_groups')

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.recipe)


