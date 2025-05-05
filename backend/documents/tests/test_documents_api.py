from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from projects.models import Projeto
from documents.models import Documento
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

class DocumentAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.project = Projeto.objects.create(
            name='Projeto Documento',
            description='Teste',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=10),
            status='PLANNED',
            priority='MEDIUM',
            created_by=self.admin
        )

    def test_upload_document(self):
        url = reverse('documento-list')
        file = SimpleUploadedFile('doc.txt', b'conteudo de teste', content_type='text/plain')
        data = {
            'projeto': self.project.id,
            'arquivo': file,
            'descricao': 'Documento Teste'
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Documento.objects.filter(descricao='Documento Teste').exists())

    def test_list_documents(self):
        url = reverse('documento-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
