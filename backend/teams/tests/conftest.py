"""
Fixtures compartilhadas para os testes do módulo Teams usando pytest.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from teams.models import Equipe, MembroEquipe, PermissaoEquipe

User = get_user_model()


@pytest.fixture
def api_client():
    """Cliente API para testes."""
    return APIClient()


@pytest.fixture
def user1():
    """Primeiro usuário de teste."""
    return User.objects.create_user(
        username='user1',
        email='user1@example.com',
        full_name='User One',
        password='testpass123'
    )


@pytest.fixture
def user2():
    """Segundo usuário de teste."""
    return User.objects.create_user(
        username='user2',
        email='user2@example.com',
        full_name='User Two',
        password='testpass123'
    )


@pytest.fixture
def user3():
    """Terceiro usuário de teste."""
    return User.objects.create_user(
        username='user3',
        email='user3@example.com',
        full_name='User Three',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(api_client, user1):
    """Cliente API autenticado com user1."""
    api_client.force_authenticate(user=user1)
    return api_client


@pytest.fixture
def equipe1(user1):
    """Primeira equipe de teste."""
    return Equipe.objects.create(
        nome="Equipe 1",
        descricao="Primeira equipe de teste",
        criado_por=user1
    )


@pytest.fixture
def equipe2(user2):
    """Segunda equipe de teste."""
    return Equipe.objects.create(
        nome="Equipe 2",
        descricao="Segunda equipe de teste",
        criado_por=user2
    )


@pytest.fixture
def equipe_teste(user1):
    """Equipe para testes de actions."""
    return Equipe.objects.create(
        nome="Equipe Teste",
        criado_por=user1
    )


@pytest.fixture
def membro_equipe_user1(equipe_teste, user1):
    """Membro equipe - user1 como PO."""
    return MembroEquipe.objects.create(
        equipe=equipe_teste,
        usuario=user1,
        papel='PO',
        adicionado_por=user1
    )


@pytest.fixture
def membro_equipe_user2(equipe_teste, user2, user1):
    """Membro equipe - user2 como DEV."""
    return MembroEquipe.objects.create(
        equipe=equipe_teste,
        usuario=user2,
        papel='DEV',
        adicionado_por=user1
    )


@pytest.fixture
def permissao_equipe(equipe_teste):
    """Permissão de equipe para testes."""
    return PermissaoEquipe.objects.create(
        papel='DEV',
        equipe=equipe_teste,
        modulo='TAREFAS',
        permissao='CRIAR'
    )
