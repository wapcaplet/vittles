from django.core.exceptions import ObjectDoesNotExist


class NoEquivalence (Exception):
    pass


def convert_unit(unit, to_unit):
    """Convert `unit` to the equivalent quantity `to_unit`. Requires that an
    :py:class:`Equivalence` be defined for the relevant units; if no `Equivalence` is
    found, raise a `NoEquivalence` exception.
    """
    from core.models import Equivalence

    # Degenerate case
    if str(unit) == str(to_unit):
        return 1.0

    # Try to find a direct mapping between units
    try:
        equivalence = Equivalence.objects.get(unit__name=unit, to_unit__name=to_unit)
    except ObjectDoesNotExist:
        # OK, see if there's a mapping in the other direction
        try:
            equivalence = Equivalence.objects.get(unit__name=to_unit, to_unit__name=unit)
        except ObjectDoesNotExist:
            raise NoEquivalence("Cannot convert '%s' to '%s'" % (unit, to_unit))
        # Got a reverse mapping -- divide
        else:
            return 1.0 / equivalence.to_quantity
    # Got a direct mapping -- multiply
    else:
        return equivalence.to_quantity


def to_grams(unit, food=None):
    """Return the given unit in terms of grams. If `unit` is a volume, attempt
    to convert based on the given food's density (g/ml). If `food` is not
    given, assume a density of 1.0 g/ml.
    """
    if not unit:
        raise NoEquivalence("Cannot convert '%s' to grams" % (unit))

    if unit.kind == 'weight':
        return convert_unit(unit, 'gram')
    elif unit.kind == 'volume':
        try:
            density = food.grams_per_ml
        except AttributeError:
            density = 1.0
        return density * convert_unit(unit, 'milliliter')
    else:
        raise NoEquivalence("Cannot convert '%s' to grams" % (unit))


def to_ml(unit, food=None):
    """Return the given unit in terms of milliliters. If `unit` is a weight,
    attempt to convert based on the given `food`'s density (g/ml). If `food` is
    not given, assume a density of 1.0 g/ml.
    """
    if not unit:
        raise NoEquivalence("Cannot convert '%s' to grams" % (unit))

    if unit.kind == 'volume':
        return convert_unit(unit, 'milliliter')
    elif unit.kind == 'weight':
        try:
            density = food.grams_per_ml
        except AttributeError:
            density = 1.0
        return convert_unit(unit, 'gram') / density
    else:
        raise NoEquivalence("Cannot convert '%s' to milliliters" % (unit))


def convert_amount(quantity, unit, to_unit):
    """Convert a quantity in a given unit to the equivalent quantity in another
    unit. Requires that an `Equivalence` be defined for the relevant units; if
    no `Equivalence` is found, raise a `NoEquivalence` exception.
    """
    if unit == to_unit:
        return quantity
    else:
        return quantity * convert_unit(unit, to_unit)


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


