from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from django.utils.html import conditional_escape as esc
from django.template import loader, Context


class MealCalendar (HTMLCalendar):
    """Displays scheduled meals in an HTML calendar.
    """
    def __init__(self, meals):
        super(MealCalendar, self).__init__()
        self.meals = self.group_by_day(meals)
        print(self.meals)


    def group_by_day(self, meals):
        """Group the given Meals by day.
        """
        def field(meal):
            return meal.date.day

        return dict(
            [(day, list(items)) for day, items in groupby(meals, field)]
        )


    def formatday(self, day, weekday):
        day_template = loader.get_template('diet/meal_calendar_day.html')
        vars = {
            'css_class': self.cssclasses[weekday],
            'day': day,
        }
        if day > 0:
            cell_date = date(self.year, self.month, day)
            vars['yyyy_mm_dd'] = cell_date.strftime('%Y-%m-%d')

            if date.today() == cell_date:
                vars['css_class'] += ' today'

            if day in self.meals:
                vars['css_class'] += ' filled'
                vars['meals'] = self.meals[day]

        return day_template.render(Context(vars))


    def formatmonth(self, year, month):
        self.year = year
        self.month = month
        return super(MealCalendar, self).formatmonth(year, month)


