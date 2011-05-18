import os, sys
from django.core.management import setup_environ

# Add root project directory to import path
sys.path.append(os.path.abspath('.'))

# Include settings, so it's not necessary to set DJANGO_SETTINGS_MODULE
import settings
setup_environ(settings)

