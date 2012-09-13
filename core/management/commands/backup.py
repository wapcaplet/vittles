import os
import sys
from django.core.management.base import BaseCommand
from django.core.management import call_command

# TODO: Support command-line args for app name(s) and backup directory

class Command (BaseCommand):
    help = "Backup the database to YAML format"

    def handle(self, *args, **options):
        backup_dir = os.path.join(os.path.abspath('.'), 'db_backup')
        if not os.path.isdir(backup_dir):
            os.mkdir(backup_dir)

        apps = ['core', 'nutrition', 'cookbook', 'diet']
        real_stdout = sys.stdout
        for app in apps:
            yaml_file = os.path.join(backup_dir, '%s.yaml' % app)
            sys.stdout = real_stdout
            print("%s -> %s" % (app, yaml_file))
            sys.stdout = open(yaml_file, 'w')
            call_command('dumpdata', app, format='yaml')
            sys.stdout.close()
        sys.stdout = real_stdout

