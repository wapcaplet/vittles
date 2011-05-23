from django import forms
from django.contrib import admin
from cookbook.models import Ingredient, Recipe, IngredientList
from core.helpers import fraction_to_float

# Custom forms and fields

class QuantityField (forms.Field):
    """A field for entering a quantity. Accepts decimal or fractional values.
    """
    def to_python(self, value):
        return fraction_to_float(value)

class IngredientForm (forms.ModelForm):
    quantity = QuantityField(
        help_text="""Decimal or fraction value, like "1.75" or "1 3/4".""")
    class Meta:
        model = Ingredient

# Inline forms

class IngredientInline (admin.TabularInline):
    model = IngredientList.ingredients.through
    form = IngredientForm

class IngredientListInline (admin.StackedInline):
    model = IngredientList
    extra = 1
    filter_horizontal = ('ingredients',)


# Main forms

class IngredientAdmin (admin.ModelAdmin):
    form = IngredientForm
    #fieldsets = (
        #(None, {'fields': (('quantity', 'unit', 'preparation', 'food'),)}),
    #)

class RecipeAdmin (admin.ModelAdmin):
    """Customized recipe admin interface, with ingredients included.
    """
    inlines = [IngredientListInline]
    fields = ('name', 'preheat', 'directions', 'servings')

class IngredientListAdmin (admin.ModelAdmin):
    """Ingredient Group admin interface.
    """
    #filter_horizontal = ('ingredients',)
    inlines = [IngredientInline]

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientList, IngredientListAdmin)

