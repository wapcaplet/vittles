import re
from fractions import Fraction

def float_to_fraction(quantity, denominator=16):
    """Convert the given quantity into a fraction string. The ``denominator``
    argument limits how large the fraction's denominator is allowed to be
    (though the denominator may be smaller if it gives a better approximation
    to the original value).
    """
    whole = int(quantity)
    frac = Fraction(unicode(quantity - whole)).limit_denominator(denominator)
    if whole > 0:
        if frac > 0:
            return u'%d-%s' % (whole, frac)
        else:
            return u'%d' % whole
    else:
        return u'%s' % frac


def fraction_to_float(fraction_string):
    """Convert a fraction string into a floating-point value. Fractions may be
    simple (like ``3/4``), or mixed with a hyphen between the whole and
    fractional parts (like ``1-1/2`` or ``3-2/3``).
    """
    result = 0.0
    for numpart in re.split('[ -]+', fraction_string):
        result += float(Fraction(numpart))
    return result


def pluralize(word):
    """Pluralize the given noun, using a simple heuristic. Will pluralize
    some nouns incorrectly because English is beastly complicated.
    """
    word = unicode(word)

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
    word = unicode(word)

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
        (2.0, u'cup', u'flour')
        >>> parse_food_unit("3 eggs")
        (3.0, None, u'egg')
        >>> parse_food_unit("1-1/2 teaspoons salt")
        (1.5, u'teaspoon', u'salt')
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
        food = unicode(' '.join(parts))

    return (qty, unit, food)

