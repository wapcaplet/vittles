from django import template
register = template.Library()

@register.filter
def times(count):
    return range(int(count))

@register.inclusion_tag('cookbook/nutrition_summary.html')
def nutrition_summary(nutrition_info):
    """Render the nutrition summary for the given `NutritionInfo`.
    """
    return {'nutrition_info': nutrition_info}

