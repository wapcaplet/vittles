from django.test import TestCase
from core.utils import singularize, pluralize

class InflectionTest (TestCase):
    def setUp(self):
        self.words = [
            ('potato', 'potatoes'),
            ('tomato', 'tomatoes'),

            ('cherry', 'cherries'),
            ('berry', 'berries'),

            ('box', 'boxes'),
            ('radish', 'radishes'),
            ('kiss', 'kisses'),
            ('pinch', 'pinches'),
            ('dash', 'dashes'),

            ('loaf', 'loaves'),
            ('bay leaf', 'bay leaves'),

            ('ounce', 'ounces'),
            ('egg', 'eggs'),
            ('chive', 'chives'),
            ('slice', 'slices'),
            ('gram', 'grams'),
            ('pint', 'pints'),
            ('clove', 'cloves'),
        ]

    def test_singularize(self):
        """Singularize plural nouns"""
        for singular, plural in self.words:
            self.assertEqual(singularize(plural), singular)

    def test_pluralize(self):
        """Pluralize singular nouns"""
        for singular, plural in self.words:
            self.assertEqual(pluralize(singular), plural)

