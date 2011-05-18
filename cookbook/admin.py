from django.contrib import admin
from pyantry.cookbook.models import Preparation, Ingredient, Recipe

class IngredientInline (admin.TabularInline):
    """Displays ingredients in a table, with 10 rows.
    """
    model = Recipe.ingredients.through
    verbose_name = 'ingredient'
    verbose_name_plural = 'ingredients'
    #fields = ('food', 'quantity', 'preparation', 'unit')
    #extra = 10

class RecipeAdmin (admin.ModelAdmin):
    """Customized recipe admin interface, with ingredients included.
    """
    #inlines = [IngredientInline]
    #exclude = ('ingredients',)
    filter_horizontal = ('ingredients',)
    #list_display = ('name', 'servings', 'directions', 'ingredients')

admin.site.register(Preparation)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)

