from django.contrib import admin
from nutrition.models import NutritionInfo



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

    actions = ['normalize_nutrition_info']

    def normalize_nutrition_info(self, request, queryset):
        """Custom admin action to "normalize" all the given `NutritionInfo`
        objects, setting their serving size to 1, and adjusting all other
        attributes accordingly.
        """
        for nutrition_info in queryset:
            nutrition_info.normalize()
    normalize_nutrition_info.short_description = "Normalize quantity to 1.0"

admin.site.register(NutritionInfo, NutritionInfoAdmin)

