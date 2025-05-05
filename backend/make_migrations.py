import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planify.settings')
django.setup()

from django.core.management import call_command

# Faz as migrações
call_command('makemigrations')
call_command('migrate')
