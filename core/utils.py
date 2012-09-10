import re
from fractions import Fraction

def float_to_fraction(quantity, denominator=16):
    """Convert the given quantity into a fraction string, rounded to the nearest
    ``1 / denominator`` increment. For example, if `denominator` is 16, round
    the result to the nearest 1/16th.

    If `quantity` is less than 1.0, a simple fraction is returned:

        >>> float_to_fraction(0.5)
        u'1/2'

        >>> float_to_fraction(0.33)
        u'1/3'

        >>> float_to_fraction(0.25)
        u'1/4'

        >>> float_to_fraction(0.125)
        u'1/8'

        >>> float_to_fraction(0.1)
        u'1/10'

    If `quantity` is 1.0 or greater, a mixed fraction is returned, with a
    hyphen separating the integer part from the fractional part.

        >>> float_to_fraction(1.25)
        u'1-1/4'

        >>> float_to_fraction(2.75)
        u'2-3/4'

        >>> float_to_fraction(9.33)
        u'9-1/3'

    All results are rounded to the nearest ``1 / denominator`` increment, so
    you can decide how precise you need the result to be:

        >>> float_to_fraction(0.1875, 16)
        u'3/16'

        >>> float_to_fraction(0.1875, 8)
        u'1/5'

        >>> float_to_fraction(0.1875, 4)
        u'1/4'

    """
    whole = int(quantity)
    frac = Fraction(str(quantity - whole)).limit_denominator(denominator)
    if whole > 0:
        if frac > 0:
            return u'%d-%s' % (whole, frac)
        else:
            return u'%d' % whole
    else:
        return u'%s' % frac


def fraction_to_float(fraction_string):
    """Convert a fraction string into a floating-point value.

    Simple fractions take the form of "n/d":

        >>> fraction_to_float("1/2")
        0.5
        >>> fraction_to_float("3/8")
        0.375

    Mixed fractions may be separated by one or more spaces or hyphens.

        >>> fraction_to_float("1 1/4")
        1.25
        >>> fraction_to_float("1-1/4")
        1.25
        >>> fraction_to_float("1 - 1/4")
        1.25

    Any string that is already a decimal expression is just converted to
    its numeric form:

        >>> fraction_to_float("5.75")
        5.75
        >>> fraction_to_float(".5")
        0.5

    """
    result = 0.0
    for numpart in re.split('[ -]+', fraction_string):
        result += float(Fraction(numpart))
    return result


def pluralize(word):
    """Pluralize the given noun, using a simple heuristic. Will pluralize
    some nouns incorrectly because English is beastly complicated.
    """
    word = str(word)

    rules = (
        ('(?i)([^aeiouy])o$', '\\1oes'),        # potatoes, tomatoes
        ('(?i)([^aeiouy])y$', '\\1ies'),        # cherries, berries
        ('(?i)(x|z|s|sh|ch|ss)$', '\\1es'),     # boxes, radishes
        ('(?i)(f|fe)$', 'ves'),                 # loaves, leaves, knives
        ('(?i)$', 's'),
    )

    for expr, replace in rules:
        if re.search(expr, word):
            return re.sub(expr, replace, word)


def singularize(word):
    """Convert a plural word into singular form.
    """
    word = str(word)

    rules = (
        ('(?i)([^aeiouy])oes$', '\\1o'),        # potatoes, tomatoes
        ('(?i)([^aeiouy])ies$', '\\1y'),        # cherries, berries
        ('(?i)(x|z|s|sh|ch|ss)es$', '\\1'),     # boxes, radishes
        ('(?i)(chive|clove)s$', '\\1'),         # special cases of -ves
        ('(?i)ves$', 'f'),                      # loaves, leaves
        ('(?i)s$', ''),
    )

    for expr, replace in rules:
        if re.search(expr, word):
            return re.sub(expr, replace, word)


def format_food_unit(quantity, unit, food):
    """Return a unicode string describing the given quantity of food.
    `quantity` may be an actual number (int or float), or a string containing a
    decimal or fraction as understood by :py:func:`fraction_to_float`.

    If a unit is given, the unit is pluralized when appropriate:

        >>> format_food_unit(2, 'cup', 'flour')
        u'2 cups flour'
        >>> format_food_unit(1.5, 'teaspoon', 'salt')
        u'1-1/2 teaspoons salt'
        >>> format_food_unit('1-3/4', 'ounce', 'butter')
        u'1-3/4 ounces butter'

    If no unit is given, the food is pluralized:

        >>> format_food_unit(3, None, 'egg')
        u'3 eggs'
        >>> format_food_unit(2, None, 'potato')
        u'2 potatoes'
        >>> format_food_unit('4-1/2', None, 'bell pepper')
        u'4-1/2 bell peppers'

    In all cases, if the quantity is <= 1, no pluralization is done:

        >>> format_food_unit(1, None, 'egg')
        u'1 egg'
        >>> format_food_unit(0.75, 'cup', 'flour')
        u'3/4 cup flour'
        >>> format_food_unit(0.5, 'cup', 'oil')
        u'1/2 cup oil'
        >>> format_food_unit('1/4', 'teaspoon', 'baking powder')
        u'1/4 teaspoon baking powder'

    """
    # Convert quantity from string if necessary
    if type(quantity) in [str, unicode]:
        quantity = fraction_to_float(quantity)

    # Pluralize the unit or the food
    if quantity > 1.0:
        if unit:
            unit = pluralize(unit)
        else:
            food = pluralize(food)

    # Convert quantity back to a string
    string = float_to_fraction(quantity)

    # Add optional unit
    if unit:
        string += " %s %s" % (unit, food)
    else:
        string += " %s" % food

    return string


def parse_food_unit(text):
    """Parse a string containing a quantity, optional unit, and
    food name. Effectively the reverse of `format_food_unit`.

    Examples:

        >>> parse_food_unit("2 cups flour")
        (2.0, 'cup', 'flour')
        >>> parse_food_unit("3 eggs")
        (3.0, None, 'egg')
        >>> parse_food_unit("1-1/2 teaspoons salt")
        (1.5, 'teaspoon', 'salt')
    """
    parts = text.split(' ')

    # Assume quantity is the first part
    qty = fraction_to_float(parts.pop(0))

    # Assume unit is the next part
    if len(parts) == 1:
        unit = None
        food = singularize(' '.join(parts))
    else:
        unit = singularize(parts.pop(0))
        food = ' '.join(parts)

    return (qty, unit, food)

