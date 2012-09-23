from django.conf.urls.defaults import patterns, url, include
from rest.api import core_api, cookbook_api

urlpatterns = patterns(
    'rest.views',
    url(r'^api/', include(core_api.urls)),
    url(r'^api/', include(cookbook_api.urls)),
)

