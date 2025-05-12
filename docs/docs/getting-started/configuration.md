---
sidebar_position: 2
---

# Configuração

Após a instalação do Planify, você precisará configurar o sistema de acordo com as necessidades da sua organização. Este guia aborda as principais configurações disponíveis.

## Configurações do Backend

### Configurações do Django

O Planify utiliza o framework Django, que oferece várias configurações que podem ser ajustadas no arquivo `settings.py` ou através de variáveis de ambiente.

#### Principais Variáveis de Ambiente

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `DEBUG` | Modo de depuração | `True` (desenvolvimento), `False` (produção) |
| `SECRET_KEY` | Chave secreta para criptografia | Gerada aleatoriamente |
| `DATABASE_URL` | URL de conexão com o banco de dados | `sqlite:///db.sqlite3` (desenvolvimento) |
| `ALLOWED_HOSTS` | Hosts permitidos para acessar a aplicação | `[]` (desenvolvimento), lista de domínios (produção) |
| `EMAIL_*` | Configurações de email | Varia conforme provedor |

### Configuração de Email

O Planify utiliza email para enviar notificações, confirmações de conta e recuperação de senha. Configure as seguintes variáveis:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'seu-servidor-smtp.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@exemplo.com'
EMAIL_HOST_PASSWORD = 'sua-senha'
DEFAULT_FROM_EMAIL = 'Planify <noreply@seudominio.com>'
```

### Configuração de Armazenamento de Arquivos

Por padrão, o Planify armazena arquivos localmente. Para ambientes de produção, recomendamos configurar o Amazon S3 ou outro serviço de armazenamento:

1. Instale as dependências necessárias:

```bash
pip install django-storages boto3
```

2. Adicione as seguintes configurações:

```python
# settings.py
INSTALLED_APPS += ['storages']

# Configurações do S3
AWS_ACCESS_KEY_ID = 'sua-chave-de-acesso'
AWS_SECRET_ACCESS_KEY = 'sua-chave-secreta'
AWS_STORAGE_BUCKET_NAME = 'seu-bucket'
AWS_S3_REGION_NAME = 'sua-regiao'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = 'private'

# Configuração de arquivos estáticos e mídia
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

## Configurações do Frontend

### Variáveis de Ambiente

O frontend do Planify utiliza o Nuxt.js, que carrega variáveis de ambiente de um arquivo `.env`. As principais variáveis são:

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `NUXT_PUBLIC_API_BASE` | URL base da API do backend | `http://localhost:8000/api` (desenvolvimento) |
| `NUXT_PUBLIC_APP_NAME` | Nome da aplicação | `Planify` |
| `NUXT_PUBLIC_APP_URL` | URL base do frontend | `http://localhost:3000` (desenvolvimento) |

### Personalização de Tema

O Planify utiliza Tailwind CSS e Material UI para estilização. Você pode personalizar o tema editando os seguintes arquivos:

1. **Cores e Tipografia**: Edite o arquivo `frontend/tailwind.config.js`

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#4dabf5',
          main: '#1976d2',  // Cor principal
          dark: '#1565c0',
        },
        secondary: {
          light: '#f73378',
          main: '#f50057',  // Cor secundária
          dark: '#ab003c',
        },
        // Adicione suas cores personalizadas aqui
      },
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
        // Adicione suas fontes personalizadas aqui
      },
    },
  },
  // ...
};
```

2. **Componentes UI**: Personalize os componentes no diretório `frontend/components/ui/`

## Configurações de Segurança

### CORS (Cross-Origin Resource Sharing)

Para permitir que o frontend acesse a API do backend, configure o CORS:

```python
# settings.py
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE

# Em desenvolvimento
CORS_ALLOW_ALL_ORIGINS = True  # Apenas para desenvolvimento!

# Em produção
CORS_ALLOWED_ORIGINS = [
    'https://seudominio.com',
    'https://www.seudominio.com',
]
```

### Configuração de Autenticação

O Planify utiliza JWT (JSON Web Tokens) para autenticação. Configure as seguintes opções:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

## Configurações Avançadas

### Cache

Para melhorar o desempenho em produção, configure o cache:

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Filas de Tarefas Assíncronas

Para processamento em segundo plano (como envio de emails), configure o Celery:

```python
# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```

## Próximos Passos

Agora que você configurou o Planify, continue para o [Guia Rápido](./quick-start) para começar a usar o sistema.
