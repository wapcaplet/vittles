from django.shortcuts import render_to_response
from cookbook.models import Recipe
from core.helpers import group_by_category

def index(request):
    """Cookbook homepage.
    """
    variables = {
        'recipe_categories': group_by_category(Recipe.objects.all()),
    }
    return render_to_response('cookbook/index.html', variables)


def show_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    variables = {
        'recipe': recipe,
        'serving': recipe.portion or 'serving',
        'nutrition_info': recipe.nutrition_info,
    }
    return render_to_response('cookbook/recipe.html', variables)

