from datetime import date
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from diet.models import Meal
from diet.helpers import MealCalendar
from diet.forms import MealForm

def diet(request):
    return render_to_response('diet/index.html', {})


def meal_calendar(request, year, month):
    year, month = int(year), int(month)
    meals = Meal.objects.order_by('date').filter(
        date__year=year, date__month=month
    )
    cal = MealCalendar(meals).formatmonth(year, month)
    return render_to_response('diet/meal_calendar.html', {'calendar': mark_safe(cal)})


def add_meal(request, year, month, day):
    meal_date = date(int(year), int(month), int(day))
    if request.method == 'GET':
        form = MealForm(initial = {'date': meal_date})
    else:
        form = MealForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/diet/%s' % meal_date.strftime('%Y-%m'))
    return render_to_response('diet/add_meal.html', {'form': form})

