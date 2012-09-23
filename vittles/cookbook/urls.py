from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'cookbook.views',
    url(r'^$', 'index', name='cookbook_index'),
    url(r'^add/$', 'add_recipe', name='cookbook_add_recipe'),
    url(r'^(?P<recipe_id>\w+)/$', 'show_recipe', name='cookbook_show_recipe'),
)
