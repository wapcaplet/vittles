from django.test import TestCase
from core.models import Food, Unit, Equivalence
from core.helpers import convert_unit, convert_amount, to_grams, to_ml, NoEquivalence

class ConversionTest (TestCase):
    fixtures = ['test_unit', 'test_food', 'test_equivalence']


class ConvertUnitTest (ConversionTest):
    """Test basic unit conversion.
    """
    def test_convert_unit(self):
        self.failUnlessEqual(convert_unit('pound', 'ounce'), 16)
        self.failUnlessEqual(convert_unit('ounce', 'pound'), 1.0 / 16)

    def test_convert_unit_without_equivalence(self):
        self.assertRaises(NoEquivalence, convert_unit, 'pound', 'quart')
        self.assertRaises(NoEquivalence, convert_unit, 'ounce', 'quart')


class ConvertDifferentUnitKindsTest (ConversionTest):
    """Test conversion between volume and weight.
    """
    def test_convert_volume_to_grams(self):
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


    def test_convert_weight_to_ml(self):
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


class ConvertAmountTest (ConversionTest):
    """Test conversion of amounts to other units.
    """
    def test_convert_amount(self):
        self.failUnlessEqual(convert_amount(2, 'pound', 'ounce'), 32)
        self.failUnlessEqual(convert_amount(4, 'ounce', 'pound'), 0.25)

    def test_convert_amount_without_equivalence(self):
        self.assertRaises(NoEquivalence, convert_amount, 2, 'pound', 'quart')
        self.assertRaises(NoEquivalence, convert_amount, 2, 'ounce', 'quart')



