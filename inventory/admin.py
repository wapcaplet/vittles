from django.contrib import admin
from pyantry.inventory.models import ShoppingList, Provision

# Admin forms

class ProvisionAdmin (admin.ModelAdmin):
    fields = ('food', 'quantity', 'unit')

class ShoppingListAdmin (admin.ModelAdmin):
    filter_horizontal = ('foods',)

admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Provision, ProvisionAdmin)

