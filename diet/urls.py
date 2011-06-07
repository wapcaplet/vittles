from django.conf.urls.defaults import patterns, url
from django.views.generic import create_update
from diet.models import Meal

# Diet
urlpatterns = patterns(
    'diet.views',
    url(r'^$', 'index', {}, 'diet-index'),
    url(r'^meals/$', 'meal_calendar', {}, 'diet-meal-calendar'),
    url(r'^meals/(?P<yyyy_mm>\d{4}-\d{2})/$', 'meal_calendar', {}, 'diet-meal-calendar'),
    url(r'^meals/(?P<yyyy_mm_dd>\d{4}-\d{2}-\d{2})/add/$', 'add_meal', {}, 'diet-meal-add'),
)

# Experiments

urlpatterns += patterns(
    '',
    url(r'^meals/(?P<object_id>\w+)/edit/$', create_update.update_object,
     {'model': Meal}, 'diet-meal-edit'),
    url(r'^meals/(?P<object_id>\w+)/delete/$', create_update.delete_object,
     {'model': Meal, 'post_delete_redirect': '/diet/meals/'}, 'diet-meal-delete'),
)

