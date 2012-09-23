import os
import sys
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command (BaseCommand):
    help = "Restore the database from YAML files"

    def handle(self, *args, **options):
        backup_dir = os.path.join(os.path.abspath('.'), 'db_backup')
        if not os.path.isdir(backup_dir):
            os.mkdir(backup_dir)

        apps = ['core', 'nutrition', 'cookbook', 'diet']
        for app in apps:
            yaml_file = os.path.join(backup_dir, '%s.yaml' % app)
            print("%s -> %s" % (yaml_file, app))
            call_command('loaddata', yaml_file)

