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
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.CustomJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Configurações JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),  # Aceitar ambos os formatos
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}
    
    
# Configurações para a biblioteca DJOSER (facilita endpoints de autenticação)
DJOSER = {
    'LOGIN_FIELD': 'username',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,
    'SEND_CONFIRMATION_EMAIL': False,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'TOKEN_MODEL': None,  # We'll use JWT only
    'SERIALIZERS': {
        'user': 'users.serializers.UserSerializer',
        'user_create': 'users.serializers.UserCreateSerializer',
        'current_user': 'users.serializers.UserSerializer',
    },
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['rest_framework.permissions.IsAdminUser'],
    },
    'HIDE_USERS': False,
    'AUTHENTICATION_BACKENDS': ['django.contrib.auth.backends.ModelBackend'],
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
    'DESCRIPTION': 'Sistema de Gerenciamento de Projetos',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/',
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    'SECURITY': [
        {'Bearer': []}
    ],
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Digite: JWT <token>'
        }
    },
    'TAGS': [
        {'name': 'Autenticação', 'description': 'Endpoints de autenticação'},
        {'name': 'Usuários', 'description': 'Gerenciamento de usuários'},
        {'name': 'Projetos', 'description': 'Gerenciamento de projetos'},
        {'name': 'Tarefas', 'description': 'Gerenciamento de tarefas'},
        {'name': 'Equipes', 'description': 'Gerenciamento de equipes'},
        {'name': 'Comunicações', 'description': 'Gerenciamento de comunicações'},
        {'name': 'Riscos', 'description': 'Gerenciamento de riscos'},
        {'name': 'Custos', 'description': 'Gerenciamento de custos'},
        {'name': 'Documentos', 'description': 'Gerenciamento de documentos'},
    ],
    'SERVERS': [
        {'url': 'http://localhost:8000', 'description': 'Local Development'},
    ],
    'SERVE_PUBLIC': True,
    'ENUM_NAME_OVERRIDES': {
        'StatusAnteriorA52Enum': 'StatusAnteriorEnum',
        'StatusAnterior607Enum': 'StatusAnteriorEnum',
        'NovoStatusA52Enum': 'NovoStatusEnum',
        'NovoStatus607Enum': 'NovoStatusEnum',
        'PapelF38Enum': 'PapelEnum',
        'MensagemChatEnum': 'MensagemChatEnum',
        'NovaProbabilidadeEnum': 'ProbabilidadeEnum',
        'NovoImpactoEnum': 'ImpactoEnum',
        'ProbabilidadeEnum': 'ProbabilidadeEnum'
    },
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.hooks.postprocess_schema_enums'
    ],
}
# Configurações CORS (Cross-Origin Resource Sharing)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True  # Only for development!

# Configurações adicionais do CORS
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

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

