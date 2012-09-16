from django.conf.urls.defaults import patterns, url, include
from core.api import core_api

urlpatterns = patterns(
    'core.views',
    (r'', include(core_api.urls)),
)
