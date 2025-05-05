from rest_framework import serializers
from .models import Categoria, Custo, OrcamentoProjeto, OrcamentoTarefa, Alerta
from decimal import Decimal


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']


class CustoSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(source='criado_por.full_name', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = Custo
        fields = ['id', 'projeto', 'projeto_nome', 'tarefa', 'tarefa_titulo', 
                  'categoria', 'categoria_nome', 'descricao', 'valor', 'tipo', 
                  'tipo_display', 'data', 'comprovante', 'observacoes', 
                  'criado_por', 'criado_por_nome', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']


class CustoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de custos"""
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = Custo
        fields = ['id', 'projeto', 'projeto_nome', 'tarefa', 'tarefa_titulo', 
                  'categoria_nome', 'descricao', 'valor', 'tipo_display', 'data']


class OrcamentoProjetoSerializer(serializers.ModelSerializer):
    aprovado_por_nome = serializers.CharField(source='aprovado_por.full_name', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    valor_utilizado = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    valor_restante = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    percentual_utilizado = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrcamentoProjeto
        fields = ['id', 'projeto', 'projeto_nome', 'valor_total', 'data_aprovacao', 
                  'aprovado_por', 'aprovado_por_nome', 'observacoes', 
                  'valor_utilizado', 'valor_restante', 'percentual_utilizado']
        read_only_fields = ['data_aprovacao', 'valor_utilizado', 'valor_restante', 'percentual_utilizado']


class OrcamentoTarefaSerializer(serializers.ModelSerializer):
    aprovado_por_nome = serializers.CharField(source='aprovado_por.full_name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    projeto_nome = serializers.CharField(source='tarefa.projeto.name', read_only=True)
    valor_utilizado = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    valor_restante = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    percentual_utilizado = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrcamentoTarefa
        fields = ['id', 'tarefa', 'tarefa_titulo', 'projeto_nome', 'valor', 
                  'data_aprovacao', 'aprovado_por', 'aprovado_por_nome', 
                  'observacoes', 'valor_utilizado', 'valor_restante', 'percentual_utilizado']
        read_only_fields = ['data_aprovacao', 'valor_utilizado', 'valor_restante', 'percentual_utilizado']


class AlertaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    resolvido_por_nome = serializers.CharField(source='resolvido_por.full_name', read_only=True)
    
    class Meta:
        model = Alerta
        fields = ['id', 'tipo', 'tipo_display', 'projeto', 'projeto_nome', 
                  'tarefa', 'tarefa_titulo', 'percentual', 'mensagem', 
                  'status', 'status_display', 'data_criacao', 'data_resolucao', 
                  'resolvido_por', 'resolvido_por_nome']
        read_only_fields = ['data_criacao', 'data_resolucao']


class RelatorioGastoProjetoSerializer(serializers.Serializer):
    """Serializer para relatório de gastos por projeto"""
    projeto_id = serializers.IntegerField()
    projeto_nome = serializers.CharField()
    orcamento_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    valor_gasto = serializers.DecimalField(max_digits=12, decimal_places=2)
    valor_restante = serializers.DecimalField(max_digits=12, decimal_places=2)
    percentual_gasto = serializers.DecimalField(max_digits=5, decimal_places=2)
    
    def to_representation(self, instance):
        # Calcula valores derivados
        orcamento_total = instance.get('orcamento_total') or Decimal('0.00')
        valor_gasto = instance.get('valor_gasto') or Decimal('0.00')
        valor_restante = orcamento_total - valor_gasto
        
        # Calcula percentual gasto
        if orcamento_total > 0:
            percentual_gasto = (valor_gasto / orcamento_total) * 100
        else:
            percentual_gasto = Decimal('0.00')
        
        # Retorna representação completa
        return {
            'projeto_id': instance.get('projeto_id'),
            'projeto_nome': instance.get('projeto_nome'),
            'orcamento_total': orcamento_total,
            'valor_gasto': valor_gasto,
            'valor_restante': valor_restante,
            'percentual_gasto': percentual_gasto
        }


class RelatorioGastoCategoriasSerializer(serializers.Serializer):
    """Serializer para relatório de gastos por categoria"""
    categoria_id = serializers.IntegerField(allow_null=True)
    categoria_nome = serializers.CharField()
    valor_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    percentual = serializers.DecimalField(max_digits=5, decimal_places=2)
    
    def to_representation(self, instance):
        return {
            'categoria_id': instance.get('categoria_id'),
            'categoria_nome': instance.get('categoria_nome') or 'Sem Categoria',
            'valor_total': instance.get('valor_total') or Decimal('0.00'),
            'percentual': instance.get('percentual') or Decimal('0.00')
        }
