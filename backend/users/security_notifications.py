# users/security_notifications.py - Sistema de notificações de segurança
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


class SecurityNotificationService:
    """
    Serviço para envio de notificações de segurança por email
    """
    
    @staticmethod
    def _send_notification(subject, html_message, recipient_list, context=None):
        """
        Método auxiliar para envio de emails
        """
        try:
            plain_message = strip_tags(html_message)
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@planify.com'),
                recipient_list=recipient_list,
                fail_silently=False,
            )
            logger.info(f"Notificação de segurança enviada: {subject} para {recipient_list}")
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar notificação de segurança: {str(e)}")
            return False
    
    @staticmethod
    def notify_password_change(user, ip_address=None):
        """
        Notifica sobre alteração de senha
        """
        subject = 'Senha alterada - Planify'
        context = {
            'user': user,
            'timestamp': timezone.now().strftime('%d/%m/%Y às %H:%M'),
            'ip_address': ip_address or 'N/A',
        }
        
        html_message = f"""
        <html>
        <body>
            <h2>Senha alterada com sucesso</h2>
            <p>Olá {user.full_name or user.username},</p>
            
            <p>Sua senha foi alterada com sucesso em <strong>{context['timestamp']}</strong>.</p>
            
            {f"<p>IP de origem: <strong>{context['ip_address']}</strong></p>" if ip_address else ""}
            
            <p><strong>Se você não fez esta alteração:</strong></p>
            <ul>
                <li>Entre em contato conosco imediatamente</li>
                <li>Altere sua senha assim que possível</li>
                <li>Verifique sua conta em busca de atividades suspeitas</li>
            </ul>
            
            <p>Atenciosamente,<br>Equipe Planify</p>
        </body>
        </html>
        """
        
        return SecurityNotificationService._send_notification(
            subject, html_message, [user.email], context
        )

    @staticmethod
    def notify_suspicious_login(user, ip_address, user_agent=None):
        """
        Notifica sobre login suspeito
        """
        subject = 'Atividade suspeita detectada - Planify'
        context = {
            'user': user,
            'timestamp': timezone.now().strftime('%d/%m/%Y às %H:%M'),
            'ip_address': ip_address,
            'user_agent': user_agent or 'N/A',
        }
        
        html_message = f"""
        <html>
        <body>
            <h2>Atividade suspeita detectada</h2>
            <p>Olá {user.full_name or user.username},</p>
            
            <p>Detectamos uma atividade suspeita em sua conta em <strong>{context['timestamp']}</strong>.</p>
            
            <p><strong>Detalhes do acesso:</strong></p>
            <ul>
                <li>IP: <strong>{context['ip_address']}</strong></li>
                <li>Navegador: <strong>{context['user_agent']}</strong></li>
            </ul>
            
            <p><strong>Se não foi você:</strong></p>
            <ul>
                <li>Altere sua senha imediatamente</li>
                <li>Verifique se há atividades não autorizadas em sua conta</li>
                <li>Entre em contato conosco se precisar de ajuda</li>
            </ul>
            
            <p>Atenciosamente,<br>Equipe Planify</p>
        </body>
        </html>
        """
        
        return SecurityNotificationService._send_notification(
            subject, html_message, [user.email], context
        )

    @staticmethod
    def notify_account_locked(user, reason='Múltiplas tentativas de login falhadas'):
        """
        Notifica sobre bloqueio de conta
        """
        subject = 'Conta bloqueada - Planify'
        context = {
            'user': user,
            'timestamp': timezone.now().strftime('%d/%m/%Y às %H:%M'),
            'reason': reason,
        }
        
        html_message = f"""
        <html>
        <body>
            <h2>Conta bloqueada por segurança</h2>
            <p>Olá {user.full_name or user.username},</p>
            
            <p>Sua conta foi bloqueada em <strong>{context['timestamp']}</strong> por motivos de segurança.</p>
            
            <p><strong>Motivo:</strong> {context['reason']}</p>
            
            <p><strong>Para desbloquear sua conta:</strong></p>
            <ul>
                <li>Entre em contato com o administrador do sistema</li>
                <li>Ou aguarde o desbloqueio automático</li>
            </ul>
            
            <p>Atenciosamente,<br>Equipe Planify</p>
        </body>
        </html>
        """
        
        return SecurityNotificationService._send_notification(
            subject, html_message, [user.email], context
        )

    @staticmethod
    def notify_account_unlocked(user):
        """
        Notifica sobre desbloqueio de conta
        """
        subject = 'Conta desbloqueada - Planify'
        context = {
            'user': user,
            'timestamp': timezone.now().strftime('%d/%m/%Y às %H:%M'),
        }
        
        html_message = f"""
        <html>
        <body>
            <h2>Conta desbloqueada</h2>
            <p>Olá {user.full_name or user.username},</p>
            
            <p>Sua conta foi desbloqueada em <strong>{context['timestamp']}</strong>.</p>
            
            <p>Você já pode fazer login normalmente.</p>
            
            <p><strong>Para sua segurança:</strong></p>
            <ul>
                <li>Use uma senha forte e única</li>
                <li>Não compartilhe suas credenciais</li>
                <li>Faça logout ao terminar de usar o sistema</li>
            </ul>
            
            <p>Atenciosamente,<br>Equipe Planify</p>
        </body>
        </html>
        """
        
        return SecurityNotificationService._send_notification(
            subject, html_message, [user.email], context
        )