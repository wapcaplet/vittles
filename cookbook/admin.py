from django.contrib import admin
from pyantry.cookbook.models import Preparation, Ingredient, Recipe

admin.site.register(Preparation)
admin.site.register(Ingredient)
admin.site.register(Recipe)

