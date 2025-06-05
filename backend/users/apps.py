from django.apps import AppConfig
from django.contrib import admin


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Usuários'
    
    def ready(self):
        # Importar a extensão de autenticação para garantir que seja carregada
        import users.openapi
        
        # Configure admin site
        admin.site.enable_nav_sidebar = True
        admin.site.site_url = None  # Disable "View Site" link
