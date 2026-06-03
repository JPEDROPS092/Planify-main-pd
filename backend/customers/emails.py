"""Envio de e-mails do fluxo de convite multi-tenant.

Em desenvolvimento o ``EMAIL_BACKEND`` é o console; em produção, o SMTP
configurado. R3 (2026-06-03): sem subdomínio por tenant — o link de aceite
aponta para o domínio único do app (``FRONTEND_URL``); o tenant é resolvido
pelo token do convite no aceite.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def build_invitation_accept_url(invitation):
    """Monta a URL de aceite no domínio único do app (``FRONTEND_URL``).

    Usa ``TENANT_INVITATION_ACCEPT_PATH`` (template com ``{token}``). O tenant
    é identificado pelo token, não pelo host.
    """
    path_template = getattr(settings, 'TENANT_INVITATION_ACCEPT_PATH', '/convite/{token}')
    accept_path = path_template.format(token=invitation.token)

    base = getattr(settings, 'FRONTEND_URL', '').rstrip('/')
    return f'{base}{accept_path}'


def send_invitation_email(invitation):
    accept_url = build_invitation_accept_url(invitation)
    subject = f'Convite para participar de {invitation.tenant.name} no Planify'
    body = (
        f'Você foi convidado(a) para participar da empresa "{invitation.tenant.name}" '
        f'no Planify com o papel de {invitation.get_role_display()}.\n\n'
        f'Para aceitar o convite, acesse:\n{accept_url}\n\n'
        f'Este convite expira em {invitation.expires_at:%d/%m/%Y %H:%M}.'
    )
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [invitation.email],
        fail_silently=False,
    )
    logger.info(
        'Convite enviado: email=%s tenant=%s role=%s',
        invitation.email, invitation.tenant.name, invitation.role,
    )
    return accept_url
