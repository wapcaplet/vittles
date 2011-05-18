from django.db import models
from core.models import Unit, Food

class Preparation (models.Model):
    """A method of preparing food for cooking or eating.
    """
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Ingredient (models.Model):
    """A quantity of food used in a recipe.
    """
    quantity    = models.FloatField()
    unit        = models.ForeignKey(Unit)
    preparation = models.ForeignKey(Preparation, null=True, blank=True)
    food        = models.ForeignKey(Food)

    def __unicode__(self):
        if self.preparation:
            return "%s %s %s %s" % \
                    (self.quantity, self.unit, self.preparation, self.food)
        else:
            return "%s %s %s" % \
                    (self.quantity, self.unit, self.food)


class Recipe (models.Model):
    """Instructions for preparing a meal.
    """
    name        = models.CharField(max_length=100)
    directions  = models.TextField()
    servings    = models.IntegerField(default=2)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')

    def __unicode__(self):
        return "%s (%s servings)" % (self.name, self.servings)


