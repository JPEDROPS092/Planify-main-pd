from django.apps import AppConfig


class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customers'
    verbose_name = 'Clientes'

    def ready(self):
        # R4: conecta o carimbo de tenant_id no create dos models de negócio.
        from customers.scoping import register

        register()
