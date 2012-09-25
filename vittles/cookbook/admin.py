from django import forms
from django.contrib import admin
from cookbook.models import Ingredient, Recipe, Portion, IngredientCategory, RecipeCategory
from support.utils import fraction_to_float, string_to_minutes

# Custom forms and fields

class QuantityField (forms.Field):
    """A field for entering a quantity. Accepts decimal or fractional values.
    """
    def to_python(self, value):
        return fraction_to_float(value)

class TimeField (forms.Field):
    """A field for entering a duration of time in minutes or hours.
    """
    def to_python(self, value):
        return string_to_minutes(value)

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

class RecipeAdmin (admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ('name', 'source')
    search_fields = ('name', 'source')
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'category'),
                'preheat',
                ('prep_minutes', 'inactive_prep_minutes', 'cook_minutes'),
                'directions',
                ('num_portions', 'portion'),
                ('rating', 'source'),
                'photo',
            )
        }),
    )

    actions = ['refresh_nutrition']

    def refresh_nutrition(self, request, queryset):
        """Custom action to recalculate the `RecipeNutrition`
        for the selected recipes.
        """
        for recipe in queryset:
            recipe.nutrition.recalculate()
            recipe.save()

    refresh_nutrition.short_description = "Recalculate nutrition information"


class PortionAdmin (admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Portion, PortionAdmin)
admin.site.register(IngredientCategory)
admin.site.register(RecipeCategory)

