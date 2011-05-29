from django.contrib import admin
from nutrition.models import NutritionInfo

class NutritionInfoAdmin (admin.ModelAdmin):
    list_display = (
        '__unicode__', 'serving_size', 'serving_unit',
        'calories', 'fat_calories',
        'fat', 'carb', 'sodium', 'protein', 'cholesterol')
    fieldsets = (
        (None, {
            'fields': (
                'food',
                ('serving_size', 'serving_unit'),
                ('calories', 'fat_calories'),
                'fat', 'carb', 'sodium', 'protein', 'cholesterol',
            )
        }),
    )

admin.site.register(NutritionInfo, NutritionInfoAdmin)

