from datetime import date, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from documents.models import Documento
from projects.models import Projeto
from tests.tenant_base import TenantAPITestCase


class DocumentAPITests(TenantAPITestCase):
    def setUp(self):
        super().setUp()
        self.project = Projeto.objects.create(
            titulo='Projeto Documento',
            descricao='Teste',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=10),
            status='PLANEJADO',
            prioridade='MEDIA',
            criado_por=self.user,
        )

    def test_upload_document(self):
        url = reverse('documento-list')
        file = SimpleUploadedFile('doc.txt', b'conteudo de teste', content_type='text/plain')
        data = {
            'projeto': self.project.id,
            'titulo': 'Documento Teste',
            'descricao': 'Documento Teste',
            'tipo': 'OUTRO',
            'arquivo': file,
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201, response.data)
        self.assertTrue(Documento.objects.filter(titulo='Documento Teste').exists())

    def test_list_documents(self):
        url = reverse('documento-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
