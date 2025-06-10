"""
Django settings for planify project.
"""

import os
from pathlib import Path
from datetime import timedelta
from typing import List, Dict, Any # Moved typing imports to the top

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Define o diretório base do projeto (duas pastas acima deste arquivo)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Chave secreta do Django usada para segurança (mantenha em segredo em produção)
SECRET_KEY = 'django-insecure-p1e@s3ch@ng3th1sk3y1npr0duct10n'

# SECURITY WARNING: don't run with debug turned on in production!
# Define se o projeto está em modo DEBUG (exibe erros detalhados, usando em desenvolvimento)
DEBUG = True

# Define quais hosts podem acessar a aplicação (em produção deve conter o domínio real)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
# Lista de apps registrados no projeto, incluindo apps padrão, de terceiros e locais
INSTALLED_APPS = [
    # Apps padrão do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',               # Ferramenta de depuração para desenvolvimento
    # Apps de terceiros usados para funcionalidades extras
    'rest_framework',              # Framework para APIs REST
    'rest_framework_simplejwt',    # JWT para autenticação via tokens
    'djoser',                      # REST framework views for user management
    'corsheaders',                 # Configuração CORS para permitir acesso cross-origin
    'django_filters',              # Filtros para DRF
    'colorfield',                  # Campo de cores personalizado
    'chartjs',                    # Integração com Chart.js para gráficos
    'django_seed',                 # Para popular banco com dados de teste
    'drf_spectacular',             # Documentação automática da API
    
    # Apps locais do projeto
    'users',
    'projects',
    'tasks',
    'teams',
    'communications',
    'risks',
    'costs',
    'documents',
]

# Middleware são componentes que processam requisições e respostas
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve arquivos estáticos em produção
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',       # Middleware para CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # Proteção contra CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.PermissionMiddleware',       # Middleware customizado para permissões
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug Toolbar middleware
    # 'django.middleware.common.CommonMiddleware',   # Middleware duplicado, REMOVED
    # 'django.middleware.csrf.CsrfViewMiddleware',   # Middleware duplicado, REMOVED
]

# Arquivo raiz de URLs do projeto
ROOT_URLCONF = 'planify.urls'

# Configuração dos templates (HTML) do Django
TEMPLATES: List[Dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Engine padrão
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Diretório customizado para templates
        'APP_DIRS': True,                               # Permite carregar templates dos apps
        'OPTIONS': {
            'context_processors': [                    # Variáveis e funções globais para templates
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application entry point
WSGI_APPLICATION = 'planify.wsgi.application'

# Configuração do banco de dados (SQLite para desenvolvimento)
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Motor SQLite
        'NAME': BASE_DIR / 'db.sqlite3',         
    }
}

# Validação de senhas para o usuário
AUTH_PASSWORD_VALIDATORS: List[Dict[str, Any]] = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Senha mínima de 8 caracteres
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Define modelo de usuário customizado do app 'users'
AUTH_USER_MODEL = 'users.User'

# Configuração para permitir debug toolbar só no localhost
INTERNAL_IPS = [
    "127.0.0.1",
]

# Configurações de internacionalização e fuso horário
LANGUAGE_CODE = 'pt-br'  # Idioma padrão português do Brasil
TIME_ZONE = 'America/Sao_Paulo'  # Fuso horário de São Paulo
USE_I18N = True  # Ativa tradução de strings
USE_TZ = True    # Usa timezone-aware datetimes

# Configurações para arquivos estáticos (CSS, JS, imagens fixas)
STATIC_URL = 'static/'  # URL base para arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Pasta onde os arquivos estáticos são coletados para produção
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  
# Armazenamento otimizado para servir arquivos estáticos com compressão e cache

# Configuração para arquivos de mídia (uploads, imagens do usuário, documentos)
MEDIA_URL = '/media/'  # URL base para arquivos de mídia
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Diretório onde arquivos de mídia são armazenados

# Tipo padrão para chaves primárias (ID) nas models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações do Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.CustomJWTAuthentication',  # Autenticação JWT customizada
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT padrão
        'rest_framework.authentication.SessionAuthentication',  # Sessões tradicionais Django
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Requer autenticação para todas views por padrão
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',  # Suporte a filtros em consultas
        'rest_framework.filters.SearchFilter',                # Pesquisa por texto
        'rest_framework.filters.OrderingFilter',              # Ordenação de resultados
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # Paginação por número de página
    'PAGE_SIZE': 10,  # Itens por página

    # Exceções personalizadas para API
    # TODO: Ensure 'core.utils.custom_exception_handler' exists or remove/replace this line.
    # 'EXCEPTION_HANDLER': 'core.utils.custom_exception_handler',

    # Renderizadores padrão para respostas
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',         # Resposta JSON
        'rest_framework.renderers.BrowsableAPIRenderer', # Interface web para APIs no navegador
    ],

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # Geração automática do esquema OpenAPI

    # Parsers para requisições
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',      # JSON
        'rest_framework.parsers.FormParser',      # Formulários
        'rest_framework.parsers.MultiPartParser', # Upload de arquivos
    ],
    # Old doc settings removed as drf-spectacular handles this
    # 'DOC_EXPANSION': 'list',
    # 'DOCS_TEMPLATE': 'rest_framework/docs/index.html',
}

# Customizações do Swagger UI (These are handled by SPECTACULAR_SETTINGS['SWAGGER_UI_SETTINGS'])
# SWAGGER_UI_SETTINGS = { ... } # REMOVED standalone block
    
# Configurações específicas do Simple JWT para tokens
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),  # Token válido por 7 dias (as per code)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30), # Refresh token válido por 30 dias (as per code)
    'ROTATE_REFRESH_TOKENS': True,                # Gera refresh token novo a cada uso
    'BLACKLIST_AFTER_ROTATION': True,             # Blacklist do token antigo após rotação
    'UPDATE_LAST_LOGIN': True,                    # Atualiza o campo last_login do usuário
    'AUTH_HEADER_TYPES': ('Bearer',),             # Prefixo do token no header Authorization
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # Classe de token permitida
}
    
# Configurações para a biblioteca DJOSER (facilita endpoints de autenticação)
DJOSER = {
    'LOGIN_FIELD': 'username', # Djoser uses 'email' or 'username' or your custom field. 'username' is common.
    'USER_CREATE_PASSWORD_RETYPE': True,  # Usuário deve confirmar senha na criação
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,
    'SEND_CONFIRMATION_EMAIL': False,
    'SET_PASSWORD_RETYPE': True,           # Confirmação para alteração de senha
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {  # Serializadores customizados para os endpoints
        'user': 'users.serializers.UserSerializer',
        'user_create': 'users.serializers.UserCreateSerializer',
        'user_delete': 'users.serializers.UserSerializer', # Make sure this exists and is appropriate for delete
        'password_reset': 'users.serializers.ResetPasswordSerializer', # Ensure 'ResetPasswordSerializer' exists
        'password_reset_confirm': 'users.serializers.SetNewPasswordSerializer',
        'set_password': 'users.serializers.ChangePasswordSerializer', # Ensure 'ChangePasswordSerializer' exists
        'current_user': 'users.serializers.UserSerializer',
    },
    'EMAIL': {  # Classes para envio de emails customizados
        'activation': 'users.email.ActivationEmail',
        'confirmation': 'users.email.ConfirmationEmail',
        'password_reset': 'users.email.PasswordResetEmail',
        'password_changed_confirmation': 'users.email.PasswordChangedConfirmationEmail',
    },
    'ACTIVATION_REQUIRED': False,  # Ativação via email desabilitada
}
    
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO', # Tie logging level to DEBUG
    },
}
# Configurações para drf-spectacular (Swagger/OpenAPI)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Planify API',
    'DESCRIPTION': 'API para o sistema Planify - Gerenciamento de Projetos',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '', # Ensure your API URLs are prefixed with /api/ or adjust this
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX_TRIM': True,
    'AUTHENTICATION_WHITELIST': ['rest_framework_simplejwt.authentication.JWTAuthentication'],

    # Customizações do Swagger UI
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'displayOperationId': False,
        'defaultModelsExpandDepth': 3,
        'defaultModelExpandDepth': 3,
        'defaultModelRendering': 'model',
        'displayRequestDuration': True,
        'docExpansion': 'list',
        'filter': True,
        'showExtensions': True,
        'showCommonExtensions': True,
        'supportedSubmitMethods': ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'],
        'tryItOutEnabled': True,
    },
    'SWAGGER_UI_DIST': '//unpkg.com/swagger-ui-dist@5.10.3', # Updated to a more recent version
    'SWAGGER_UI_FAVICON_HREF': '//unpkg.com/swagger-ui-dist@5.10.3/favicon-32x32.png', # Updated
    'REDOC_DIST': '//unpkg.com/redoc@next/bundles/redoc.standalone.js', # Updated to 'next' for latest
    'TAGS': [
        '''
        {'name': 'Autenticação', 'description': 'Endpoints para autenticação e gerenciamento de usuários'},
        {'name': 'Projetos', 'description': 'Endpoints para gerenciamento de projetos e sprints'},
        {'name': 'Tarefas', 'description': 'Endpoints para gerenciamento de tarefas'},
        {'name': 'Equipes', 'description': 'Endpoints para gerenciamento de equipes e membros'},
        {'name': 'Riscos', 'description': 'Endpoints para gerenciamento de riscos'},
        {'name': 'Custos', 'description': 'Endpoints para controle de orçamentos e gastos'},
        {'name': 'Documentos', 'description': 'Endpoints para gerenciamento de documentos'},
        {'name': 'Comunicações', 'description': 'Endpoints para mensagens e notificações'},
        {'name': 'Dashboard', 'description': 'Endpoints para painéis e métricas'},
        {'name': 'Saúde do Sistema', 'description': 'Endpoints para verificação de status da API'},
        '''
    ],
}



# Configurações CORS (Cross-Origin Resource Sharing)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
#liberado para desenvolvimento, permite que qualquer origem acesse a API
#CORS_ALLOW_ALL_ORIGINS = True

# Configurações para envio de emails via SMTP (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Backend SMTP padrão do Django
EMAIL_HOST = 'smtp.gmail.com'     # Servidor SMTP do Gmail
EMAIL_PORT = 587                  # Porta para TLS
EMAIL_USE_TLS = True              # Usa TLS para segurança
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'seuemail@gmail.com')  # Usuário do email (use env var)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'suasenha') # Senha do email (use env var)

# Variáveis personalizadas
LOGO_PATH = 'static/img/logo.png'  # Caminho do logo do sistema
SITE_NAME = 'Planify'              # Nome do sistema

LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/login/'

# Admin site customization
ADMIN_SITE_HEADER = "Planify - Administração"
ADMIN_SITE_TITLE = "Planify - Sistema de Gerenciamento de Projetos"
ADMIN_INDEX_TITLE = "Dashboard"

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds
SESSION_SAVE_EVERY_REQUEST = True

