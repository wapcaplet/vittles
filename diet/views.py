from datetime import datetime
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
#from django.utils.safestring import mark_safe
#from diet.models import Meal
from diet.forms import MealForm

def index(request):
    vars = {
        'this_month': datetime.today()
    }
    return render_to_response('diet/index.html', vars)


def meal_calendar(request, yyyy_mm=''):
    if yyyy_mm:
        date = datetime.strptime(yyyy_mm, '%Y-%m')
    else:
        date = datetime.today()

    vars = {
        'year': date.year,
        'month': date.month,
    }
    return render_to_response('diet/meal_calendar.html', vars)


def add_meal(request, yyyy_mm_dd):
    if yyyy_mm_dd:
        date = datetime.strptime(yyyy_mm_dd, '%Y-%m-%d')
    else:
        date = datetime.today()

    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/diet/meals/%s' % date.strftime('%Y-%m'))
    else:
        form = MealForm(initial = {'date': date})
    vars = {
        'form': form,
        'meal_date': date,
    }
    return render_to_response('diet/add_meal.html', vars)


