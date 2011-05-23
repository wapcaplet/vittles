from django.contrib import admin
from vittles.cookbook.models import Ingredient, Recipe, IngredientList

# Inline forms

class IngredientListInline (admin.StackedInline):
    model = IngredientList
    extra = 1
    filter_horizontal = ('ingredients',)


# Main forms

class IngredientAdmin (admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (('quantity', 'unit', 'preparation', 'food'),)}),
    )

class RecipeAdmin (admin.ModelAdmin):
    """Customized recipe admin interface, with ingredients included.
    """
    inlines = [IngredientListInline]
    fields = ('name', 'preheat', 'directions', 'servings')

class IngredientListAdmin (admin.ModelAdmin):
    """Ingredient Group admin interface.
    """
    filter_horizontal = ('ingredients',)

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientList, IngredientListAdmin)

