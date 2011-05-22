from fractions import Fraction

def fractionize(quantity, denominator=16):
    """Convert the given quantity into a fraction, rounded to the nearest
    ``1 / denominator`` increment. For example, if `denominator` is 16, round
    the result to the nearest 1/16th.

    If `quantity` is less than 1.0, a simple fraction is returned:

        >>> fractionize(0.5)
        "1/2"

        >>> fractionize(0.33)
        "1/3"

        >>> fractionize(0.25)
        "1/4"

        >>> fractionize(0.125)
        "1/8"

        >>> fractionize(0.1)
        "1/10"

    If `quantity` is 1.0 or greater, a mixed fraction is returned:

        >>> fractionize(1.25)
        "1 1/4"

        >>> fractionize(2.75)
        "2 3/4"

        >>> fractionize(9.33)
        "9 1/3"

    All results are rounded to the nearest ``1 / denominator`` increment, so
    you can decide how precise you need the result to be:

        >>> fractionize(0.1875, 16)
        "3/16"

        >>> fractionize(0.1875, 8)
        "1/5"

        >>> fractionize(0.1875, 4)
        "1/4"

    """
    whole = int(quantity)
    frac = Fraction(str(quantity - whole)).limit_denominator(denominator)
    if whole > 0:
        if frac > 0:
            return "%d %s" % (whole, frac)
        else:
            return "%d" % whole
    else:
        return "%s" % frac


def format_food_unit(quantity, unit, food):
    """Return a string describing the given quantity of food.

    Examples:

        >>> format_food_unit(2, 'cup', 'flour')
        "2 cups flour"
        >>> format_food_unit(0.5, 'cup', 'oil')
        "1/2 cup oil"
        >>> format_food_unit(3, None, 'egg')
        "3 eggs"

    """
    string = fractionize(quantity)

    # Optional unit
    if unit:
        string += " %s" % unit

    # Pluralize the unit or the food
    if quantity > 1.0:
        if unit:
            string += "s %s" % food
        else:
            string += " %ss" % food
    else:
        string += " %s" % food

    return string

