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
# Chave secreta do Django usada para segurança (MANTENHA EM SEGREDO EM PRODUÇÃO)
SECRET_KEY = 'django-insecure-p1e@s3ch@ng3th1sk3y1npr0duct10n' # OK para DEV, MUDE PARA PRODUÇÃO

# SECURITY WARNING: don't run with debug turned on in production!
# Define se o projeto está em modo DEBUG (exibe erros detalhados, usando em desenvolvimento)
DEBUG = True # MANTENHA TRUE PARA DESENVOLVIMENTO

# Define quais hosts podem acessar a aplicação (em produção deve conter o domínio real)
ALLOWED_HOSTS = ['localhost', '127.0.0.1'] # OK para DESENVOLVIMENTO LOCAL

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
    'core', # Adicionei o app 'core' aqui, pois ele aparece na sua estrutura e tem utils/openapi
]

# Middleware são componentes que processam requisições e respostas
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware', # Desabilitado para dev, STATICFILES_STORAGE padrão é melhor
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',       # Middleware para CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # Proteção contra CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.PermissionMiddleware',       # Middleware customizado para permissões
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug Toolbar middleware
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
# Para DESENVOLVIMENTO, o storage padrão é geralmente mais rápido e não requer WhiteNoise.
# WhiteNoise é excelente para PRODUÇÃO.
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # Adicione se você tiver estáticos na raiz do projeto

# Configuração para arquivos de mídia (uploads, imagens do usuário, documentos)
MEDIA_URL = '/media/'  # URL base para arquivos de mídia
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Diretório onde arquivos de mídia são armazenados

# Tipo padrão para chaves primárias (ID) nas models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações do Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT padrão
        'rest_framework.authentication.SessionAuthentication',  # Sessões tradicionais Django (útil para Admin e Browsable API)
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', # Um pouco mais restritivo que AllowAny para dev
        # 'rest_framework.permissions.AllowAny',  # Permite acesso não autenticado por padrão (considere com cautela)
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',  # Suporte a filtros em consultas
        'rest_framework.filters.SearchFilter',                # Pesquisa por texto
        'rest_framework.filters.OrderingFilter',              # Ordenação de resultados
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # Paginação por número de página
    'PAGE_SIZE': 10,  # Itens por página

    # Exceções personalizadas para API
    # Se 'core.utils.custom_exception_handler' existir e estiver pronto, descomente.
    # 'EXCEPTION_HANDLER': 'core.utils.custom_exception_handler',

    # Renderizadores padrão para respostas
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',         # Resposta JSON
        'rest_framework.renderers.BrowsableAPIRenderer', # Interface web para APIs no navegador (ótimo para dev)
    ],

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # Geração automática do esquema OpenAPI

    # Parsers para requisições
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',      # JSON
        'rest_framework.parsers.FormParser',      # Formulários
        'rest_framework.parsers.MultiPartParser', # Upload de arquivos
    ],
}


# Configurações específicas do Simple JWT para tokens
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7), # Longo, mas ok para dev. Considere menor para testar refresh.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_COOKIE': 'access_token',   # Cookie name
    'AUTH_COOKIE_DOMAIN': None,      # Use None for localhost
    'AUTH_COOKIE_SECURE': False,     # False para HTTP em desenvolvimento
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_SAMESITE': 'Lax',   # 'Lax' é um bom padrão
    'UPDATE_LAST_LOGIN': True,       # Atualiza o campo last_login do usuário
    'AUTH_HEADER_TYPES': ('Bearer',), # Prefixo do token no header Authorization
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # Classe de token permitida
}

# Configurações para a biblioteca DJOSER (facilita endpoints de autenticação)
DJOSER = {
    'LOGIN_FIELD': 'username', # ou 'email', dependendo do seu modelo User
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False, # Geralmente False para dev
    'SEND_CONFIRMATION_EMAIL': False,             # Geralmente False para dev
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False, # Geralmente False para dev, para não depender de email
    'TOKEN_MODEL': None,  # Usamos JWT, então Djoser não precisa gerenciar seu próprio token
    'SERIALIZERS': {  # Serializadores customizados para os endpoints
        'user': 'users.serializers.UserSerializer',
        'user_create': 'users.serializers.UserCreateSerializer',
        'user_delete': 'users.serializers.UserSerializer', # Verifique se este serializer é adequado para deleção
        'password_reset': 'users.serializers.ResetPasswordSerializer', # Certifique-se que este serializer existe
        'password_reset_confirm': 'users.serializers.SetNewPasswordSerializer', # Certifique-se que este serializer existe
        'set_password': 'users.serializers.ChangePasswordSerializer', # Certifique-se que este serializer existe
        'current_user': 'users.serializers.UserSerializer',
    },
    'PERMISSIONS': { # Ajuste conforme necessidade
        'user_list': ['rest_framework.permissions.IsAdminUser'],
        # 'user': ['rest_framework.permissions.IsAuthenticated'], # Djoser lida com isso por endpoint
    },
    'HIDE_USERS': False, # True para esconder a lista de usuários de não-admins
    'EMAIL': {  # Classes para envio de emails customizados (usará EMAIL_BACKEND configurado)
        'activation': 'users.email.ActivationEmail',
        'confirmation': 'users.email.ConfirmationEmail',
        'password_reset': 'users.email.PasswordResetEmail',
        'password_changed_confirmation': 'users.email.PasswordChangedConfirmationEmail',
    },
    'ACTIVATION_REQUIRED': False,  # Ativação via email desabilitada para facilitar dev
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
        'level': 'DEBUG', # Sempre DEBUG quando DEBUG=True
    },
    'loggers': { # Silenciar alguns loggers mais verbosos, se necessário
        'django': {
            'handlers': ['console'],
            'level': 'INFO', # Ou WARNING para menos verbosidade do Django Core
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG', # Para ver queries SQL no console quando DEBUG=True
            'propagate': False,
        },
    }
}

# Configurações para drf-spectacular (Swagger/OpenAPI)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Planify API (Development)',
    'DESCRIPTION': 'API para o sistema Planify - Gerenciamento de Projetos',
    'VERSION': '1.0.0-dev',
    'SERVE_INCLUDE_SCHEMA': False, # True para servir o schema.json/yaml no endpoint da UI
    'SERVE_PUBLIC': True,  # Torna a documentação pública (OK para dev)
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX_TRIM': True,
    'SERVE_AUTHENTICATION': None,  # Remove autenticação para acessar docs (OK para dev)
    'SECURITY': [{'Bearer': []}],  # Define o esquema de segurança
    # 'SECURITY_DEFINITIONS' foi depreciado em favor de 'SECURITY_SCHEMES' em OpenAPI 3
    # No entanto, 'SECURITY' acima deve ser suficiente para drf-spectacular lidar com JWT.
    # Se precisar de definições explícitas, seria algo como:
    # 'OPENAPI_SECURITY_SCHEMES': {
    #     'BearerAuth': {
    #         'type': 'http',
    #         'scheme': 'bearer',
    #         'bearerFormat': 'JWT',
    #         'description': 'Token JWT no formato: "Bearer {seu_token}"'
    #     }
    # },

    # Customizações do Swagger UI
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'displayOperationId': False,
        'defaultModelsExpandDepth': 3,
        'defaultModelExpandDepth': 3,
        'defaultModelRendering': 'model',
        'displayRequestDuration': True,
        'docExpansion': 'list', # 'none', 'list', 'full'
        'filter': True, # Habilita barra de filtro
        'showExtensions': True,
        'showCommonExtensions': True,
        'supportedSubmitMethods': ['get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'],
        'tryItOutEnabled': True, # Habilita o botão "Try it out"
    },
    'SWAGGER_UI_DIST': '//unpkg.com/swagger-ui-dist@5.10.3',
    'SWAGGER_UI_FAVICON_HREF': '//unpkg.com/swagger-ui-dist@5.10.3/favicon-32x32.png',
    'REDOC_DIST': '//unpkg.com/redoc@next/bundles/redoc.standalone.js',
}


# Configurações CORS (Cross-Origin Resource Sharing)
CORS_ALLOWED_ORIGINS = [ # Seja específico se souber as portas do seu frontend
    "http://localhost:3000",  # Ex: React
    "http://127.0.0.1:3000",
    "http://localhost:3001",  # Ex: Outro serviço frontend
    "http://127.0.0.1:3001",
    "http://localhost:5173",  # Ex: Vite/Vue
    "http://127.0.0.1:5173",
    # Django dev server (se o frontend estiver servido pelo Django ou para testar com Postman/Insomnia da mesma origem)
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
# Para desenvolvimento, se você tiver muitos frontends em portas diferentes ou não souber,
# CORS_ALLOW_ALL_ORIGINS = True pode ser mais conveniente, mas menos seguro.
# Se usar CORS_ALLOW_ALL_ORIGINS = True, CORS_ALLOWED_ORIGINS é ignorado.
CORS_ALLOW_ALL_ORIGINS = True  # DEFINITIVAMENTE MUDE PARA FALSE EM PRODUÇÃO
CORS_ALLOW_CREDENTIALS = True # Necessário se o frontend envia cookies (ex: CSRF, session) ou Authorization headers

# Configurações adicionais do CORS (geralmente os padrões são suficientes se CORS_ALLOW_ALL_ORIGINS=True)
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

# Configurações para envio de emails
# Para DESENVOLVIMENTO, é melhor usar o backend de console para ver os e-mails no terminal.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# As configurações SMTP abaixo seriam para produção ou se você realmente precisar enviar e-mails em dev
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER') # Use variáveis de ambiente!
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') # Use variáveis de ambiente!

# Variáveis personalizadas
LOGO_PATH = 'static/img/logo.png'  # Caminho do logo do sistema
SITE_NAME = 'Planify'              # Nome do sistema

LOGIN_REDIRECT_URL = '/admin/' # Ou para a página principal da sua API/Frontend
LOGOUT_REDIRECT_URL = '/admin/login/' # Ou para a página de login

# Admin site customization
ADMIN_SITE_HEADER = "Planify - Administração (DEV)"
ADMIN_SITE_TITLE = "Planify - Sistema de Gerenciamento de Projetos (DEV)"
ADMIN_INDEX_TITLE = "Dashboard (DEV)"

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds
SESSION_SAVE_EVERY_REQUEST = True