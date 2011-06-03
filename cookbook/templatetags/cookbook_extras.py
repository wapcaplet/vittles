from django import template
register = template.Library()

@register.filter
def times(count):
    return range(int(count))

@register.inclusion_tag('nutrition_info.html')
def show_nutrition(nutrition_info):
    """Render the nutrition template for the given `NutritionInfo`.
    """
    return {'nutrition_info': nutrition_info}

