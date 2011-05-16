from django.db import models
from core.models import Unit, Food

class Preparation (models.Model):
    """A method of preparing food for cooking or eating.
    """
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Recipe (models.Model):
    """Instructions for preparing a meal.
    """
    name = models.CharField(max_length=100)
    directions = models.TextField()
    servings = models.IntegerField()

    def __unicode__(self):
        return "%s (%s servings)" % (self.name, self.servings)


class Ingredient (models.Model):
    """A quantity of food used in a recipe.
    """
    quantity = models.FloatField()
    unit = models.ForeignKey(Unit)
    food = models.ForeignKey(Food)
    preparation = models.ForeignKey(Preparation, null=True, blank=True)
    recipe = models.ForeignKey(Recipe)

    def __unicode__(self):
        if self.preparation:
            return "%s %s %s %s" % \
                    (self.quantity, self.unit, self.preparation, self.food)
        else:
            return "%s %s %s" % \
                    (self.quantity, self.unit, self.food)

