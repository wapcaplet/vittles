import re
from fractions import Fraction

def float_to_fraction(quantity, denominator=16):
    """Convert the given quantity into a fraction, rounded to the nearest
    ``1 / denominator`` increment. For example, if `denominator` is 16, round
    the result to the nearest 1/16th.

    If `quantity` is less than 1.0, a simple fraction is returned:

        >>> float_to_fraction(0.5)
        "1/2"

        >>> float_to_fraction(0.33)
        "1/3"

        >>> float_to_fraction(0.25)
        "1/4"

        >>> float_to_fraction(0.125)
        "1/8"

        >>> float_to_fraction(0.1)
        "1/10"

    If `quantity` is 1.0 or greater, a mixed fraction is returned, with a
    hyphen separating the integer part from the fractional part.

        >>> float_to_fraction(1.25)
        "1-1/4"

        >>> float_to_fraction(2.75)
        "2-3/4"

        >>> float_to_fraction(9.33)
        "9-1/3"

    All results are rounded to the nearest ``1 / denominator`` increment, so
    you can decide how precise you need the result to be:

        >>> float_to_fraction(0.1875, 16)
        "3/16"

        >>> float_to_fraction(0.1875, 8)
        "1/5"

        >>> float_to_fraction(0.1875, 4)
        "1/4"

    """
    whole = int(quantity)
    frac = Fraction(str(quantity - whole)).limit_denominator(denominator)
    if whole > 0:
        if frac > 0:
            return "%d-%s" % (whole, frac)
        else:
            return "%d" % whole
    else:
        return "%s" % frac


def fraction_to_float(fraction_string):
    """Convert a fraction string into a floating-point value.

    Simple fractions take the form of ``numerator/denominator``:

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


def pluralize(noun):
    """Pluralize the given noun, using a simple heuristic. Will pluralize
    some nouns incorrectly because English is beastly complicated.

    Consonant + 'o' gets '-es':

        >>> pluralize('potato')
        'potatoes'

    Sibilants get '-es':

        >>> pluralize('batch')
        'batches'
        >>> pluralize('box')
        'boxes'

    Consonant + 'y' becomes '-ies':

        >>> pluralize('cherry')
        'cherries'

    Endings of 'f' or 'fe' become '-ves':

        >>> pluralize('loaf')
        'loaves'
        >>> pluralize('bay leaf')
        'bay leaves'
        >>> pluralize('knife')
        'knives'

    Simple 's' ending:

        >>> pluralize('ounce')
        'ounces'
        >>> pluralize('egg')
        'eggs'

    """
    noun = str(noun)

    #vowel = '[aeiouy]'
    consonant = '[bcdfghjklmnpqrstvwxz]'

    # Nouns ending in 'o' preceded by a consonant are pluralized with '-es'
    # (vowel + 'o' will fall back on '-s')
    if re.search(consonant + 'o$', noun):
        return noun + 'es'

    # Nouns ending in 'y' preceded by a consonant drop the 'y' and add '-ies'
    # (vowel + 'y' will fall back on '-s')
    elif re.search(consonant + 'y$', noun):
        return noun[:-1] + 'ies'

    # Nouns ending with x, z, s, sh, ch usually get pluralized with '-es'
    elif re.search('(x|z|s|sh|ch)$', noun):
        return noun + 'es'

    # Nouns ending in 'f' drop the 'f' and add '-ves'
    elif re.search('f$', noun):
        return noun[:-1] + 'ves'

    # Nouns ending in 'fe' drop the 'fe' and add '-ves'
    elif re.search('fe$', noun):
        return noun[:-2] + 'ves'

    # Default case: just add '-s'
    else:
        return noun + 's'


def format_food_unit(quantity, unit, food):
    """Return a string describing the given quantity of food. `quantity` may be
    an actual number (int or float), or a string containing a decimal or
    fraction as understood by `fraction_to_float`.

    If a unit is given, the unit is pluralized when appropriate:

        >>> format_food_unit(2, 'cup', 'flour')
        "2 cups flour"
        >>> format_food_unit(1.5, 'teaspoon', 'salt')
        "1-1/2 teaspoons salt"
        >>> format_food_unit('1-3/4', 'ounce', 'butter')
        "1-3/4 ounces butter"

    If no unit is given, the food is pluralized:

        >>> format_food_unit(3, None, 'egg')
        "3 eggs"
        >>> format_food_unit(2, None, 'potato')
        "2 potatoes"
        >>> format_food_unit('4-1/2', None, 'bell pepper')
        "4-1/2 bell peppers"

    In all cases, if the quantity is <= 1, no pluralization is done:

        >>> format_food_unit(1, None, 'egg')
        "1 egg"
        >>> format_food_unit(0.75, 'cup', 'flour')
        "3/4 cup flour"
        >>> format_food_unit(0.5, 'cup', 'oil')
        "1/2 cup oil"
        >>> format_food_unit('1/4', 'teaspoon', 'baking powder')
        "1/4 teaspoon baking powder"

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


