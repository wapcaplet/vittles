from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from core.models import ModelWrapper, Food, Preparation, Unit
from core.helpers import NoEquivalence
from nutrition.models import NutritionInfo
from core.utils import format_food_unit, pluralize


class Portion (ModelWrapper):
    """Serving or portion names for recipe yields.
    Examples: muffin, roll, loaf, serving.
    """
    name = models.CharField(max_length=50, unique=True)

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
    prep_minutes = models.IntegerField(blank=True, null=True)
    inactive_prep_minutes = models.IntegerField(blank=True, null=True)
    cook_minutes = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        string = u"%s" % self.name
        if self.num_portions:
            string += " (%s)" % self.servings()
        return string


    @models.permalink
    def get_absolute_url(self):
        return ('cookbook.views.show_recipe', [str(self.id)])


    def servings(self):
        """Return a string indicating the yield or serving size of this recipe.
        """
        string = "%d" % self.num_portions
        if self.portion:
            if self.num_portions > 1:
                string += " %s" % pluralize(self.portion)
            else:
                string += " %s" % self.portion
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


    def nutrition_info(self):
        """Return total `NutritionInfo` for this recipe.
        """
        # FIXME: This is horribly inefficient, because all nutrition info
        # is recalculated every time this function is called. Some day, need
        # to find a way to cache this and rebuild it only when requested.
        nutritions = [ingred.nutrition_info() for ingred in self.ingredients.all()]
        total = sum(nutritions[1:], nutritions[0])
        if self.num_portions:
            return total * (1.0 / self.num_portions)
        else:
            return total


    def nutrition_info_is_incomplete(self):
        """Return True if this recipe's nutrition information is incomplete
        (that is, if any ingredients are missing nutrition info).
        """
        nutritions = [ingred.nutrition_info() for ingred in self.ingredients.all()]
        return not all(info.is_defined() for info in nutritions)


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

    def __unicode__(self):
        string = format_food_unit(self.quantity, self.unit, self.food)
        if self.preparation:
            string += ", %s" % self.preparation
        if self.optional:
            string += " (optional)"
        return string


    def nutrition_info(self):
        """Return total `NutritionInfo` for this ingredient.
        """
        # TODO: Maybe move some of this code into a NutritionInfo method?

        # Find all nutritions for this food, or return undefined if none exist
        try:
            nutritions = NutritionInfo.objects.filter(food=self.food)
        except ObjectDoesNotExist:
            return NutritionInfo.undefined()

        # Are there any nutrition infos in terms of the current unit?
        for matching_unit in nutritions.filter(unit=self.unit):
            try:
                return matching_unit.for_amount(self.quantity, self.unit)
            except NoEquivalence:
                pass

        # No matching units. See if there's any other unit that can be converted
        for other_unit in nutritions.filter(unit__isnull=False):
            try:
                return other_unit.for_amount(self.quantity, self.unit)
            except NoEquivalence:
                pass

        # If we get here, no attempts at conversion succeeded
        return NutritionInfo.undefined()

