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

FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000') # Exemplo

# SECURITY WARNING: keep the secret key used in production secret!
# Chave secreta do Django usada para segurança (mantenha em segredo em produção)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-p1e@s3ch@ng3th1sk3y1npr0duct10n') # OK para DEV, MUDE PARA PRODUÇÃO

# SECURITY WARNING: don't run with debug turned on in production!
# Define se o projeto está em modo DEBUG (exibe erros detalhados, usando em desenvolvimento)
DEBUG = True # OK para DEV, MUDE PARA PRODUÇÃO

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
    # Apps de terceiros usados para funcionalidades extras
    'rest_framework',              # Framework para APIs REST
    'rest_framework_simplejwt',    # JWT para autenticação via tokens
    'rest_framework_simplejwt.token_blacklist',  # Sistema de blacklist automático
    'djoser',                      # Sistema de autenticação simplificado
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
    'django_extensions',
    'core'
]

# Middleware são componentes que processam requisições e respostas
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve arquivos estáticos em produção
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


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'users.validators.PasswordPolicyValidator',
        'OPTIONS': {
            'min_length': 10, # Exemplo de sobrescrita
            'require_uppercase': True,
            'require_lowercase': True,
            'require_numbers': True,
            'require_special': True,
            'password_history_count': 5 # Configura a verificação do histórico
        }
    },
]

# Define modelo de usuário customizado do app 'users'
AUTH_USER_MODEL = 'users.User'

# Configurações de internacionalização e fuso horário
LANGUAGE_CODE = 'pt-br'  # Idioma padrão português do Brasil
TIME_ZONE = 'America/Sao_Paulo'  # Fuso horário de São Paulo
USE_I18N = True  # Ativa tradução de strings
USE_TZ = True    # Usa timezone-aware datetimes

# Configurações para arquivos estáticos (CSS, JS, imagens fixas)
STATIC_URL = 'static/'  # URL base para arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Pasta onde os arquivos estáticos são coletados para produção
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # Adicione se você tiver estáticos na raiz do projeto
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
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', # Um pouco mais restritivo que AllowAny para dev
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer', # Interface web para APIs no navegador (ótimo para dev)
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
# planify/settings.py

# ...

SPECTACULAR_SETTINGS = {
    'TITLE': 'Planify API',
    'DESCRIPTION': 'Sistema de Gerenciamento de Projetos',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/', # Garante que os caminhos no schema comecem com /api/
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
        'displayOperationId': True,
        'filter': True,
        'deepLinking': True,
        'docExpansion': 'none',
        'defaultModelsExpandDepth': 1,
        'defaultModelExpandDepth': 1,
        # Configurações para melhor funcionamento
        'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'patch'],
        'requestInterceptor': None,  # Será definido no template
    },

    # --- SEÇÃO DE SEGURANÇA ---

    # classe de autenticação simplificada 
    'AUTHENTICATION_SCHEMES': [
        'users.openapi.JWTAuthenticationScheme',
    ],

    # 2.  segurança globalmente.
    'SECURITY': [
        {'JWT Authentication': []}
    ],


    # --- FIM DA SEÇÃO DE SEGURANÇA ---

    'TAGS': [
        {'name': 'Autenticação', 'description': 'Endpoints de autenticação'},
        {'name': 'Usuários', 'description': 'Gerenciamento de usuários'},
    ],
    'SERVERS': [
        {'url': 'http://localhost:8000', 'description': 'Servidor de Desenvolvimento Local'},
    ],
    'SERVE_PUBLIC': True,
    'ENUM_NAME_OVERRIDES': {
        # Formato correto: app_label.ModelName.field_name
        'projects.Projeto.status': 'ProjectStatusEnum',
        'projects.Sprint.status': 'SprintStatusEnum', 
        'tasks.Tarefa.status': 'TaskStatusEnum',
        'risks.Risco.status': 'RiskStatusEnum',
        
        # Campos 'prioridade' com nomes únicos
        'projects.Projeto.prioridade': 'ProjectPriorityEnum',
        'tasks.Tarefa.prioridade': 'TaskPriorityEnum',
        'communications.Notificacao.prioridade': 'NotificationPriorityEnum',
        
        # Campos 'tipo' com nomes únicos
        'communications.Comunicacao.tipo': 'CommunicationTypeEnum',
        'communications.Notificacao.tipo': 'NotificationTypeEnum',
        
        # Campos 'papel' com nomes únicos
        'projects.MembroProjeto.papel': 'ProjectRoleEnum',
        'teams.MembroEquipe.papel': 'TeamRoleEnum',
        
        # Outros campos específicos
        'risks.Risco.probabilidade': 'RiskProbabilityEnum',
        'risks.Risco.impacto': 'RiskImpactEnum',
        'communications.ConfiguracaoNotificacao.tarefa_atribuida': 'NotificationChannelEnum',
        'communications.ConfiguracaoNotificacao.tarefa_comentario': 'NotificationChannelEnum', 
        'communications.ConfiguracaoNotificacao.tarefa_prazo': 'NotificationChannelEnum',
        'communications.ConfiguracaoNotificacao.projeto_status': 'NotificationChannelEnum',
        'communications.ConfiguracaoNotificacao.equipe_alteracao': 'NotificationChannelEnum',
        'communications.ConfiguracaoNotificacao.documento_novo': 'NotificationChannelEnum',
        'communications.ConfiguracaoNotificacao.risco_novo': 'NotificationChannelEnum',
        'communications.ConfiguracaoNotificacao.mensagem_chat': 'NotificationChannelEnum',
        'users.Permission.module': 'PermissionModuleEnum',
        'users.Permission.action': 'PermissionActionEnum',
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
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'CONFIGURE_EMAIL_PASSWORD_IN_ENV') # Senha do email (use env var)

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

# CSRF settings
# Exime os endpoints de API da verificação CSRF
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Para APIs REST, geralmente não precisamos de CSRF
# Mas mantemos para o admin e outras views tradicionais
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_HTTPONLY = False

# === CONFIGURAÇÕES DO DJOSER ===
# Sistema de autenticação simplificado com JWT
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,  # Mude para True se quiser ativação por email
    'SEND_CONFIRMATION_EMAIL': False,  # Email de confirmação após registro
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,  # Email quando senha é alterada
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,  # Email quando username é alterado
    
    # Serializers customizados - reutilizamos os que você já criou
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializer',  # Mantém suas validações
        'user': 'users.serializers.UserSerializer',
        'current_user': 'users.serializers.UserSerializer',
        'user_create_password_retype': 'users.serializers.UserCreateSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
        'set_password': 'djoser.serializers.SetPasswordSerializer',
        'password_reset': 'djoser.serializers.SendEmailResetSerializer',
        'password_reset_confirm': 'djoser.serializers.PasswordResetConfirmSerializer',
    },
    
    # Permissões para cada endpoint
    'PERMISSIONS': {
        'user_create': ['rest_framework.permissions.AllowAny'],
        'user_list': ['rest_framework.permissions.IsAdminUser'],
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_delete': ['rest_framework.permissions.IsAuthenticated'],
        'set_password': ['rest_framework.permissions.IsAuthenticated'],
        'username_reset': ['rest_framework.permissions.AllowAny'],
        'username_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'set_username': ['rest_framework.permissions.IsAuthenticated'],
        'password_reset': ['rest_framework.permissions.AllowAny'],
        'password_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'activation': ['rest_framework.permissions.AllowAny'],
        'resend_activation': ['rest_framework.permissions.AllowAny'],
        'token_create': ['rest_framework.permissions.AllowAny'],
        'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
    },
    
    # Configurações de tokens e headers
    'AUTH_HEADER_TYPES': ('Bearer',),
    'HIDE_USERS': False,  # Se True, apenas admins podem listar usuários
    
    # URLs customizadas para frontend (opcional)
    'LOGIN_FIELD': 'email',  # Usar email para login ao invés de username
}

