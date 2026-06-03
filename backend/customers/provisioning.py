"""Helpers compartilhados de provisionamento de usuários, tenants e owners.

Centraliza a *mecânica* idempotente usada pelos management commands para não
duplicar a criação de usuários, tenants e vínculos de owner:

- ``seed_initial``     → garante o superuser SaaS (dev e prod).
- ``seed_demo_data``   → garante o tenant Demo + owner Demo (apenas dev).
- ``provision_tenant`` → cadastra um tenant real + owner (prod).

Aqui ficam só os mecanismos (idempotentes e reutilizáveis). A *política* de cada
comando — falhar-se-já-existe vs. garantir, senhas temporárias, etc. — fica em
cada comando, que orquestra estes helpers.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from django.utils.text import slugify

from customers.models import Client, TenantMembership
from users.models import UserProfile


def normalize_slug(value, *, required=False):
    """Normaliza um slug de tenant (<=120 chars).

    Retorna string vazia quando ``value`` é vazio, a menos que ``required`` seja
    ``True`` (aí levanta ``CommandError``). Slug vazio deixa o ``Client.save``
    gerar um slug único a partir do nome.
    """
    slug = slugify(value or '')
    if not slug:
        if required:
            raise CommandError('Slug do tenant inválido.')
        return ''
    return slug[:120]


def ensure_user(
    *,
    username,
    email,
    full_name,
    password,
    role,
    is_staff=False,
    is_superuser=False,
    password_change_required=False,
    reset_password=False,
):
    """Cria ou atualiza (idempotente) um usuário e o seu ``UserProfile``.

    Procura o usuário por ``username`` e, em seguida, por ``email``. Ao criar,
    usa ``password``; ao atualizar um já existente, só redefine a senha se
    ``reset_password`` for ``True``.
    """
    User = get_user_model()
    email = User.objects.normalize_email(email)

    user = User.objects.filter(username__iexact=username).first()
    if user is None:
        user = User.objects.filter(email__iexact=email).first()

    if user is None:
        user = User.objects.create_user(
            email=email,
            username=username,
            full_name=full_name,
            password=password,
            role=role,
        )
        update_fields = []
    else:
        update_fields = []
        if user.username != username:
            if User.objects.filter(username__iexact=username).exclude(pk=user.pk).exists():
                raise CommandError(f'O username "{username}" ja esta em uso.')
            user.username = username
            update_fields.append('username')
        if user.email != email:
            if User.objects.filter(email__iexact=email).exclude(pk=user.pk).exists():
                raise CommandError(f'O e-mail "{email}" ja esta em uso.')
            user.email = email
            update_fields.append('email')
        if reset_password:
            user.set_password(password)
            update_fields.append('password')

    desired = {
        'full_name': full_name,
        'is_staff': is_staff,
        'is_superuser': is_superuser,
        'is_active': True,
        'role': role,
        'password_change_required': password_change_required,
    }
    for field, value in desired.items():
        if getattr(user, field) != value:
            setattr(user, field, value)
            update_fields.append(field)

    if update_fields:
        user.save(update_fields=sorted(set(update_fields)))

    UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'theme_preference': 'SYSTEM',
            'email_notifications': True,
            'system_notifications': True,
        },
    )
    return user


def ensure_tenant(*, slug, name, status=Client.STATUS_ACTIVE):
    """Cria ou atualiza (idempotente) um tenant pelo ``slug``.

    Retorna ``(tenant, created)``. Criar o ``Client`` dispara o ``post_save`` que
    cria as suas ``TenantSettings`` (R5).
    """
    slug = normalize_slug(slug, required=True)
    tenant, created = Client.objects.get_or_create(
        slug=slug,
        defaults={'name': name, 'status': status},
    )
    updates = []
    if tenant.name != name:
        tenant.name = name
        updates.append('name')
    if tenant.status != status:
        tenant.status = status
        updates.append('status')
    if updates:
        tenant.save(update_fields=updates)
    return tenant, created


def ensure_owner_membership(*, user, tenant):
    """Garante (idempotente) um vínculo de owner ativo para ``user`` em ``tenant``.

    Respeita a regra "um usuário = uma empresa": levanta ``CommandError`` se o
    usuário já tiver um vínculo ativo com outro tenant.
    """
    active = TenantMembership.objects.filter(user=user, is_active=True).first()
    if active and active.tenant_id != tenant.id:
        raise CommandError(
            f'O usuario "{user.username}" ja possui vinculo ativo com "{active.tenant}".'
        )

    membership, _ = TenantMembership.objects.get_or_create(
        user=user,
        tenant=tenant,
        defaults={'role': TenantMembership.ROLE_OWNER, 'is_active': True},
    )
    updates = []
    if membership.role != TenantMembership.ROLE_OWNER:
        membership.role = TenantMembership.ROLE_OWNER
        updates.append('role')
    if not membership.is_active:
        membership.is_active = True
        updates.append('is_active')
    if updates:
        membership.full_clean()
        membership.save(update_fields=updates)
    return membership
