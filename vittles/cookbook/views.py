from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from cookbook.models import Recipe
from cookbook.forms import RecipeForm
from core.helpers import group_by_category

def index(request):
    """Cookbook homepage.
    """
    variables = {
        'recipe_categories': group_by_category(Recipe.objects.all()),
    }
    return render_to_response('cookbook/index.html', variables)


def show_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    variables = {
        'recipe': recipe,
        'serving': recipe.portion or 'serving',
        'nutrition': recipe.nutrition,
    }
    return render_to_response('cookbook/recipe.html', variables)


def add_recipe(request):
    """Add a new recipe.
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cookbook/')
    else:
        form = RecipeForm()
    vars = {
        'form': form,
    }
    return render_to_response('cookbook/add_recipe.html', vars)

