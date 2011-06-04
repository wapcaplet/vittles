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

class IngredientAdmin (admin.ModelAdmin):
    form = IngredientForm
    #fieldsets = (
        #(None, {'fields': (('quantity', 'unit', 'preparation', 'food'),)}),
    #)

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
            )
        }),
    )

    actions = ['refresh_nutrition_info']

    def refresh_nutrition_info(self, request, queryset):
        """Custom action to recalculate the `RecipeNutritionInfo`
        for the selected recipes.
        """
        status = []
        for recipe in queryset:
            status.append(recipe.nutrition_info.recalculate())
            recipe.save()
        message = str(status.count(True)) + \
            " recipes with complete nutritional info; " + \
            str(status.count(False)) + \
            " recipes are missing some nutritional info."
        self.message_user(request, message)

    refresh_nutrition_info.short_description = "Recalculate nutrition information"


class PortionAdmin (admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Portion, PortionAdmin)
admin.site.register(IngredientCategory)
admin.site.register(RecipeCategory)

