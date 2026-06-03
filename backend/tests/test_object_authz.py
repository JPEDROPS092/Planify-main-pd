"""Autorização a nível de objeto (escrita por papel) sobre o isolamento por tenant.

Exercita o caminho HTTP real (JWT + middleware + ``TenantObjectWritePermission``)
para garantir a regra de produto: a **leitura** de um ``member`` é ampla (qualquer
recurso dos projetos que ele participa), mas a **escrita** é estreita (somente os
recursos atribuídos/criados por ele). ``viewer`` é somente-leitura; ``owner``/``admin``
escrevem qualquer recurso do tenant.
"""
from datetime import date, timedelta

from django.urls import reverse

from projects.models import MembroProjeto, Projeto
from tasks.models import AtribuicaoTarefa, Tarefa
from tests.tenant_base import TenantAPITestCase, bearer_client


class ObjectWriteAuthzTests(TenantAPITestCase):
    """Owner cria o projeto; dois members e um viewer participam dele."""

    def setUp(self):
        super().setUp()  # self.user é owner do tenant
        self.member_a = self.create_member(
            email='member_a@planify.test', username='member_a',
            full_name='Member A', role='member',
        )
        self.member_b = self.create_member(
            email='member_b@planify.test', username='member_b',
            full_name='Member B', role='member',
        )
        self.viewer = self.create_member(
            email='viewer@planify.test', username='viewer',
            full_name='Viewer', role='viewer',
        )
        self.client_a = bearer_client(self.member_a, tenant_id=self.tenant.id)
        self.client_b = bearer_client(self.member_b, tenant_id=self.tenant.id)
        self.client_viewer = bearer_client(self.viewer, tenant_id=self.tenant.id)

        self.project = Projeto.objects.create(
            titulo='Projeto Compartilhado', descricao='x',
            data_inicio=date.today(), data_fim=date.today() + timedelta(days=30),
            status='PLANEJADO', prioridade='MEDIA', criado_por=self.user,
        )
        # Ambos os members participam do projeto -> leem todas as tarefas dele.
        for usuario in (self.member_a, self.member_b):
            MembroProjeto.objects.create(
                projeto=self.project, usuario=usuario, papel='DESENVOLVEDOR',
            )

        # Uma tarefa atribuída a cada member.
        self.task_a = self._make_task('Tarefa do A', self.member_a)
        self.task_b = self._make_task('Tarefa do B', self.member_b)

    def _make_task(self, titulo, assignee):
        task = Tarefa.objects.create(
            titulo=titulo, descricao='x',
            data_inicio=date.today(), data_termino=date.today() + timedelta(days=5),
            prioridade='MEDIA', status='A_FAZER', projeto=self.project,
            criado_por=self.user,
        )
        AtribuicaoTarefa.objects.create(
            tarefa=task, usuario=assignee, atribuido_por=self.user,
        )
        return task

    # --- member: leitura ampla, escrita estreita -------------------------------

    def test_member_can_read_task_not_assigned_to_him(self):
        # member_a participa do projeto -> ENXERGA a tarefa do member_b.
        url = reverse('tarefas-detail', args=[self.task_b.id])
        response = self.client_a.get(url)
        self.assertEqual(response.status_code, 200)

    def test_member_can_update_own_task(self):
        url = reverse('tarefas-detail', args=[self.task_a.id])
        response = self.client_a.patch(url, {'titulo': 'Renomeada por A'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.task_a.refresh_from_db()
        self.assertEqual(self.task_a.titulo, 'Renomeada por A')

    def test_member_cannot_update_task_of_another_member(self):
        # Lê (acima), mas NÃO escreve a tarefa do member_b.
        url = reverse('tarefas-detail', args=[self.task_b.id])
        response = self.client_a.patch(url, {'titulo': 'Invasao'}, format='json')
        self.assertEqual(response.status_code, 403)
        self.task_b.refresh_from_db()
        self.assertEqual(self.task_b.titulo, 'Tarefa do B')

    def test_member_cannot_delete_task_of_another_member(self):
        url = reverse('tarefas-detail', args=[self.task_b.id])
        response = self.client_a.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Tarefa.objects.filter(pk=self.task_b.id).exists())

    def test_member_cannot_change_status_of_another_member_task(self):
        # A @action de detalhe chama get_object() -> mesma trava por objeto.
        url = reverse('tarefas-atualizar-status', args=[self.task_b.id])
        response = self.client_a.post(url, {'status': 'FEITO'}, format='json')
        self.assertEqual(response.status_code, 403)

    # --- viewer: somente leitura ----------------------------------------------

    def test_viewer_can_read(self):
        url = reverse('tarefas-detail', args=[self.task_a.id])
        self.assertEqual(self.client_viewer.get(url).status_code, 200)

    def test_viewer_cannot_update(self):
        url = reverse('tarefas-detail', args=[self.task_a.id])
        response = self.client_viewer.patch(url, {'titulo': 'x'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_viewer_cannot_create(self):
        url = reverse('tarefas-list')
        data = {
            'titulo': 'Nao deveria criar', 'descricao': 'x',
            'data_inicio': date.today(), 'data_termino': date.today() + timedelta(days=1),
            'prioridade': 'MEDIA', 'status': 'A_FAZER', 'projeto': self.project.id,
        }
        response = self.client_viewer.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)

    # --- owner: escrita plena --------------------------------------------------

    def test_owner_can_update_any_task(self):
        url = reverse('tarefas-detail', args=[self.task_b.id])
        response = self.client.patch(url, {'titulo': 'Owner manda'}, format='json')
        self.assertEqual(response.status_code, 200)
