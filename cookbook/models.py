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


class Recipe (ModelWrapper):
    """Instructions for preparing a meal.
    """
    name        = models.CharField(max_length=100)
    directions  = models.TextField()
    servings    = models.IntegerField(default=2)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')

    def __unicode__(self):
        return "%s (%s servings)" % (self.name, self.servings)


