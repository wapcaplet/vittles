#! /usr/bin/env python
import os
import sys
import site

venvpath = '/home/eric/.virtualenvs/vittles/lib/python2.7/site-packages/'
site.addsitedir(venvpath)
sys.path.append('/var/www/vittles')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

