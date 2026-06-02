"""Envio de e-mails do fluxo de convite multi-tenant.

Em desenvolvimento o ``EMAIL_BACKEND`` é o console; em produção, o SMTP
configurado. O link de aceite aponta para o domínio do próprio tenant
(subdomínio), de modo que o convidado caia já no contexto correto.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def build_invitation_accept_url(invitation):
    """Monta a URL de aceite no domínio primário do tenant.

    Usa ``TENANT_INVITATION_ACCEPT_PATH`` (template com ``{token}``) e o
    domínio primário do tenant. Cai para ``FRONTEND_URL`` se não houver
    domínio cadastrado.
    """
    path_template = getattr(settings, 'TENANT_INVITATION_ACCEPT_PATH', '/convite/{token}')
    accept_path = path_template.format(token=invitation.token)

    domain = invitation.tenant.domains.filter(is_primary=True).first()
    if domain is not None:
        scheme = getattr(settings, 'TENANT_INVITATION_URL_SCHEME', 'https' if not settings.DEBUG else 'http')
        return f'{scheme}://{domain.domain}{accept_path}'

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
        invitation.email, invitation.tenant.schema_name, invitation.role,
    )
    return accept_url
