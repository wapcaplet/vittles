from django.db import models
from core.models import ModelWrapper, Food, Preparation, Unit, FoodNutrition
from core.helpers import NoEquivalence, group_by_category
from nutrition.models import Nutrition
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
    num_portions = models.IntegerField("Yield", default=1)
    portion      = models.ForeignKey(Portion, blank=True, null=True)
    source       = models.CharField(max_length=100, blank=True, null=True)
    rating       = models.IntegerField(blank=True, null=True)
    category     = models.ForeignKey(RecipeCategory, blank=True, null=True)
    prep_minutes = models.IntegerField(blank=True, null=True)
    inactive_prep_minutes = models.IntegerField(blank=True, null=True)
    cook_minutes = models.IntegerField(blank=True, null=True)
    photo        = models.ImageField(blank=True, null=True, upload_to='recipes')

    def __unicode__(self):
        string = u"%s" % self.name
        if self.num_portions:
            string += " (%s)" % self.servings()
        return string


    @models.permalink
    def get_absolute_url(self):
        return ('cookbook.views.show_recipe', [str(self.id)])


    def save(self, *args, **kwargs):
        """Customized save method; creates and (if possible) calculates
        `Nutrition` for the Ingredient.
        """
        super(Recipe, self).save(*args, **kwargs)
        RecipeNutrition.objects.get_or_create(recipe=self)
        self.nutrition.recalculate()


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
        return group_by_category(self.ingredients.all())


class RecipeNutrition (Nutrition):
    """Nutritional information for a Recipe.
    """
    recipe = models.OneToOneField(Recipe, related_name='nutrition')

    def recalculate(self):
        """Recalculate the nutrition for the current `Recipe`.
        Return `True` if all nutrition info could be calculated,
        `False` otherwise.
        """
        # Force a reload of the recipe object
        # See: https://code.djangoproject.com/ticket/901
        recipe = Recipe.objects.get(pk=self.recipe.id)

        if recipe.ingredients.count() == 0:
            return

        # Recalculate all Ingredients' nutrition info
        for ingredient in recipe.ingredients.all():
            ingredient.nutrition.recalculate()

        # Sum them up
        nutritions = [
            ingredient.nutrition
            for ingredient in recipe.ingredients.all()
        ]
        total = sum(nutritions[1:], nutritions[0])
        # Divide by servings
        total = total * (1.0 / recipe.num_portions)
        self.set_equal(total)


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


    def save(self, *args, **kwargs):
        """Customized save method; creates and (if possible) calculates
        `Nutrition` for the Ingredient.
        """
        super(Ingredient, self).save(*args, **kwargs)
        IngredientNutrition.objects.get_or_create(ingredient=self)
        self.nutrition.recalculate()


class IngredientNutrition (Nutrition):
    """Nutritional information for an Ingredient.
    """
    ingredient = models.OneToOneField(Ingredient, related_name='nutrition')

    def recalculate(self):
        """Recalculate the nutrition for the current `Ingredient`.
        Return `True` if recalculation was successful, `False` otherwise.
        """
        # Force a reload of the Ingredient instance
        # See: https://code.djangoproject.com/ticket/901
        ingredient = Ingredient.objects.get(pk=self.ingredient.id)

        # Find all nutritions for this food (maybe none)
        nutritions = FoodNutrition.objects.filter(food=ingredient.food)

        # Is there any nutrition info in terms of the current unit?
        matches = nutritions.filter(unit=ingredient.unit)
        if matches.count() > 0:
            info = matches[0].for_amount(ingredient.quantity, ingredient.unit)
            self.set_equal(info)
            return

        # No matching units. Any other non-null unit that can be converted?
        for nutrition in nutritions.filter(unit__isnull=False):
            try:
                info = nutrition.for_amount(ingredient.quantity, ingredient.unit)
            except NoEquivalence:
                pass
            # Success
            else:
                self.set_equal(info)
                return

        # If we get here, no attempts at conversion succeeded. Leave the
        # nutrition info at zero.


# Signals

# FIXME: This is commented out, pending a better solution. Turns out the
# pre_save signal is also emitted when loading fixture data, causing every
# single Food object loaded to have its Recipe recalculated. Not good.
# Would be better to have a signal that only prompts recalculation when a
# user actually modifies a Food instance through the admin site.

#from django.dispatch import receiver

#@receiver(models.signals.post_save, sender=Food)
#def model_updated(sender, **kwargs):
    #"""After a Food is saved, recalculate `Nutrition` for related
    #`Recipe`\s.
    #"""
    #recipes = set([
        #ingredient.recipe
        #for ingredient in kwargs['instance'].ingredient_set.all()
    #])
    #for recipe in recipes:
        #print("Recalculating: %s" % recipe)
        #recipe.nutrition.recalculate()


