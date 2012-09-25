from tastypie.resources import ModelResource
from tastypie.api import Api
from tastypie import fields
from core.models import Food, Unit
from cookbook.models import Recipe, Portion, RecipeCategory, Ingredient
from tastypie.constants import ALL

# Core

class FoodResource (ModelResource):
    class Meta:
        queryset = Food.objects.all()
        filtering = {
            'name': ALL,
        }

class UnitResource (ModelResource):
    class Meta:
        queryset = Unit.objects.all()

class PortionResource (ModelResource):
    class Meta:
        queryset = Portion.objects.all()

class RecipeCategoryResource (ModelResource):
    class Meta:
        queryset = RecipeCategory.objects.all()

class IngredientResource (ModelResource):
    class Meta:
        queryset = Ingredient.objects.all()

class RecipeResource (ModelResource):
    portion = fields.ForeignKey(PortionResource, 'portion')
    category = fields.ForeignKey(RecipeCategoryResource, 'category')
    ingredients = fields.ToManyField('rest.api.IngredientResource', 'ingredients')

    class Meta:
        queryset = Recipe.objects.all()

core_api = Api(api_name='core')
core_api.register(FoodResource())
core_api.register(UnitResource())

cookbook_api = Api(api_name='cookbook')
cookbook_api.register(PortionResource())
cookbook_api.register(RecipeResource())
cookbook_api.register(RecipeCategoryResource())
cookbook_api.register(IngredientResource())

