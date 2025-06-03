from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.test import override_settings
from django.conf import settings
from users.models import User
from projects.models import Projeto
from documents.models import Documento
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

# Disable the custom middleware for tests
@override_settings(MIDDLEWARE=[m for m in settings.MIDDLEWARE if 'users.middleware.PermissionMiddleware' not in m])
class DocumentAPITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.admin = User.objects.create_superuser( # type: ignore
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        
        # Set up the client with proper authentication
        self.client = APIClient()
        self.client.login(username='admin', password='admin123')
        
        # Create a test project
        self.project = Projeto.objects.create(
            titulo='Projeto Documento',
            descricao='Teste',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=10),
            status='PLANEJADO',
            prioridade='MEDIA',
            criado_por=self.admin
        )

    def test_upload_document(self):
        url = reverse('documento-list')
        file = SimpleUploadedFile('doc.txt', b'conteudo de teste', content_type='text/plain')
        data = {
            'projeto': self.project.id,
            'titulo': 'Documento de Teste',
            'descricao': 'Documento Teste',
            'tipo': 'OUTRO',
            'arquivo': file,
            'tamanho_arquivo': len(b'conteudo de teste'),
            'tipo_arquivo': 'text/plain'
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Documento.objects.filter(titulo='Documento de Teste').exists())

    def test_list_documents(self):
        # Create a test document first
        file = SimpleUploadedFile('doc.txt', b'conteudo de teste', content_type='text/plain')
        doc = Documento.objects.create(
            projeto=self.project,
            titulo='Documento Existente',
            descricao='Documento para listar',
            tipo='OUTRO',
            arquivo=file,
            tamanho_arquivo=len(b'conteudo de teste'),
            tipo_arquivo='text/plain',
            versao='1.0',
            enviado_por=self.admin
        )
        
        url = reverse('documento-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Check that the response contains data
        self.assertTrue(response.data)
        
        # Verify the document exists in the response
        # The response might be paginated or have a different structure
        # so we'll check if any item has our document's title
        found = False
        if isinstance(response.data, list):
            # Direct list of results
            for item in response.data:
                if item.get('titulo') == 'Documento Existente':
                    found = True
                    break
        elif isinstance(response.data, dict) and 'results' in response.data:
            # Paginated results
            for item in response.data['results']:
                if item.get('titulo') == 'Documento Existente':
                    found = True
                    break
        
        self.assertTrue(found, "Document not found in the response data")
        
    def test_document_detail(self):
        # Create a test document first
        file = SimpleUploadedFile('doc.txt', b'conteudo de teste', content_type='text/plain')
        documento = Documento.objects.create(
            projeto=self.project,
            titulo='Documento para Detalhar',
            descricao='Documento para teste de detalhes',
            tipo='OUTRO',
            arquivo=file,
            tamanho_arquivo=len(b'conteudo de teste'),
            tipo_arquivo='text/plain',
            versao='1.0',
            enviado_por=self.admin
        )
        
        url = reverse('documento-detail', args=[documento.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titulo'], 'Documento para Detalhar')