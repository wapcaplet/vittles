from django.contrib import admin
from pyantry.core.models import Category, Food, Unit, Equivalence

class CategoryAdmin (admin.ModelAdmin):
    list_display = ('name', 'parent')
    #list_editable = ('parent',)
    ordering = ('name',)

class FoodAdmin (admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    #list_editable = ('category',)
    ordering = ('name',)

class UnitAdmin (admin.ModelAdmin):
    list_display = ('name', 'abbr')
    list_editable = ('abbr',)
    ordering = ('name',)

class EquivalenceAdmin (admin.ModelAdmin):
    #list_display = ('__unicode__', 'unit', 'to_quantity', 'to_unit')
    ordering = ('unit', 'to_unit')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Equivalence, EquivalenceAdmin)

