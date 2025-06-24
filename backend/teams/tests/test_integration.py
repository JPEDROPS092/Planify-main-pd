"""
Testes de integração para o módulo Teams.
"""
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.test import APIClient
from rest_framework import status
from teams.models import Equipe, MembroEquipe, PermissaoEquipe

User = get_user_model()  # type: ignore


class TeamIntegrationTest(TransactionTestCase):
    """Testes de integração para funcionalidades completas de equipes"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = APIClient()
        
        # Cria usuários para os testes
        self.product_owner = User.objects.create_user(  # type: ignore
            username='po_user',
            email='po@example.com',
            password='testpass123',
            first_name='Product',
            last_name='Owner'
        )
        
        self.scrum_master = User.objects.create_user(  # type: ignore
            username='sm_user',
            email='sm@example.com',
            password='testpass123',
            first_name='Scrum',
            last_name='Master'
        )
        
        self.developer = User.objects.create_user(  # type: ignore
            username='dev_user',
            email='dev@example.com',
            password='testpass123',
            first_name='Developer',
            last_name='User'
        )
        
        self.qa_engineer = User.objects.create_user(  # type: ignore
            username='qa_user',
            email='qa@example.com',
            password='testpass123',
            first_name='QA',
            last_name='Engineer'
        )
        
    def test_complete_team_workflow(self):
        """Testa um fluxo completo de criação e gerenciamento de equipe"""
        # 1. Product Owner cria uma equipe
        self.client.force_authenticate(user=self.product_owner)  # type: ignore
        
        equipe_data = {
            'nome': 'Equipe Ágil de Desenvolvimento',
            'descricao': 'Equipe responsável pelo desenvolvimento do produto X'
        }
        
        response = self.client.post('/equipes/', equipe_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        equipe_id = response.json()['id']
        
        # Verifica que o PO foi automaticamente adicionado como membro
        equipe = Equipe.objects.get(id=equipe_id)
        po_membro = MembroEquipe.objects.filter(
            equipe=equipe,
            usuario=self.product_owner,
            papel='PO'
        ).first()
        self.assertIsNotNone(po_membro)
        
        # 2. PO adiciona Scrum Master à equipe
        sm_data = {
            'usuario': self.scrum_master.pk,
            'papel': 'SM'
        }
        
        response = self.client.post(
            f'/equipes/{equipe_id}/adicionar_membro/',
            sm_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 3. PO adiciona Developer à equipe
        dev_data = {
            'usuario': self.developer.pk,
            'papel': 'DEV'
        }
        
        response = self.client.post(
            f'/equipes/{equipe_id}/adicionar_membro/',
            dev_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 4. PO adiciona QA Engineer à equipe
        qa_data = {
            'usuario': self.qa_engineer.pk,
            'papel': 'QA'
        }
        
        response = self.client.post(
            f'/equipes/{equipe_id}/adicionar_membro/',
            qa_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 5. Verifica que todos os membros foram adicionados
        response = self.client.get(f'/equipes/{equipe_id}/membros/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        membros = response.json()
        self.assertEqual(len(membros), 4)  # PO + SM + DEV + QA
        
        # Verifica papéis dos membros
        papeis = {membro['usuario']: membro['papel'] for membro in membros}
        self.assertEqual(papeis[self.product_owner.pk], 'PO')
        self.assertEqual(papeis[self.scrum_master.pk], 'SM')
        self.assertEqual(papeis[self.developer.pk], 'DEV')
        self.assertEqual(papeis[self.qa_engineer.pk], 'QA')
        
        # 6. PO configura permissões para desenvolvedores
        permissao_dev = {
            'papel': 'DEV',
            'equipe': equipe_id,
            'modulo': 'TASKS',
            'permissao': 'CREATE'
        }
        
        response = self.client.post('/permissoes/', permissao_dev, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 7. PO configura permissões para QA
        permissao_qa = {
            'papel': 'QA',
            'equipe': equipe_id,
            'modulo': 'TASKS',
            'permissao': 'UPDATE'
        }
        
        response = self.client.post('/permissoes/', permissao_qa, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 8. Verifica que a equipe está completa
        response = self.client.get(f'/equipes/{equipe_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        equipe_detalhes = response.json()
        self.assertEqual(equipe_detalhes['total_membros'], 4)
        self.assertEqual(len(equipe_detalhes['membros']), 4)
        self.assertEqual(len(equipe_detalhes['permissoes']), 2)
        
    def test_team_member_permissions_workflow(self):
        """Testa o fluxo de atualização de papéis e permissões"""
        # Cria equipe como PO
        self.client.force_authenticate(user=self.product_owner)  # type: ignore
        
        equipe_data = {
            'nome': 'Equipe de Teste',
            'descricao': 'Equipe para testar permissões'
        }
        
        response = self.client.post('/equipes/', equipe_data, format='json')
        equipe_id = response.json()['id']
        
        # Adiciona desenvolvedor
        dev_data = {
            'usuario': self.developer.pk,
            'papel': 'DEV'
        }
        
        self.client.post(
            f'/equipes/{equipe_id}/adicionar_membro/',
            dev_data,
            format='json'
        )
        
        # Atualiza papel do desenvolvedor para Senior Developer (mantém DEV)
        update_data = {
            'usuario': self.developer.pk,
            'papel': 'DEV'
        }
        
        response = self.client.post(
            f'/equipes/{equipe_id}/atualizar_papel_membro/',
            update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Promove desenvolvedor para Scrum Master
        promote_data = {
            'usuario': self.developer.pk,
            'papel': 'SM'
        }
        
        response = self.client.post(
            f'/equipes/{equipe_id}/atualizar_papel_membro/',
            promote_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica que o papel foi atualizado
        membro = MembroEquipe.objects.get(
            equipe_id=equipe_id,
            usuario=self.developer
        )
        self.assertEqual(membro.papel, 'SM')
        
    def test_team_member_removal_workflow(self):
        """Testa o fluxo de remoção de membros da equipe"""
        # Configura equipe com membros
        self.client.force_authenticate(user=self.product_owner)  # type: ignore
        
        equipe = Equipe.objects.create(
            nome='Equipe Temporária',
            criado_por=self.product_owner
        )
        
        # Adiciona membros
        MembroEquipe.objects.create(
            equipe=equipe,
            usuario=self.product_owner,
            papel='PO',
            adicionado_por=self.product_owner
        )
        
        MembroEquipe.objects.create(
            equipe=equipe,
            usuario=self.developer,
            papel='DEV',
            adicionado_por=self.product_owner
        )
        
        MembroEquipe.objects.create(
            equipe=equipe,
            usuario=self.qa_engineer,
            papel='QA',
            adicionado_por=self.product_owner
        )
        
        # Verifica membros iniciais
        membros_inicial = MembroEquipe.objects.filter(equipe=equipe).count()
        self.assertEqual(membros_inicial, 3)
        
        # Remove desenvolvedor
        remove_data = {'usuario': self.developer.pk}
        
        response = self.client.post(
            f'/equipes/{equipe.pk}/remover_membro/',
            remove_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verifica que o desenvolvedor foi removido
        membros_final = MembroEquipe.objects.filter(equipe=equipe).count()
        self.assertEqual(membros_final, 2)
        
        self.assertFalse(
            MembroEquipe.objects.filter(
                equipe=equipe,
                usuario=self.developer
            ).exists()
        )
        
    def test_available_users_filtering(self):
        """Testa o filtro de usuários disponíveis"""
        # Cria equipe e adiciona alguns membros
        self.client.force_authenticate(user=self.product_owner)  # type: ignore
        
        equipe = Equipe.objects.create(
            nome='Equipe Filtro',
            criado_por=self.product_owner
        )
        
        # Adiciona PO e Developer como membros
        MembroEquipe.objects.create(
            equipe=equipe,
            usuario=self.product_owner,
            papel='PO',
            adicionado_por=self.product_owner
        )
        
        MembroEquipe.objects.create(
            equipe=equipe,
            usuario=self.developer,
            papel='DEV',
            adicionado_por=self.product_owner
        )
        
        # Consulta usuários disponíveis
        response = self.client.get(
            '/equipes/usuarios_disponiveis/',
            {'equipe': equipe.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        usuarios_disponiveis = response.json()
        usuarios_ids = [user['id'] for user in usuarios_disponiveis]
        
        # Deve incluir SM e QA (não são membros)
        self.assertIn(self.scrum_master.pk, usuarios_ids)
        self.assertIn(self.qa_engineer.pk, usuarios_ids)
        
        # Não deve incluir PO e Developer (já são membros)
        self.assertNotIn(self.product_owner.pk, usuarios_ids)
        self.assertNotIn(self.developer.pk, usuarios_ids)
        
    def test_team_search_and_filtering(self):
        """Testa funcionalidades de busca e filtro de equipes"""
        # Cria múltiplas equipes
        self.client.force_authenticate(user=self.product_owner)  # type: ignore
        
        equipe1 = Equipe.objects.create(
            nome='Equipe Frontend',
            descricao='Desenvolvimento de interfaces',
            criado_por=self.product_owner
        )
        
        equipe2 = Equipe.objects.create(
            nome='Equipe Backend',
            descricao='Desenvolvimento de APIs',
            criado_por=self.scrum_master
        )
        
        equipe3 = Equipe.objects.create(
            nome='Equipe Mobile',
            descricao='Desenvolvimento de aplicativos móveis',
            criado_por=self.developer
        )
        
        # Adiciona PO como membro de todas as equipes
        for equipe in [equipe1, equipe2, equipe3]:
            MembroEquipe.objects.create(
                equipe=equipe,
                usuario=self.product_owner,
                papel='PO' if equipe == equipe1 else 'STAKEHOLDER',
                adicionado_por=equipe.criado_por
            )
        
        # Teste de busca por texto
        response = self.client.get('/equipes/', {'search': 'Frontend'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        equipes = response.json()['results']
        self.assertEqual(len(equipes), 1)
        self.assertEqual(equipes[0]['nome'], 'Equipe Frontend')
        
        # Teste de filtro "minhas equipes"
        response = self.client.get('/equipes/', {'minhas_equipes': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        minhas_equipes = response.json()['results']
        self.assertEqual(len(minhas_equipes), 3)  # PO é membro de todas
        
        # Teste de filtro por usuário
        response = self.client.get('/equipes/', {'usuario': self.developer.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        equipes_dev = response.json()['results']
        # Developer é membro apenas da equipe3 (além de ser criador)
        self.assertGreaterEqual(len(equipes_dev), 1)
        
        # Teste de busca em descrição
        response = self.client.get('/equipes/', {'search': 'APIs'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        equipes_api = response.json()['results']
        self.assertEqual(len(equipes_api), 1)
        self.assertEqual(equipes_api[0]['nome'], 'Equipe Backend')


class TeamCascadeDeleteTest(TestCase):
    """Testa comportamentos de deleção em cascata"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user1 = User.objects.create_user(  # type: ignore
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(  # type: ignore
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        
    def test_delete_equipe_cascades_to_members_and_permissions(self):
        """Testa que deletar equipe remove membros e permissões"""
        equipe = Equipe.objects.create(
            nome='Equipe Para Deletar',
            criado_por=self.user1
        )
        
        # Adiciona membros
        membro1 = MembroEquipe.objects.create(
            equipe=equipe,
            usuario=self.user1,
            papel='PO',
            adicionado_por=self.user1
        )
        
        membro2 = MembroEquipe.objects.create(
            equipe=equipe,
            usuario=self.user2,
            papel='DEV',
            adicionado_por=self.user1
        )
        
        # Adiciona permissões
        permissao1 = PermissaoEquipe.objects.create(
            papel='PO',
            equipe=equipe,
            modulo='PROJECTS',
            permissao='CREATE'
        )
        
        permissao2 = PermissaoEquipe.objects.create(
            papel='DEV',
            equipe=equipe,
            modulo='TASKS',
            permissao='UPDATE'
        )
        
        # Verifica que tudo foi criado
        self.assertTrue(Equipe.objects.filter(pk=equipe.pk).exists())
        self.assertEqual(MembroEquipe.objects.filter(equipe=equipe).count(), 2)
        self.assertEqual(PermissaoEquipe.objects.filter(equipe=equipe).count(), 2)
        
        # Deleta a equipe
        equipe_id = equipe.id  # type: ignore
        equipe.delete()
        
        # Verifica que tudo foi deletado em cascata
        self.assertFalse(Equipe.objects.filter(pk=equipe_id).exists())
        self.assertEqual(MembroEquipe.objects.filter(equipe_id=equipe_id).count(), 0)
        self.assertEqual(PermissaoEquipe.objects.filter(equipe_id=equipe_id).count(), 0)
        
        # Verifica que os usuários não foram deletados
        self.assertTrue(User.objects.filter(pk=self.user1.pk).exists())
        self.assertTrue(User.objects.filter(pk=self.user2.pk).exists())
        
    def test_delete_user_removes_team_memberships(self):
        """Testa que deletar usuário remove suas participações em equipes"""
        equipe1 = Equipe.objects.create(
            nome='Equipe 1',
            criado_por=self.user1
        )
        
        equipe2 = Equipe.objects.create(
            nome='Equipe 2',
            criado_por=self.user1
        )
        
        # User2 é membro de ambas as equipes
        MembroEquipe.objects.create(
            equipe=equipe1,
            usuario=self.user2,
            papel='DEV',
            adicionado_por=self.user1
        )
        
        MembroEquipe.objects.create(
            equipe=equipe2,
            usuario=self.user2,
            papel='QA',
            adicionado_por=self.user1
        )
        
        # Verifica que user2 é membro de 2 equipes
        self.assertEqual(
            MembroEquipe.objects.filter(usuario=self.user2).count(),
            2
        )
        
        # Deleta user2
        user2_id = self.user2.id  # type: ignore
        self.user2.delete()
        
        # Verifica que as participações foram removidas
        self.assertEqual(
            MembroEquipe.objects.filter(usuario_id=user2_id).count(),
            0
        )
        
        # Verifica que as equipes continuam existindo
        self.assertTrue(Equipe.objects.filter(pk=equipe1.pk).exists())
        self.assertTrue(Equipe.objects.filter(pk=equipe2.pk).exists())
