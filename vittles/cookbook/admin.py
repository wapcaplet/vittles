from django import forms
from django.contrib import admin
from cookbook.models import Ingredient, Recipe, Portion, IngredientCategory, RecipeCategory
from core.utils import fraction_to_float

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

    actions = ['refresh_nutrition_info']

    def refresh_nutrition_info(self, request, queryset):
        """Custom action to recalculate the `RecipeNutritionInfo`
        for the selected recipes.
        """
        for recipe in queryset:
            recipe.nutrition_info.recalculate()
            recipe.save()

    refresh_nutrition_info.short_description = "Recalculate nutrition information"


class PortionAdmin (admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Portion, PortionAdmin)
admin.site.register(IngredientCategory)
admin.site.register(RecipeCategory)

