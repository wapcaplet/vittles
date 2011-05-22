from django.contrib import admin
from vittles.cookbook.models import Ingredient, Recipe, IngredientGroup

# Inline forms

class IngredientInline (admin.TabularInline):
    model = Recipe.ingredients.through
    verbose_name = 'ingredient'
    verbose_name_plural = 'ingredients'

class IngredientGroupInline (admin.StackedInline):
    model = IngredientGroup
    extra = 0
    filter_horizontal = ('ingredients',)


# Main forms

class RecipeAdmin (admin.ModelAdmin):
    """Customized recipe admin interface, with ingredients included.
    """
    inlines = [IngredientGroupInline]
    fields = ('name', 'ingredients', 'preheat', 'directions', 'servings')
    filter_horizontal = ('ingredients',)

class IngredientGroupAdmin (admin.ModelAdmin):
    """Ingredient Group admin interface.
    """
    filter_horizontal = ('ingredients',)

admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientGroup)
