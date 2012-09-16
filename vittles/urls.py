from django.conf.urls.defaults import include, patterns
from django.contrib import admin

# Hack to allow --with-doctest to work with django-nose
# (http://mtrichardson.com/2009/05/testing-django-with-nose-and-with-doctest/)
try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    pass

urlpatterns = patterns(
    '',
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^core/', include('core.urls')),
    (r'^cookbook/', include('cookbook.urls')),
    (r'^diet/', include('diet.urls')),
)

