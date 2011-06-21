from django.test import TestCase
from django.core import serializers
from core.models import Food
import yaml


class YamlSerializerTest (TestCase):
    """Test the custom YAML serializer.
    """
    def setUp(self):
        self.butter, created = Food.objects.get_or_create(name='butter')
        self.flour, created = Food.objects.get_or_create(name='flour')


    def test_serialize(self):
        """Data is correctly serialized to YAML format.
        """
        yaml_text = serializers.serialize('yaml', Food.objects.all())
        self.assertEqual(
            yaml.load(yaml_text), {
                'core.food': {
                    1: {'food_group': None, 'grams_per_ml': 1.0, 'name': 'butter'},
                    2: {'food_group': None, 'grams_per_ml': 1.0, 'name': 'flour'},
                }
            }
        )


    def test_deserialize(self):
        """Data is correctly deserialized from YAML format.
        """
        yaml_text = """
            core.food:
                1: {food_group: null, grams_per_ml: 1.0, name: butter}
                2: {food_group: null, grams_per_ml: 1.0, name: flour}
            """
        foods = [obj for obj in serializers.deserialize('yaml', yaml_text)]
        self.assertEqual(foods[0].object, self.butter)
        self.assertEqual(foods[1].object, self.flour)


    def test_roundtrip(self):
        """Data is successfully serialized, then deserialized.
        """
        yaml_text = serializers.serialize('yaml', Food.objects.all())
        foods = [obj for obj in serializers.deserialize('yaml', yaml_text)]
        self.assertEqual(foods[0].object, self.butter)
        self.assertEqual(foods[1].object, self.flour)


