from tastypie.resources import ModelResource
from tastypie.api import Api
from core.models import Food, Unit
from cookbook.models import Recipe

class FoodResource (ModelResource):
    class Meta:
        queryset = Food.objects.all()
        resource_name = 'food'

class UnitResource (ModelResource):
    class Meta:
        queryset = Unit.objects.all()
        resource_name = 'unit'

class RecipeResource (ModelResource):
    class Meta:
        queryset = Recipe.objects.all()
        resource_name = 'recipe'

core_api = Api(api_name='core')
core_api.register(FoodResource())
core_api.register(UnitResource())

cookbook_api = Api(api_name='cookbook')
cookbook_api.register(RecipeResource())

