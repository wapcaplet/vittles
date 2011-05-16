from django.contrib import admin
from pyantry.core.models import Category, Food, Unit, Equivalence

class FoodAdmin (admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

admin.site.register(Category)
admin.site.register(Food, FoodAdmin)
admin.site.register(Unit)
admin.site.register(Equivalence)

