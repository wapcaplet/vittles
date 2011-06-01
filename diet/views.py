from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from diet.models import Meal
from diet.helpers import MealCalendar

def meal_calendar(request, year, month):
    year, month = int(year), int(month)
    meals = Meal.objects.order_by('date').filter(
        date__year=year, date__month=month
    )
    cal = MealCalendar(meals).formatmonth(year, month)
    return render_to_response('meal_calendar.html', {'calendar': mark_safe(cal)})

