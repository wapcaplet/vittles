from datetime import date
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from diet.models import Meal
from diet.helpers import MealCalendar
from diet.forms import MealForm

def index(request):
    vars = {
        'this_month': date.today()
    }
    return render_to_response('diet/index.html', vars)


def meal_calendar(request, year, month):
    year, month = int(year), int(month)
    meals = Meal.objects.order_by('date').filter(
        date__year=year, date__month=month
    )
    cal = MealCalendar(meals).formatmonth(year, month)
    vars = {
        'calendar': mark_safe(cal),
    }
    return render_to_response('diet/meal_calendar.html', vars)


def add_meal(request, year, month, day):
    meal_date = date(int(year), int(month), int(day))
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/diet/%s' % meal_date.strftime('%Y-%m'))
    else:
        form = MealForm(initial = {'date': meal_date})
    vars = {
        'form': form,
        'meal_date': meal_date,
    }
    return render_to_response('diet/add_meal.html', vars)


