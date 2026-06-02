from django.conf import settings
from django.db import models
from django_tenants.models import DomainMixin, TenantMixin


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    class Meta:
        verbose_name = 'Domínio'
        verbose_name_plural = 'Domínios'

    def __str__(self):
        return self.domain


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
