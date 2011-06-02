from django.contrib import admin
from diet.models import Meal, DietPlan, TargetServing

# Inline forms

class TargetServingInline (admin.TabularInline):
    model = TargetServing
    extra = 5

# Main forms

class MealAdmin (admin.ModelAdmin):
    list_display = ('__unicode__', 'date')

class DietPlanAdmin (admin.ModelAdmin):
    inlines = [TargetServingInline]

class TargetServingAdmin (admin.ModelAdmin):
    list_display = ('__unicode__', 'diet_plan')

admin.site.register(Meal, MealAdmin)
admin.site.register(DietPlan, DietPlanAdmin)
admin.site.register(TargetServing, TargetServingAdmin)

