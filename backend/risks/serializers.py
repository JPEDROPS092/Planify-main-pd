from rest_framework import serializers
from .models import Risco, HistoricoRisco


class HistoricoRiscoSerializer(serializers.ModelSerializer):
    alterado_por_nome = serializers.CharField(source='alterado_por.full_name', read_only=True)
    status_anterior_display = serializers.CharField(source='get_status_anterior_display', read_only=True)
    novo_status_display = serializers.CharField(source='get_novo_status_display', read_only=True)
    probabilidade_anterior_display = serializers.CharField(source='get_probabilidade_anterior_display', read_only=True)
    nova_probabilidade_display = serializers.CharField(source='get_nova_probabilidade_display', read_only=True)
    impacto_anterior_display = serializers.CharField(source='get_impacto_anterior_display', read_only=True)
    novo_impacto_display = serializers.CharField(source='get_novo_impacto_display', read_only=True)
    
    class Meta:
        model = HistoricoRisco
        fields = ['id', 'risco', 'status_anterior', 'status_anterior_display', 
                  'novo_status', 'novo_status_display', 
                  'probabilidade_anterior', 'probabilidade_anterior_display', 
                  'nova_probabilidade', 'nova_probabilidade_display', 
                  'impacto_anterior', 'impacto_anterior_display', 
                  'novo_impacto', 'novo_impacto_display', 
                  'alterado_por', 'alterado_por_nome', 'alterado_em', 'observacao']
        read_only_fields = ['alterado_em']


class RiscoSerializer(serializers.ModelSerializer):
    historico = HistoricoRiscoSerializer(many=True, read_only=True)
    criado_por_nome = serializers.CharField(source='criado_por.full_name', read_only=True)
    responsavel_mitigacao_nome = serializers.CharField(source='responsavel_mitigacao.full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    probabilidade_display = serializers.CharField(source='get_probabilidade_display', read_only=True)
    impacto_display = serializers.CharField(source='get_impacto_display', read_only=True)
    nivel_risco = serializers.CharField(read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    
    class Meta:
        model = Risco
        fields = ['id', 'projeto', 'projeto_nome', 'descricao', 
                  'probabilidade', 'probabilidade_display', 
                  'impacto', 'impacto_display', 
                  'status', 'status_display', 
                  'responsavel_mitigacao', 'responsavel_mitigacao_nome', 
                  'plano_mitigacao', 'plano_contingencia', 
                  'data_identificacao', 'criado_por', 'criado_por_nome', 
                  'atualizado_em', 'nivel_risco', 'historico']
        read_only_fields = ['data_identificacao', 'atualizado_em', 'nivel_risco']
    
    def create(self, validated_data):
        # Cria o risco
        risco = Risco.objects.create(**validated_data)
        
        # Cria o histórico inicial
        HistoricoRisco.objects.create(
            risco=risco,
            status_anterior='',
            novo_status=risco.status,
            probabilidade_anterior='',
            nova_probabilidade=risco.probabilidade,
            impacto_anterior='',
            novo_impacto=risco.impacto,
            alterado_por=validated_data.get('criado_por'),
            observacao='Risco criado'
        )
        
        return risco
    
    def update(self, instance, validated_data):
        # Salva os valores anteriores
        status_anterior = instance.status
        probabilidade_anterior = instance.probabilidade
        impacto_anterior = instance.impacto
        
        # Atualiza a instância
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        # Se houve alteração, registra no histórico
        if (status_anterior != instance.status or 
            probabilidade_anterior != instance.probabilidade or 
            impacto_anterior != instance.impacto):
            
            HistoricoRisco.objects.create(
                risco=instance,
                status_anterior=status_anterior,
                novo_status=instance.status,
                probabilidade_anterior=probabilidade_anterior,
                nova_probabilidade=instance.probabilidade,
                impacto_anterior=impacto_anterior,
                novo_impacto=instance.impacto,
                alterado_por=self.context['request'].user if 'request' in self.context else None,
                observacao='Risco atualizado'
            )
        
        return instance


class RiscoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de riscos"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    probabilidade_display = serializers.CharField(source='get_probabilidade_display', read_only=True)
    impacto_display = serializers.CharField(source='get_impacto_display', read_only=True)
    nivel_risco = serializers.CharField(read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    responsavel_mitigacao_nome = serializers.CharField(source='responsavel_mitigacao.full_name', read_only=True)
    
    class Meta:
        model = Risco
        fields = ['id', 'projeto', 'projeto_nome', 'descricao', 
                  'probabilidade', 'probabilidade_display', 
                  'impacto', 'impacto_display', 
                  'status', 'status_display', 
                  'responsavel_mitigacao', 'responsavel_mitigacao_nome',
                  'data_identificacao', 'nivel_risco']
