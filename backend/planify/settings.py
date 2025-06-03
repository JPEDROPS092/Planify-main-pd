"""
Django settings for planify project.
"""

import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p1e@s3ch@ng3th1sk3y1npr0duct10n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'colorfield',
    'chartjs',
    'django_seed',
    'drf_spectacular',  # Desabilitado temporariamente
    
    # Local apps
    'users',
    'projects',
    'tasks',
    'teams',
    'communications',
    'risks',
    'costs',
    'documents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.PermissionMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'rest_framework.authentication.SessionAuthentication',
]

ROOT_URLCONF = 'planify.urls'

from typing import List, Dict, Any

TEMPLATES: List[Dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'planify.wsgi.application'

# Database
DATABASES = { # type: ignore
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
from typing import List, Dict

AUTH_PASSWORD_VALIDATORS: List[Dict[str, Any]] = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.CustomJWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # Desabilitado temporariamente
    'EXCEPTION_HANDLER': 'core.utils.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    # Configurações para documentação em português
    'DOC_EXPANSION': 'list',
    'DOCS_TEMPLATE': 'rest_framework/docs/index.html',
}

# Simple JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# DJOSER settings
DJOSER = {
    'LOGIN_FIELD': 'username',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,
    'SEND_CONFIRMATION_EMAIL': False,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
        'user': 'users.serializers.UserSerializer',
        'user_create': 'users.serializers.UserCreateSerializer',
        'user_delete': 'users.serializers.UserSerializer',
        'password_reset': 'users.serializers.ResetPasswordSerializer',
        'password_reset_confirm': 'users.serializers.SetNewPasswordSerializer',
        'set_password': 'users.serializers.ChangePasswordSerializer',
        'current_user': 'users.serializers.UserSerializer',
    },
    'EMAIL': {
        'activation': 'users.email.ActivationEmail',
        'confirmation': 'users.email.ConfirmationEmail',
        'password_reset': 'users.email.PasswordResetEmail',
        'password_changed_confirmation': 'users.email.PasswordChangedConfirmationEmail',
    },
    'ACTIVATION_REQUIRED': False,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Planify API',
    'DESCRIPTION': 'Documentação completa da API do sistema Planify.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Comentário: Registra a extensão de autenticação personalizada para que o drf-spectacular a reconheça.
    # Isso é crucial para que a documentação da API reflita corretamente o esquema de autenticação JWT customizado.
    'OPENAPI_AUTHENTICATION_EXTENSIONS': [
        'users.openapi.CustomJWTAuthenticationScheme',
    ],
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
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
    'SWAGGER_UI_DIST': '//unpkg.com/swagger-ui-dist@3.35.0',
    'SWAGGER_UI_FAVICON_HREF': '//unpkg.com/swagger-ui-dist@3.35.0/favicon-32x32.png',
    'REDOC_DIST': '//unpkg.com/redoc@2.0.0-rc.48/bundles/redoc.standalone.js',
    'TAGS': [
        {'name': 'Autenticação', 'description': 'Endpoints para autenticação e gerenciamento de usuários'},
        {'name': 'Projetos', 'description': 'Gerenciamento de projetos'},
        {'name': 'Tarefas', 'description': 'Gerenciamento de tarefas'},
        {'name': 'Equipes', 'description': 'Gerenciamento de equipes e membros'},
        {'name': 'Riscos', 'description': 'Gerenciamento de riscos do projeto'},
        {'name': 'Custos', 'description': 'Gerenciamento de custos e orçamentos'},
        {'name': 'Documentos', 'description': 'Gerenciamento de documentos do projeto'},
        {'name': 'Comunicações', 'description': 'Gerenciamento de comunicações'},
    ],
    'ENUM_NAME_OVERRIDES': {
        # Comentário: Mapeia nomes de enumeração para os campos de choices nos modelos.
        # Isso ajuda drf-spectacular a gerar nomes de enumeração consistentes e significativos na documentação da API.
        'UserRoleEnum': 'users.models.User.ROLE_CHOICES',
        
        'TarefaStatusEnum': 'tasks.models.Tarefa.STATUS_CHOICES',
        'TarefaPriorityEnum': 'tasks.models.Tarefa.PRIORITY_CHOICES',
        
        'RiscoImpactoEnum': 'risks.models.Risco.IMPACTO_CHOICES', # Anteriormente RiskSeverityEnum
        'RiscoProbabilidadeEnum': 'risks.models.Risco.PROBABILIDADE_CHOICES',
        'RiscoStatusEnum': 'risks.models.Risco.STATUS_CHOICES',

        'ProjetoStatusEnum': 'projects.models.Projeto.STATUS_CHOICES',
        'ProjetoPrioridadeEnum': 'projects.models.Projeto.PRIORIDADE_CHOICES',

        'SprintStatusEnum': 'projects.models.Sprint.STATUS_CHOICES',
        
        'DocumentoTipoEnum': 'documents.models.Documento.TIPO_CHOICES',
        
        'MembroProjetoPapelEnum': 'projects.models.MembroProjeto.PAPEL_CHOICES',

        'NotificacaoTipoEnum': 'communications.models.Notificacao.TIPO_CHOICES',
        'NotificacaoPrioridadeEnum': 'communications.models.Notificacao.PRIORIDADE_CHOICES',
        'ConfigNotificacaoCanalEnum': 'communications.models.ConfiguracaoNotificacao.CANAL_CHOICES',

        # Para campos em modelos de histórico que usam os mesmos choices,
        # drf-spectacular geralmente os nomeia com sufixos.
        # Se nomes mais explícitos forem desejados, podem ser adicionados aqui, por exemplo:
        # 'HistoricoTarefaStatusAnteriorEnum': 'tasks.models.Tarefa.STATUS_CHOICES',
        # 'HistoricoTarefaNovoStatusEnum': 'tasks.models.Tarefa.STATUS_CHOICES',
    },
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://192.168.137.132:3000"
]
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

# Email settings (for password reset)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '\033[1;36m[{asctime}]\033[0m \033[1;33m[{levelname}]\033[0m \033[1;35m[{name}]\033[0m {message}',
            'style': '{',
        },
        'auth': {
            'format': '\033[1;36m[{asctime}]\033[0m \033[1;32m[AUTH]\033[0m \033[1;33m[{levelname}]\033[0m {message}',
            'style': '{',
        },
        'middleware': {
            'format': '\033[1;36m[{asctime}]\033[0m \033[1;34m[MIDDLEWARE]\033[0m \033[1;33m[{levelname}]\033[0m {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'auth_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'auth',
        },
        'middleware_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'middleware',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'users.authentication': {
            'handlers': ['auth_console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'users.middleware': {
            'handlers': ['middleware_console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
