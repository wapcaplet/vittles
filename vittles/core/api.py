from tastypie.resources import ModelResource
from tastypie.api import Api
from core.models import Food, Unit

class FoodResource (ModelResource):
    class Meta:
        queryset = Food.objects.all()
        resource_name = 'food'

class UnitResource (ModelResource):
    class Meta:
        queryset = Unit.objects.all()
        resource_name = 'unit'

core_api = Api(api_name='api')
core_api.register(FoodResource())
core_api.register(UnitResource())

