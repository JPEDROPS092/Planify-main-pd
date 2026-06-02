"""Serializers do fluxo de convite multi-tenant.

- ``TenantInvitationSerializer``: gestão de convites por owner/admin dentro do
  tenant (criação/listagem). Resolve ``tenant`` e ``invited_by`` a partir da
  requisição; nunca os aceita do cliente.
- ``InvitationPublicSerializer``: visão pública (somente leitura) de um convite
  por token, para a tela de aceite.
- ``InvitationAcceptSerializer``: payload de aceite. Para um usuário novo exige
  ``username``/``full_name``/``password``; para um usuário já existente (mesmo
  e-mail, sem vínculo ativo) o próprio token comprova a posse do e-mail.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import TenantInvitation, TenantMembership

User = get_user_model()


class TenantInvitationSerializer(serializers.ModelSerializer):
    invited_by_username = serializers.CharField(source='invited_by.username', read_only=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)

    class Meta:
        model = TenantInvitation
        fields = [
            'id', 'email', 'role', 'status', 'token',
            'invited_by', 'invited_by_username', 'tenant_name',
            'accepted_user', 'created_at', 'expires_at', 'accepted_at',
        ]
        read_only_fields = [
            'id', 'status', 'token', 'invited_by', 'invited_by_username',
            'tenant_name', 'accepted_user', 'created_at', 'expires_at', 'accepted_at',
        ]

    def validate_role(self, value):
        if value not in TenantInvitation.INVITABLE_ROLES:
            raise serializers.ValidationError(
                'Papel inválido para convite. O papel "owner" é provisionado pelo '
                'superuser, não convidado.'
            )
        return value

    def validate_email(self, value):
        return User.objects.normalize_email(value)

    def validate(self, attrs):
        request = self.context['request']
        tenant = getattr(request, 'tenant', None)
        email = attrs['email']

        if tenant is None:
            raise serializers.ValidationError(
                'Convites só podem ser criados no contexto de um tenant.'
            )

        # Convite pendente duplicado para o mesmo e-mail neste tenant.
        if TenantInvitation.objects.filter(
            tenant=tenant, email__iexact=email, status=TenantInvitation.STATUS_PENDING
        ).exists():
            raise serializers.ValidationError(
                {'email': 'Já existe um convite pendente para este e-mail neste tenant.'}
            )

        # O convidado não pode já possuir um vínculo ativo (regra "um usuário = uma empresa").
        existing = User.objects.filter(email__iexact=email).first()
        if existing and TenantMembership.objects.filter(
            user=existing, is_active=True
        ).exists():
            raise serializers.ValidationError(
                {'email': 'Este usuário já possui vínculo ativo com uma empresa.'}
            )

        return attrs

    def create(self, validated_data):
        request = self.context['request']
        validated_data['tenant'] = request.tenant
        validated_data['invited_by'] = request.user
        return super().create(validated_data)


class InvitationPublicSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    is_pending = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    requires_new_account = serializers.SerializerMethodField()

    class Meta:
        model = TenantInvitation
        fields = [
            'email', 'role', 'status', 'tenant_name',
            'is_pending', 'is_expired', 'requires_new_account',
        ]

    def get_requires_new_account(self, obj):
        return not User.objects.filter(email__iexact=obj.email).exists()


class InvitationAcceptSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    full_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(required=False, allow_blank=True, write_only=True)

    def validate(self, attrs):
        invitation = self.context['invitation']
        existing = User.objects.filter(email__iexact=invitation.email).first()

        if existing is None:
            # Usuário novo: exige dados completos de criação de conta.
            missing = [f for f in ('username', 'full_name', 'password') if not attrs.get(f)]
            if missing:
                raise serializers.ValidationError(
                    {f: 'Campo obrigatório para criar a conta.' for f in missing}
                )
            if User.objects.filter(username__iexact=attrs['username']).exists():
                raise serializers.ValidationError(
                    {'username': 'Nome de usuário já está em uso.'}
                )
            validate_password(attrs['password'])

        attrs['existing_user'] = existing
        return attrs
