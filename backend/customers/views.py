"""Views do fluxo de convite multi-tenant.

Gestão (tenant-scoped, owner/admin): criar, listar, revogar e reenviar convites.
Aceite (público): inspecionar um convite por token e aceitá-lo, criando o
usuário (quando novo) e a ``TenantMembership`` ativa.
"""
import logging

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .emails import send_invitation_email
from .models import TenantInvitation, TenantMembership
from .permissions import HasTenantRole
from .serializers import (
    InvitationAcceptSerializer,
    InvitationPublicSerializer,
    TenantInvitationSerializer,
)

User = get_user_model()
logger = logging.getLogger(__name__)


class TenantInvitationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Gestão de convites do tenant atual. Restrito a owner/admin."""

    serializer_class = TenantInvitationSerializer
    permission_classes = [IsAuthenticated, HasTenantRole.with_roles(
        TenantMembership.ROLE_OWNER, TenantMembership.ROLE_ADMIN,
    )]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        if tenant is None:
            return TenantInvitation.objects.none()
        return TenantInvitation.objects.filter(tenant=tenant)

    def perform_create(self, serializer):
        invitation = serializer.save()
        try:
            send_invitation_email(invitation)
        except Exception:  # noqa: BLE001 - não falhar o convite por erro de e-mail
            logger.exception('Falha ao enviar e-mail de convite id=%s', invitation.pk)

    @action(detail=True, methods=['post'])
    def revoke(self, request, pk=None):
        invitation = self.get_object()
        if invitation.status != TenantInvitation.STATUS_PENDING:
            return Response(
                {'detail': 'Apenas convites pendentes podem ser revogados.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        invitation.revoke()
        return Response({'detail': 'Convite revogado.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def resend(self, request, pk=None):
        invitation = self.get_object()
        if not invitation.is_pending:
            return Response(
                {'detail': 'Apenas convites pendentes e válidos podem ser reenviados.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            send_invitation_email(invitation)
        except Exception:  # noqa: BLE001
            logger.exception('Falha ao reenviar e-mail de convite id=%s', invitation.pk)
            return Response(
                {'detail': 'Falha ao reenviar o e-mail de convite.'},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return Response({'detail': 'Convite reenviado.'}, status=status.HTTP_200_OK)


class InvitationDetailView(APIView):
    """Inspeção pública de um convite por token (para a tela de aceite)."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, token):
        invitation = get_object_or_404(TenantInvitation, token=token)
        serializer = InvitationPublicSerializer(invitation)
        return Response(serializer.data)


class InvitationAcceptView(APIView):
    """Aceite público de um convite por token."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, token):
        invitation = get_object_or_404(TenantInvitation, token=token)

        if not invitation.is_pending:
            return Response(
                {'detail': 'Convite inválido, expirado ou já utilizado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = InvitationAcceptSerializer(
            data=request.data, context={'invitation': invitation}
        )
        serializer.is_valid(raise_exception=True)
        existing_user = serializer.validated_data['existing_user']

        try:
            with transaction.atomic():
                if existing_user is None:
                    user = self._create_user(invitation, serializer.validated_data)
                else:
                    user = existing_user

                TenantMembership.objects.create(
                    user=user,
                    tenant=invitation.tenant,
                    role=invitation.role,
                    is_active=True,
                )
                invitation.mark_accepted(user)
        except IntegrityError:
            # Corrida com a constraint "um vínculo ativo por usuário".
            return Response(
                {'detail': 'Este usuário já possui vínculo ativo com uma empresa.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info(
            'Convite aceito: email=%s tenant=%s role=%s user_id=%s',
            invitation.email, invitation.tenant.name, invitation.role, user.pk,
        )
        return Response(
            {
                'detail': 'Convite aceito com sucesso.',
                'tenant': invitation.tenant.name,
                'username': user.username,
                'created_account': existing_user is None,
            },
            status=status.HTTP_201_CREATED,
        )

    def _create_user(self, invitation, data):
        from users.models import UserProfile

        user = User.objects.create_user(
            email=invitation.email,
            username=data['username'],
            full_name=data['full_name'],
            password=data['password'],
        )
        # Conta de convite já chega ativa e sem exigir troca de senha imediata.
        user.password_change_required = False
        user.is_active = True
        user.save(update_fields=['password_change_required', 'is_active'])
        UserProfile.objects.get_or_create(user=user)
        return user
