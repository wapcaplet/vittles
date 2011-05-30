from django.contrib import admin
from nutrition.models import NutritionInfo

def normalize_nutrition_info(modeladmin, request, queryset):
    """Custom admin action to "normalize" all the given `NutritionInfo`
    objects, setting their serving size to 1, and adjusting all other
    attributes accordingly.
    """
    for nutrition_info in queryset:
        nutrition_info.normalize()
normalize_nutrition_info.short_description = "Adjust serving size to 1.0"


class NutritionInfoAdmin (admin.ModelAdmin):
    list_display = (
        '__unicode__', 'quantity', 'unit',
        'calories', 'fat_calories',
        'fat', 'carb', 'sodium', 'protein', 'cholesterol')
    fieldsets = (
        (None, {
            'fields': (
                'food',
                ('quantity', 'unit'),
                ('calories', 'fat_calories'),
                'fat', 'carb', 'sodium', 'protein', 'cholesterol',
            )
        }),
    )
    list_filter = ('unit',)
    actions = [normalize_nutrition_info]

admin.site.register(NutritionInfo, NutritionInfoAdmin)

