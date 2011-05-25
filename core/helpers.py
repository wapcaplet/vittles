from django.core.exceptions import ObjectDoesNotExist
from vittles.core.models import Equivalence


class NoEquivalence (Exception):
    pass


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


