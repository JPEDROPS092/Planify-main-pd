from rest_framework import serializers
from .models import Categoria, Custo, OrcamentoProjeto, OrcamentoTarefa, Alerta
from decimal import Decimal


# --- Serializers para Modelos ---

class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Categoria.

    Utilizado para serializar/desserializar dados da categoria.
    Inclui todos os campos do modelo.
    """
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']


class CustoSerializer(serializers.ModelSerializer):
    """
    Serializer detalhado para o modelo Custo.

    Inclui todos os campos do modelo Custo e adiciona campos de leitura
    para exibir nomes relacionados de outros modelos (usuário, projeto, tarefa, categoria)
    e o valor textual dos campos de escolha ('tipo').
    """
    # Campos de leitura para exibir nomes relacionados
    criado_por_nome = serializers.CharField(source='criado_por.full_name', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    # Campo de leitura para exibir o valor 'display' do campo 'tipo'
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Custo
        fields = ['id', 'projeto', 'projeto_nome', 'tarefa', 'tarefa_titulo', 
                  'categoria', 'categoria_nome', 'descricao', 'valor', 'tipo', 
                  'tipo_display', 'data', 'comprovante', 'observacoes', 
                  'criado_por', 'criado_por_nome', 'criado_em', 'atualizado_em']
        
        # Campos que são definidos automaticamente pelo modelo
        read_only_fields = ['criado_em', 'atualizado_em']


class CustoListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de custos.

    Projetado para exibir uma visão concisa dos custos, ideal para listas
    ou tabelas onde nem todos os detalhes do Custo são necessários.
    Inclui campos de leitura para nomes relacionados e o valor 'display' do tipo.
    """
    # Campos de leitura para exibir nomes relacionados e o valor 'display' do tipo
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = Custo
        fields = ['id', 'projeto', 'projeto_nome', 'tarefa', 'tarefa_titulo', 
                  'categoria_nome', 'descricao', 'valor', 'tipo_display', 'data']


class OrcamentoProjetoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo OrcamentoProjeto.

    Inclui campos para o orçamento total e informações de aprovação.
    Adiciona campos de leitura para nomes relacionados (aprovador, projeto)
    e campos calculados (valor utilizado, valor restante, percentual utilizado).
    """
    # Campos de leitura para exibir nomes relacionados
    aprovado_por_nome = serializers.CharField(source='aprovado_por.full_name', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    
    # Campos calculados dinamicamente no modelo/view/queryset, tornados read_only
    valor_utilizado = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    valor_restante = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    percentual_utilizado = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrcamentoProjeto
        fields = ['id', 'projeto', 'projeto_nome', 'valor_total', 'data_aprovacao', 
                  'aprovado_por', 'aprovado_por_nome', 'observacoes', 
                  'valor_utilizado', 'valor_restante', 'percentual_utilizado']
        
        # Campos que são definidos automaticamente ou calculados
        read_only_fields = ['data_aprovacao', 'valor_utilizado', 'valor_restante', 'percentual_utilizado']


class OrcamentoTarefaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo OrcamentoTarefa.

    Inclui campos para o orçamento de uma tarefa específica e informações de aprovação.
    Adiciona campos de leitura para nomes relacionados (aprovador, tarefa, projeto da tarefa)
    e campos calculados (valor utilizado, valor restante, percentual utilizado).
    """
    # Campos de leitura para exibir nomes relacionados
    aprovado_por_nome = serializers.CharField(source='aprovado_por.full_name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    # Acessa o nome do projeto através da tarefa relacionada
    projeto_nome = serializers.CharField(source='tarefa.projeto.name', read_only=True)
    
    # Campos calculados dinamicamente no modelo/view/queryset, tornados read_only
    valor_utilizado = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    valor_restante = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    percentual_utilizado = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrcamentoTarefa
        fields = ['id', 'tarefa', 'tarefa_titulo', 'projeto_nome', 'valor', 
                  'data_aprovacao', 'aprovado_por', 'aprovado_por_nome', 
                  'observacoes', 'valor_utilizado', 'valor_restante', 'percentual_utilizado']
        
        # Campos que são definidos automaticamente ou calculados
        read_only_fields = ['data_aprovacao', 'valor_utilizado', 'valor_restante', 'percentual_utilizado']


class AlertaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Alerta.

    Inclui todos os campos do modelo Alerta.
    Adiciona campos de leitura para exibir o valor textual dos campos de escolha
    ('tipo', 'status') e nomes relacionados (projeto, tarefa, resolvedor).
    """
    # Campos de leitura para exibir o valor 'display' dos campos de escolha
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    # Campos de leitura para exibir nomes relacionados
    projeto_nome = serializers.CharField(source='projeto.name', read_only=True)
    tarefa_titulo = serializers.CharField(source='tarefa.titulo', read_only=True)
    resolvido_por_nome = serializers.CharField(source='resolvido_por.full_name', read_only=True)
    
    class Meta:
        model = Alerta
        fields = ['id', 'tipo', 'tipo_display', 'projeto', 'projeto_nome', 
                  'tarefa', 'tarefa_titulo', 'percentual', 'mensagem', 
                  'status', 'status_display', 'data_criacao', 'data_resolucao', 
                  'resolvido_por', 'resolvido_por_nome']
        
        # Campos que são definidos automaticamente
        read_only_fields = ['data_criacao', 'data_resolucao']


# --- Serializers para Relatórios (não baseados diretamente em um único modelo) ---

class RelatorioGastoProjetoSerializer(serializers.Serializer):
    """
    Serializer para dados agregados de relatório de gastos por projeto.

    Este serializer *não* está associado a um modelo específico, mas sim
    projetado para formatar dados resultantes de agregações ou consultas
    personalizadas (geralmente vindas de views).
    Define a estrutura esperada dos dados de relatório.
    Sobrescreve `to_representation` para calcular 'valor_restante' e 'percentual_gasto'.
    """
    # Campos que se esperam receber dos dados agregados
    projeto_id = serializers.IntegerField()
    projeto_nome = serializers.CharField()
    orcamento_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    valor_gasto = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    # Campos calculados no método to_representation, não esperados na entrada
    valor_restante = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    percentual_gasto = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    
    def to_representation(self, instance):
        """
        Sobrescreve o método para calcular campos derivados (`valor_restante`, `percentual_gasto`).

        Recebe a instância de dados agregados (geralmente um dicionário) e
        calcula os valores adicionais antes de formatar a saída final.
        Trata casos onde o orçamento é zero para evitar divisão por zero.
        """
        # Obtém os valores da instância, tratando possíveis casos None
        orcamento_total = instance.get('orcamento_total') or Decimal('0.00')
        valor_gasto = instance.get('valor_gasto') or Decimal('0.00')
        
        # Calcula o valor restante
        valor_restante = orcamento_total - valor_gasto
        
        # Calcula o percentual gasto, evitando divisão por zero
        if orcamento_total > 0:
            percentual_gasto = (valor_gasto / orcamento_total) * 100
        else:
            percentual_gasto = Decimal('0.00')
        
        # Retorna a representação final com todos os campos, incluindo os calculados
        return {
            'projeto_id': instance.get('projeto_id'),
            'projeto_nome': instance.get('projeto_nome'),
            'orcamento_total': orcamento_total,
            'valor_gasto': valor_gasto,
            'valor_restante': valor_restante,
            'percentual_gasto': percentual_gasto
        }


class RelatorioGastoCategoriasSerializer(serializers.Serializer):
    """
    Serializer para dados agregados de relatório de gastos por categoria.

    Similar ao `RelatorioGastoProjetoSerializer`, este serializer formata
    dados agregados por categoria, geralmente vindos de consultas.
    Define a estrutura esperada dos dados de relatório.
    Sobrescreve `to_representation` para tratar categorias nulas e garantir
    valores Decimal.
    """
    # Campos que se esperam receber dos dados agregados
    # categoria_id pode ser None para custos sem categoria
    categoria_id = serializers.IntegerField(allow_null=True)
    categoria_nome = serializers.CharField()
    valor_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    # Percentual geralmente é calculado na view/queryset antes de ser passado para o serializer
    percentual = serializers.DecimalField(max_digits=5, decimal_places=2)
    
    def to_representation(self, instance):
        """
        Sobrescreve o método para formatar a representação, tratando casos nulos.

        Recebe a instância de dados agregados e garante que campos como
        `categoria_nome` tenham um valor padrão ('Sem Categoria') se forem nulos
        e que os valores monetários sejam Decimais.
        """
        # Retorna a representação formatada, tratando possíveis valores None
        return {
            'categoria_id': instance.get('categoria_id'),
            # Fornece um nome padrão se a categoria_nome for None
            'categoria_nome': instance.get('categoria_nome') or 'Sem Categoria',
            # Garante que o valor_total é um Decimal, default 0.00
            'valor_total': instance.get('valor_total') or Decimal('0.00'),
             # Garante que o percentual é um Decimal, default 0.00
            'percentual': instance.get('percentual') or Decimal('0.00')
        }