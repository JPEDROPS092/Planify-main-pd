from rest_framework import serializers
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
    membros = MembroEquipeSerializer(many=True, read_only=True)
    permissoes = PermissaoEquipeSerializer(many=True, read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.full_name', read_only=True)
    total_membros = serializers.SerializerMethodField()
    
    class Meta:
        model = Equipe
        fields = ['id', 'nome', 'descricao', 'criado_por', 'criado_por_nome', 
                  'criado_em', 'atualizado_em', 'membros', 'permissoes', 'total_membros']
        read_only_fields = ['criado_em', 'atualizado_em']
    
    def get_total_membros(self, obj):
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
    total_membros = serializers.SerializerMethodField()
    criado_por_nome = serializers.CharField(source='criado_por.full_name', read_only=True)
    
    class Meta:
        model = Equipe
        fields = ['id', 'nome', 'criado_por_nome', 'criado_em', 'total_membros']
    
    def get_total_membros(self, obj):
        return obj.membros.count()


class UserMinimalSerializer(serializers.ModelSerializer):
    """Serializer mínimo para usuários, usado para seleção de membros"""
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email']
