from django.contrib import admin
from diet.models import Meal, DietPlan, TargetServing, DietPlanNutrition

# Inline forms

class TargetServingInline (admin.TabularInline):
    model = TargetServing
    extra = 5

class DietPlanNutritionInline (admin.TabularInline):
    model = DietPlanNutrition
    can_delete = False

# Main forms

class MealAdmin (admin.ModelAdmin):
    list_display = ('__unicode__', 'date')

class DietPlanAdmin (admin.ModelAdmin):
    inlines = [DietPlanNutritionInline, TargetServingInline]

admin.site.register(Meal, MealAdmin)
admin.site.register(DietPlan, DietPlanAdmin)

