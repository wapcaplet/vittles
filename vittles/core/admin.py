from django.contrib import admin
from core.models import FoodGroup, Food, Unit, Equivalence, Preparation, FoodNutrition

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

class FoodNutritionInline (admin.TabularInline):
    model = FoodNutrition
    extra = 0
    fields = ('quantity', 'unit', 'calories', 'fat_calories',
              'fat', 'carb', 'sodium', 'protein', 'cholesterol')
    verbose_name = 'Nutrition information'
    verbose_name_plural = 'Nutrition information'

# Main forms

class FoodGroupAdmin (admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    inlines = [FoodInline, FoodGroupInline]

class FoodAdmin (admin.ModelAdmin):
    inlines = [FoodNutritionInline]
    ordering = ('name',)
    list_display = ('name', 'food_group', 'grams_per_ml', 'has_nutrition')
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

# Hack to allow --with-doctest to work with django-nose
# (http://mtrichardson.com/2009/05/testing-django-with-nose-and-with-doctest/)
try:
    admin.site.register(FoodGroup, FoodGroupAdmin)
    admin.site.register(Food, FoodAdmin)
    admin.site.register(Unit, UnitAdmin)
    admin.site.register(Equivalence, EquivalenceAdmin)
    admin.site.register(Preparation, PreparationAdmin)
except admin.sites.AlreadyRegistered:
    pass

