
def format_food_unit(quantity, unit, food):
    """Return a string describing the given quantity of food.

    Examples:

        >>> format_food_unit(2, 'cup', 'flour')
        "2 cups flour"
        >>> format_food_unit(0.5, 'cup', 'oil')
        "1 cup oil"
        >>> format_food_unit(3, None, 'egg')
        "3 eggs"

    """
    # Quantity and optional unit
    if unit:
        string = "%g %s" % (quantity, unit)
    else:
        string = "%g" % quantity

    # Pluralize the unit or the food
    if quantity > 1.0:
        if unit:
            string += "s %s" % food
        else:
            string += " %ss" % food
    else:
        string += " %s" % food

    return string

