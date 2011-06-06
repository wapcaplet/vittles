from django.conf.urls.defaults import patterns

urlpatterns = patterns(
    'cookbook.views',
    (r'^$', 'index'),
    (r'^(?P<recipe_id>\w+)/$', 'show_recipe'),
)
