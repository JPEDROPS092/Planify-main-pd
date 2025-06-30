"""
Camada de serviços para o módulo de comunicações.

Este módulo centraliza a lógica de negócio para criação de notificações
e mensagens, facilitando a reutilização e testes.
"""

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from typing import Optional, Any
from .models import Notificacao, ChatMensagem, ConfiguracaoNotificacao


class NotificationService:
    """
    Serviço centralizado para criação e gerenciamento de notificações.
    """
    
    @staticmethod
    def create_notification(
        usuario, 
        tipo: str, 
        titulo: str, 
        mensagem: str, 
        obj: Optional[Any] = None,
        prioridade: str = 'MEDIA',
        url: Optional[str] = None,
        **kwargs
    ) -> Notificacao:
        """
        Cria uma notificação para um usuário, opcionalmente ligada a um objeto.
        
        Args:
            usuario: Instância do usuário que receberá a notificação
            tipo: Tipo da notificação (deve estar em TIPO_CHOICES)
            titulo: Título da notificação
            mensagem: Conteúdo da notificação
            obj: Objeto relacionado (Projeto, Tarefa, Risco, etc.)
            prioridade: Prioridade da notificação ('BAIXA', 'MEDIA', 'ALTA')
            url: URL opcional para redirecionamento
            **kwargs: Argumentos adicionais
            
        Returns:
            Notificacao: A notificação criada
        """
        # Preparar dados para GenericForeignKey
        content_type = None
        object_id = None
        if obj:
            content_type = ContentType.objects.get_for_model(obj)
            object_id = obj.pk
        
        # Criar a notificação
        notificacao = Notificacao.objects.create(
            usuario=usuario,
            tipo=tipo,
            titulo=titulo,
            mensagem=mensagem,
            content_type=content_type,
            object_id=object_id,
            prioridade=prioridade,
            url=url,
            **kwargs
        )
        
        # Aqui você pode adicionar lógica adicional como:
        # - Envio de email
        # - Push notifications
        # - Webhooks
        # - Logging
        
        return notificacao
    
    @staticmethod
    def bulk_notify_users(
        usuarios, 
        tipo: str, 
        titulo: str, 
        mensagem: str, 
        obj: Optional[Any] = None,
        **kwargs
    ) -> list[Notificacao]:
        """
        Cria notificações em lote para múltiplos usuários.
        
        Args:
            usuarios: Lista de usuários que receberão a notificação
            tipo: Tipo da notificação
            titulo: Título da notificação
            mensagem: Conteúdo da notificação
            obj: Objeto relacionado opcional
            **kwargs: Argumentos adicionais
            
        Returns:
            list[Notificacao]: Lista das notificações criadas
        """
        notificacoes = []
        
        with transaction.atomic():
            for usuario in usuarios:
                notificacao = NotificationService.create_notification(
                    usuario=usuario,
                    tipo=tipo,
                    titulo=titulo,
                    mensagem=mensagem,
                    obj=obj,
                    **kwargs
                )
                notificacoes.append(notificacao)
        
        return notificacoes
    
    @staticmethod
    def should_notify_user(usuario, tipo_evento: str) -> bool:
        """
        Verifica se o usuário deve receber notificação para um tipo de evento.
        
        Args:
            usuario: Instância do usuário
            tipo_evento: Tipo do evento (ex: 'tarefa_atribuida', 'projeto_status')
            
        Returns:
            bool: True se deve notificar, False caso contrário
        """
        try:
            config = ConfiguracaoNotificacao.objects.get(usuario=usuario)
            canal_preferido = getattr(config, tipo_evento, 'SISTEMA')
            return canal_preferido in ['SISTEMA', 'AMBOS']
        except ConfiguracaoNotificacao.DoesNotExist:
            # Se não tem configuração, usar padrão (notificar)
            return True


class ChatService:
    """
    Serviço para gerenciamento de mensagens de chat.
    """
    
    @staticmethod
    def send_message(
        projeto, 
        autor, 
        texto: str, 
        anexo=None,
        notify_members: bool = True
    ) -> ChatMensagem:
        """
        Envia uma mensagem de chat e opcionalmente notifica os membros do projeto.
        
        Args:
            projeto: Instância do projeto
            autor: Usuário que envia a mensagem
            texto: Conteúdo da mensagem
            anexo: Arquivo anexo opcional
            notify_members: Se deve notificar outros membros
            
        Returns:
            ChatMensagem: A mensagem criada
        """
        # Criar a mensagem
        message = ChatMensagem.objects.create(
            projeto=projeto,
            autor=autor,
            texto=texto,
            anexo=anexo
        )
        
        # Notificar outros membros do projeto se solicitado
        if notify_members:
            ChatService._notify_project_members(message)
        
        return message
    
    @staticmethod
    def _notify_project_members(message: ChatMensagem):
        """
        Notifica membros do projeto sobre nova mensagem de chat.
        
        Args:
            message: Instância da mensagem criada
        """
        # Obter membros do projeto (excluindo o autor da mensagem)
        # Assumindo que existe um relacionamento membros no modelo Projeto
        if hasattr(message.projeto, 'membros'):
            membros_para_notificar = []
            
            for membro in message.projeto.membros.all():
                usuario = getattr(membro, 'usuario', membro)
                if usuario != message.autor:
                    # Verificar se o usuário quer receber notificações de chat
                    if NotificationService.should_notify_user(usuario, 'mensagem_chat'):
                        membros_para_notificar.append(usuario)
            
            # Criar notificações em lote
            if membros_para_notificar:
                titulo = f'Nova mensagem em {message.projeto.titulo}'
                mensagem_preview = f'{message.autor.get_full_name() or message.autor.username}: {message.texto[:50]}'
                if len(message.texto) > 50:
                    mensagem_preview += '...'
                
                NotificationService.bulk_notify_users(
                    usuarios=membros_para_notificar,
                    tipo='CHAT',
                    titulo=titulo,
                    mensagem=mensagem_preview,
                    obj=message,
                    prioridade='BAIXA'
                )


class CommunicationService:
    """
    Serviço para comunicações formais.
    """
    
    @staticmethod
    def send_formal_communication(
        projeto,
        remetente,
        destinatarios,
        tipo: str,
        titulo: str,
        texto: str,
        notify_recipients: bool = True
    ):
        """
        Envia uma comunicação formal e notifica os destinatários.
        
        Args:
            projeto: Instância do projeto
            remetente: Usuário remetente
            destinatarios: Lista de usuários destinatários
            tipo: Tipo de comunicação
            titulo: Título da comunicação
            texto: Conteúdo da comunicação
            notify_recipients: Se deve notificar os destinatários
            
        Returns:
            Comunicacao: A comunicação criada
        """
        from .models import Comunicacao
        
        with transaction.atomic():
            # Criar a comunicação
            comunicacao = Comunicacao.objects.create(
                projeto=projeto,
                remetente=remetente,
                tipo=tipo,
                titulo=titulo,
                texto=texto
            )
            
            # Adicionar destinatários
            comunicacao.destinatarios.set(destinatarios)
            
            # Notificar destinatários se solicitado
            if notify_recipients:
                CommunicationService._notify_recipients(comunicacao)
        
        return comunicacao
    
    @staticmethod
    def _notify_recipients(comunicacao):
        """
        Notifica os destinatários sobre nova comunicação formal.
        
        Args:
            comunicacao: Instância da comunicação criada
        """
        destinatarios_para_notificar = [
            dest for dest in comunicacao.destinatarios.all()
            if NotificationService.should_notify_user(dest, 'documento_novo')
        ]
        
        if destinatarios_para_notificar:
            titulo = f'Nova {comunicacao.get_tipo_display().lower()}: {comunicacao.titulo}'
            mensagem = f'Você recebeu uma nova comunicação de {comunicacao.remetente.get_full_name() or comunicacao.remetente.username}'
            
            NotificationService.bulk_notify_users(
                usuarios=destinatarios_para_notificar,
                tipo='DOCUMENTO',
                titulo=titulo,
                mensagem=mensagem,
                obj=comunicacao,
                prioridade='MEDIA'
            )
