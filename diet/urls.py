from django.conf.urls.defaults import patterns
from django.views.generic import list_detail
from django.views.generic.create_update import update_object, delete_object
from diet.models import Meal

# Diet
urlpatterns = patterns(
    'diet.views',
    (r'^$', 'index'),
    (r'^(?P<year>\d\d\d\d)-(?P<month>\d\d)/$', 'meal_calendar'),
    (r'^add_meal/(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)/$', 'add_meal'),

)

# Experiments

urlpatterns += patterns(
    '',
    (r'^meals/$', list_detail.object_list, {'queryset': Meal.objects.all()}),
    (r'^meals/(?P<object_id>\w+)/edit/$', update_object, {'model': Meal}),
    (r'^meals/(?P<object_id>\w+)/delete/$', delete_object, {'model': Meal, 'post_delete_redirect': '/diet/meals/'}),
)

