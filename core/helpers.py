import re
from fractions import Fraction
from django.core.exceptions import ObjectDoesNotExist
from vittles.core.models import Equivalence


class NoEquivalence (Exception):
    pass


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
    string = float_to_fraction(quantity)

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


def convert_amount(quantity, unit, to_unit):
    """Convert a quantity in a given unit to the equivalent quantity in another
    unit. Requires that an `Equivalence` be defined for the relevant units; if
    no `Equivalence` is found, raise a `NoEquivalence` exception.
    """
    # If units are the same, no conversion is necessary
    if unit == to_unit:
        return quantity
    # Otherwise, try to find a direct mapping between units
    try:
        equivalence = Equivalence.objects.get(unit=unit, to_unit=to_unit)
    except ObjectDoesNotExist:
        # OK, see if there's a mapping in the other direction
        try:
            equivalence = Equivalence.objects.get(unit=to_unit, to_unit=unit)
        except ObjectDoesNotExist:
            raise NoEquivalence("Cannot convert '%s' to '%s'" % (unit, to_unit))
        # Got a reverse mapping -- divide
        else:
            return quantity / equivalence.to_quantity
    # Got a direct mapping -- multiply
    else:
        return quantity * equivalence.to_quantity


def add_amount(quantity, unit, to_quantity, to_unit):
    """Add two amounts together (possibly using different units),
    and return the resulting quantity in terms of the first unit.
    """
    return quantity + convert_amount(to_quantity, to_unit, unit)


def subtract_amount(quantity, unit, to_quantity, to_unit):
    """Subtract one amount from another (possibly using different units),
    and return the resulting quantity in terms of the first unit.
    """
    return quantity - convert_amount(to_quantity, to_unit, unit)


