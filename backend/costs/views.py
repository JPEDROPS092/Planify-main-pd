from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, F, DecimalField, Value, Case, When, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Categoria, Custo, OrcamentoProjeto, OrcamentoTarefa, Alerta
from .serializers import (
    CategoriaSerializer, CustoSerializer, CustoListSerializer,
    OrcamentoProjetoSerializer, OrcamentoTarefaSerializer, AlertaSerializer,
    RelatorioGastoProjetoSerializer, RelatorioGastoCategoriasSerializer
)
from projects.models import Projeto
from tasks.models import Tarefa

@extend_schema_view(
    list=extend_schema(
        summary="Listar categorias",
        tags=["Custo"],
        description="Retorna uma lista paginada de categorias.",
        responses={200: CategoriaSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes da categoria",
        tags=["Custo"],
        description="Retorna informações detalhadas de uma categoria específica.",
        responses={200: CategoriaSerializer}
    ),
    create=extend_schema(
        summary="Criar nova categoria",
        tags=["Custo"],
        description="Cria uma novo categoria.",
        responses={201: CategoriaSerializer}
    ),
    update=extend_schema(
        summary="Atualizar categoria",
        tags=["Custo"],
        description="Atualiza todos os campos de uma categoria existente.",
        responses={200: CategoriaSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar categoria parcialmente",
        tags=["Custo"],
        description="Atualiza parcialmente uma categoria existente.",
        responses={200: CategoriaSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir categoria",
        tags=["Custo"],
        description="Remove uma categoria existente.",
        responses={204: None}
    )
)
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

@extend_schema_view(
    list=extend_schema(
        summary="Listar custos",
        tags=["Custo"],
        description="Retorna uma lista paginada de custos.",
        responses={200: CustoListSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes do custo",
        tags=["Custo"],
        description="Retorna informações detalhadas de um custo específico.",
        responses={200: CustoSerializer}
    ),
    create=extend_schema(
        summary="Criar novo custo",
        tags=["Custo"],
        description="Cria um novo custo.",
        responses={201: CustoSerializer}
    ),
    update=extend_schema(
        summary="Atualizar custo",
        tags=["Custo"],
        description="Atualiza todos os campos de um custo existente.",
        responses={200: CustoSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar custo parcialmente",
        tags=["Custo"],
        description="Atualiza parcialmente um custo existente.",
        responses={200: CustoSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir custo",
        tags=["Custo"],
        description="Remove um custo existente.",
        responses={204: None}
    )
)
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
    
    def get_queryset(self):
        """
        Filtra custos com base nos parâmetros da URL.
        Otimiza consultas com select_related para reduzir o número de queries.
        """
        queryset = Custo.objects.select_related(
            'projeto', 'tarefa', 'categoria', 'criado_por'
        ).all()
        
        # Filtra por projeto
        projeto_id = self.request.GET.get('projeto')
        if projeto_id:
            try:
                queryset = queryset.filter(projeto_id=int(projeto_id))
            except (ValueError, TypeError):
                pass  # Ignora filtro se o valor não for um número válido
        
        # Filtra por tarefa
        tarefa_id = self.request.GET.get('tarefa')
        if tarefa_id:
            try:
                queryset = queryset.filter(tarefa_id=int(tarefa_id))
            except (ValueError, TypeError):
                pass  # Ignora filtro se o valor não for um número válido
        
        # Filtra por categoria
        categoria = self.request.GET.get('categoria')
        if categoria:
            # Tenta primeiro filtrar por ID numérico
            try:
                queryset = queryset.filter(categoria_id=int(categoria))
            except (ValueError, TypeError):
                # Se não for um ID numérico, tenta filtrar pelo nome da categoria
                queryset = queryset.filter(categoria__nome__iexact=categoria)
        
        # Filtra por tipo
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        # Filtra por período
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        
        # Filtra por valor mínimo/máximo
        valor_min = self.request.GET.get('valor_min')
        valor_max = self.request.GET.get('valor_max')
        
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
        texto = self.request.GET.get('texto')
        if texto:
            queryset = queryset.filter(
                Q(descricao__icontains=texto) | Q(observacoes__icontains=texto)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        custo = serializer.save(criado_por=self.request.user)
        
        # Verifica se precisa criar alertas de orçamento
        self._verificar_alertas_orcamento(custo)
    
    def perform_update(self, serializer):
        """
        Sobrescreve o método para atualizar alertas de orçamento quando um custo é modificado
        """
        custo = serializer.save()
        # Verifica se o valor foi alterado e, se sim, verifica os alertas
        if 'valor' in serializer.validated_data:
            self._verificar_alertas_orcamento(custo)
    
    def _verificar_alertas_orcamento(self, custo):
        """
        Verifica se o custo adicionado/atualizado ultrapassa o limite de 80% do orçamento
        e cria alertas se necessário.
        
        Usa agregações diretas no banco de dados para calcular os valores utilizados
        e percentuais, evitando consultas N+1.
        """
        # Verifica orçamento do projeto
        if custo.projeto is not None:
            try:
                # Obter orçamento e calcular valor utilizado em uma única query
                from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Case, When, Value
                
                orcamento_projeto = OrcamentoProjeto.objects.filter(projeto=custo.projeto).annotate(
                    valor_utilizado=Coalesce(Sum('projeto__custos__valor'), Value(0), output_field=DecimalField()),
                    percentual_calculado=Case(
                        When(valor_total=0, then=Value(0, output_field=DecimalField())),
                        default=ExpressionWrapper(
                            Coalesce(Sum('projeto__custos__valor'), Value(0), output_field=DecimalField()) * 100 / F('valor_total'),
                            output_field=DecimalField(max_digits=5, decimal_places=2)
                        )
                    )
                ).first()
                
                if not orcamento_projeto:
                    return
                
                percentual = getattr(orcamento_projeto, 'percentual_calculado', 0)
                
                # Verificar se já existe alerta ativo
                alertas_ativos_projeto = Alerta.objects.filter(
                    projeto=custo.projeto, 
                    tipo='PROJETO', 
                    status='ATIVO'
                ).exists()
                
                # Se ultrapassou 80% e não existir alerta ativo
                if percentual >= 80 and not alertas_ativos_projeto:
                    Alerta.objects.create(
                        tipo='PROJETO',
                        projeto=custo.projeto,
                        percentual=percentual,
                        mensagem=f"O projeto {custo.projeto.name} atingiu {percentual:.2f}% do orçamento planejado."
                    )
            except Exception as e:
                # Registrar o erro para depuração
                print(f"Erro ao verificar orçamento do projeto: {e}")
                pass
        
        # Verifica orçamento da tarefa
        if custo.tarefa:
            try:
                # Obter orçamento e calcular valor utilizado em uma única query
                orcamento_tarefa = OrcamentoTarefa.objects.filter(tarefa=custo.tarefa).annotate(
                    valor_utilizado=Coalesce(Sum('tarefa__custos__valor'), Value(0), output_field=DecimalField()),
                    percentual_calculado=Case(
                        When(valor=0, then=Value(0, output_field=DecimalField())),
                        default=ExpressionWrapper(
                            Coalesce(Sum('tarefa__custos__valor'), Value(0), output_field=DecimalField()) * 100 / F('valor'),
                            output_field=DecimalField(max_digits=5, decimal_places=2)
                        )
                    )
                ).first()
                
                if not orcamento_tarefa:
                    return
                
                percentual = getattr(orcamento_tarefa, 'percentual_calculado', 0)
                
                # Verificar se já existe alerta ativo
                alerta_existe = Alerta.objects.filter(
                    tarefa=custo.tarefa, 
                    tipo='TAREFA', 
                    status='ATIVO'
                ).exists()
                
                # Se ultrapassou 80% e não existir alerta ativo
                if percentual >= 80 and not alerta_existe:
                    Alerta.objects.create(
                        tipo='TAREFA',
                        projeto=custo.projeto,
                        tarefa=custo.tarefa,
                        percentual=percentual,
                        mensagem=f"A tarefa {custo.tarefa.titulo} atingiu {percentual:.2f}% do orçamento planejado."
                    )
            except Exception as e:
                # Registrar o erro para depuração
                print(f"Erro ao verificar orçamento da tarefa: {e}")
                pass
    
    @extend_schema(
        summary="Dashboard financeiro",
        tags=["Custo"],
        responses={200: None}
    )
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Endpoint para dashboard financeiro: retorna dados resumidos de custos.
        Inclui total gasto, gasto mensal, top categorias e alertas recentes.
        """
        # Filtra por projeto específico, se fornecido
        projeto_id = request.query_params.get('projeto_id')
        filtro_projeto = Q(projeto_id=projeto_id) if projeto_id else Q()
        
        # Total gasto (todos os custos)
        total_gasto = Custo.objects.filter(filtro_projeto).aggregate(
            total=Coalesce(Sum('valor'), Value(0), output_field=DecimalField())
        )['total'] or Decimal('0.00')
        
        # Gastos por mês (últimos 12 meses)
        from django.db.models.functions import TruncMonth
        from datetime import timedelta
        data_limite = timezone.now().date().replace(day=1) - timedelta(days=365)

        
        gastos_mensais = Custo.objects.filter(
            filtro_projeto, 
            data__gte=data_limite
        ).annotate(
            mes=TruncMonth('data')
        ).values(
            'mes'
        ).annotate(
            total=Sum('valor')
        ).order_by('mes')
        
        # Top 5 categorias de custos
        top_categorias = Custo.objects.filter(
            filtro_projeto
        ).values(
            'categoria', 'categoria__nome'
        ).annotate(
            total=Sum('valor')
        ).order_by('-total')[:5]
        
        # Alertas recentes (últimos 5)
        alertas_recentes = Alerta.objects.filter(
            filtro_projeto
        ).order_by('-data_criacao')[:5]
        
        # Serializa alertas recentes
        # Removed unused import
        alertas_serializados = AlertaSerializer(alertas_recentes, many=True).data
        
        # Monta e retorna resposta
        resposta = {
            'total_gasto': total_gasto,
            'gastos_mensais': list(gastos_mensais),
            'top_categorias': [{
                'categoria_id': cat['categoria'],
                'categoria_nome': cat['categoria__nome'] if cat['categoria'] else 'Sem Categoria',
                'total': cat['total']
            } for cat in top_categorias],
            'alertas_recentes': alertas_serializados
        }
        
        return Response(resposta)
    
    @extend_schema(
        summary="Relatório de gastos por projeto",
        tags=["Custo"],
        responses={200: None}
    )
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
        # Prefetch aggregated values for all projects
        valores_gastos = Custo.objects.values('projeto').annotate(
            total_gasto=Coalesce(Sum('valor'), Value(0), output_field=DecimalField())
        )
        valores_gastos_dict = {item['projeto']: item['total_gasto'] for item in valores_gastos}

        for projeto in projetos:
            # Obtém orçamento total (ou 0 se não existir)
            try:
                orcamento = OrcamentoProjeto.objects.get(projeto=projeto)
                orcamento_total = orcamento.valor_total
            except OrcamentoProjeto.DoesNotExist:
                orcamento_total = Decimal('0.00')
            
            # Obtém valor gasto do dicionário prefetchado
            valor_gasto = valores_gastos_dict.get(getattr(projeto, 'id', None), Decimal('0.00'))
            
            # Adiciona ao relatório
            dados_relatorio.append({
                'projeto_id': getattr(projeto, 'id', None),
                'projeto_nome': getattr(projeto, 'name', 'Unknown'),
                'orcamento_total': orcamento_total,
                'valor_gasto': valor_gasto
            })
        
        # Serializa e retorna
        serializer = RelatorioGastoProjetoSerializer(dados_relatorio, many=True)
        return Response(serializer.data)
    

    @extend_schema(
        summary="Relatório de gastos por categoria",
        tags=["Custo"],
        responses={200: None}
    )
    @action(detail=False, methods=['get'])
    def relatorio_por_categoria(self, request):
        """
        Gera um relatório de gastos por categoria.
        Utiliza anotações para calcular percentuais diretamente no banco de dados.
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
        
        # Obtém total de gastos para calcular percentuais em uma única query
        from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Value, CharField, Case, When
        from django.db.models.functions import Coalesce
        
        total_gastos = Custo.objects.filter(
            filtro_projeto & filtro_data
        ).aggregate(total=Coalesce(Sum('valor'), Value(0), output_field=DecimalField()))['total']
        
        # Se não houver gastos, retorna lista vazia
        if not total_gastos or total_gastos == 0:
            return Response([])
        
        # Agrupa gastos por categoria e calcula percentuais diretamente no banco de dados
        gastos_por_categoria = Custo.objects.filter(
            filtro_projeto & filtro_data
        ).values(
            'categoria', 'categoria__nome'
        ).annotate(
            valor_total=Sum('valor'),
            percentual=ExpressionWrapper(
                (Sum('valor') * 100) / Value(total_gastos),
                output_field=DecimalField(max_digits=5, decimal_places=2)
            )
        ).order_by('-valor_total')
        
        # Prepara dados do relatório com os percentuais já calculados pelo banco
        dados_relatorio = []
        
        for gasto in gastos_por_categoria:
            dados_relatorio.append({
                'categoria_id': gasto['categoria'],
                'categoria_nome': gasto['categoria__nome'] if gasto['categoria'] else 'Sem Categoria',
                'valor_total': gasto['valor_total'],
                'percentual': gasto['percentual']
            })
        
        # Serializa e retorna
        serializer = RelatorioGastoCategoriasSerializer(dados_relatorio, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Relatório de gastos mensais",
        tags=["Custo"],
        responses={200: None}
    )
    @action(detail=False, methods=['get'])
    def relatorio_mensal(self, request):
        """
        Gera um relatório de gastos mensais para análise de tendências.
        Agrupa os custos por mês e retorna série temporal.
        """
        # Filtra por projeto específico, se fornecido
        projeto_id = request.query_params.get('projeto_id')
        filtro_projeto = Q(projeto_id=projeto_id) if projeto_id else Q()
        
        # Período de análise (padrão: últimos 12 meses)
        from dateutil.relativedelta import relativedelta
        
        meses = int(request.query_params.get('meses', 12))
        data_final = request.query_params.get('data_final')
        
        if data_final:
            try:
                from datetime import datetime
                data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                data_final = timezone.now().date()
        else:
            data_final = timezone.now().date()
        
        data_inicial = (data_final.replace(day=1) - relativedelta(months=meses-1))
        
        # Consulta custos agrupados por mês
        from django.db.models.functions import TruncMonth
        
        gastos_mensais = Custo.objects.filter(
            filtro_projeto,
            data__gte=data_inicial,
            data__lte=data_final
        ).annotate(
            mes=TruncMonth('data')
        ).values(
            'mes'
        ).annotate(
            total=Sum('valor')
        ).order_by('mes')
        
        # Formata resultado para incluir todos os meses, mesmo sem valores
        resultado = []
        
        # Gera lista de todos os meses no período
        mes_atual = data_inicial
        while mes_atual <= data_final.replace(day=1):
            # Procura valor para o mês atual
            valor_mes = next(
                (item['total'] for item in gastos_mensais if item['mes'].date().replace(day=1) == mes_atual),
                Decimal('0.00')
            )
            
            resultado.append({
                'mes': mes_atual.strftime('%Y-%m'),
                'nome_mes': mes_atual.strftime('%b/%Y'),
                'valor': valor_mes
            })
            
            # Avança para o próximo mês
            mes_atual = (mes_atual + relativedelta(months=1))
        
        return Response(resultado)

@extend_schema_view(
    list=extend_schema(
        summary="Listar custos",
        tags=["Custo"],
        description="Retorna uma lista paginada de custos.",
        responses={200: OrcamentoProjetoSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes do custo",
        tags=["Custo"],
        description="Retorna informações detalhadas de um custo específico.",
        responses={200: OrcamentoProjetoSerializer}
    ),
    create=extend_schema(
        summary="Criar novo custo",
        tags=["Custo"],
        description="Cria um novo custo.",
        responses={201: OrcamentoProjetoSerializer}
    ),
    update=extend_schema(
        summary="Atualizar custo",
        tags=["Custo"],
        description="Atualiza todos os campos de um custo existente.",
        responses={200: OrcamentoProjetoSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar custo parcialmente",
        tags=["Custo"],
        description="Atualiza parcialmente um custo existente.",
        responses={200: OrcamentoProjetoSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir custo",
        tags=["Custo"],
        description="Remove um custo existente.",
        responses={204: None}
    )
)
class OrcamentoProjetoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de orçamentos de projetos.
    Inclui anotações para calcular campos derivados diretamente no banco de dados.
    """
    queryset = OrcamentoProjeto.objects.all()
    serializer_class = OrcamentoProjetoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['projeto']
    
    def get_queryset(self):
        """
        Retorna queryset com anotações para campos calculados:
        - valor_utilizado: soma de todos os custos do projeto
        - valor_restante: diferença entre valor_total e valor_utilizado
        - percentual_utilizado: percentual do orçamento já utilizado
        """
        return OrcamentoProjeto.objects.annotate(
            valor_utilizado=Coalesce(Sum('projeto__custos__valor'), Value(0), output_field=DecimalField()),
            valor_restante=F('valor_total') - Coalesce(Sum('projeto__custos__valor'), Value(0), output_field=DecimalField()),
            percentual_utilizado=Case(
                When(valor_total=0, then=Value(0, output_field=DecimalField())),
                default=Coalesce(Sum('projeto__custos__valor'), Value(0), output_field=DecimalField()) * 100 / F('valor_total'),
                output_field=DecimalField()
            )
        ).select_related('projeto', 'aprovado_por')
    
    def perform_create(self, serializer):
        serializer.save(aprovado_por=self.request.user)
    
    @extend_schema(
        summary="Listar projetos sem orçamento definido",
        tags=["Custo"],
        responses={200: None}
    )
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
            {'id': getattr(p, 'id', None), 'nome': getattr(p, 'name', 'Unknown')}
            for p in projetos_sem_orcamento
        ]
        
        return Response(dados)
    
    @extend_schema(
        summary="Ajustar orçamento de um projeto",
        tags=["Custo"],
        responses={200: None}
    )
    @action(detail=True, methods=['post'])
    def ajustar_orcamento(self, request, pk=None):
        """
        Permite ajustar o orçamento de um projeto com justificativa.
        Mantém histórico da alteração no campo de observações.
        """
        orcamento = self.get_object()
        
        # Obtém o novo valor e justificativa
        novo_valor = request.data.get('novo_valor')
        justificativa = request.data.get('justificativa')
        
        if not novo_valor:
            return Response(
                {"error": "O novo valor do orçamento é obrigatório"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            novo_valor = Decimal(novo_valor)
            if novo_valor <= 0:
                raise ValueError("Valor deve ser maior que zero")
        except (ValueError, TypeError, InvalidOperation):
            return Response(
                {"error": "Valor de orçamento inválido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calcula diferença e registra histórico
        valor_anterior = orcamento.valor_total
        diferenca = novo_valor - valor_anterior
        
        # Adiciona registro à observação
        from datetime import datetime
        data_atual = datetime.now().strftime('%d/%m/%Y')
        usuario = request.user.get_full_name() or request.user.username
        
        nova_observacao = f"[{data_atual}] {usuario}: Orçamento ajustado de R$ {valor_anterior} para R$ {novo_valor}"
        if justificativa:
            nova_observacao += f" - Justificativa: {justificativa}"
        
        # Atualiza observações (mantém histórico)
        if orcamento.observacoes:
            orcamento.observacoes = f"{orcamento.observacoes}\n\n{nova_observacao}"
        else:
            orcamento.observacoes = nova_observacao
        
        # Atualiza valor
        orcamento.valor_total = novo_valor
        orcamento.save()
        
        # Verifica se precisa criar alerta de orçamento
        self._verificar_necessidade_alerta(orcamento)
        
        serializer = self.get_serializer(orcamento)
        return Response(serializer.data)
    
    def _verificar_necessidade_alerta(self, orcamento):
        """
        Verifica se o ajuste de orçamento requer criação de alerta.
        """
        # Calcula percentual atual de utilização
        try:
            valor_utilizado = Custo.objects.filter(
                projeto=orcamento.projeto
            ).aggregate(
                total=Coalesce(Sum('valor'), Value(0), output_field=DecimalField())
            )['total'] or Decimal('0.00')
            
            if orcamento.valor_total > 0:
                percentual = (valor_utilizado / orcamento.valor_total) * 100
            else:
                percentual = Decimal('0.00')
            
            # Se percentual >= 80% e não existir alerta ativo
            if percentual >= 80:
                alerta_existe = Alerta.objects.filter(
                    projeto=orcamento.projeto,
                    tipo='PROJETO',
                    status='ATIVO'
                ).exists()
                
                if not alerta_existe:
                    Alerta.objects.create(
                        tipo='PROJETO',
                        projeto=orcamento.projeto,
                        percentual=percentual,
                        mensagem=f"O projeto {orcamento.projeto.name} atingiu {percentual:.2f}% do orçamento planejado após ajuste."
                    )
        except Exception as e:
            # Registrar erro para depuração
            print(f"Erro ao verificar necessidade de alerta: {e}")
            pass

@extend_schema_view(
    list=extend_schema(
        summary="Listar tarefas",
        tags=["Custo"],
        description="Retorna uma lista paginada de tarefas.",
        responses={200: OrcamentoTarefaSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes da tarefa",
        tags=["Custo"],
        description="Retorna informações detalhadas de uma tarefa específica.",
        responses={200: OrcamentoTarefaSerializer}
    ),
    create=extend_schema(
        summary="Criar nova tarefa",
        tags=["Custo"],
        description="Cria uma novo tarefa.",
        responses={201: OrcamentoTarefaSerializer}
    ),
    update=extend_schema(
        summary="Atualizar tarefa",
        tags=["Custo"],
        description="Atualiza todos os campos de uma tarefa existente.",
        responses={200: OrcamentoTarefaSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar tarefa parcialmente",
        tags=["Custo"],
        description="Atualiza parcialmente uma tarefa existente.",
        responses={200: OrcamentoTarefaSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir tarefa",
        tags=["Custo"],
        description="Remove uma tarefa existente.",
        responses={204: None}
    )
)
class OrcamentoTarefaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de orçamentos de tarefas.
    Inclui anotações para calcular campos derivados diretamente no banco de dados.
    """
    queryset = OrcamentoTarefa.objects.all()
    serializer_class = OrcamentoTarefaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tarefa', 'tarefa__projeto']
    
    def get_queryset(self):
        """
        Retorna queryset com anotações para campos calculados:
        - valor_utilizado: soma de todos os custos da tarefa
        - valor_restante: diferença entre valor e valor_utilizado
        - percentual_utilizado: percentual do orçamento já utilizado
        """
        from django.db.models import Case, When
        
        return OrcamentoTarefa.objects.annotate(
            valor_utilizado=Coalesce(Sum('tarefa__custos__valor'), Value(0), output_field=DecimalField()),
            valor_restante=F('valor') - Coalesce(Sum('tarefa__custos__valor'), Value(0), output_field=DecimalField()),
            percentual_utilizado=Case(
                When(valor=0, then=Value(0, output_field=DecimalField())),
                default=Coalesce(Sum('tarefa__custos__valor'), Value(0), output_field=DecimalField()) * 100 / F('valor'),
                output_field=DecimalField()
            )
        ).select_related('tarefa', 'aprovado_por', 'tarefa__projeto')
    
    def perform_create(self, serializer):
        serializer.save(aprovado_por=self.request.user)
    
    @extend_schema(
        summary="Listar tarefas sem orçamento",
        tags=["Custo"],
        responses={200: None}
    )
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
        tarefas_sem_orcamento = Tarefa.objects.filter(filtro_projeto).exclude(id__in=tarefas_com_orcamento).select_related('projeto')
        
        # Retorna lista simplificada
        dados = [
            {'id': getattr(t, 'id', None), 'titulo': getattr(t, 'titulo', 'Unknown'), 'projeto_id': getattr(t, 'projeto_id', None), 'projeto_nome': getattr(getattr(t, 'projeto', None), 'name', 'Unknown')}
            for t in tarefas_sem_orcamento
        ]
        
        return Response(dados)
    
    @extend_schema(
        summary="Ajustar orçamento de uma tarefas",
        tags=["Custo"],
        responses={200: None}
    )
    @action(detail=True, methods=['post'])
    def ajustar_orcamento(self, request, pk=None):
        """
        Permite ajustar o orçamento de uma tarefa com justificativa.
        Mantém histórico da alteração no campo de observações.
        """
        orcamento = self.get_object()
        
        # Obtém o novo valor e justificativa
        novo_valor = request.data.get('novo_valor')
        justificativa = request.data.get('justificativa')
        
        if not novo_valor:
            return Response(
                {"error": "O novo valor do orçamento é obrigatório"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from decimal import Decimal, InvalidOperation
            novo_valor = Decimal(novo_valor)
            if novo_valor <= 0:
                raise ValueError("Valor deve ser maior que zero")
        except (ValueError, TypeError, InvalidOperation):
            return Response(
                {"error": "Valor de orçamento inválido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calcula diferença e registra histórico
        valor_anterior = orcamento.valor
        diferenca = novo_valor - valor_anterior
        
        # Adiciona registro à observação
        from datetime import datetime
        data_atual = datetime.now().strftime('%d/%m/%Y')
        usuario = request.user.get_full_name() or request.user.username
        
        nova_observacao = f"[{data_atual}] {usuario}: Orçamento ajustado de R$ {valor_anterior} para R$ {novo_valor}"
        if justificativa:
            nova_observacao += f" - Justificativa: {justificativa}"
        
        # Atualiza observações (mantém histórico)
        if orcamento.observacoes:
            orcamento.observacoes = f"{orcamento.observacoes}\n\n{nova_observacao}"
        else:
            orcamento.observacoes = nova_observacao
        
        # Atualiza valor
        orcamento.valor = novo_valor
        orcamento.save()
        
        # Verifica se precisa criar alerta de orçamento
        self._verificar_necessidade_alerta(orcamento)
        
        serializer = self.get_serializer(orcamento)
        return Response(serializer.data)
    
    def _verificar_necessidade_alerta(self, orcamento):
        """
        Verifica se o ajuste de orçamento requer criação de alerta.
        """
        # Calcula percentual atual de utilização
        try:
            valor_utilizado = Custo.objects.filter(
                tarefa=orcamento.tarefa
            ).aggregate(
                total=Coalesce(Sum('valor'), Value(0), output_field=DecimalField())
            )['total'] or Decimal('0.00')
            
            if orcamento.valor > 0:
                percentual = (valor_utilizado / orcamento.valor) * 100
            else:
                percentual = Decimal('0.00')
            
            # Se percentual >= 80% e não existir alerta ativo
            if percentual >= 80:
                alerta_existe = Alerta.objects.filter(
                    tarefa=orcamento.tarefa,
                    tipo='TAREFA',
                    status='ATIVO'
                ).exists()
                
                if not alerta_existe:
                    Alerta.objects.create(
                        tipo='TAREFA',
                        projeto=orcamento.tarefa.projeto,
                        tarefa=orcamento.tarefa,
                        percentual=percentual,
                        mensagem=f"A tarefa {orcamento.tarefa.titulo} atingiu {percentual:.2f}% do orçamento planejado após ajuste."
                    )
        except Exception as e:
            # Registrar erro para depuração
            print(f"Erro ao verificar necessidade de alerta: {e}")
            pass

@extend_schema_view(
    list=extend_schema(
        summary="Listar alertas",
        tags=["Custo"],
        description="Retorna uma lista paginada de alertas.",
        responses={200: AlertaSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes da alerta",
        tags=["Custo"],
        description="Retorna informações detalhadas de uma alerta específica.",
        responses={200: AlertaSerializer}
    ),
    create=extend_schema(
        summary="Criar nova alerta",
        tags=["Custo"],
        description="Cria uma novo alerta.",
        responses={201: AlertaSerializer}
    ),
    update=extend_schema(
        summary="Atualizar alerta",
        tags=["Custo"],
        description="Atualiza todos os campos de uma alerta existente.",
        responses={200: AlertaSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar alerta parcialmente",
        tags=["Custo"],
        description="Atualiza parcialmente uma alerta existente.",
        responses={200: AlertaSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir alerta",
        tags=["Custo"],
        description="Remove uma alerta existente.",
        responses={204: None}
    )
)
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
    
    def get_queryset(self):
        """
        Retorna queryset com relacionamentos já carregados para evitar N+1 queries.
        """
        return Alerta.objects.select_related(
            'projeto', 'tarefa', 'resolvido_por'
        ).all()
    
    @extend_schema(
        summary="Marcar alertas como resolvido",
        tags=["Custo"],
        responses={200: None}
    )
    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        """
        Marca um alerta como resolvido.
        Opcionalmente, pode incluir uma observação sobre a resolução.
        """
        alerta = self.get_object()
        
        # Verifica se o alerta já está resolvido ou ignorado
        if alerta.status in ['RESOLVIDO', 'IGNORADO']:
            return Response(
                {"detail": f"Este alerta já está {alerta.status.lower()}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualiza o status e observações, se fornecidas
        alerta.status = 'RESOLVIDO'
        alerta.data_resolucao = timezone.now()
        alerta.resolvido_por = request.user
        
        observacao = request.data.get('observacao')
        if observacao:
            alerta.observacoes = observacao
        
        alerta.save(update_fields=['status', 'data_resolucao', 'resolvido_por', 'observacoes'])
        
        serializer = self.get_serializer(alerta)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Marcar alertas como ignorado",
        tags=["Custo"],
        responses={200: None}
    )
    @action(detail=True, methods=['post'])
    def ignorar(self, request, pk=None):
        """
        Marca um alerta como ignorado.
        Opcionalmente, pode incluir uma justificativa para ignorar o alerta.
        """
        alerta = self.get_object()
        
        # Verifica se o alerta já está resolvido ou ignorado
        if alerta.status in ['RESOLVIDO', 'IGNORADO']:
            return Response(
                {"detail": f"Este alerta já está {alerta.status.lower()}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualiza o status e justificativa, se fornecida
        alerta.status = 'IGNORADO'
        alerta.data_resolucao = timezone.now()
        alerta.resolvido_por = request.user
        
        justificativa = request.data.get('justificativa')
        if justificativa:
            alerta.observacoes = f"Ignorado: {justificativa}"
        
        alerta.save(update_fields=['status', 'data_resolucao', 'resolvido_por', 'observacoes'])
        
        serializer = self.get_serializer(alerta)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Listar alertas com status ATIVO",
        tags=["Custo"],
        responses={200: None}
    )
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """
        Retorna apenas os alertas pendentes (status ATIVO).
        Permite filtrar por projeto, tarefa e tipo.
        """
        # Filtra apenas alertas ativos
        queryset = self.get_queryset().filter(status='ATIVO')
        
        # Aplica filtros adicionais, se fornecidos
        projeto_id = request.query_params.get('projeto_id')
        if projeto_id:
            queryset = queryset.filter(projeto_id=projeto_id)
        
        tarefa_id = request.query_params.get('tarefa_id')
        if tarefa_id:
            queryset = queryset.filter(tarefa_id=tarefa_id)
        
        tipo = request.query_params.get('tipo')
        if tipo in ['PROJETO', 'TAREFA']:
            queryset = queryset.filter(tipo=tipo)
        
        # Serializa e retorna
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
