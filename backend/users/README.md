# Documentação da API Planify - Módulo de Usuários

## 1. Introdução

Esta documentação detalha os endpoints da API para o módulo de Usuários do Planify. Ela cobre autenticação, gerenciamento de usuários, perfis, perfis de acesso e permissões.

**URL Base da API:** `/api/`

## 2. Endpoints de Autenticação

Esses endpoints são tipicamente fornecidos por Djoser e JWT Simple, localizados sob o prefixo `/api/auth/`.

### 2.1. Login (Obter Tokens JWT)

-   **Endpoint:** `POST /api/auth/jwt/create/`
-   **Descrição:** Autentica um usuário e retorna tokens JWT de acesso e atualização.
-   **Permissões:** `AllowAny`
-   **Request Body:**
    ```json
    {
        "username": "seu_usuario",
        "password": "sua_senha"
    }
    ```
-   **Response Body (200 OK):**
    ```json
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

### 2.2. Logout (Invalidar Tokens)

-   **Endpoint:** `POST /api/auth/logout/`
-   **Descrição:** Invalida o token de atualização (refresh token) adicionando-o à blacklist. O token de acesso deve ser descartado pelo cliente.
-   **Permissões:** `IsAuthenticated`
-   **Request Body:**
    ```json
    {
        "refresh": "seu_refresh_token"
    }
    ```
-   **Response Body (200 OK):** (Utilizando `LogoutResponseSerializer`)
    ```json
    {
        "message": "Logout bem-sucedido."
    }
    ```
    *(Nota: A implementação exata da resposta pode variar; Djoser pode retornar 204 No Content para logout se configurado para invalidar tokens)*

### 2.3. Atualizar Token de Acesso (Refresh Token)

-   **Endpoint:** `POST /api/auth/jwt/refresh/`
-   **Descrição:** Gera um novo token de acesso usando um token de atualização válido.
-   **Permissões:** `AllowAny` (o token de atualização em si é a autorização)
-   **Request Body:**
    ```json
    {
        "refresh": "seu_refresh_token_valido"
    }
    ```
-   **Response Body (200 OK):**
    ```json
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

### 2.4. Verificar Token de Acesso

-   **Endpoint:** `POST /api/auth/jwt/verify/`
-   **Descrição:** Verifica se um token de acesso é válido.
-   **Permissões:** `AllowAny`
-   **Request Body:**
    ```json
    {
        "token": "seu_token_de_acesso"
    }
    ```
-   **Response Body (200 OK):**
    ```json
    {}
    ```
    *(Retorna 200 OK se válido, 401 Unauthorized se inválido)*

## 3. Registro de Usuário

Endpoint fornecido por Djoser.

### 3.1. Registrar Novo Usuário

-   **Endpoint:** `POST /api/auth/users/`
-   **Descrição:** Cria um novo usuário no sistema.
-   **Permissões:** `AllowAny` (tipicamente)
-   **Request Body (`UserCreateSerializer`):**
    ```json
    {
        "username": "novousuario",
        "email": "novousuario@example.com",
        "full_name": "Nome Completo do Novo Usuário",
        "password": "senha_forte_123!",
        "role": "TEAM_MEMBER" // Opcional, default 'TEAM_MEMBER'
    }
    ```
-   **Response Body (201 Created - `UserSerializer` ou similar Djoser):**
    ```json
    {
        "id": 1,
        "username": "novousuario",
        "email": "novousuario@example.com",
        "full_name": "Nome Completo do Novo Usuário",
        "role": "TEAM_MEMBER",
        "is_active": true,
        "date_joined": "YYYY-MM-DDTHH:MM:SSZ",
        "profile": null // ou dados do perfil se criado automaticamente
    }
    ```

## 4. Gerenciamento da Conta do Usuário (Logado)

Endpoints fornecidos por Djoser, para o usuário atualmente autenticado.

### 4.1. Obter Detalhes do Usuário Logado

-   **Endpoint:** `GET /api/auth/users/me/`
-   **Descrição:** Retorna os detalhes do usuário atualmente autenticado.
-   **Permissões:** `IsAuthenticated`
-   **Response Body (200 OK - `UserSerializer` ou similar Djoser):**
    ```json
    {
        "id": 1,
        "username": "usuario_logado",
        "email": "usuario@example.com",
        "full_name": "Nome do Usuário Logado",
        "role": "PROJECT_MANAGER",
        "is_active": true,
        "date_joined": "YYYY-MM-DDTHH:MM:SSZ",
        "profile": {
            "user": 1,
            "phone": "123456789",
            "profile_picture": null, // ou URL da imagem
            "theme_preference": "SYSTEM",
            "email_notifications": true,
            "system_notifications": true
        },
        "access_profiles": [
            // Lista de UserAccessProfileSerializer
        ]
    }
    ```

### 4.2. Atualizar Detalhes do Usuário Logado

-   **Endpoint:** `PUT /api/auth/users/me/` (atualização completa) ou `PATCH /api/auth/users/me/` (atualização parcial)
-   **Descrição:** Atualiza os detalhes do usuário atualmente autenticado.
-   **Permissões:** `IsAuthenticated`
-   **Request Body (`UserSerializer` campos relevantes, ou Djoser's UserSerializer):**
    ```json
    // Exemplo para PATCH
    {
        "full_name": "Novo Nome Completo",
        "email": "novoemail@example.com"
    }
    ```
-   **Response Body (200 OK - `UserSerializer` ou similar Djoser):**
    *Similar ao GET, com os dados atualizados.*

### 4.3. Alterar Senha do Usuário Logado

-   **Endpoint:** `POST /api/auth/users/set_password/`
-   **Descrição:** Permite que o usuário autenticado altere sua própria senha.
-   **Permissões:** `IsAuthenticated`
-   **Request Body (Djoser's `SetPasswordSerializer`):**
    ```json
    {
        "new_password": "nova_senha_super_forte!",
        "current_password": "senha_antiga_correta"
    }
    ```
-   **Response Body (204 No Content ou mensagem de sucesso):**
    *(Djoser normalmente retorna 204 No Content)*

### 4.4. Solicitar Redefinição de Senha

-   **Endpoint:** `POST /api/auth/users/reset_password/`
-   **Descrição:** Envia um email para o usuário com um link para redefinir a senha.
-   **Permissões:** `AllowAny`
-   **Request Body (`ResetPasswordSerializer`):**
    ```json
    {
        "email": "email_do_usuario@example.com"
    }
    ```
-   **Response Body (204 No Content ou mensagem de sucesso):**
    *(Djoser normalmente retorna 204 No Content)*

### 4.5. Confirmar Redefinição de Senha

-   **Endpoint:** `POST /api/auth/users/reset_password_confirm/`
-   **Descrição:** Define uma nova senha usando o token e uid enviados por email.
-   **Permissões:** `AllowAny`
-   **Request Body (`SetNewPasswordSerializer` ou Djoser's `PasswordResetConfirmSerializer`):**
    ```json
    {
        "uid": "base64_encoded_user_id",
        "token": "password_reset_token",
        "new_password": "nova_senha_escolhida"
    }
    ```
-   **Response Body (204 No Content ou mensagem de sucesso):**
    *(Djoser normalmente retorna 204 No Content)*

## 5. Gerenciamento de Usuários (Administração)

Endpoints para administradores gerenciarem todos os usuários, localizados sob `/api/users/admin/users/`.

### 5.1. Listar Usuários

-   **Endpoint:** `GET /api/users/admin/users/`
-   **Sumário:** Listar usuários.
-   **Descrição:** Retorna uma lista paginada de usuários.
-   **Permissões:** `HasModulePermission('USERS', 'VIEW')`
-   **Response Body (200 OK - Lista de `UserSerializer`):**
    ```json
    [
        {
            "id": 1,
            "username": "usuario1",
            "email": "usuario1@example.com",
            "full_name": "Nome Usuário Um",
            "role": "TEAM_MEMBER",
            "is_active": true,
            "date_joined": "YYYY-MM-DDTHH:MM:SSZ",
            "profile": { /* UserProfileSerializer data */ },
            "access_profiles": [ /* UserAccessProfileSerializer data */ ]
        },
        // ... outros usuários
    ]
    ```

### 5.2. Criar Novo Usuário (Admin)

-   **Endpoint:** `POST /api/users/admin/users/`
-   **Sumário:** Criar novo usuário.
-   **Descrição:** Cria um novo usuário.
-   **Permissões:** `HasModulePermission('USERS', 'CREATE')`
-   **Request Body (`UserCreateSerializer`):**
    ```json
    {
        "username": "novoadminuser",
        "email": "novoadminuser@example.com",
        "full_name": "Admin Criado Usuario",
        "password": "senha_segura123!",
        "role": "PROJECT_MANAGER" // Ou outro papel
    }
    ```
-   **Response Body (201 Created - `UserCreateSerializer` ou `UserSerializer`):**
    *Similar à resposta do registro de usuário.*

### 5.3. Obter Detalhes do Usuário (Admin)

-   **Endpoint:** `GET /api/users/admin/users/{id}/`
-   **Sumário:** Obter detalhes do usuário.
-   **Descrição:** Retorna informações detalhadas de um usuário específico.
-   **Permissões:** `HasModulePermission('USERS', 'VIEW')`
-   **Response Body (200 OK - `UserSerializer`):**
    *Similar à resposta de "Listar Usuários", para um único usuário.*

### 5.4. Atualizar Usuário (Admin)

-   **Endpoint:** `PUT /api/users/admin/users/{id}/`
-   **Sumário:** Atualizar usuário.
-   **Descrição:** Atualiza todos os campos de um usuário existente.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Request Body (`UserSerializer`):**
    ```json
    {
        "username": "usuario_atualizado",
        "email": "email_atualizado@example.com",
        "full_name": "Nome Completo Atualizado",
        "role": "TEAM_LEADER",
        "is_active": true,
        // "password": "nova_senha_se_for_alterar", // Opcional
        "profile": { /* UserProfileSerializer data para atualizar/criar perfil */ }
    }
    ```
-   **Response Body (200 OK - `UserSerializer`):**
    *Dados do usuário atualizado.*

### 5.5. Atualizar Usuário Parcialmente (Admin)

-   **Endpoint:** `PATCH /api/users/admin/users/{id}/`
-   **Sumário:** Atualizar usuário parcialmente.
-   **Descrição:** Atualiza parcialmente um usuário existente.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Request Body (Campos parciais do `UserSerializer`):**
    ```json
    {
        "full_name": "Apenas Nome Atualizado",
        "is_active": false
    }
    ```
-   **Response Body (200 OK - `UserSerializer`):**
    *Dados do usuário atualizado.*

### 5.6. Excluir Usuário (Admin)

-   **Endpoint:** `DELETE /api/users/admin/users/{id}/`
-   **Sumário:** Excluir usuário.
-   **Descrição:** Remove um usuário existente.
-   **Permissões:** `HasModulePermission('USERS', 'DELETE')`
-   **Response Body (204 No Content):**

### 5.7. Obter Minhas Permissões (Usuário Logado)

-   **Endpoint:** `GET /api/users/admin/users/permissions/`
-   **Sumário:** Retornar minhas permissões.
-   **Descrição:** Retorna as permissões do usuário autenticado.
-   **Permissões:** `IsAuthenticated`
-   **Response Body (200 OK):**
    ```json
    {
        "role": "PROJECT_MANAGER",
        "permissions": [
            "PROJECTS.VIEW",
            "PROJECTS.CREATE",
            "TASKS.EDIT"
            // ... outras permissões no formato "MODULO.ACAO"
        ]
    }
    ```

### 5.8. Ativar Usuário (Admin)

-   **Endpoint:** `POST /api/users/admin/users/{id}/activate/`
-   **Sumário:** Ativar usuário.
-   **Descrição:** Ativa um usuário inativo.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Response Body (200 OK):**
    ```json
    {
        "detail": "Usuário ativado com sucesso"
    }
    ```

### 5.9. Desativar Usuário (Admin)

-   **Endpoint:** `POST /api/users/admin/users/{id}/deactivate/`
-   **Sumário:** Desativar usuário.
-   **Descrição:** Desativa um usuário ativo.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Response Body (200 OK):**
    ```json
    {
        "detail": "Usuário desativado com sucesso"
    }
    ```

### 5.10. Desbloquear Usuário (Admin)

-   **Endpoint:** `POST /api/users/admin/users/{id}/unlock/`
-   **Sumário:** Desbloquear usuário.
-   **Descrição:** Desbloqueia um usuário após tentativas de login malsucedidas.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Response Body (200 OK):**
    ```json
    {
        "detail": "Usuário desbloqueado com sucesso"
    }
    ```

## 6. Gerenciamento de Perfis de Usuário (Administração)

Endpoints para administradores gerenciarem perfis de usuários, localizados sob `/api/users/admin/profiles/`.

### 6.1. Listar Perfis de Usuário

-   **Endpoint:** `GET /api/users/admin/profiles/`
-   **Sumário:** Listar perfis de usuário.
-   **Descrição:** Retorna uma lista de perfis de usuário. (Sem paginação)
-   **Permissões:** `IsAuthenticated`
-   **Response Body (200 OK):**
    ```json
    {
        "results": [
            {
                "user": 1, // ID do usuário
                "phone": "11999998888",
                "profile_picture": "/media/profile_pictures/user1.jpg", // URL
                "theme_preference": "DARK",
                "email_notifications": true,
                "system_notifications": false
            }
            // ... outros perfis
        ]
    }
    ```

### 6.2. Criar Novo Perfil de Usuário (para o Admin Logado)

-   **Endpoint:** `POST /api/users/admin/profiles/`
-   **Sumário:** Criar novo perfil de usuário.
-   **Descrição:** Cria um novo perfil de usuário **para o usuário autenticado (admin)**.
-   **Permissões:** `IsAuthenticated`
-   **Request Body (`UserProfileSerializer` - campo `user` é ignorado e definido como o admin logado):**
    ```json
    {
        // "user": 1, // Este campo será ignorado e definido como o admin logado
        "phone": "22888887777",
        "profile_picture": null, // ou URL de uma imagem pré-upload
        "theme_preference": "LIGHT",
        "email_notifications": false,
        "system_notifications": true
    }
    ```
-   **Response Body (201 Created - `UserProfileSerializer`):**
    *Dados do perfil criado, com o campo `user` preenchido com o ID do admin.*

### 6.3. Obter Detalhes do Perfil de Usuário

-   **Endpoint:** `GET /api/users/admin/profiles/{id}/` (onde `{id}` é o PK do UserProfile)
-   **Sumário:** Obter detalhes do perfil de usuário.
-   **Descrição:** Retorna informações detalhadas de um perfil de usuário específico.
-   **Permissões:** `IsAuthenticated`
-   **Response Body (200 OK - `UserProfileSerializer`):**
    *Similar à entrada na lista de perfis.*

### 6.4. Atualizar Perfil de Usuário

-   **Endpoint:** `PUT /api/users/admin/profiles/{id}/`
-   **Sumário:** Atualizar perfil de usuário.
-   **Descrição:** Atualiza todos os campos de um perfil de usuário existente.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Request Body (`UserProfileSerializer`):**
    ```json
    {
        "user": 1, // ID do usuário associado (geralmente não alterado)
        "phone": "33777776666",
        "profile_picture": null,
        "theme_preference": "SYSTEM",
        "email_notifications": true,
        "system_notifications": true
    }
    ```
-   **Response Body (200 OK - `UserProfileSerializer`):**
    *Dados do perfil atualizado.*

### 6.5. Atualizar Perfil de Usuário Parcialmente

-   **Endpoint:** `PATCH /api/users/admin/profiles/{id}/`
-   **Sumário:** Atualizar perfil de usuário parcialmente.
-   **Descrição:** Atualiza parcialmente um perfil de usuário existente.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Request Body (Campos parciais do `UserProfileSerializer`):**
    ```json
    {
        "phone": "44666665555",
        "theme_preference": "DARK"
    }
    ```
-   **Response Body (200 OK - `UserProfileSerializer`):**
    *Dados do perfil atualizado.*

### 6.6. Excluir Perfil de Usuário

-   **Endpoint:** `DELETE /api/users/admin/profiles/{id}/`
-   **Sumário:** Excluir perfil de usuário.
-   **Descrição:** Remove um perfil de usuário existente.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Response Body (204 No Content):**

## 7. Gerenciamento de Perfis de Acesso (Administração)

Endpoints para administradores gerenciarem perfis de acesso, localizados sob `/api/users/admin/access-profiles/`.

### 7.1. Listar Perfis de Acesso

-   **Endpoint:** `GET /api/users/admin/access-profiles/`
-   **Sumário:** Listar perfis de acesso.
-   **Descrição:** Retorna uma lista paginada de perfis de acesso.
-   **Permissões:** `HasModulePermission('USERS', 'VIEW')`
-   **Response Body (200 OK - Lista de `AccessProfileSerializer`):**
    ```json
    [
        {
            "id": 1,
            "name": "Gerente de Projeto",
            "description": "Perfil para gerentes de projeto com acesso total a projetos.",
            "permissions": [
                {
                    "id": 1,
                    "access_profile": 1,
                    "module": "PROJECTS",
                    "module_display": "Projects",
                    "action": "VIEW",
                    "action_display": "View"
                }
                // ... outras permissões
            ],
            "created_at": "YYYY-MM-DDTHH:MM:SSZ",
            "updated_at": "YYYY-MM-DDTHH:MM:SSZ"
        }
        // ... outros perfis de acesso
    ]
    ```

### 7.2. Criar Novo Perfil de Acesso

-   **Endpoint:** `POST /api/users/admin/access-profiles/`
-   **Sumário:** Criar novo perfil de acesso.
-   **Descrição:** Cria um novo perfil de acesso.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Request Body (`AccessProfileSerializer` - sem `id`, `permissions`, `created_at`, `updated_at`):**
    ```json
    {
        "name": "Visualizador de Relatórios",
        "description": "Perfil com permissão apenas para visualizar relatórios."
    }
    ```
-   **Response Body (201 Created - `AccessProfileSerializer`):**
    *Dados do perfil de acesso criado.*

### 7.3. Obter Detalhes do Perfil de Acesso

-   **Endpoint:** `GET /api/users/admin/access-profiles/{id}/`
-   **Sumário:** Obter detalhes do perfil de acesso.
-   **Descrição:** Retorna informações detalhadas de um perfil de acesso específico.
-   **Permissões:** `HasModulePermission('USERS', 'VIEW')`
-   **Response Body (200 OK - `AccessProfileSerializer`):**
    *Similar à entrada na lista de perfis de acesso.*

### 7.4. Atualizar Perfil de Acesso

-   **Endpoint:** `PUT /api/users/admin/access-profiles/{id}/`
-   **Sumário:** Atualizar perfil de acesso.
-   **Descrição:** Atualiza todos os campos de um perfil de acesso existente.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Request Body (`AccessProfileSerializer` - sem `id`, `permissions`, `created_at`, `updated_at`):**
    ```json
    {
        "name": "Visualizador de Relatórios (Atualizado)",
        "description": "Descrição atualizada."
    }
    ```
-   **Response Body (200 OK - `AccessProfileSerializer`):**
    *Dados do perfil de acesso atualizado.*

### 7.5. Atualizar Perfil de Acesso Parcialmente

-   **Endpoint:** `PATCH /api/users/admin/access-profiles/{id}/`
-   **Sumário:** Atualizar perfil de acesso parcialmente.
-   **Descrição:** Atualiza parcialmente um perfil de acesso existente.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Request Body (Campos parciais do `AccessProfileSerializer`):**
    ```json
    {
        "description": "Nova descrição parcial."
    }
    ```
-   **Response Body (200 OK - `AccessProfileSerializer`):**
    *Dados do perfil de acesso atualizado.*

### 7.6. Excluir Perfil de Acesso

-   **Endpoint:** `DELETE /api/users/admin/access-profiles/{id}/`
-   **Sumário:** Excluir perfil de acesso.
-   **Descrição:** Remove um perfil de acesso existente.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Response Body (204 No Content):**

## 8. Gerenciamento de Permissões (Administração)

Endpoints para administradores gerenciarem permissões individuais, localizados sob `/api/users/admin/permissions/`.

### 8.1. Listar Permissões

-   **Endpoint:** `GET /api/users/admin/permissions/`
-   **Sumário:** Listar permissões do sistema.
-   **Descrição:** Retorna uma lista de permissões do sistema. (Sem paginação)
-   **Permissões:** `HasModulePermission('USERS', 'VIEW')`
-   **Response Body (200 OK):**
    ```json
    {
        "results": [
            {
                "id": 1,
                "access_profile": 1, // ID do AccessProfile associado
                "module": "TASKS",
                "module_display": "Tasks",
                "action": "CREATE",
                "action_display": "Create"
            }
            // ... outras permissões
        ]
    }
    ```

### 8.2. Criar Nova Permissão

-   **Endpoint:** `POST /api/users/admin/permissions/`
-   **Sumário:** Criar nova permissão.
-   **Descrição:** Cria uma nova permissão e a associa a um perfil de acesso.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Request Body (`PermissionSerializer` - sem `id`, `module_display`, `action_display`):**
    ```json
    {
        "access_profile": 1, // ID do AccessProfile
        "module": "REPORTS",
        "action": "VIEW"
    }
    ```
-   **Response Body (201 Created - `PermissionSerializer`):**
    *Dados da permissão criada.*

### 8.3. Obter Detalhes da Permissão

-   **Endpoint:** `GET /api/users/admin/permissions/{id}/`
-   **Sumário:** Obter detalhes da permissão.
-   **Descrição:** Retorna informações detalhadas de uma permissão específica.
-   **Permissões:** `HasModulePermission('USERS', 'VIEW')`
-   **Response Body (200 OK - `PermissionSerializer`):**
    *Similar à entrada na lista de permissões.*

### 8.4. Atualizar Permissão

-   **Endpoint:** `PUT /api/users/admin/permissions/{id}/`
-   **Sumário:** Atualizar permissão.
-   **Descrição:** Atualiza todos os campos de uma permissão existente.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Request Body (`PermissionSerializer` - sem `id`, `module_display`, `action_display`):**
    ```json
    {
        "access_profile": 2,
        "module": "DOCUMENTS",
        "action": "EDIT"
    }
    ```
-   **Response Body (200 OK - `PermissionSerializer`):**
    *Dados da permissão atualizada.*

### 8.5. Atualizar Permissão Parcialmente

-   **Endpoint:** `PATCH /api/users/admin/permissions/{id}/`
-   **Sumário:** Atualizar permissão parcialmente.
-   **Descrição:** Atualiza parcialmente uma permissão existente.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Request Body (Campos parciais do `PermissionSerializer`):**
    ```json
    {
        "action": "DELETE"
    }
    ```
-   **Response Body (200 OK - `PermissionSerializer`):**
    *Dados da permissão atualizada.*

### 8.6. Excluir Permissão

-   **Endpoint:** `DELETE /api/users/admin/permissions/{id}/`
-   **Sumário:** Excluir permissão.
-   **Descrição:** Remove uma permissão existente.
-   **Permissões:** `HasModulePermission('USERS', 'EDIT')`
-   **Response Body (204 No Content):**

## 9. Modelos de Dados (Serializers) Principais

### UserSerializer

Representa um usuário do sistema.

-   `id` (Integer, Read-only): Identificador único do usuário.
-   `username` (String): Nome de usuário único.
-   `email` (String): Endereço de email único.
-   `full_name` (String): Nome completo do usuário.
-   `role` (String): Papel do usuário (ex: 'ADMIN', 'TEAM_MEMBER').
-   `is_active` (Boolean): Indica se o usuário está ativo.
-   `date_joined` (DateTime, Read-only): Data de registro do usuário.
-   `password` (String, Write-only): Senha do usuário (usada para criação/atualização).
-   `profile` (Object, Opcional): Dados do perfil do usuário (`UserProfileSerializer`).
-   `access_profiles` (Array de Objects, Read-only): Perfis de acesso associados ao usuário (`UserAccessProfileSerializer`).

### UserCreateSerializer

Usado para criar novos usuários.

-   `username` (String): Nome de usuário único.
-   `email` (String): Endereço de email único.
-   `full_name` (String): Nome completo do usuário.
-   `password` (String, Write-only): Senha para o novo usuário.
-   `role` (String, Opcional): Papel do usuário (default: 'TEAM_MEMBER').

### UserProfileSerializer

Representa o perfil de um usuário.

-   `user` (Integer): ID do usuário associado.
-   `phone` (String, Opcional): Número de telefone.
-   `profile_picture` (String/File, Opcional): URL da foto de perfil ou arquivo para upload.
-   `theme_preference` (String): Preferência de tema (ex: 'LIGHT', 'DARK', 'SYSTEM').
-   `email_notifications` (Boolean): Habilita/desabilita notificações por email.
-   `system_notifications` (Boolean): Habilita/desabilita notificações no sistema.

### AccessProfileSerializer

Representa um perfil de acesso (conjunto de permissões).

-   `id` (Integer, Read-only): Identificador único do perfil de acesso.
-   `name` (String): Nome do perfil de acesso.
-   `description` (String, Opcional): Descrição do perfil.
-   `permissions` (Array de Objects, Read-only): Lista de permissões associadas (`PermissionSerializer`).
-   `created_at` (DateTime, Read-only): Data de criação.
-   `updated_at` (DateTime, Read-only): Data da última atualização.

### PermissionSerializer

Representa uma permissão individual.

-   `id` (Integer, Read-only): Identificador único da permissão.
-   `access_profile` (Integer): ID do `AccessProfile` ao qual esta permissão pertence.
-   `module` (String): Módulo do sistema (ex: 'PROJECTS', 'TASKS').
-   `module_display` (String, Read-only): Nome de exibição do módulo.
-   `action` (String): Ação permitida (ex: 'VIEW', 'CREATE', 'EDIT').
-   `action_display` (String, Read-only): Nome de exibição da ação.

### UserAccessProfileSerializer

Representa a associação entre um usuário e um perfil de acesso.

-   `id` (Integer, Read-only): Identificador único da associação.
-   `access_profile` (Object, Read-only): Dados do perfil de acesso associado (`AccessProfileSerializer`).
-   `access_profile_id` (Integer, Write-only): ID do `AccessProfile` para associar ao criar/atualizar.

---
**Última atualização:** Baseado nos arquivos fornecidos.