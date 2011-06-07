from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'cookbook.views',
    url(r'^$', 'index', name='cookbook-index'),
    url(r'^(?P<recipe_id>\w+)/$', 'show_recipe', name='cookbook-show-recipe'),
)
