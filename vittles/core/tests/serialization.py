from django.test import TestCase
from django.core import serializers
from core.models import Food, Unit, Equivalence


class YamlSerializerTest (TestCase):
    """Test the custom YAML serializer.
    """
    def setUp(self):
        self.model_fields = [
            (Food, {'name': 'butter', 'grams_per_ml': 1.0, 'food_group': None}),
            (Food, {'name': 'flour', 'grams_per_ml': 0.5, 'food_group': None}),
            (Unit, {'name': 'ounce', 'abbreviation': 'oz', 'kind': 'weight'}),
            (Unit, {'name': 'gram', 'abbreviation': 'g', 'kind': 'weight'}),
            (Equivalence, {'unit_id': 1, 'to_quantity': 28.34, 'to_unit_id': 2}),
        ]
        # Note: Model and field order is wonky due to the nature of dicts
        self.yaml_text = '\n'.join([
            'core.equivalence:',
            '  1: {to_quantity: 28.34, to_unit: 2, unit: 1}',
            'core.food:',
            '  1: {food_group: null, grams_per_ml: 1.0, name: butter}',
            '  2: {food_group: null, grams_per_ml: 0.5, name: flour}',
            'core.unit:',
            '  1: {abbreviation: oz, kind: weight, name: ounce}',
            '  2: {abbreviation: g, kind: weight, name: gram}',
        ]) + '\n'


    def test_serialize(self):
        """Data is correctly serialized to YAML format.
        """
        objects = []
        for model, fields in self.model_fields:
            obj = model(**fields)
            obj.save()
            objects.append(obj)

        actual_yaml = serializers.serialize('yaml', objects)
        expect_yaml = self.yaml_text
        # Ensure output matches expected text
        self.assertEqual(expect_yaml, actual_yaml)


    def test_deserialize(self):
        """Data is correctly deserialized from YAML format.
        """
        foods = list(serializers.deserialize('yaml', self.yaml_text))

        # Ensure the correct number of objects were deserialized
        self.assertEqual(len(foods), len(self.model_fields))

        # Ensure the objects' data is correct
        for index, food in enumerate(foods):
            model, fields = self.model_fields[index]
            for field, value in fields.iteritems():
                actual = food.object.__getattribute__(field)
                self.assertEqual(actual, value)

