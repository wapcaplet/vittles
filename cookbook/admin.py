from django.contrib import admin
from pyantry.cookbook.models import Ingredient, Recipe, IngredientGroup

# Inline forms

class IngredientInline (admin.TabularInline):
    """Displays ingredients in a table, with 10 rows.
    """
    model = Recipe.ingredients.through
    verbose_name = 'ingredient'
    verbose_name_plural = 'ingredients'

class IngredientGroupInline (admin.StackedInline):
    """Displays ingredient groups inline.
    """
    model = IngredientGroup
    extra = 0
    filter_horizontal = ('ingredients',)


# Main forms

class RecipeAdmin (admin.ModelAdmin):
    """Customized recipe admin interface, with ingredients included.
    """
    inlines = [IngredientGroupInline]
    filter_horizontal = ('ingredients',)

class IngredientGroupAdmin (admin.ModelAdmin):
    """Ingredient Group admin interface.
    """
    filter_horizontal = ('ingredients',)

admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientGroup)
