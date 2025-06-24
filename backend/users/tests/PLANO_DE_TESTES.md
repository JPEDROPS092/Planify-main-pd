# Plano de Testes - Módulo Users

## Visão Geral
Este documento descreve o plano completo de testes para o módulo **users** do projeto Planify. O módulo users é responsável pelo gerenciamento de usuários, autenticação, autorização, perfis de acesso e funcionalidades de segurança.

## Estrutura do Módulo Users

### Modelos
1. **User** - Modelo principal de usuário (extends AbstractBaseUser)
2. **UserProfile** - Perfil adicional do usuário
3. **AccessProfile** - Perfis de acesso/permissões
4. **Permission** - Permissões específicas por módulo/ação
5. **UserAccessProfile** - Relacionamento usuário-perfil de acesso
6. **PasswordHistory** - Histórico de senhas
7. **AccessAttempt** - Tentativas de acesso
8. **AuditLog** - Log de auditoria
9. **BlacklistedTokens** - Tokens revogados

### Serializers
1. **UserSerializer** - Serializer principal para usuários
2. **UserCreateSerializer** - Serializer para criação de usuários
3. **BaseUserSerializer** - Serializer base
4. **UserProfileSerializer** - Serializer para perfis
5. **AccessProfileSerializer** - Serializer para perfis de acesso
6. **PermissionSerializer** - Serializer para permissões
7. **UserAccessProfileSerializer** - Serializer para relacionamentos
8. **ChangePasswordSerializer** - Serializer para mudança de senha
9. **ResetPasswordSerializer** - Serializer para reset de senha
10. **SetNewPasswordSerializer** - Serializer para definir nova senha
11. **LogoutResponseSerializer** - Serializer para resposta de logout

### Views
1. **UserViewSet** - ViewSet principal para usuários
2. **UserProfileViewSet** - ViewSet para perfis
3. **PermissionViewSet** - ViewSet para permissões

### URLs
- `/users/` - Endpoints para usuários
- `/profiles/` - Endpoints para perfis
- `/permissions/` - Endpoints para permissões
- `/auth/` - Endpoints de autenticação

## Estratégia de Testes

### 1. Testes de Modelos (`test_models.py`)

#### 1.1 User Model
- ✅ Criação de usuário básico
- ✅ Criação de superusuário
- ✅ Validação de campos obrigatórios
- ✅ Unicidade de email e username
- ✅ Criptografia de senha
- ✅ Métodos personalizados (increment_failed_login, reset_failed_login, has_permission)
- ✅ Propriedades (locked)
- ✅ Representação string (__str__)

#### 1.2 UserProfile Model
- ✅ Criação de perfil associado ao usuário
- ✅ Relacionamento OneToOne com User
- ✅ Valores padrão dos campos
- ✅ Validação de escolhas (theme_preference)

#### 1.3 AccessProfile Model
- ✅ Criação de perfil de acesso
- ✅ Validação de campos
- ✅ Timestamps automáticos

#### 1.4 Permission Model
- ✅ Criação de permissão
- ✅ Relacionamento com AccessProfile
- ✅ Validação de escolhas (module, action)
- ✅ Unique constraint (access_profile, module, action)
- ✅ Método get_action_display

#### 1.5 UserAccessProfile Model
- ✅ Relacionamento Many-to-Many entre User e AccessProfile
- ✅ Unique constraint (user, access_profile)

#### 1.6 PasswordHistory Model
- ✅ Criação de histórico de senha
- ✅ Relacionamento com User
- ✅ Ordenação por data de criação

#### 1.7 AccessAttempt Model
- ✅ Registro de tentativas de acesso
- ✅ Campos obrigatórios
- ✅ Ordenação por timestamp

#### 1.8 AuditLog Model
- ✅ Criação de log de auditoria
- ✅ Relacionamento com User
- ✅ GenericForeignKey para outros objetos
- ✅ Validação de choices (action)

#### 1.9 BlacklistedTokens Model
- ✅ Criação de token blacklisted
- ✅ Relacionamento com User
- ✅ Unicidade de token

### 2. Testes de Serializers (`test_serializers.py`)

#### 2.1 UserProfileSerializer
- ✅ Serialização de dados válidos
- ✅ Campos incluídos/excluídos
- ✅ Validação de dados

#### 2.2 PermissionSerializer
- ✅ Serialização com campos display
- ✅ Validação de dados
- ✅ Relacionamento com AccessProfile

#### 2.3 AccessProfileSerializer
- ✅ Serialização com permissões aninhadas
- ✅ Validação de dados
- ✅ Campos read-only

#### 2.4 UserAccessProfileSerializer
- ✅ Serialização de relacionamento
- ✅ Campos write-only vs read-only
- ✅ Validação de foreign key

#### 2.5 BaseUserSerializer
- ✅ Serialização básica de usuário
- ✅ Validação de role
- ✅ Campos obrigatórios

#### 2.6 UserSerializer
- ✅ Criação de usuário com perfil
- ✅ Atualização de usuário e perfil
- ✅ Atualização de senha
- ✅ Campos read-only

#### 2.7 UserCreateSerializer
- ✅ Criação de usuário com validação de senha
- ✅ Role padrão
- ✅ Campos obrigatórios

#### 2.8 ChangePasswordSerializer
- ✅ Validação de senha atual
- ✅ Validação de nova senha
- ✅ Context do request
- ✅ Método save()

#### 2.9 ResetPasswordSerializer
- ✅ Validação de email
- ✅ Campos obrigatórios

#### 2.10 SetNewPasswordSerializer
- ✅ Validação de nova senha
- ✅ Validação de token
- ✅ Campos obrigatórios

### 3. Testes de Views (`test_views.py`)

#### 3.1 UserViewSet
- **Listagem de usuários**
  - ✅ Listar todos os usuários (admin)
  - ✅ Permissão negada para não-admin
  - ✅ Paginação
  - ✅ Filtros

- **Detalhes do usuário**
  - ✅ Obter detalhes de usuário específico
  - ✅ Permissões de acesso
  - ✅ Usuário não encontrado

- **Criação de usuário**
  - ✅ Criar usuário válido
  - ✅ Validação de dados
  - ✅ Permissões para criação
  - ✅ Dados inválidos

- **Atualização de usuário**
  - ✅ Atualizar usuário completo
  - ✅ Atualização parcial
  - ✅ Permissões de edição
  - ✅ Validação de dados

- **Exclusão de usuário**
  - ✅ Excluir usuário
  - ✅ Permissões de exclusão
  - ✅ Usuário não encontrado

- **Ações personalizadas**
  - ✅ `/me/` - Informações do usuário autenticado
  - ✅ `/permissions/` - Permissões do usuário
  - ✅ `/change_password/` - Alterar senha
  - ✅ `/reset_password/` - Reset de senha
  - ✅ `/activate/` - Ativar usuário
  - ✅ `/deactivate/` - Desativar usuário
  - ✅ `/unlock/` - Desbloquear usuário

#### 3.2 UserProfileViewSet
- ✅ CRUD completo para perfis
- ✅ Permissões de acesso
- ✅ Validação de dados

#### 3.3 PermissionViewSet
- ✅ CRUD completo para permissões
- ✅ Permissões de admin
- ✅ Filtros por access_profile, module, action

### 4. Testes de Integração (`test_integration.py`)

#### 4.1 Fluxo Completo de Usuário
- ✅ Criação → Ativação → Login → Operações → Logout
- ✅ Criação de usuário com perfil
- ✅ Atribuição de permissões
- ✅ Verificação de acesso a recursos

#### 4.2 Fluxo de Autenticação
- ✅ Login com credenciais válidas
- ✅ Login com credenciais inválidas
- ✅ Logout e invalidação de token
- ✅ Refresh de token

#### 4.3 Fluxo de Permissões
- ✅ Criação de perfil de acesso
- ✅ Atribuição de permissões
- ✅ Associação usuário-perfil
- ✅ Verificação de permissões

#### 4.4 Fluxo de Segurança
- ✅ Tentativas de login falhas
- ✅ Bloqueio de conta
- ✅ Desbloqueio de conta
- ✅ Histórico de senhas

#### 4.5 Fluxo de Reset de Senha
- ✅ Solicitação de reset
- ✅ Definição de nova senha
- ✅ Validações de segurança

### 5. Testes de Fixtures (`test_fixtures.py`)

#### 5.1 User Fixtures
- ✅ `user_data` - Dados básicos de usuário
- ✅ `user` - Usuário simples
- ✅ `admin_user` - Usuário administrador
- ✅ `team_leader_user` - Usuário líder de equipe
- ✅ `team_member_user` - Usuário membro de equipe

#### 5.2 Profile Fixtures
- ✅ `user_profile_data` - Dados de perfil
- ✅ `user_profile` - Perfil de usuário

#### 5.3 Access Profile Fixtures
- ✅ `access_profile_data` - Dados de perfil de acesso
- ✅ `admin_access_profile` - Perfil administrador
- ✅ `manager_access_profile` - Perfil gerente

#### 5.4 Permission Fixtures
- ✅ `permission_data` - Dados de permissão
- ✅ `view_permission` - Permissão de visualização
- ✅ `create_permission` - Permissão de criação
- ✅ `edit_permission` - Permissão de edição
- ✅ `delete_permission` - Permissão de exclusão

### 6. Testes de Utils (`test_utils.py`)

#### 6.1 Funções de Senha
- ✅ `generate_secure_password`
- ✅ `update_user_password`
- ✅ Validação de histórico de senhas

#### 6.2 Funções de Permissão
- ✅ `check_user_permission`
- ✅ Verificação para diferentes roles

#### 6.3 Funções de Request
- ✅ `get_client_ip`
- ✅ `get_user_agent`

## Cobertura de Testes

### Métricas Esperadas
- **Cobertura de código**: ≥ 95%
- **Cobertura de branches**: ≥ 90%
- **Cobertura de linhas**: ≥ 95%

### Áreas Críticas
1. **Autenticação e autorização** - 100%
2. **Gerenciamento de senhas** - 100%
3. **Validações de segurança** - 100%
4. **CRUD de usuários** - 95%
5. **Permissões e perfis** - 95%

## Configuração de Testes

### Fixtures Globais
- Usuários de diferentes roles
- Perfis de acesso padrão
- Permissões básicas
- Tokens de autenticação

### Configuração de Banco
- SQLite em memória para testes
- Dados isolados por teste
- Cleanup automático

### Mocks e Patches
- Email sending
- External API calls
- File uploads
- Time-sensitive operations

## Execução dos Testes

### Comandos
```bash
# Todos os testes do módulo users
pytest users/tests/ -v

# Testes específicos
pytest users/tests/test_models.py -v
pytest users/tests/test_serializers.py -v
pytest users/tests/test_views.py -v
pytest users/tests/test_integration.py -v
pytest users/tests/test_fixtures.py -v
pytest users/tests/test_utils.py -v

# Com cobertura
pytest users/tests/ --cov=users --cov-report=html -v
```

### Relatórios
- **HTML Coverage Report**: `htmlcov/index.html`
- **Terminal Coverage**: `--cov-report=term`
- **XML Coverage**: `--cov-report=xml`

## Validações Especiais

### Segurança
- Validação de força de senha
- Prevenção de ataques de força bruta
- Auditoria de ações sensíveis
- Proteção contra CSRF/XSS

### Performance
- Queries eficientes (select_related, prefetch_related)
- Paginação adequada
- Cache quando apropriado
- Índices de banco de dados

### Usabilidade
- Mensagens de erro claras
- Validações client-side compatíveis
- Responses consistentes
- Documentação API (OpenAPI)

## Manutenção

### Revisão Regular
- Atualização de fixtures conforme mudanças
- Revisão de cenários de teste
- Atualização de documentação
- Análise de cobertura

### Integração Contínua
- Execução automática em PRs
- Bloqueio de merge com testes falhando
- Relatórios de cobertura
- Notificações de regressão

---

**Status**: ✅ Implementado
**Última Atualização**: 2025-06-24
**Responsável**: Sistema de Testes Automatizado
