import secrets
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Client(models.Model):
    """Registro de uma empresa (tenant).

    Re-arquitetura R1 (2026-06-03): deixou de herdar ``TenantMixin`` do
    django-tenants. Não há mais schema por tenant; o isolamento dos dados de
    negócio passa a ser por ``tenant_id`` (FK para este model) a partir da R2.
    """

    STATUS_ACTIVE = 'active'
    STATUS_SUSPENDED = 'suspended'

    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Ativo'),
        (STATUS_SUSPENDED, 'Suspenso'),
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base = slugify(self.name) or 'tenant'
        slug = base[:120]
        suffix = 2

        queryset = Client.objects.filter(slug=slug)
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        while queryset.exists():
            suffix_text = f'-{suffix}'
            slug = f'{base[:120 - len(suffix_text)]}{suffix_text}'
            queryset = Client.objects.filter(slug=slug)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            suffix += 1

        return slug


class TenantMembership(models.Model):
    ROLE_OWNER = 'owner'
    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_MEMBER = 'member'
    ROLE_VIEWER = 'viewer'

    ROLE_CHOICES = (
        (ROLE_OWNER, 'Owner'),
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_MEMBER, 'Member'),
        (ROLE_VIEWER, 'Viewer'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tenant_memberships',
    )
    tenant = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Membro do tenant'
        verbose_name_plural = 'Membros dos tenants'
        constraints = [
            models.UniqueConstraint(fields=['user', 'tenant'], name='unique_user_tenant_membership'),
            # Regra de negócio: um usuário pertence a uma única empresa.
            # Permite manter vínculos inativos (histórico/troca de empresa),
            # mas no máximo um vínculo ativo por usuário em toda a plataforma.
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_active=True),
                name='unique_active_membership_per_user',
            ),
        ]
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['tenant', 'is_active']),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.is_active:
            conflito = TenantMembership.objects.filter(user=self.user, is_active=True)
            if self.pk:
                conflito = conflito.exclude(pk=self.pk)
            if conflito.exists():
                raise ValidationError(
                    'Este usuário já possui um vínculo ativo com uma empresa. '
                    'Um usuário pode pertencer a apenas uma empresa.'
                )

    def __str__(self):
        return f'{self.user} - {self.tenant} ({self.role})'


def _default_invitation_expiry():
    days = getattr(settings, 'TENANT_INVITATION_TTL_DAYS', 7)
    return timezone.now() + timedelta(days=days)


def _generate_invitation_token():
    return secrets.token_urlsafe(32)


class TenantInvitation(models.Model):
    """Convite para um usuário entrar em um tenant com um papel definido.

    Modelo compartilhado (schema ``public``), pois envolve a identidade global
    (``users.User``) e a empresa (``Client``). O owner/admin do tenant cria o
    convite; o convidado o aceita e ganha uma ``TenantMembership`` ativa,
    respeitando a regra "um usuário = uma empresa".

    O papel ``owner`` não é convidável: o primeiro owner é provisionado pelo
    superuser (management command ``provision_tenant``).
    """

    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REVOKED = 'revoked'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pendente'),
        (STATUS_ACCEPTED, 'Aceito'),
        (STATUS_REVOKED, 'Revogado'),
    )

    # Papéis que podem ser atribuídos via convite (owner é provisionado, não convidado).
    INVITABLE_ROLES = (
        TenantMembership.ROLE_ADMIN,
        TenantMembership.ROLE_MANAGER,
        TenantMembership.ROLE_MEMBER,
        TenantMembership.ROLE_VIEWER,
    )

    tenant = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='invitations',
    )
    email = models.EmailField()
    role = models.CharField(
        max_length=20,
        choices=TenantMembership.ROLE_CHOICES,
        default=TenantMembership.ROLE_MEMBER,
    )
    token = models.CharField(
        max_length=64,
        unique=True,
        default=_generate_invitation_token,
        editable=False,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_tenant_invitations',
    )
    accepted_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_tenant_invitations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=_default_invitation_expiry)
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Convite de tenant'
        verbose_name_plural = 'Convites de tenant'
        ordering = ['-created_at']
        constraints = [
            # No máximo um convite pendente por (tenant, email).
            models.UniqueConstraint(
                fields=['tenant', 'email'],
                condition=models.Q(status='pending'),
                name='unique_pending_invitation_per_tenant_email',
            ),
        ]
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['email', 'status']),
        ]

    @property
    def is_expired(self):
        return self.status == self.STATUS_PENDING and self.expires_at < timezone.now()

    @property
    def is_pending(self):
        return self.status == self.STATUS_PENDING and not self.is_expired

    def revoke(self):
        self.status = self.STATUS_REVOKED
        self.save(update_fields=['status', 'updated_at'])

    def mark_accepted(self, user):
        self.status = self.STATUS_ACCEPTED
        self.accepted_user = user
        self.accepted_at = timezone.now()
        self.save(update_fields=['status', 'accepted_user', 'accepted_at', 'updated_at'])

    def __str__(self):
        return f'Convite {self.email} -> {self.tenant} ({self.role}, {self.status})'


class TenantSettings(models.Model):
    """Customização por empresa via config/feature-flags (R5).

    Modelo 1-1 com ``Client`` que guarda as diferenças de comportamento de cada
    tenant **sem** schema físico separado. Dois campos JSON livres e extensíveis:

    - ``features``: liga/desliga funcionalidades (``chave -> bool``).
    - ``config``: parâmetros de configuração arbitrários (``chave -> valor``).

    Ponto único de leitura: ``customers.config.get_tenant_settings(tenant)``
    (cria com defaults na primeira leitura). É criado automaticamente para todo
    ``Client`` novo (``post_save`` em ``customers.config``).

    Schema físico separado por empresa é **exceção dura** (contrato/lei), tratada
    caso a caso fora deste model — não é o caminho de customização padrão.
    """

    tenant = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name='settings',
    )
    features = models.JSONField(
        default=dict,
        blank=True,
        help_text='Feature flags por empresa (chave -> booleano).',
    )
    config = models.JSONField(
        default=dict,
        blank=True,
        help_text='Parâmetros de configuração por empresa (chave -> valor).',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração do tenant'
        verbose_name_plural = 'Configurações dos tenants'

    def is_feature_enabled(self, key, default=False):
        return bool(self.features.get(key, default))

    def set_feature(self, key, enabled):
        self.features[key] = bool(enabled)

    def get_config(self, key, default=None):
        return self.config.get(key, default)

    def __str__(self):
        return f'Configurações de {self.tenant}'
