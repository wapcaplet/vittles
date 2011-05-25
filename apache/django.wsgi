import os
import sys
import site

vepath = '/usr/local/pythonenv/VITTLES/lib/python2.6/site-packages'
site.addsitedir(vepath)
sys.path.append('/var/www')

#prev_sys_path = list(sys.path)

#new_sys_path = []
#for item in list(sys.path):
    #if item not in prev_sys_path:
        #print(item)
        #new_sys_path.append(item)
        #sys.path.remove(item)
#sys.path[:0] = new_sys_path


#print("sys.path:")
#print(sys.path)
#import django

from django.core.handlers.wsgi import WSGIHandler
os.environ['DJANGO_SETTINGS_MODULE'] = 'vittles.settings'
application = WSGIHandler()

