from django.conf.urls.defaults import patterns
from django.views.generic import create_update
from diet.models import Meal

# Diet
urlpatterns = patterns(
    'diet.views',
    (r'^$', 'index'),
    (r'^meals/$', 'meal_calendar'),
    (r'^meals/(?P<year>\d\d\d\d)-(?P<month>\d\d)/$', 'meal_calendar'),
    (r'^meals/(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)/add/$', 'add_meal'),
)

# Experiments

urlpatterns += patterns(
    '',
    (r'^meals/(?P<object_id>\w+)/edit/$', create_update.update_object,
     {'model': Meal}),
    (r'^meals/(?P<object_id>\w+)/delete/$', create_update.delete_object,
     {'model': Meal, 'post_delete_redirect': '/diet/meals/'}),
)

