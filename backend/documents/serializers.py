from rest_framework import serializers
from .models import Documento, HistoricoDocumento, Comentario


class ComentarioSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(source='autor.full_name', read_only=True)
    
    class Meta:
        model = Comentario
        fields = ['id', 'documento', 'autor', 'autor_nome', 'texto', 'criado_em']
        read_only_fields = ['criado_em']


class HistoricoDocumentoSerializer(serializers.ModelSerializer):
    alterado_por_nome = serializers.CharField(source='alterado_por.full_name', read_only=True)
    
    class Meta:
        model = HistoricoDocumento
        fields = ['id', 'documento', 'versao_anterior', 'arquivo_anterior', 
                  'tamanho_arquivo', 'alterado_por', 'alterado_por_nome', 
                  'data_alteracao', 'observacao']
        read_only_fields = ['data_alteracao']


class DocumentoSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)
    historico = HistoricoDocumentoSerializer(many=True, read_only=True)
    enviado_por_nome = serializers.CharField(source='enviado_por.full_name', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    
    class Meta:
        model = Documento
        fields = ['id', 'projeto', 'projeto_nome', 'tarefa', 'tarefa_titulo', 
                  'titulo', 'descricao', 'tipo', 'tipo_display', 'arquivo', 
                  'tamanho_arquivo', 'tipo_arquivo', 'versao', 'enviado_por', 
                  'enviado_por_nome', 'data_upload', 'atualizado_em', 
                  'comentarios', 'historico']
        read_only_fields = ['data_upload', 'atualizado_em', 'tamanho_arquivo', 'tipo_arquivo']
    
    def create(self, validated_data):
        arquivo = validated_data.get('arquivo')
        
        # Adiciona informações sobre o arquivo
        if arquivo:
            validated_data['tamanho_arquivo'] = arquivo.size
            validated_data['tipo_arquivo'] = arquivo.content_type
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        arquivo = validated_data.get('arquivo')
        
        # Se está atualizando o arquivo, salva a versão anterior no histórico
        if arquivo and arquivo != instance.arquivo:
            HistoricoDocumento.objects.create(
                documento=instance,
                versao_anterior=instance.versao,
                arquivo_anterior=instance.arquivo,
                tamanho_arquivo=instance.tamanho_arquivo,
                alterado_por=self.context['request'].user if 'request' in self.context else None,
                observacao=f"Atualização da versão {instance.versao} para {validated_data.get('versao', instance.versao)}"
            )
            
            # Atualiza informações sobre o novo arquivo
            validated_data['tamanho_arquivo'] = arquivo.size
            validated_data['tipo_arquivo'] = arquivo.content_type
        
        return super().update(instance, validated_data)


class DocumentoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de documentos"""
    enviado_por_nome = serializers.CharField(source='enviado_por.full_name', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    
    class Meta:
        model = Documento
        fields = ['id', 'projeto', 'projeto_nome', 'tarefa', 'tarefa_titulo', 
                  'titulo', 'tipo', 'tipo_display', 'versao', 'enviado_por_nome', 
                  'data_upload', 'tamanho_arquivo', 'tipo_arquivo']
