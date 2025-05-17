from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, F, DecimalField, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from decimal import Decimal
from .models import Categoria, Custo, OrcamentoProjeto, OrcamentoTarefa, Alerta
from .serializers import (
    CategoriaSerializer, CustoSerializer, CustoListSerializer,
    OrcamentoProjetoSerializer, OrcamentoTarefaSerializer, AlertaSerializer,
    RelatorioGastoProjetoSerializer, RelatorioGastoCategoriasSerializer
)
from projects.models import Projeto
from tasks.models import Tarefa


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de categorias de custos.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome']


class CustoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de custos.
    Permite criar, listar, atualizar e excluir custos.
    """
    queryset = Custo.objects.all()
    serializer_class = CustoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['projeto', 'tarefa', 'categoria', 'tipo', 'data']
    search_fields = ['descricao', 'observacoes']
    ordering_fields = ['data', 'valor', 'criado_em']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CustoListSerializer
        return CustoSerializer
    
    def perform_create(self, serializer):
        custo = serializer.save(criado_por=self.request.user)
        
        # Verifica se precisa criar alertas de orçamento
        self._verificar_alertas_orcamento(custo)
    
    def _verificar_alertas_orcamento(self, custo):
        """
        Verifica se o custo adicionado/atualizado ultrapassa o limite de 80% do orçamento
        e cria alertas se necessário.
        """
        # Verifica orçamento do projeto
        try:
            orcamento_projeto = OrcamentoProjeto.objects.get(projeto=custo.projeto)
            percentual = (orcamento_projeto.valor_utilizado / orcamento_projeto.valor_total) * 100
            
            # Se ultrapassou 80% e não existir alerta ativo
            if percentual >= 80 and not Alerta.objects.filter(
                projeto=custo.projeto, 
                tipo='PROJETO', 
                status='ATIVO'
            ).exists():
                Alerta.objects.create(
                    tipo='PROJETO',
                    projeto=custo.projeto,
                    percentual=percentual,
                    mensagem=f"O projeto {custo.projeto.name} atingiu {percentual:.2f}% do orçamento planejado."
                )
        except OrcamentoProjeto.DoesNotExist:
            pass
        
        # Verifica orçamento da tarefa, se houver
        if custo.tarefa:
            try:
                orcamento_tarefa = OrcamentoTarefa.objects.get(tarefa=custo.tarefa)
                percentual = (orcamento_tarefa.valor_utilizado / orcamento_tarefa.valor) * 100
                
                # Se ultrapassou 80% e não existir alerta ativo
                if percentual >= 80 and not Alerta.objects.filter(
                    tarefa=custo.tarefa, 
                    tipo='TAREFA', 
                    status='ATIVO'
                ).exists():
                    Alerta.objects.create(
                        tipo='TAREFA',
                        projeto=custo.projeto,
                        tarefa=custo.tarefa,
                        percentual=percentual,
                        mensagem=f"A tarefa {custo.tarefa.titulo} atingiu {percentual:.2f}% do orçamento planejado."
                    )
            except OrcamentoTarefa.DoesNotExist:
                pass
    
    def get_queryset(self):
        """
        Filtra custos com base nos parâmetros da URL.
        """
        queryset = Custo.objects.all()
        
        # Filtra por projeto
        projeto_id = self.request.query_params.get('projeto')
        if projeto_id:
            try:
                queryset = queryset.filter(projeto_id=int(projeto_id))
            except (ValueError, TypeError):
                pass  # Ignora filtro se o valor não for um número válido
        
        # Filtra por tarefa
        tarefa_id = self.request.query_params.get('tarefa')
        if tarefa_id:
            try:
                queryset = queryset.filter(tarefa_id=int(tarefa_id))
            except (ValueError, TypeError):
                pass  # Ignora filtro se o valor não for um número válido
        
        # Filtra por categoria
        categoria = self.request.query_params.get('categoria')
        if categoria:
            # Tenta primeiro filtrar por ID numérico
            try:
                queryset = queryset.filter(categoria_id=int(categoria))
            except (ValueError, TypeError):
                # Se não for um ID numérico, tenta filtrar pelo nome da categoria
                queryset = queryset.filter(categoria__nome__iexact=categoria)
        
        # Filtra por tipo
        tipo = self.request.query_params.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        # Filtra por período
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        # Filtra por valor mínimo/máximo
        valor_min = self.request.query_params.get('valor_min')
        valor_max = self.request.query_params.get('valor_max')
        
        if valor_min:
            try:
                queryset = queryset.filter(valor__gte=float(valor_min))
            except (ValueError, TypeError):
                pass  # Ignora filtro se o valor não for um número válido
        
        if valor_max:
            try:
                queryset = queryset.filter(valor__lte=float(valor_max))
            except (ValueError, TypeError):
                pass  # Ignora filtro se o valor não for um número válido
        
        # Filtra por texto (busca em descrição e observações)
        texto = self.request.query_params.get('texto')
        if texto:
            queryset = queryset.filter(
                Q(descricao__icontains=texto) | Q(observacoes__icontains=texto)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def relatorio_por_projeto(self, request):
        """
        Gera um relatório de gastos por projeto.
        """
        # Obtém todos os projetos
        projetos = Projeto.objects.all()
        
        # Filtra por projeto específico, se fornecido
        projeto_id = request.query_params.get('projeto_id')
        if projeto_id:
            projetos = projetos.filter(id=projeto_id)
        
        # Prepara dados do relatório
        dados_relatorio = []
        
        for projeto in projetos:
            # Obtém orçamento total (ou 0 se não existir)
            try:
                orcamento = OrcamentoProjeto.objects.get(projeto=projeto)
                orcamento_total = orcamento.valor_total
            except OrcamentoProjeto.DoesNotExist:
                orcamento_total = Decimal('0.00')
            
            # Calcula valor gasto
            valor_gasto = Custo.objects.filter(projeto=projeto).aggregate(
                total=Coalesce(Sum('valor'), Value(0), output_field=DecimalField())
            )['total']
            
            # Adiciona ao relatório
            dados_relatorio.append({
                'projeto_id': projeto.id,
                'projeto_nome': projeto.name,
                'orcamento_total': orcamento_total,
                'valor_gasto': valor_gasto
            })
        
        # Serializa e retorna
        serializer = RelatorioGastoProjetoSerializer(dados_relatorio, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def relatorio_por_categoria(self, request):
        """
        Gera um relatório de gastos por categoria.
        """
        # Filtra por projeto específico, se fornecido
        projeto_id = request.query_params.get('projeto_id')
        filtro_projeto = Q(projeto_id=projeto_id) if projeto_id else Q()
        
        # Filtra por período, se fornecido
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        filtro_data = Q()
        if data_inicio:
            filtro_data &= Q(data__gte=data_inicio)
        if data_fim:
            filtro_data &= Q(data__lte=data_fim)
        
        # Obtém total de gastos para calcular percentuais
        total_gastos = Custo.objects.filter(
            filtro_projeto & filtro_data
        ).aggregate(
            total=Coalesce(Sum('valor'), Value(0), output_field=DecimalField())
        )['total']
        
        # Se não houver gastos, retorna lista vazia
        if total_gastos == 0:
            return Response([])
        
        # Agrupa gastos por categoria
        gastos_por_categoria = Custo.objects.filter(
            filtro_projeto & filtro_data
        ).values(
            'categoria', 'categoria__nome'
        ).annotate(
            valor_total=Sum('valor')
        ).order_by('-valor_total')
        
        # Prepara dados do relatório
        dados_relatorio = []
        
        for gasto in gastos_por_categoria:
            percentual = (gasto['valor_total'] / total_gastos) * 100
            
            dados_relatorio.append({
                'categoria_id': gasto['categoria'],
                'categoria_nome': gasto['categoria__nome'] if gasto['categoria'] else 'Sem Categoria',
                'valor_total': gasto['valor_total'],
                'percentual': percentual
            })
        
        # Serializa e retorna
        serializer = RelatorioGastoCategoriasSerializer(dados_relatorio, many=True)
        return Response(serializer.data)


class OrcamentoProjetoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de orçamentos de projetos.
    """
    queryset = OrcamentoProjeto.objects.all()
    serializer_class = OrcamentoProjetoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['projeto']
    
    def perform_create(self, serializer):
        serializer.save(aprovado_por=self.request.user)
    
    @action(detail=False, methods=['get'])
    def projetos_sem_orcamento(self, request):
        """
        Retorna a lista de projetos que ainda não possuem orçamento definido.
        """
        # Obtém IDs de projetos que já têm orçamento
        projetos_com_orcamento = OrcamentoProjeto.objects.values_list('projeto_id', flat=True)
        
        # Filtra projetos sem orçamento
        projetos_sem_orcamento = Projeto.objects.exclude(id__in=projetos_com_orcamento)
        
        # Retorna lista simplificada
        dados = [
            {'id': p.id, 'nome': p.name}
            for p in projetos_sem_orcamento
        ]
        
        return Response(dados)


class OrcamentoTarefaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de orçamentos de tarefas.
    """
    queryset = OrcamentoTarefa.objects.all()
    serializer_class = OrcamentoTarefaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tarefa', 'tarefa__projeto']
    
    def perform_create(self, serializer):
        serializer.save(aprovado_por=self.request.user)
    
    @action(detail=False, methods=['get'])
    def tarefas_sem_orcamento(self, request):
        """
        Retorna a lista de tarefas que ainda não possuem orçamento definido.
        """
        # Filtra por projeto, se fornecido
        projeto_id = request.query_params.get('projeto_id')
        filtro_projeto = Q(projeto_id=projeto_id) if projeto_id else Q()
        
        # Obtém IDs de tarefas que já têm orçamento
        tarefas_com_orcamento = OrcamentoTarefa.objects.values_list('tarefa_id', flat=True)
        
        # Filtra tarefas sem orçamento
        tarefas_sem_orcamento = Tarefa.objects.filter(filtro_projeto).exclude(id__in=tarefas_com_orcamento)
        
        # Retorna lista simplificada
        dados = [
            {'id': t.id, 'titulo': t.titulo, 'projeto_id': t.projeto_id, 'projeto_nome': t.projeto.name}
            for t in tarefas_sem_orcamento
        ]
        
        return Response(dados)


class AlertaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de alertas de orçamento.
    """
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['projeto', 'tarefa', 'tipo', 'status']
    ordering_fields = ['data_criacao', 'percentual']
    
    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        """
        Marca um alerta como resolvido.
        """
        alerta = self.get_object()
        
        if alerta.status != 'ATIVO':
            return Response(
                {'erro': 'Este alerta já foi resolvido ou ignorado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        alerta.status = 'RESOLVIDO'
        alerta.data_resolucao = timezone.now()
        alerta.resolvido_por = request.user
        alerta.save()
        
        serializer = self.get_serializer(alerta)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def ignorar(self, request, pk=None):
        """
        Marca um alerta como ignorado.
        """
        alerta = self.get_object()
        
        if alerta.status != 'ATIVO':
            return Response(
                {'erro': 'Este alerta já foi resolvido ou ignorado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        alerta.status = 'IGNORADO'
        alerta.data_resolucao = timezone.now()
        alerta.resolvido_por = request.user
        alerta.save()
        
        serializer = self.get_serializer(alerta)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def alertas_ativos(self, request):
        """
        Retorna apenas os alertas ativos.
        """
        alertas = Alerta.objects.filter(status='ATIVO')
        
        # Filtra por projeto, se fornecido
        projeto_id = request.query_params.get('projeto_id')
        if projeto_id:
            alertas = alertas.filter(projeto_id=projeto_id)
        
        serializer = self.get_serializer(alertas, many=True)
        return Response(serializer.data)
