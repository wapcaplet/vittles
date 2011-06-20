from django.test import TestCase
from core.models import Food, Unit, Equivalence
from core.helpers import convert_unit, convert_amount, to_grams, to_ml, NoEquivalence

class ConversionTest (TestCase):
    fixtures = [
        'test_unit',
        'test_food',
        'test_equivalence',
    ]


class ConvertUnitTest (ConversionTest):
    """Test basic unit conversion.
    """
    def test_convert_unit(self):
        """Convert from one unit to another with direct Equivalence.
        """
        self.failUnlessEqual(convert_unit('pound', 'ounce'), 16)
        self.failUnlessEqual(convert_unit('ounce', 'pound'), 1.0 / 16)


    def test_convert_unit_reverse_equivalence(self):
        """Convert from one unit to another with reverse Equivalence.
        """
        # tablespoon --> teaspoon is defined in fixture, but
        # teaspoon --> tablespoon is not, and must use a reverse lookup
        self.failUnlessEqual(convert_unit('teaspoon', 'tablespoon'), 1.0 / 3.0)


    def test_convert_unit_without_equivalence(self):
        """NoEquivalence exception when converting units.
        """
        self.assertRaises(NoEquivalence, convert_unit, 'pound', 'quart')
        self.assertRaises(NoEquivalence, convert_unit, 'ounce', 'quart')


class ConvertToMilliliters (ConversionTest):
    """Test conversion of weights and volumes to milliliters.
    """
    def test_convert_volume_to_ml(self):
        """Convert units of volume to milliliters.
        """
        cup = Unit.objects.get(name='cup')
        ml_per_cup = convert_unit('cup', 'milliliter')
        self.failUnlessEqual(to_ml(cup), ml_per_cup)


    def test_convert_weight_to_ml(self):
        """Convert units of weight to milliliters.
        """
        # Two foods with very different densities
        honey = Food.objects.get(name='honey')
        paprika = Food.objects.get(name='paprika')
        # Two units of weight
        gram = Unit.objects.get(name='gram')
        ounce = Unit.objects.get(name='ounce')
        g_per_oz = Equivalence.objects.get(unit=ounce, to_unit=gram).to_quantity

        # Convert units of weight into milliliters
        # Without food, assume 1.0 g/ml
        self.failUnlessEqual(to_ml(gram), 1.0)
        self.failUnlessEqual(to_ml(ounce), g_per_oz)
        # With food, use its density
        self.failUnlessEqual(to_ml(gram, honey), 1.0 / honey.grams_per_ml)
        self.failUnlessEqual(to_ml(gram, paprika), 1.0 / paprika.grams_per_ml)
        self.failUnlessEqual(to_ml(ounce, honey), g_per_oz / honey.grams_per_ml)
        self.failUnlessEqual(to_ml(ounce, paprika), g_per_oz / paprika.grams_per_ml)


    def test_convert_to_ml_without_equivalence(self):
        """NoEquivalence when converting to milliliters without Equivalence.
        """
        slice, created = Unit.objects.get_or_create(name='slice', kind='individual')
        self.assertRaises(NoEquivalence, to_ml, slice)


    def test_convert_to_ml_without_unit(self):
        """NoEquivalence when converting to milliliters without Unit.
        """
        self.assertRaises(NoEquivalence, to_ml, None)


class ConvertToGrams (ConversionTest):
    """Test conversion from weight and volume to grams.
    """
    def test_convert_weight_to_grams(self):
        """Convert units of weight to grams.
        """
        pound = Unit.objects.get(name='pound')
        grams_per_pound = convert_unit('pound', 'gram')
        self.failUnlessEqual(to_grams(pound), grams_per_pound)

        kilo = Unit.objects.get(name='kilogram')
        grams_per_kilo = convert_unit('kilogram', 'gram')
        self.failUnlessEqual(to_grams(kilo), grams_per_kilo)


    def test_convert_volume_to_grams(self):
        """Convert units of volume to grams.
        """
        # Two foods with very different densities
        honey = Food.objects.get(name='honey')
        paprika = Food.objects.get(name='paprika')

        # Two units of volume
        ml = Unit.objects.get(name='milliliter')
        cup = Unit.objects.get(name='cup')
        ml_per_cup = Equivalence.objects.get(unit=cup, to_unit=ml).to_quantity

        # Convert units of volume into grams
        # Without food, assume 1.0 g/ml
        self.failUnlessEqual(to_grams(ml), 1.0)
        self.failUnlessEqual(to_grams(cup), 1.0 * ml_per_cup)
        # With food, use its density
        self.failUnlessEqual(to_grams(ml, honey), honey.grams_per_ml)
        self.failUnlessEqual(to_grams(ml, paprika), paprika.grams_per_ml)
        self.failUnlessEqual(to_grams(cup, honey), honey.grams_per_ml * ml_per_cup)
        self.failUnlessEqual(to_grams(cup, paprika), paprika.grams_per_ml * ml_per_cup)


    def test_convert_to_grams_without_equivalence(self):
        """NoEquivalence when converting to grams without Equivalence.
        """
        slice, created = Unit.objects.get_or_create(name='slice', kind='individual')
        self.assertRaises(NoEquivalence, to_grams, slice)


    def test_convert_to_grams_without_unit(self):
        """NoEquivalence when converting to grams without Unit.
        """
        self.assertRaises(NoEquivalence, to_grams, None)


class ConvertAmountTest (ConversionTest):
    """Test conversion of amounts to other units.
    """
    def test_convert_amount(self):
        """Convert an amount to a different unit.
        """
        self.failUnlessEqual(convert_amount(2, 'pound', 'ounce'), 32)
        self.failUnlessEqual(convert_amount(4, 'ounce', 'pound'), 0.25)

    def test_convert_amount_without_equivalence(self):
        """NoEquivalence when converting amounts without Equivalence.
        """
        self.assertRaises(NoEquivalence, convert_amount, 2, 'pound', 'quart')
        self.assertRaises(NoEquivalence, convert_amount, 2, 'ounce', 'quart')



