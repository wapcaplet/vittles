from django.conf.urls.defaults import include, patterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
)

# Cookbook
urlpatterns += patterns(
    'cookbook.views',
    (r'^cookbook/$', 'cookbook'),
    (r'^cookbook/(?P<recipe_id>\w+)/$', 'show_recipe'),
)

# Diet
urlpatterns += patterns(
    'diet.views',
    (r'^diet/$', 'diet'),
    (r'^diet/(?P<year>\d\d\d\d)-(?P<month>\d\d)/$', 'meal_calendar'),
    (r'^diet/add_meal/(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)/$', 'add_meal'),
)

