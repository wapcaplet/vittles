from django.contrib import admin
from core.models import FoodGroup, Food, Unit, Equivalence, Preparation, FoodNutritionInfo
#from nutrition.models import NutritionInfo

# Inline forms

class FoodGroupInline (admin.TabularInline):
    model = FoodGroup
    extra = 5
    fk_name = 'parent'
    verbose_name = 'Sub-group'
    verbose_name_plural = 'Sub-groups'

class EquivalenceInline (admin.TabularInline):
    model = Equivalence
    extra = 5
    fk_name = 'unit'

class FoodInline (admin.TabularInline):
    model = Food
    extra = 5

class FoodNutritionInfoInline (admin.TabularInline):
    model = FoodNutritionInfo
    extra = 1

# Main forms

class FoodGroupAdmin (admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    inlines = [FoodInline, FoodGroupInline]

class FoodAdmin (admin.ModelAdmin):
    inlines = [FoodNutritionInfoInline]
    ordering = ('name',)
    list_display = ('name', 'food_group', 'grams_per_ml')
    list_filter = ('food_group', 'grams_per_ml')
    list_editable = ('food_group', 'grams_per_ml')
    search_fields = ('name',)

class UnitAdmin (admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'abbreviation', 'kind')
    list_filter = ('kind',)
    list_editable = ('abbreviation', 'kind')
    inlines = [EquivalenceInline]

class EquivalenceAdmin (admin.ModelAdmin):
    ordering = ('unit', 'to_unit')
    list_filter = ('unit', 'to_unit')

class PreparationAdmin (admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(FoodGroup, FoodGroupAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Equivalence, EquivalenceAdmin)
admin.site.register(Preparation, PreparationAdmin)


