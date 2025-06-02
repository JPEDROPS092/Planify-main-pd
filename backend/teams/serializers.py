from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field # Adicionado para type hints
from drf_spectacular.types import OpenApiTypes # Adicionado para tipos OpenAPI
from .models import Equipe, MembroEquipe, PermissaoEquipe
from django.contrib.auth import get_user_model

User = get_user_model()


class PermissaoEquipeSerializer(serializers.ModelSerializer):
    papel_display = serializers.CharField(source='get_papel_display', read_only=True)
    modulo_display = serializers.CharField(source='get_modulo_display', read_only=True)
    permissao_display = serializers.CharField(source='get_permissao_display', read_only=True)
    
    class Meta:
        model = PermissaoEquipe
        fields = ['id', 'papel', 'papel_display', 'equipe', 'modulo', 
                  'modulo_display', 'permissao', 'permissao_display']


class MembroEquipeSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.full_name', read_only=True)
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    papel_display = serializers.CharField(source='get_papel_display', read_only=True)
    adicionado_por_nome = serializers.CharField(source='adicionado_por.full_name', read_only=True)
    
    class Meta:
        model = MembroEquipe
        fields = ['id', 'equipe', 'usuario', 'usuario_nome', 'usuario_email', 
                  'papel', 'papel_display', 'adicionado_em', 
                  'adicionado_por', 'adicionado_por_nome']
        read_only_fields = ['adicionado_em']


class EquipeSerializer(serializers.ModelSerializer):
    membros = MembroEquipeSerializer(many=True, read_only=True, help_text="Lista de membros desta equipe.")
    permissoes = PermissaoEquipeSerializer(many=True, read_only=True, help_text="Lista de permissões associadas a esta equipe.")
    criado_por_nome = serializers.CharField(source='criado_por.full_name', read_only=True, help_text="Nome completo do usuário que criou a equipe.")
    # Comentário: Número total de membros na equipe.
    total_membros = serializers.SerializerMethodField(help_text="Número total de membros nesta equipe.")
    
    class Meta:
        model = Equipe
        fields = ['id', 'nome', 'descricao', 'criado_por', 'criado_por_nome', 
                  'criado_em', 'atualizado_em', 'membros', 'permissoes', 'total_membros']
        read_only_fields = ['criado_em', 'atualizado_em']
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_total_membros(self, obj):
        # Comentário: Retorna a contagem de membros associados à equipe.
        return obj.membros.count()
    
    def create(self, validated_data):
        # Cria a equipe
        equipe = Equipe.objects.create(**validated_data)
        
        # Adiciona o criador como membro da equipe com papel de PO (Product Owner)
        if 'request' in self.context:
            MembroEquipe.objects.create(
                equipe=equipe,
                usuario=self.context['request'].user,
                papel='PO',
                adicionado_por=self.context['request'].user
            )
        
        return equipe


class EquipeListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de equipes"""
    # Comentário: Número total de membros na equipe.
    total_membros = serializers.SerializerMethodField(help_text="Número total de membros nesta equipe.")
    criado_por_nome = serializers.CharField(source='criado_por.full_name', read_only=True, help_text="Nome completo do criador da equipe.")
    
    class Meta:
        model = Equipe
        fields = ['id', 'nome', 'criado_por_nome', 'criado_em', 'total_membros']
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_total_membros(self, obj):
        # Comentário: Retorna a contagem de membros associados à equipe.
        return obj.membros.count()


class UserMinimalSerializer(serializers.ModelSerializer):
    """Serializer mínimo para usuários, usado para seleção de membros"""
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email']
