from django.forms import ModelForm
from cookbook.models import Recipe

class RecipeForm (ModelForm):
    class Meta:
        model = Recipe

