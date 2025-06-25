"""
Exemplos de uso dos novos serviços de comunicação.

Este arquivo demonstra como usar os serviços NotificationService,
ChatService e CommunicationService após a refatoração.
"""

from django.contrib.auth import get_user_model
from communications.services import NotificationService, ChatService, CommunicationService
from projects.models import Projeto
from tasks.models import Tarefa

User = get_user_model()


def exemplo_notificacao_simples():
    """
    Exemplo de criação de uma notificação simples.
    """
    # Obter um usuário
    usuario = User.objects.first()
    
    # Criar notificação simples
    notificacao = NotificationService.create_notification(
        usuario=usuario,
        tipo='SISTEMA',
        titulo='Bem-vindo ao sistema!',
        mensagem='Você foi cadastrado com sucesso no sistema.',
        prioridade='MEDIA'
    )
    
    print(f"Notificação criada: {notificacao.titulo}")
    return notificacao


def exemplo_notificacao_com_objeto():
    """
    Exemplo de criação de notificação relacionada a um objeto.
    """
    # Obter dados
    usuario = User.objects.first()
    projeto = Projeto.objects.first()
    
    if not usuario or not projeto:
        print("Dados não encontrados para o exemplo")
        return None
    
    # Criar notificação relacionada ao projeto
    notificacao = NotificationService.create_notification(
        usuario=usuario,
        tipo='PROJETO',
        titulo='Status do projeto alterado',
        mensagem=f'O projeto {projeto.titulo} teve seu status alterado.',
        obj=projeto,  # O objeto será relacionado via GenericForeignKey
        prioridade='ALTA',
        url=f'/projetos/{projeto.pk}/'
    )
    
    print(f"Notificação criada para projeto: {notificacao.titulo}")
    print(f"Objeto relacionado: {notificacao.get_related_object_info()}")
    return notificacao


def exemplo_notificacao_em_lote():
    """
    Exemplo de criação de notificações em lote.
    """
    # Obter múltiplos usuários
    usuarios = User.objects.all()[:3]
    tarefa = Tarefa.objects.first()
    
    if not usuarios.exists() or not tarefa:
        print("Dados não encontrados para o exemplo")
        return []
    
    # Criar notificações em lote
    notificacoes = NotificationService.bulk_notify_users(
        usuarios=usuarios,
        tipo='TAREFA',
        titulo='Nova tarefa criada',
        mensagem=f'A tarefa "{tarefa.titulo}" foi criada e pode ser do seu interesse.',
        obj=tarefa,
        prioridade='MEDIA'
    )
    
    print(f"{len(notificacoes)} notificações criadas em lote")
    return notificacoes


def exemplo_mensagem_chat():
    """
    Exemplo de envio de mensagem de chat com notificações automáticas.
    """
    # Obter dados
    projeto = Projeto.objects.first()
    autor = User.objects.first()
    
    # Enviar mensagem de chat (irá notificar automaticamente outros membros)
    mensagem = ChatService.send_message(
        projeto=projeto,
        autor=autor,
        texto='Olá pessoal! Como está o andamento do projeto?',
        notify_members=True
    )
    
    print(f"Mensagem enviada: {mensagem.texto[:50]}...")
    return mensagem


def exemplo_comunicacao_formal():
    """
    Exemplo de envio de comunicação formal com notificações.
    """
    # Obter dados
    projeto = Projeto.objects.first()
    remetente = User.objects.first()
    destinatarios = User.objects.all()[:2]
    
    # Enviar comunicação formal
    comunicacao = CommunicationService.send_formal_communication(
        projeto=projeto,
        remetente=remetente,
        destinatarios=destinatarios,
        tipo='ATA',
        titulo='Ata da Reunião de Kickoff',
        texto='Esta é a ata da reunião de kickoff do projeto...',
        notify_recipients=True
    )
    
    print(f"Comunicação enviada: {comunicacao.titulo}")
    return comunicacao


def exemplo_verificacao_configuracao():
    """
    Exemplo de verificação de configurações de notificação.
    """
    usuario = User.objects.first()
    
    if not usuario:
        print("Usuário não encontrado para o exemplo")
        return
    
    # Verificar se o usuário deve receber notificações de diferentes tipos
    tipos_evento = [
        'tarefa_atribuida',
        'projeto_status', 
        'mensagem_chat',
        'documento_novo'
    ]
    
    username = getattr(usuario, 'username', str(usuario))
    for tipo in tipos_evento:
        deve_notificar = NotificationService.should_notify_user(usuario, tipo)
        print(f"Usuário {username} - {tipo}: {'✓' if deve_notificar else '✗'}")


if __name__ == '__main__':
    print("=== Exemplos de uso dos serviços de comunicação ===")
    
    print("\n1. Notificação simples:")
    exemplo_notificacao_simples()
    
    print("\n2. Notificação com objeto relacionado:")
    exemplo_notificacao_com_objeto()
    
    print("\n3. Notificações em lote:")
    exemplo_notificacao_em_lote()
    
    print("\n4. Mensagem de chat:")
    exemplo_mensagem_chat()
    
    print("\n5. Comunicação formal:")
    exemplo_comunicacao_formal()
    
    print("\n6. Verificação de configurações:")
    exemplo_verificacao_configuracao()
    
    print("\n=== Fim dos exemplos ===")
