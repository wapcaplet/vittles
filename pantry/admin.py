from django.contrib import admin
from pyantry.pantry.models import Provision

class ProvisionAdmin (admin.ModelAdmin):
    fields = ('food', 'quantity', 'unit')

admin.site.register(Provision, ProvisionAdmin)

