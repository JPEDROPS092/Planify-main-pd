from rest_framework import serializers
from .models import ChatMensagem, ChatMensagemLeitura, Notificacao, ConfiguracaoNotificacao, Comunicacao


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
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    
    class Meta:
        model = Notificacao
        fields = ['id', 'usuario', 'tipo', 'tipo_display', 'titulo', 'mensagem', 
                  'lida', 'prioridade', 'prioridade_display', 'criada_em', 'lida_em', 
                  'projeto', 'projeto_nome', 'tarefa', 'tarefa_titulo', 'url']
        read_only_fields = ['criada_em', 'lida_em']


class ConfiguracaoNotificacaoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.full_name', read_only=True)
    
    class Meta:
        model = ConfiguracaoNotificacao
        fields = ['id', 'usuario', 'usuario_nome', 'tarefa_atribuida', 'tarefa_comentario', 
                  'tarefa_prazo', 'projeto_status', 'equipe_alteracao', 'documento_novo', 
                  'risco_novo', 'mensagem_chat']
    
    def create(self, validated_data):
        """
        Cria ou atualiza a configuração de notificação para o usuário.
        """
        usuario = validated_data.get('usuario')
        
        # Tenta obter a configuração existente
        try:
            config = ConfiguracaoNotificacao.objects.get(usuario=usuario)
            
            # Atualiza os campos
            for attr, value in validated_data.items():
                setattr(config, attr, value)
            
            config.save()
            return config
        except ConfiguracaoNotificacao.DoesNotExist:
            # Cria uma nova configuração
            return super().create(validated_data)


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
    
    def get_destinatarios_info(self, obj):
        """Retorna informações básicas sobre os destinatários."""
        return [{
            'id': user.id,
            'username': user.username,
            'nome': user.full_name
        } for user in obj.destinatarios.all()]
