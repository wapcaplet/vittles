from django.contrib import admin
from diet.models import Meal, DietPlan, TargetServing, DietPlanNutritionInfo

# Inline forms

class TargetServingInline (admin.TabularInline):
    model = TargetServing
    extra = 5

class DietPlanNutritionInfoInline (admin.TabularInline):
    model = DietPlanNutritionInfo
    can_delete = False

# Main forms

class MealAdmin (admin.ModelAdmin):
    list_display = ('__unicode__', 'date')

class DietPlanAdmin (admin.ModelAdmin):
    inlines = [DietPlanNutritionInfoInline, TargetServingInline]

class TargetServingAdmin (admin.ModelAdmin):
    list_display = ('__unicode__', 'diet_plan')

admin.site.register(Meal, MealAdmin)
admin.site.register(DietPlan, DietPlanAdmin)
admin.site.register(TargetServing, TargetServingAdmin)

