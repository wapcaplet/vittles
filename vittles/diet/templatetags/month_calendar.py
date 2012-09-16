# Template tag
from datetime import date, timedelta
from django import template
from diet.models import Meal
from calendar import monthrange
from dateutil.relativedelta import relativedelta

register = template.Library()

@register.inclusion_tag('diet/_month_calendar.html')
def month_cal(year, month, weekday_name_format='%a'):
    event_list = Meal.objects.filter(date__year=year, date__month=month)

    first_day_of_month = date(year, month, 1)
    last_day_of_month = date(year, month, monthrange(year, month)[1])
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())

    calendar = []
    week = []
    headers = []

    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        if i < 7:
            headers.append(day.strftime(weekday_name_format))

        cal_day = {
            'day': day,
            'events': [e for e in event_list if e.date == day],
        }
        if day == date.today():
            cal_day['class'] = 'today'
        elif day.month != month:
            cal_day['class'] = 'other_month'

        week.append(cal_day)

        # Start a new week?
        if day.weekday() == 6:
            calendar.append(week)
            week = []

        i += 1
        day += timedelta(1)

    return {
        'this_month': date(year, month, 1),
        'prev_month': date(year, month, 1) + relativedelta(months=-1),
        'next_month': date(year, month, 1) + relativedelta(months=+1),
        'calendar': calendar,
        'headers': headers,
    }


