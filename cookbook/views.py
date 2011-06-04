from django.shortcuts import render_to_response
from cookbook.models import Recipe

def cookbook(request):
    """Cookbook homepage.
    """
    recipes = Recipe.objects.all()
    categories = set(recipe.category for recipe in recipes)
    recipe_categories = []
    for category in categories:
        if category:
            category = category.name
        recipe_categories.append((category, recipes.filter(category__name=category)))

    variables = {
        'recipe_categories': recipe_categories,
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

