from django import template
register = template.Library()

@register.filter
def times(count):
    return range(int(count))

@register.inclusion_tag('cookbook/_nutrition_summary.html')
def nutrition_summary(nutrition):
    """Render the nutrition summary for the given `Nutrition`.
    """
    return {'nutrition': nutrition}

