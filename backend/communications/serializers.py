from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import ChatMensagem, ChatMensagemLeitura, Notificacao, ConfiguracaoNotificacao, Comunicacao


# Serializer auxiliar para informações de destinatários
class DestinatarioInfoSerializer(serializers.Serializer):
    """Serializer auxiliar para descrever informações básicas de um destinatário."""
    id = serializers.IntegerField()
    username = serializers.CharField()
    nome = serializers.CharField()


# Serializer auxiliar para informações de objetos relacionados
class RelatedObjectInfoSerializer(serializers.Serializer):
    """Serializer auxiliar para descrever informações de objetos relacionados via GenericForeignKey."""
    type = serializers.CharField()
    app_label = serializers.CharField()
    id = serializers.IntegerField()
    str_representation = serializers.CharField()
    # Campos específicos são adicionados dinamicamente baseados no tipo


class ChatMensagemLeituraSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.full_name', read_only=True)
    
    class Meta:
        model = ChatMensagemLeitura
        fields = ['id', 'mensagem', 'usuario', 'usuario_nome', 'lido_em']
        read_only_fields = ['lido_em']


class ChatMensagemSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(source='autor.full_name', read_only=True)
    autor_username = serializers.CharField(source='autor.username', read_only=True)
    leituras = ChatMensagemLeituraSerializer(many=True, read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    
    class Meta:
        model = ChatMensagem
        fields = ['id', 'projeto', 'projeto_nome', 'autor', 'autor_nome', 'autor_username', 
                  'texto', 'anexo', 'enviado_em', 'editado', 'leituras']
        read_only_fields = ['enviado_em', 'editado', 'autor']


class NotificacaoSerializer(serializers.ModelSerializer):
    """
    Serializer para notificações com suporte ao GenericForeignKey.
    
    Inclui campos para exibir informações sobre o objeto relacionado
    através do GenericForeignKey de forma amigável.
    """
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)
    
    # Campos mantidos para compatibilidade durante migração
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    
    # Campos para o objeto relacionado via GenericForeignKey
    related_object_info = serializers.SerializerMethodField(read_only=True)
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = Notificacao
        fields = [
            'id', 'usuario', 'tipo', 'tipo_display', 'titulo', 'mensagem', 
            'lida', 'prioridade', 'prioridade_display', 'criada_em', 'lida_em', 
            'projeto', 'projeto_nome', 'tarefa', 'tarefa_titulo', 'url',
            'content_type', 'object_id', 'content_type_name', 'related_object_info'
        ]
        read_only_fields = ['criada_em', 'lida_em']
    
    @extend_schema_field(RelatedObjectInfoSerializer)
    def get_related_object_info(self, obj):
        """
        Retorna informações sobre o objeto relacionado via GenericForeignKey.
        
        Returns:
            dict: Informações do objeto relacionado ou None
        """
        info = obj.get_related_object_info()
        if info and info['object']:
            related_obj = info['object']
            
            # Retorna informações básicas do objeto relacionado
            return {
                'type': info['type'],
                'app_label': info['app_label'],
                'id': related_obj.pk,
                'str_representation': str(related_obj),
                # Adicionar campos específicos baseados no tipo
                **self._get_specific_object_info(related_obj, info['type'])
            }
        return None
    
    def _get_specific_object_info(self, obj, obj_type):
        """
        Retorna informações específicas baseadas no tipo do objeto.
        
        Args:
            obj: O objeto relacionado
            obj_type: Tipo do objeto (string)
            
        Returns:
            dict: Informações específicas do tipo
        """
        specific_info = {}
        
        try:
            if obj_type == 'projeto':
                specific_info.update({
                    'name': getattr(obj, 'name', ''),
                    'status': getattr(obj, 'status', ''),
                })
            elif obj_type == 'tarefa':
                specific_info.update({
                    'titulo': getattr(obj, 'titulo', ''),
                    'status': getattr(obj, 'status', ''),
                })
            elif obj_type == 'chatmensagem':
                specific_info.update({
                    'texto': getattr(obj, 'texto', '')[:50] + '...' if len(getattr(obj, 'texto', '')) > 50 else getattr(obj, 'texto', ''),
                    'autor': getattr(obj.autor, 'username', '') if hasattr(obj, 'autor') else '',
                })
        except AttributeError:
            # Se algum campo não existir, ignora silenciosamente
            pass
            
        return specific_info


class ConfiguracaoNotificacaoSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para configurações de notificação.
    
    A lógica de get_or_create foi movida para a view, tornando este
    serializer mais simples e focado apenas na serialização/deserialização.
    """
    usuario_nome = serializers.CharField(source='usuario.full_name', read_only=True)
    
    class Meta:
        model = ConfiguracaoNotificacao
        fields = [
            'id', 'usuario', 'usuario_nome', 'tarefa_atribuida', 
            'tarefa_comentario', 'tarefa_prazo', 'projeto_status', 
            'equipe_alteracao', 'documento_novo', 'risco_novo', 'mensagem_chat'
        ]
        read_only_fields = ['usuario', 'usuario_nome']  # O usuário é definido pela view


class ComunicacaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Comunicacao.
    
    Permite criar, listar, atualizar e excluir comunicações formais em projetos.
    Inclui campos calculados para exibir informações relacionadas de forma mais amigável.
    """
    remetente_nome = serializers.CharField(source='remetente.full_name', read_only=True)
    remetente_username = serializers.CharField(source='remetente.username', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    destinatarios_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Comunicacao
        fields = ['id', 'projeto', 'projeto_nome', 'tipo', 'tipo_display', 'titulo', 'texto', 
                  'remetente', 'remetente_nome', 'remetente_username', 
                  'destinatarios', 'destinatarios_info', 'criada_em', 'atualizada_em']
        read_only_fields = ['remetente', 'criada_em', 'atualizada_em']
    
    @extend_schema_field(DestinatarioInfoSerializer(many=True))
    def get_destinatarios_info(self, obj):
        """Retorna informações básicas sobre os destinatários."""
        return [{
            'id': user.id,
            'username': user.username,
            'nome': user.full_name
        } for user in obj.destinatarios.all()]
