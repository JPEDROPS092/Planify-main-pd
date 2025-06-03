from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Risco, HistoricoRisco
from .serializers import RiscoSerializer, RiscoListSerializer, HistoricoRiscoSerializer


class RiscoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de riscos.
    Permite criar, listar, atualizar e excluir riscos.
    """
    queryset = Risco.objects.all()
    serializer_class = RiscoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['projeto', 'status', 'probabilidade', 'impacto', 'responsavel_mitigacao']
    search_fields = ['descricao', 'plano_mitigacao', 'plano_contingencia']
    ordering_fields = ['data_identificacao', 'status', 'probabilidade', 'impacto']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RiscoListSerializer
        return RiscoSerializer
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
    
    def get_queryset(self):
        """
        Filtra riscos com base nos parâmetros da URL e permissões do usuário.
        """
        queryset = Risco.objects.all()
        
        # Filtra por projeto
        projeto_id = self.request.GET.get('projeto')
        if projeto_id:
            queryset = queryset.filter(projeto_id=projeto_id)
        
        # Filtra por status
        status_param = self.request.GET.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filtra por nível de risco
        nivel_risco = self.request.GET.get('nivel_risco')
        if nivel_risco:
            # Filtra com base na propriedade calculada nivel_risco
            riscos_filtrados = []
            for risco in queryset:
                if risco.nivel_risco == nivel_risco:
                    riscos_filtrados.append(risco.pk)
            queryset = queryset.filter(id__in=riscos_filtrados)
        
        # Filtra por responsável
        responsavel_id = self.request.GET.get('responsavel')
        if responsavel_id:
            queryset = queryset.filter(responsavel_mitigacao_id=responsavel_id)
        
        # Filtra por texto (busca em descrição, plano de mitigação e plano de contingência)
        texto = self.request.GET.get('texto')
        if texto:
            queryset = queryset.filter(
                Q(descricao__icontains=texto) | 
                Q(plano_mitigacao__icontains=texto) | 
                Q(plano_contingencia__icontains=texto)
            )
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def historico(self, pk=None):
        """
        Retorna o histórico de alterações do risco.
        """
        risco = self.get_object()
        historico = risco.historico.all()
        serializer = HistoricoRiscoSerializer(historico, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def atualizar_status(self, pk=None):
        """
        Atualiza o status de um risco.
        """
        risco = self.get_object()
        novo_status = request.data.get('status')
        observacao = request.data.get('observacao', '')
        
        if not novo_status:
            return Response(
                {'erro': 'É necessário fornecer um status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se o status é válido
        status_validos = dict(Risco.STATUS_CHOICES).keys()
        if novo_status not in status_validos:
            return Response(
                {'erro': f'Status inválido. Opções válidas: {", ".join(status_validos)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualiza o status
        status_anterior = risco.status
        risco.status = novo_status
        risco.save()
        
        # Registra no histórico
        HistoricoRisco.objects.create(
            risco=risco,
            status_anterior=status_anterior,
            novo_status=novo_status,
            probabilidade_anterior=risco.probabilidade,
            nova_probabilidade=risco.probabilidade,
            impacto_anterior=risco.impacto,
            novo_impacto=risco.impacto,
            alterado_por=request.user,
            observacao=observacao
        )
        
        # Retorna o risco atualizado
        serializer = self.get_serializer(risco)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def excluir_varios(self, request):
        """
        Exclui múltiplos riscos de uma vez.
        """
        ids = request.data.get('ids', [])
        
        if not ids:
            return Response(
                {'erro': 'É necessário fornecer uma lista de IDs.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtra os riscos pelos IDs fornecidos
        riscos = Risco.objects.filter(id__in=ids)
        
        # Verifica se todos os IDs foram encontrados
        if len(riscos) != len(ids):
            return Response(
                {'erro': 'Alguns riscos não foram encontrados.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Exclui os riscos
        count = riscos.count()
        riscos.delete()
        
        return Response(
            {'mensagem': f'{count} riscos foram excluídos com sucesso.'},
            status=status.HTTP_200_OK
        )


class HistoricoRiscoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualização do histórico de riscos.
    Somente leitura.
    """
    queryset = HistoricoRisco.objects.all()
    serializer_class = HistoricoRiscoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['risco', 'alterado_por']
