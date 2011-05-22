import re
from django.db import models
from core.models import ModelWrapper, Food, Amount, Preparation

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
        # Handle preparations
        pattern = re.compile(
            """
            ^(?P<quantity>[\d\./ ]+)    # Integers, decimals, or mixed fractions
            [ ]+                        # At least one space
            (?P<unit>\w+)               # Unit name
            [ ]+                        # At least one space
            (
                (?P<preparation>\w+)    # Optional preparation
                [ ]+
            )?
            (?P<food>\w+)
            $
            """, re.X)
        match = pattern.match(text)

        if not match:
            raise ValueError("Could not parse ingredient from: '%s'" % text)

        parts = match.groupdict()

        amount = Amount.parse("%s %s" % (parts['quantity'], parts['unit']))

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


