from django.contrib import admin
from pyantry.inventory.models import Provision

class ProvisionAdmin (admin.ModelAdmin):
    fields = ('food', 'quantity', 'unit')

admin.site.register(Provision, ProvisionAdmin)

