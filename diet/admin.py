from django.contrib import admin
from diet.models import Meal

class MealAdmin (admin.ModelAdmin):
    pass

admin.site.register(Meal, MealAdmin)

