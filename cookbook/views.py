from django.shortcuts import render_to_response
from cookbook.models import Recipe

def index(request):
    """Cookbook homepage.
    """
    variables = {'recipes': Recipe.objects.all()}
    return render_to_response('index.html', variables)


def show_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    variables = {
        'recipe': recipe,
        'ingredient_lists': recipe.ingredient_lists.all(),
    }
    return render_to_response('recipe.html', variables)

