# Módulo de Usuários - Planify

## Visão Geral

O módulo de usuários é um componente central do sistema Planify, responsável pela autenticação, autorização e controle de acesso. Implementa um modelo robusto de segurança com controle de acesso baseado em papéis (RBAC), gerenciamento de permissões e recursos avançados de segurança de conta.

## Estrutura do Módulo

```
users/
├── __init__.py
├── models.py                    # Modelos de dados
├── views.py                     # Views da API
├── serializers.py               # Serializers DRF
├── authentication.py            # Sistema de autenticação JWT
├── permissions.py               # Sistema de permissões
├── validators.py                # Validadores customizados
├── utils.py                     # Funções utilitárias
├── security_notifications.py   # Notificações de segurança
├── audit.py                     # Sistema de auditoria
├── middleware.py                # Middleware de segurança
├── admin.py                     # Interface administrativa
├── urls.py                      # Configuração de URLs
├── apps.py                      # Configuração da aplicação
├── tests/                       # Testes automatizados
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_security.py
└── README.md                    # Esta documentação
```

## Modelos de Dados

### User (Usuário)
Modelo principal que estende `AbstractBaseUser` e `PermissionsMixin`.

**Campos principais:**
- `uuid`: UUID único para identificação segura
- `username`: Nome de usuário único
- `email`: Email único
- `full_name`: Nome completo
- `role`: Papel do usuário (ADMIN, PROJECT_MANAGER, TEAM_LEADER, TEAM_MEMBER, STAKEHOLDER, AUDITOR)
- `is_active`: Status de ativação
- `failed_login_attempts`: Contador de tentativas falhadas de login
- `is_locked`: Status de bloqueio da conta
- `locked_until`: Data/hora até quando a conta está bloqueada
- `password_change_required`: Indica se alteração de senha é obrigatória
- `last_password_change`: Data da última alteração de senha

**Métodos importantes:**
- `increment_failed_login()`: Incrementa tentativas falhadas e bloqueia se necessário
- `reset_failed_login()`: Reset contador de tentativas falhadas
- `has_permission(module, action)`: Verifica permissões específicas

### UserProfile (Perfil do Usuário)
Informações estendidas do usuário.

**Campos:**
- `user`: Relação OneToOne com User
- `phone`: Telefone (opcional)
- `profile_picture`: Foto de perfil (opcional)
- `theme_preference`: Preferência de tema (LIGHT, DARK, SYSTEM)
- `email_notifications`: Ativar notificações por email
- `system_notifications`: Ativar notificações do sistema

### AccessProfile (Perfil de Acesso)
Define conjuntos de permissões que podem ser atribuídos aos usuários.

**Campos:**
- `name`: Nome do perfil
- `description`: Descrição do perfil
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### Permission (Permissão)
Permissões individuais para módulos e ações específicas.

**Campos:**
- `access_profile`: Relação com AccessProfile
- `module`: Módulo do sistema (PROJECTS, TASKS, TEAMS, etc.)
- `action`: Ação permitida (VIEW, CREATE, EDIT, DELETE, etc.)

### UserAccessProfile (Associação Usuário-Perfil)
Relaciona usuários com perfis de acesso.

### BlacklistedTokens (Tokens Invalidados)
Armazena tokens JWT invalidados.

**Campos:**
- `token`: Token JWT invalidado
- `user`: Usuário associado (opcional)
- `created_at`: Data de criação

### PasswordHistory (Histórico de Senhas)
Mantém histórico das últimas senhas para evitar reutilização.

**Campos:**
- `user`: Usuário
- `password_hash`: Hash da senha anterior
- `created_at`: Data de criação

### AuditLog (Log de Auditoria)
Registra ações de segurança e administrativas.

**Campos:**
- `user`: Usuário que executou a ação
- `action`: Tipo de ação (LOGIN, LOGOUT, PASSWORD_CHANGE, etc.)
- `timestamp`: Data/hora da ação
- `ip_address`: Endereço IP de origem
- `user_agent`: User agent do navegador
- `details`: Detalhes adicionais em JSON

## Sistema de Autenticação

### JWT Customizado
Implementa autenticação JWT com recursos avançados:

- **CustomJWTAuthentication**: Classe customizada que verifica tokens blacklisted
- **Suporte a múltiplos formatos**: Aceita tanto "Bearer" quanto "JWT" como prefixo
- **Blacklist automática**: Tokens invalidados durante logout

### Views de Autenticação

#### LoginView
```
POST /api/auth/login/
{
    "username": "usuario",
    "password": "senha"
}
```

**Recursos:**
- Verificação de conta bloqueada
- Controle de tentativas falhadas
- Reset automático de contador após login bem-sucedido
- Logs de auditoria

#### LogoutView
```
POST /api/auth/logout/
{
    "refresh": "token_refresh"
}
```

**Recursos:**
- Adiciona tokens à blacklist
- Invalida tanto refresh quanto access token
- Logs de auditoria

#### CustomTokenRefreshView
```
POST /api/auth/token/refresh/
{
    "refresh": "token_refresh"
}
```

**Recursos:**
- Verifica blacklist antes de renovar
- Logs de auditoria

## Sistema de Permissões

### Estrutura Hierárquica
1. **Papéis (Roles)**: Definem o nível básico de acesso
2. **Perfis de Acesso**: Conjuntos de permissões específicas
3. **Permissões**: Controle granular por módulo e ação

### Módulos Disponíveis
- PROJECTS (Projetos)
- TASKS (Tarefas)
- TEAMS (Equipes)
- RESOURCES (Recursos)
- COMMUNICATIONS (Comunicações)
- RISKS (Riscos)
- COSTS (Custos)
- DOCUMENTS (Documentos)
- REPORTS (Relatórios)
- USERS (Usuários)
- SETTINGS (Configurações)
- DASHBOARD (Dashboard)
- NOTIFICATIONS (Notificações)
- APPROVALS (Aprovações)

### Ações Disponíveis
- VIEW (Visualizar)
- CREATE (Criar)
- EDIT (Editar)
- DELETE (Excluir)
- APPROVE (Aprovar)
- ASSIGN (Atribuir)
- EXPORT (Exportar)
- IMPORT (Importar)
- COMMENT (Comentar)

### HasModulePermission
Classe de permissão customizada para verificar acesso a módulos específicos:

```python
@permission_classes([HasModulePermission('PROJECTS', 'CREATE')])
def create_project(request):
    # Lógica para criar projeto
    pass
```

## Sistema de Validação

### PasswordPolicyValidator
Validador robusto de políticas de senha:

**Verificações:**
- Comprimento mínimo e máximo
- Presença de letras maiúsculas e minúsculas
- Presença de números
- Presença de caracteres especiais
- Verificação contra senhas comuns
- Verificação contra informações pessoais do usuário

### Outros Validadores
- `validate_username()`: Valida formato e unicidade de usernames
- `validate_full_name()`: Valida formato de nomes completos
- `validate_password_history()`: Verifica reutilização de senhas

## Sistema de Segurança

### Controle de Tentativas de Login
- Contador automático de tentativas falhadas
- Bloqueio automático após 5 tentativas
- Desbloqueio automático após período configurável
- Logs de todas as tentativas

### Notificações de Segurança
O `SecurityNotificationService` envia emails automáticos para:
- Alterações de senha
- Logins suspeitos
- Bloqueios de conta
- Desbloqueios de conta

### Sistema de Auditoria
Registra automaticamente:
- Logins e logouts
- Alterações de senha
- Alterações de perfil
- Bloqueios/desbloqueios de conta
- Criação/modificação de usuários

## API Endpoints

### Autenticação
```
POST /api/auth/login/          # Login
POST /api/auth/logout/         # Logout
POST /api/auth/token/refresh/  # Renovar token
```

### Usuários
```
GET    /api/users/             # Listar usuários
POST   /api/users/             # Criar usuário
GET    /api/users/{id}/        # Obter usuário
PUT    /api/users/{id}/        # Atualizar usuário
PATCH  /api/users/{id}/        # Atualizar parcialmente
DELETE /api/users/{id}/        # Excluir usuário

GET    /api/users/me/          # Meus dados
GET    /api/users/permissions/ # Minhas permissões
POST   /api/users/change-password/    # Alterar senha
POST   /api/users/{id}/reset-password/ # Reset senha (admin)
POST   /api/users/{id}/activate/      # Ativar usuário
POST   /api/users/{id}/deactivate/    # Desativar usuário
POST   /api/users/{id}/unlock/        # Desbloquear usuário
```

### Permissões
```
GET    /api/permissions/       # Listar permissões
POST   /api/permissions/       # Criar permissão
GET    /api/permissions/{id}/  # Obter permissão
PUT    /api/permissions/{id}/  # Atualizar permissão
DELETE /api/permissions/{id}/  # Excluir permissão
```

## Testes

O módulo inclui testes abrangentes organizados em:

### test_models.py
- Testes de criação e validação de modelos
- Testes de métodos personalizados
- Testes de relacionamentos
- Testes de constraints

### test_views.py
- Testes de endpoints da API
- Testes de autenticação e autorização
- Testes de permissões
- Testes de fluxos completos

### test_security.py
- Testes de validadores de senha
- Testes de sistema de bloqueio
- Testes de notificações de segurança
- Testes de auditoria
- Testes de utilitários de segurança

### Executar Testes
```bash
# Todos os testes do módulo
python manage.py test users

# Testes específicos
python manage.py test users.tests.test_models
python manage.py test users.tests.test_views
python manage.py test users.tests.test_security

# Com cobertura
coverage run --source='.' manage.py test users
coverage report
```

## Configuração

### Settings Recomendadas
```python
# settings.py

# Autenticação JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Validadores de senha
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'users.validators.PasswordPolicyValidator',
        'OPTIONS': {
            'min_length': 8,
            'max_length': 128,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_numbers': True,
            'require_special': True,
        }
    },
]

# Configurações de sessão e segurança
SESSION_COOKIE_SECURE = True  # Em produção
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True  # Em produção

# Email para notificações
DEFAULT_FROM_EMAIL = 'noreply@planify.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
        },
    },
    'loggers': {
        'users': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Comandos de Gerenciamento

### Criar Comando de Limpeza de Tokens
```python
# users/management/commands/cleanup_expired_tokens.py
from django.core.management.base import BaseCommand
from users.utils import clean_expired_tokens

class Command(BaseCommand):
    help = 'Remove tokens expirados da blacklist'
    
    def handle(self, *args, **options):
        clean_expired_tokens()
        self.stdout.write('Limpeza concluída')
```

### Uso
```bash
python manage.py cleanup_expired_tokens
```

## Boas Práticas de Segurança

### Para Desenvolvedores
1. **Sempre usar HTTPS em produção**
2. **Validar todas as entradas do usuário**
3. **Implementar rate limiting**
4. **Manter logs de segurança**
5. **Usar senhas seguras por padrão**
6. **Implementar 2FA quando possível**

### Para Administradores
1. **Revisar logs de auditoria regularmente**
2. **Monitorar tentativas de login falhadas**
3. **Configurar alertas para atividades suspeitas**
4. **Manter sistema atualizado**
5. **Fazer backup regular dos dados**

## Troubleshooting

### Problemas Comuns

#### Conta Bloqueada
**Sintoma:** Usuário não consegue fazer login
**Solução:** 
```python
from users.utils import unlock_user_account
user = User.objects.get(username='usuario')
unlock_user_account(user)
```

#### Token Inválido
**Sintoma:** Erro 401 mesmo com token aparentemente válido
**Verificar:** 
1. Token está na blacklist?
2. Token expirou?
3. Formato do header está correto?

#### Permissões Negadas
**Sintoma:** Erro 403 para usuário aparentemente autorizado
**Verificar:**
1. Usuário tem o papel correto?
2. Perfil de acesso está configurado?
3. Permissão específica existe?

## Roadmap Futuro

### Melhorias Planejadas
- [ ] Autenticação de dois fatores (2FA)
- [ ] Single Sign-On (SSO)
- [ ] Rate limiting por IP
- [ ] Análise de comportamento suspeito
- [ ] Políticas de senha mais avançadas
- [ ] Integração com sistemas externos de autenticação

### Contribuindo
Para contribuir com melhorias:
1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente os testes
4. Implemente a funcionalidade
5. Atualize a documentação
6. Abra um Pull Request

## Licença
Este módulo é parte do sistema Planify e segue a mesma licença do projeto principal.

---
**Última atualização:** Junho 2025
**Versão:** 2.0
