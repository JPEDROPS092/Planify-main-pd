"""Ponto único de leitura da customização por tenant (R5).

Todo o código de negócio que precise variar comportamento por empresa deve
consultar as flags/config **por aqui**, em vez de espalhar regras pelo código::

    from customers.config import get_tenant_settings, tenant_feature_enabled

    if tenant_feature_enabled(request.tenant, 'chat_anexos'):
        ...

    limite = get_tenant_settings(request.tenant).get_config('limite_projetos', 50)

As ``TenantSettings`` são criadas automaticamente para todo ``Client`` novo (ver
``register_tenant_settings``), e ``get_tenant_settings`` cria com defaults na
primeira leitura — cobrindo tenants pré-existentes.
"""
from django.db.models.signals import post_save


def get_tenant_settings(tenant):
    """Retorna (criando se preciso) as ``TenantSettings`` do tenant.

    ``tenant`` pode ser um ``Client`` ou ``None`` (ex.: superuser global) — neste
    caso retorna ``None`` (sem customização aplicável).
    """
    if tenant is None:
        return None
    from customers.models import TenantSettings

    settings, _ = TenantSettings.objects.get_or_create(tenant=tenant)
    return settings


def tenant_feature_enabled(tenant, key, default=False):
    """Atalho booleano para uma feature-flag do tenant."""
    settings = get_tenant_settings(tenant)
    if settings is None:
        return default
    return settings.is_feature_enabled(key, default=default)


def _create_tenant_settings(sender, instance, created, **kwargs):
    if not created:
        return
    from customers.models import TenantSettings

    TenantSettings.objects.get_or_create(tenant=instance)


def register_tenant_settings():
    """Conecta a criação automática de ``TenantSettings`` para cada ``Client`` novo."""
    from customers.models import Client

    post_save.connect(
        _create_tenant_settings,
        sender=Client,
        dispatch_uid='create_tenant_settings',
    )
