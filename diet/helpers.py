from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from django.utils.html import conditional_escape as esc


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
        if day == 0:
            return self.day_cell('noday', '&nbsp;')

        cssclass = self.cssclasses[weekday]
        if date.today() == date(self.year, self.month, day):
            cssclass += ' today'


        if day in self.meals:
            cssclass += ' filled'
            body = ['<ul>']
            for meal in self.meals[day]:
                body.append('<li>')
                #body.append('<a href="%s">' % meal.get_absolute_url())
                body.append(esc(meal.kind))
                #body.append('</a>')
                body.append('</li>')
            body.append('</ul>')
            return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))

        return self.day_cell(cssclass, day)


    def formatmonth(self, year, month):
        self.year = year
        self.month = month
        return super(MealCalendar, self).formatmonth(year, month)


    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


