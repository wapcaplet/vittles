from django.contrib import admin
from vittles.core.models import Category, Food, Unit, Equivalence, Preparation

# Inline forms

class CategoryInline (admin.TabularInline):
    model = Category
    extra = 5
    fk_name = 'parent'
    verbose_name = 'Subcategory'
    verbose_name_plural = 'Subcategories'

class EquivalenceInline (admin.TabularInline):
    model = Equivalence
    extra = 5
    fk_name = 'unit'

class FoodInline (admin.TabularInline):
    model = Food
    extra = 5

# Main forms

class CategoryAdmin (admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    inlines = [FoodInline, CategoryInline]

class FoodAdmin (admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'category', 'grams_per_ml')
    list_filter = ('category',)
    list_editable = ('category', 'grams_per_ml')
    search_fields = ('name',)

class UnitAdmin (admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'abbreviation', 'kind')
    list_editable = ('abbreviation', 'kind')
    inlines = [EquivalenceInline]

class EquivalenceAdmin (admin.ModelAdmin):
    ordering = ('unit', 'to_unit')
    list_filter = ('unit', 'to_unit')

class PreparationAdmin (admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Equivalence, EquivalenceAdmin)
admin.site.register(Preparation, PreparationAdmin)


