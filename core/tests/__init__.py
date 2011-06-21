# Unit tests
from conversion import *
from amount import *
from nutrition import *
from formatting import *
from serialization import *
from filterspecs import *

# Doctests
from vittles.core.utils import \
        float_to_fraction, fraction_to_float, pluralize, format_food_unit

__test__ = {
    'float_to_fraction': float_to_fraction,
    'fraction_to_float': fraction_to_float,
    'format_food_unit': format_food_unit,
    'pluralize': pluralize,
}

