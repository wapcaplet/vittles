from django.test import TestCase
from django.contrib import admin
from core.models import Food
from core.admin import FoodAdmin
from django.test.client import RequestFactory
from django.contrib.admin.views.main import ChangeList


class RangeValuesFilterSpecTest (TestCase):
    def setUp(self):
        # FIXME: I don't understand most of what this is doing
        # Ideas borrowed from:
        # https://github.com/django/django
        #   /blob/master/tests/regressiontests/admin_filters/tests.py
        self.modeladmin = FoodAdmin(Food, admin.site)
        self.request_factory = RequestFactory()
        self.request = self.request_factory.get('/')
        self.change_list = ChangeList(
            self.request,
            Food,
            self.modeladmin.list_display,
            self.modeladmin.list_display_links,
            self.modeladmin.list_filter,
            self.modeladmin.date_hierarchy,
            self.modeladmin.search_fields,
            self.modeladmin.list_select_related,
            self.modeladmin.list_per_page,
            self.modeladmin.list_editable,
            self.modeladmin
        )


    def test_range_values_filter(self):
        """RangeValues filter on Food's grams_per_ml works.
        """
        filter_spec = self.change_list.get_filters(self.request)[0][0]
        self.assertEqual(filter_spec.title(), 'grams per ml')
        choices = list(filter_spec.choices(self.change_list))
        self.assertEqual(choices, [
            {
                'display': u'All',
                 'query_string': '?',
                 'selected': True
            },
            {
                'display': u'&lt; 0.5',
                'query_string': '?grams_per_ml__lt=0.5',
                'selected': False
            },
            {
                'display': u'0.5 - 1.0',
                'query_string': '?grams_per_ml__gte=0.5&grams_per_ml__lt=1.0',
                'selected': False
            },
            {
                'display': u'&ge; 1.0',
                'query_string': '?grams_per_ml__gte=1.0',
                'selected': False
            }
        ])

