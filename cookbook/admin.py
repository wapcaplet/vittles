from django import forms
from django.contrib import admin
from vittles.cookbook.models import Ingredient, Recipe, Portion, IngredientCategory, RecipeCategory
from vittles.core.helpers import fraction_to_float

# Custom forms and fields

class QuantityField (forms.Field):
    """A field for entering a quantity. Accepts decimal or fractional values.
    """
    def to_python(self, value):
        return fraction_to_float(value)

class IngredientForm (forms.ModelForm):
    quantity = QuantityField(label="Quantity",
        help_text="""Decimal or fraction value, like "1.75" or "1 3/4".""")
    class Meta:
        model = Ingredient

# Inline forms

class IngredientInline (admin.TabularInline):
    model = Ingredient
    form = IngredientForm
    extra = 8


# Main forms

class IngredientAdmin (admin.ModelAdmin):
    form = IngredientForm
    #fieldsets = (
        #(None, {'fields': (('quantity', 'unit', 'preparation', 'food'),)}),
    #)

class RecipeAdmin (admin.ModelAdmin):
    inlines = [IngredientInline]
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'category'),
                'preheat',
                'directions',
                ('num_portions', 'portion'),
                ('rating', 'source')
            )
        }),
    )

class PortionAdmin (admin.ModelAdmin):
    list_display = ('name', 'plural')

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Portion, PortionAdmin)
admin.site.register(IngredientCategory)
admin.site.register(RecipeCategory)

