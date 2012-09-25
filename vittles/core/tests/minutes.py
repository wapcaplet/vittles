from django.test import TestCase
from core.utils import string_to_minutes

class TimesTest (TestCase):
    def setUp(self):
        self.no_units = [
            ("5", 5),
            ("15", 15),
            ("45", 45),
        ]

        self.in_whole_hours = [
            ("1 hour", 60),
            ("2 hours", 120),
            ("3 hrs", 180),
        ]

        self.in_minutes = [
            ("1 minute", 1),
            ("5 minutes", 5),
            ("10 mins", 10),
        ]

        self.in_fractional_hours = [
            ("1-1/2 hour", 90),
            ("1/2 hr", 30),
            ("2.5 hrs", 150),
        ]

    def test_string_to_minutes_hours(self):
        """Convert strings with hours to minutes."""
        for text, minutes in self.in_whole_hours:
            self.assertEqual(string_to_minutes(text), minutes)

    def test_string_to_minutes_minutes(self):
        """Convert strings with minutes to minutes."""
        for text, minutes in self.in_minutes:
            self.assertEqual(string_to_minutes(text), minutes)

    def test_string_to_minutes_no_unit(self):
        """Convert strings with minutes to minutes."""
        for text, minutes in self.no_units:
            self.assertEqual(string_to_minutes(text), minutes)

    def test_string_to_minutes_fractional_hours(self):
        """Convert strings with minutes to minutes."""
        for text, minutes in self.in_fractional_hours:
            self.assertEqual(string_to_minutes(text), minutes)


