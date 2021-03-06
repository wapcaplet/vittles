from django.conf.urls.defaults import include, patterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^cookbook/', include('cookbook.urls')),
    (r'^diet/', include('diet.urls')),
)

