from django.test import TestCase

from django.test.client import Client
from django.core.urlresolvers import reverse

class CookbookIndexTest (TestCase):
    def setUp(self):
        self.context = Client()

    def test_cookbook_index(self):
        index = self.context.get(reverse('cookbook-index'))
        self.assertEqual(index.status_code, 200)

        # Test templates rendered
        #print('templates:')
        #print([t.name for t in index.templates])

        # Test view context
        #print('context:')
        #print(index.context['recipe_categories'])


