from django.shortcuts import render_to_response
from vittles.cookbook.models import Recipe

def index(request):
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
    return render_to_response('index.html', variables)


def show_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    variables = {
        'recipe': recipe,
    }
    return render_to_response('recipe.html', variables)

