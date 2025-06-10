"""
Django settings for planify project.
"""

import os
import sys
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
    
    # Apps de terceiros usados para funcionalidades extras
    'rest_framework',              # Framework para APIs REST
    'rest_framework_simplejwt',    # JWT para autenticação via tokens
    'djoser',                      # REST framework views for user management
    'corsheaders',                 # Configuração CORS para permitir acesso cross-origin
    'django_filters',              # Filtros para DRF
    'colorfield',                  # Campo de cores personalizado
    'chartjs',                     # Integração com Chart.js para gráficos
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
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Configurações do drf-spectacular para Swagger/OpenAPI
SPECTACULAR_SETTINGS = {
    'TITLE': 'Planify API',
    'DESCRIPTION': 'API para o sistema Planify - Gerenciamento de Projetos',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/',
    'SERVE_PUBLIC': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'filter': True,
        'displayRequestDuration': True,
        'displayOperationId': False,
        'defaultModelsExpandDepth': -1,
        'docExpansion': 'none',
    },
    'SECURITY': [{'Bearer': []}],
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX_TRIM': True,
    'SERVE_AUTHENTICATION': None,
    
    # Enums naming configuration
    'ENUM_NAME_OVERRIDES': {
        'TipoEnum': 'communications.models.Comunicacao.TIPO_CHOICES',
        'StatusProjetoEnum': 'projects.models.Projeto.STATUS_CHOICES',
        'StatusTarefaEnum': 'tasks.models.Tarefa.STATUS_CHOICES',
        'StatusSprintEnum': 'projects.models.Sprint.STATUS_CHOICES',
        'StatusRiscoEnum': 'risks.models.Risco.STATUS_CHOICES',
        'PrioridadeEnum': 'projects.models.Projeto.PRIORIDADE_CHOICES',
        'PapelMembroEnum': 'projects.models.MembroProjeto.PAPEL_CHOICES',
        'TipoDocumentoEnum': 'documents.models.Documento.TIPO_CHOICES',
    },
    'ENUM_GENERATE_CHOICE_LABELS': True,
    'COMPONENT_NO_READ_ONLY_REQUIRED': True,
    'POSTPROCESSING_HOOKS': [],
}
    
# Configurações específicas do Simple JWT para tokens
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_COOKIE': 'access_token',   # Cookie name
    'AUTH_COOKIE_DOMAIN': None,      # Use None for localhost
    'AUTH_COOKIE_SECURE': False,     # Set to True in production with HTTPS
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_SAMESITE': 'Lax',
    'UPDATE_LAST_LOGIN': True,                    # Atualiza o campo last_login do usuário
    'AUTH_HEADER_TYPES': ('Bearer',),             # Prefixo do token no header Authorization
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',)  # Classe de token permitida
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

