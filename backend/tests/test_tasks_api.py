from datetime import date, timedelta

from django.urls import reverse

from projects.models import Projeto
from tasks.models import Tarefa
from tests.tenant_base import TenantAPITestCase


class TaskAPITests(TenantAPITestCase):
    def setUp(self):
        super().setUp()
        self.project = Projeto.objects.create(
            titulo='Projeto Tarefa',
            descricao='Teste',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=10),
            status='PLANEJADO',
            prioridade='MEDIA',
            criado_por=self.user,
        )

    def test_create_task(self):
        url = reverse('tarefas-list')
        data = {
            'titulo': 'Tarefa Teste',
            'descricao': 'Descrição de teste',
            'data_inicio': date.today(),
            'data_termino': date.today() + timedelta(days=5),
            'prioridade': 'MEDIA',
            'status': 'A_FAZER',
            'projeto': self.project.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Tarefa.objects.filter(titulo='Tarefa Teste').exists())

    def test_list_tasks(self):
        url = reverse('tarefas-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
