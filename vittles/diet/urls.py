from django.conf.urls.defaults import patterns, url
from django.views.generic import create_update
from diet.models import Meal

# Diet
urlpatterns = patterns(
    'diet.views',
    url(r'^$', 'index', {}, 'diet_index'),
    url(r'^meals/$', 'meal_calendar', {}, 'diet_meal_calendar'),
    url(r'^meals/(?P<yyyy_mm>\d{4}-\d{2})/$', 'meal_calendar', {}, 'diet_meal_calendar'),
    url(r'^meals/(?P<yyyy_mm_dd>\d{4}-\d{2}-\d{2})/add/$', 'add_meal', {}, 'diet_meal_add'),
)

# Experiments

urlpatterns += patterns(
    '',
    url(r'^meals/(?P<object_id>\w+)/edit/$', create_update.update_object,
     {'model': Meal}, 'diet_meal_edit'),
    url(r'^meals/(?P<object_id>\w+)/delete/$', create_update.delete_object,
     {'model': Meal, 'post_delete_redirect': '/diet/meals/'}, 'diet_meal_delete'),
)

