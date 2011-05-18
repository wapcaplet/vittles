from django.contrib import admin
from pyantry.inventory.models import Place, Provision

class ProvisionInline (admin.TabularInline):
    model = Provision
    extra = 10
    fields = ('food', 'quantity', 'unit')

class ProvisionAdmin (admin.ModelAdmin):
    fields = ('food', 'quantity', 'unit', 'place')
    list_filter = ('place',)

class PlaceAdmin (admin.ModelAdmin):
    inlines = [ProvisionInline]

admin.site.register(Provision, ProvisionAdmin)
admin.site.register(Place, PlaceAdmin)

