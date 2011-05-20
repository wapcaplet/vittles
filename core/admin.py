from django.contrib import admin
from pyantry.core.models import Category, Food, Unit, Equivalence, Amount, Preparation

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

# Admin forms

class CategoryAdmin (admin.ModelAdmin):
    list_display = ('name', 'parent')
    #list_editable = ('parent',)
    ordering = ('name',)
    inlines = [FoodInline, CategoryInline]

class FoodAdmin (admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    #list_editable = ('category',)
    ordering = ('name',)

class UnitAdmin (admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'pluralizable')
    list_editable = ('abbreviation', 'pluralizable')
    ordering = ('name',)
    inlines = [EquivalenceInline]

class EquivalenceAdmin (admin.ModelAdmin):
    #list_display = ('__unicode__', 'unit', 'to_quantity', 'to_unit')
    ordering = ('unit', 'to_unit')
    list_filter = ('unit', 'to_unit')

class AmountAdmin (admin.ModelAdmin):
    ordering = ('quantity', 'unit')

class PreparationAdmin (admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Equivalence, EquivalenceAdmin)
admin.site.register(Amount, AmountAdmin)
admin.site.register(Preparation, PreparationAdmin)


