from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Usuários'
    
    def ready(self):
        # Importar a extensão de autenticação para garantir que seja carregada
        import users.openapi
