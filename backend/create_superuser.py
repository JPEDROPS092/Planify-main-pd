from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

def create_superuser():
    User = get_user_model()
    
    # Check if superuser already exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print('Superuser created successfully!')
    else:
        print('Superuser already exists.')
