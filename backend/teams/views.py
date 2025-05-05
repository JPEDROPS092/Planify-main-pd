from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Equipe, MembroEquipe, PermissaoEquipe
from .serializers import (
    EquipeSerializer, EquipeListSerializer, MembroEquipeSerializer, 
    PermissaoEquipeSerializer, UserMinimalSerializer
)

User = get_user_model()


class EquipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de equipes.
    Permite criar, listar, atualizar e excluir equipes.
    """
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EquipeListSerializer
        return EquipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
    
    def get_queryset(self):
        """
        Filtra equipes com base nos parâmetros da URL e permissões do usuário.
        """
        queryset = Equipe.objects.all()
        
        # Filtra por membro
        usuario_id = self.request.query_params.get('usuario')
        if usuario_id:
            queryset = queryset.filter(membros__usuario__id=usuario_id)
        
        # Filtra minhas equipes
        minhas_equipes = self.request.query_params.get('minhas_equipes')
        if minhas_equipes and minhas_equipes.lower() == 'true':
            queryset = queryset.filter(membros__usuario=self.request.user)
        
        # Filtra por texto (busca em nome e descrição)
        texto = self.request.query_params.get('texto')
        if texto:
            queryset = queryset.filter(
                Q(nome__icontains=texto) | Q(descricao__icontains=texto)
            )
        
        return queryset.distinct()
    
    @action(detail=True, methods=['get'])
    def membros(self, request, pk=None):
        """
        Retorna a lista de membros da equipe.
        """
        equipe = self.get_object()
        membros = equipe.membros.all()
        serializer = MembroEquipeSerializer(membros, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def adicionar_membro(self, request, pk=None):
        """
        Adiciona um membro à equipe.
        """
        equipe = self.get_object()
        usuario_id = request.data.get('usuario_id')
        papel = request.data.get('papel')
        
        if not usuario_id:
            return Response(
                {'erro': 'É necessário fornecer um ID de usuário.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not papel:
            return Response(
                {'erro': 'É necessário fornecer um papel para o membro.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se o papel é válido
        papeis_validos = dict(MembroEquipe.PAPEL_CHOICES).keys()
        if papel not in papeis_validos:
            return Response(
                {'erro': f'Papel inválido. Opções válidas: {", ".join(papeis_validos)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se o usuário já é membro da equipe
        if MembroEquipe.objects.filter(equipe=equipe, usuario_id=usuario_id).exists():
            return Response(
                {'erro': 'Este usuário já é membro desta equipe.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Adiciona o membro à equipe
        membro = MembroEquipe.objects.create(
            equipe=equipe,
            usuario_id=usuario_id,
            papel=papel,
            adicionado_por=request.user
        )
        
        serializer = MembroEquipeSerializer(membro)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def remover_membro(self, request, pk=None):
        """
        Remove um membro da equipe.
        """
        equipe = self.get_object()
        usuario_id = request.data.get('usuario_id')
        
        if not usuario_id:
            return Response(
                {'erro': 'É necessário fornecer um ID de usuário.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se o usuário é membro da equipe
        try:
            membro = MembroEquipe.objects.get(equipe=equipe, usuario_id=usuario_id)
            
            # Não permite remover o último membro da equipe
            if equipe.membros.count() <= 1:
                return Response(
                    {'erro': 'Não é possível remover o último membro da equipe.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Não permite remover o Product Owner se houver apenas um
            if membro.papel == 'PO' and equipe.membros.filter(papel='PO').count() <= 1:
                return Response(
                    {'erro': 'Não é possível remover o único Product Owner da equipe.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            membro.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MembroEquipe.DoesNotExist:
            return Response(
                {'erro': 'Este usuário não é membro desta equipe.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def atualizar_papel_membro(self, request, pk=None):
        """
        Atualiza o papel de um membro da equipe.
        """
        equipe = self.get_object()
        usuario_id = request.data.get('usuario_id')
        papel = request.data.get('papel')
        
        if not usuario_id or not papel:
            return Response(
                {'erro': 'É necessário fornecer um ID de usuário e um papel.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se o papel é válido
        papeis_validos = dict(MembroEquipe.PAPEL_CHOICES).keys()
        if papel not in papeis_validos:
            return Response(
                {'erro': f'Papel inválido. Opções válidas: {", ".join(papeis_validos)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se o usuário é membro da equipe
        try:
            membro = MembroEquipe.objects.get(equipe=equipe, usuario_id=usuario_id)
            
            # Se estiver alterando de PO para outro papel, verifica se há outro PO
            if membro.papel == 'PO' and papel != 'PO' and equipe.membros.filter(papel='PO').count() <= 1:
                return Response(
                    {'erro': 'Não é possível alterar o papel do único Product Owner da equipe.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            membro.papel = papel
            membro.save()
            
            serializer = MembroEquipeSerializer(membro)
            return Response(serializer.data)
        except MembroEquipe.DoesNotExist:
            return Response(
                {'erro': 'Este usuário não é membro desta equipe.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def usuarios_disponiveis(self, request):
        """
        Retorna a lista de usuários disponíveis para adicionar a uma equipe.
        """
        equipe_id = request.query_params.get('equipe_id')
        
        if not equipe_id:
            return Response(
                {'erro': 'É necessário fornecer um ID de equipe.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obtém os IDs dos usuários que já são membros da equipe
        membros_ids = MembroEquipe.objects.filter(equipe_id=equipe_id).values_list('usuario_id', flat=True)
        
        # Filtra os usuários que não são membros da equipe
        usuarios = User.objects.exclude(id__in=membros_ids)
        
        # Filtra por texto de busca
        texto = request.query_params.get('texto')
        if texto:
            usuarios = usuarios.filter(
                Q(username__icontains=texto) | 
                Q(full_name__icontains=texto) | 
                Q(email__icontains=texto)
            )
        
        serializer = UserMinimalSerializer(usuarios, many=True)
        return Response(serializer.data)


class MembroEquipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de membros de equipe.
    """
    queryset = MembroEquipe.objects.all()
    serializer_class = MembroEquipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['equipe', 'usuario', 'papel']
    
    def perform_create(self, serializer):
        serializer.save(adicionado_por=self.request.user)


class PermissaoEquipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de permissões de equipe.
    """
    queryset = PermissaoEquipe.objects.all()
    serializer_class = PermissaoEquipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['equipe', 'papel', 'modulo', 'permissao']
