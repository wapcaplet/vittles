import os
import sys
import site

vepath = '/usr/local/pythonenv/VITTLES/lib/python2.6/site-packages'
site.addsitedir(vepath)
sys.path.append('/home/eric/git/vittles')
sys.path.append('/home/eric/git')

from django.core.handlers.wsgi import WSGIHandler
os.environ['DJANGO_SETTINGS_MODULE'] = 'vittles.settings'
application = WSGIHandler()

