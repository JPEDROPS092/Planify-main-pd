# Documentação da API Planify v1.0.0

Bem-vindo à documentação da API Planify. Esta API permite gerenciar projetos, tarefas, equipes, custos e muito mais.

**Base URL:** `/api/` (todos os endpoints são relativos a esta base)

## Autenticação

A API Planify utiliza dois métodos principais de autenticação:

1. **JWT (JSON Web Token):**

   * Obtenha um token de acesso e um token de atualização enviando credenciais para `/auth/token/`.
   * Inclua o token de acesso no header `Authorization` de requisições subsequentes como um Bearer token:
     `Authorization: Bearer <seu_token_de_acesso>`
   * Use o token de atualização para obter um novo token de acesso em `/auth/token/refresh/` quando o token de acesso expirar.
2. **Cookie Authentication:**

   * Algumas interações, especialmente aquelas originadas de um front-end web logado, podem usar autenticação baseada em cookie (`sessionid`).

Endpoints que não exigem autenticação específica (públicos) são indicados na especificação original.

---

## Endpoints da API

### 1. Raiz da API

* **`GET /`**
  * **Descrição:** Redireciona para a documentação da API (provavelmente a interface Swagger/OpenAPI).
  * **Respostas:**
    * `200 OK`: Redirecionamento.

---

### 2. Autenticação (Auth)

* **`POST /auth/token/`**

  * **Descrição:** Obtém um par de tokens JWT (acesso e atualização) usando credenciais de usuário.
  * **Request Body:** `TokenObtainPairRequest`
  * **Respostas:**
    * `200 OK`: `TokenObtainPair`
* **`POST /auth/token/refresh/`**

  * **Descrição:** Obtém um novo token de acesso JWT usando um token de atualização válido.
  * **Request Body:** `TokenRefreshRequest`
  * **Respostas:**
    * `200 OK`: `TokenRefresh`
* **`GET /auth/users/`**

  * **Descrição:** Lista usuários paginados.
  * **Parâmetros Query:** `ordering` (string), `page` (integer), `search` (string).
  * **Respostas:**
    * `200 OK`: `PaginatedUserList`
* **`POST /auth/users/`**

  * **Descrição:** Cria um novo usuário.
  * **Request Body:** `UserCreatePasswordRetypeRequest`
  * **Respostas:**
    * `201 Created`: `UserCreatePasswordRetype`
* **`GET /auth/users/{id}/`**

  * **Descrição:** Obtém detalhes de um usuário específico.
  * **Parâmetro Path:** `id` (integer) - ID do usuário.
  * **Respostas:**
    * `200 OK`: `User`
* **`PUT /auth/users/{id}/`**

  * **Descrição:** Atualiza completamente um usuário específico.
  * **Parâmetro Path:** `id` (integer) - ID do usuário.
  * **Request Body:** `UserRequest`
  * **Respostas:**
    * `200 OK`: `User`
* **`PATCH /auth/users/{id}/`**

  * **Descrição:** Atualiza parcialmente um usuário específico.
  * **Parâmetro Path:** `id` (integer) - ID do usuário.
  * **Request Body:** `PatchedUserRequest`
  * **Respostas:**
    * `200 OK`: `User`
* **`DELETE /auth/users/{id}/`**

  * **Descrição:** Deleta um usuário específico.
  * **Parâmetro Path:** `id` (integer) - ID do usuário.
  * **Respostas:**
    * `204 No Content`
* **`POST /auth/users/activation/`**

  * **Descrição:** Ativa uma conta de usuário usando UID e token.
  * **Request Body:** `ActivationRequest`
  * **Respostas:**
    * `200 OK`: `Activation`
* **`GET /auth/users/me/`**

  * **Descrição:** Obtém detalhes do usuário autenticado atualmente.
  * **Respostas:**
    * `200 OK`: `User`
* **`PUT /auth/users/me/`**

  * **Descrição:** Atualiza completamente o usuário autenticado atualmente.
  * **Request Body:** `UserRequest`
  * **Respostas:**
    * `200 OK`: `User`
* **`PATCH /auth/users/me/`**

  * **Descrição:** Atualiza parcialmente o usuário autenticado atualmente.
  * **Request Body:** `PatchedUserRequest`
  * **Respostas:**
    * `200 OK`: `User`
* **`DELETE /auth/users/me/`**

  * **Descrição:** Deleta o usuário autenticado atualmente.
  * **Respostas:**
    * `204 No Content`
* **`POST /auth/users/resend_activation/`**

  * **Descrição:** Reenvia o e-mail de ativação.
  * **Request Body:** `ResetPasswordRequest` (usa e-mail)
  * **Respostas:**
    * `200 OK`: `ResetPassword` (contém e-mail)
* **`POST /auth/users/reset_password/`**

  * **Descrição:** Solicita um reset de senha (envia e-mail com link).
  * **Request Body:** `ResetPasswordRequest` (usa e-mail)
  * **Respostas:**
    * `200 OK`: `ResetPassword` (contém e-mail)
* **`POST /auth/users/reset_password_confirm/`**

  * **Descrição:** Confirma o reset de senha com uma nova senha e token.
  * **Request Body:** `SetNewPasswordRequest`
  * **Respostas:**
    * `200 OK`: `SetNewPassword`
* **`POST /auth/users/reset_username/`**

  * **Descrição:** Solicita um reset de nome de usuário (envia e-mail com link).
  * **Request Body:** `SendEmailResetRequest`
  * **Respostas:**
    * `200 OK`: `SendEmailReset`
* **`POST /auth/users/reset_username_confirm/`**

  * **Descrição:** Confirma o reset de nome de usuário com um novo nome de usuário.
  * **Request Body:** `UsernameResetConfirmRequest`
  * **Respostas:**
    * `200 OK`: `UsernameResetConfirm`
* **`POST /auth/users/set_password/`**

  * **Descrição:** Define uma nova senha para o usuário autenticado.
  * **Request Body:** `SetPasswordRetypeRequest`
  * **Respostas:**
    * `200 OK`: `SetPasswordRetype`
* **`POST /auth/users/set_username/`**

  * **Descrição:** Define um novo nome de usuário para o usuário autenticado.
  * **Request Body:** `SetUsernameRequest`
  * **Respostas:**
    * `200 OK`: `SetUsername`

---

### 3. Comunicações (Communications)

#### 3.1 Configurações de Notificação

* **`GET /communications/configuracoes/`**

  * **Descrição:** Lista configurações de notificação.
  * **Parâmetros Query:** `ordering` (string), `page` (integer), `search` (string).
  * **Respostas:**
    * `200 OK`: `PaginatedConfiguracaoNotificacaoList`
* **`POST /communications/configuracoes/`**

  * **Descrição:** Cria uma nova configuração de notificação.
  * **Request Body:** `ConfiguracaoNotificacaoRequest`
  * **Respostas:**
    * `201 Created`: `ConfiguracaoNotificacao`
* **`GET /communications/configuracoes/{id}/`**

  * **Descrição:** Obtém detalhes de uma configuração de notificação.
  * **Parâmetro Path:** `id` (integer) - ID da configuração.
  * **Respostas:**
    * `200 OK`: `ConfiguracaoNotificacao`
* **`PUT /communications/configuracoes/{id}/`**

  * **Descrição:** Atualiza uma configuração de notificação.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `ConfiguracaoNotificacaoRequest`
  * **Respostas:**
    * `200 OK`: `ConfiguracaoNotificacao`
* **`PATCH /communications/configuracoes/{id}/`**

  * **Descrição:** Atualiza parcialmente uma configuração de notificação.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `PatchedConfiguracaoNotificacaoRequest`
  * **Respostas:**
    * `200 OK`: `ConfiguracaoNotificacao`
* **`DELETE /communications/configuracoes/{id}/`**

  * **Descrição:** Deleta uma configuração de notificação.
  * **Parâmetro Path:** `id` (integer).
  * **Respostas:**
    * `204 No Content`
* **`GET /communications/configuracoes/minha_configuracao/`**

  * **Descrição:** Retorna a configuração do usuário atual ou cria uma padrão.
  * **Respostas:**
    * `200 OK`: `ConfiguracaoNotificacao`

#### 3.2 Mensagens de Chat

* **`GET /communications/mensagens/`**

  * **Descrição:** Lista mensagens de chat.
  * **Parâmetros Query:** `autor` (integer), `ordering` (string), `page` (integer), `projeto` (integer).
  * **Respostas:**
    * `200 OK`: `PaginatedChatMensagemList`
* **`POST /communications/mensagens/`**

  * **Descrição:** Cria uma nova mensagem de chat.
  * **Request Body:** `ChatMensagemRequest`
  * **Respostas:**
    * `201 Created`: `ChatMensagem`
* **`GET /communications/mensagens/{id}/`**

  * **Descrição:** Obtém detalhes de uma mensagem de chat.
  * **Parâmetro Path:** `id` (integer) - ID da mensagem.
  * **Respostas:**
    * `200 OK`: `ChatMensagem`
* **`PUT /communications/mensagens/{id}/`** (e `PATCH`, `DELETE` similar aos anteriores)
* **`POST /communications/mensagens/{id}/marcar_como_lida/`**

  * **Descrição:** Marca uma mensagem como lida pelo usuário atual.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `ChatMensagemRequest` (verificar se o corpo é realmente necessário ou se é uma ação)
  * **Respostas:**
    * `200 OK`: `ChatMensagem`
* **`GET /communications/mensagens/mensagens_nao_lidas/`**

  * **Descrição:** Retorna mensagens não lidas pelo usuário atual.
  * **Respostas:**
    * `200 OK`: `ChatMensagem` (provavelmente uma lista)

#### 3.3 Notificações

* **`GET /communications/notificacoes/`**

  * **Descrição:** Lista notificações.
  * **Parâmetros Query:** `lida` (boolean), `ordering` (string), `page` (integer), `prioridade` (enum), `projeto` (integer), `tarefa` (integer), `tipo` (enum).
  * **Respostas:**
    * `200 OK`: `PaginatedNotificacaoList`
* **`POST /communications/notificacoes/`**

  * **Descrição:** Cria uma nova notificação.
  * **Request Body:** `NotificacaoRequest`
  * **Respostas:**
    * `201 Created`: `Notificacao`
* **`GET /communications/notificacoes/{id}/`** (e `PUT`, `PATCH`, `DELETE` similar)
* **`POST /communications/notificacoes/{id}/marcar_como_lida/`**

  * **Descrição:** Marca uma notificação como lida.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `NotificacaoRequest` (verificar se o corpo é necessário)
  * **Respostas:**
    * `200 OK`: `Notificacao`
* **`POST /communications/notificacoes/marcar_todas_como_lidas/`**

  * **Descrição:** Marca todas as notificações do usuário como lidas.
  * **Request Body:** `NotificacaoRequest` (verificar se o corpo é necessário)
  * **Respostas:**
    * `200 OK`: `Notificacao` (provavelmente um status ou contagem)
* **`GET /communications/notificacoes/nao_lidas/`**

  * **Descrição:** Retorna notificações não lidas do usuário.
  * **Respostas:**
    * `200 OK`: `Notificacao` (provavelmente uma lista)

---

### 4. Custos (Costs)

#### 4.1 Alertas de Orçamento

* **`GET /costs/alertas/`**

  * **Descrição:** Lista alertas de orçamento.
  * **Parâmetros Query:** `ordering` (string), `page` (integer), `projeto` (integer), `status` (enum), `tarefa` (integer), `tipo` (enum).
  * **Respostas:**
    * `200 OK`: `PaginatedAlertaList`
* **`POST /costs/alertas/`** (e `GET /{id}/`, `PUT /{id}/`, `PATCH /{id}/`, `DELETE /{id}/` similar)
* **`POST /costs/alertas/{id}/ignorar/`**

  * **Descrição:** Marca um alerta como ignorado.
  * **Parâmetro Path:** `id` (integer).
  * **Respostas:**
    * `200 OK`: `Alerta`
* **`POST /costs/alertas/{id}/resolver/`**

  * **Descrição:** Marca um alerta como resolvido.
  * **Parâmetro Path:** `id` (integer).
  * **Respostas:**
    * `200 OK`: `Alerta`
* **`GET /costs/alertas/alertas_ativos/`**

  * **Descrição:** Retorna apenas alertas ativos.
  * **Respostas:**
    * `200 OK`: `Alerta` (provavelmente uma lista)

#### 4.2 Categorias de Custos

* **`GET /costs/categorias/`**

  * **Descrição:** Lista categorias de custos.
  * **Parâmetros Query:** `ordering` (string), `page` (integer), `search` (string).
  * **Respostas:**
    * `200 OK`: `PaginatedCategoriaList`
* **`POST /costs/categorias/`** (e `GET /{id}/`, `PUT /{id}/`, `PATCH /{id}/`, `DELETE /{id}/` similar)

#### 4.3 Custos

* **`GET /costs/custos/`**

  * **Descrição:** Lista custos.
  * **Parâmetros Query:** `categoria` (integer), `data` (date), `ordering` (string), `page` (integer), `projeto` (integer), `search` (string), `tarefa` (integer), `tipo` (enum).
  * **Respostas:**
    * `200 OK`: `PaginatedCustoListList`
* **`POST /costs/custos/`** (e `GET /{id}/`, `PUT /{id}/`, `PATCH /{id}/`, `DELETE /{id}/` similar)
* **`GET /costs/custos/relatorio_por_categoria/`**

  * **Descrição:** Relatório de gastos por categoria.
  * **Respostas:**
    * `200 OK`: `Custo` (provavelmente uma estrutura de relatório)
* **`GET /costs/custos/relatorio_por_projeto/`**

  * **Descrição:** Relatório de gastos por projeto.
  * **Respostas:**
    * `200 OK`: `Custo` (provavelmente uma estrutura de relatório)

#### 4.4 Orçamentos de Projeto

* **`GET /costs/orcamentos-projeto/`**

  * **Descrição:** Lista orçamentos de projetos.
  * **Parâmetros Query:** `page` (integer), `projeto` (integer).
  * **Respostas:**
    * `200 OK`: `PaginatedOrcamentoProjetoList`
* **`POST /costs/orcamentos-projeto/`** (e `GET /{id}/`, `PUT /{id}/`, `PATCH /{id}/`, `DELETE /{id}/` similar)
* **`GET /costs/orcamentos-projeto/projetos_sem_orcamento/`**

  * **Descrição:** Lista projetos sem orçamento definido.
  * **Respostas:**
    * `200 OK`: `OrcamentoProjeto` (provavelmente uma lista)

#### 4.5 Orçamentos de Tarefa

* **`GET /costs/orcamentos-tarefa/`**

  * **Descrição:** Lista orçamentos de tarefas.
  * **Parâmetros Query:** `page` (integer), `tarefa` (integer), `tarefa__projeto` (integer).
  * **Respostas:**
    * `200 OK`: `PaginatedOrcamentoTarefaList`
* **`POST /costs/orcamentos-tarefa/`** (e `GET /{id}/`, `PUT /{id}/`, `PATCH /{id}/`, `DELETE /{id}/` similar)
* **`GET /costs/orcamentos-tarefa/tarefas_sem_orcamento/`**

  * **Descrição:** Lista tarefas sem orçamento definido.
  * **Respostas:**
    * `200 OK`: `OrcamentoTarefa` (provavelmente uma lista)

---

### 5. Dashboard

* **`GET /dashboard/`**
  * **Descrição:** Obtém dados para o dashboard.
  * **Respostas:**
    * `200 OK`: (Corpo da resposta não especificado, provavelmente um objeto JSON com dados agregados)

---

### 6. Documentos (Documents)

#### 6.1 Comentários de Documentos

* **`GET /documents/comentarios/`**

  * **Descrição:** Lista comentários de documentos.
  * **Parâmetros Query:** `autor` (integer), `documento` (integer), `ordering` (string), `page` (integer).
  * **Respostas:**
    * `200 OK`: (Schema não especificado, provavelmente `PaginatedComentarioDocumentoList`)
* **`POST /documents/comentarios/`**

  * **Descrição:** Cria um novo comentário para um documento.
  * **Request Body:** `ComentarioRequest`
  * **Respostas:**
    * `201 Created`: (Schema não especificado, provavelmente `ComentarioDocumento`)
* **`GET /documents/comentarios/{id}/`** (e `PUT`, `PATCH`, `DELETE` similar)

#### 6.2 Documentos

* **`GET /documents/documentos/`**

  * **Descrição:** Lista documentos.
  * **Parâmetros Query:** `enviado_por` (integer), `ordering` (string), `page` (integer), `projeto` (integer), `search` (string), `tarefa` (integer), `tipo` (enum).
  * **Respostas:**
    * `200 OK`: (Schema não especificado, provavelmente `PaginatedDocumentoList`)
* **`POST /documents/documentos/`**

  * **Descrição:** Cria um novo documento.
  * **Request Body:** `DocumentoRequest`
  * **Respostas:**
    * `201 Created`: (Schema não especificado, provavelmente `Documento`)
* **`GET /documents/documentos/{id}/`** (e `PUT`, `PATCH`, `DELETE` similar)
* **`POST /documents/documentos/{id}/adicionar_comentario/`**

  * **Descrição:** Adiciona um comentário a um documento.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `DocumentoRequest` (provavelmente um schema específico para comentário, como `ComentarioRequest`).
  * **Respostas:**
    * `201 Created`
* **`POST /documents/documentos/{id}/associar_tarefa/`**

  * **Descrição:** Associa um documento a uma tarefa.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `DocumentoRequest` (provavelmente um schema para ID da tarefa).
  * **Respostas:**
    * `200 OK`
* **`GET /documents/documentos/{id}/historico/`**

  * **Descrição:** Retorna o histórico de versões de um documento.
  * **Parâmetro Path:** `id` (integer).
  * **Respostas:**
    * `200 OK`: (Schema não especificado, provavelmente `ListaHistoricoDocumento`)

#### 6.3 Histórico de Documentos

* **`GET /documents/historico/`**

  * **Descrição:** Lista todo o histórico de documentos.
  * **Parâmetros Query:** `alterado_por` (integer), `documento` (integer), `page` (integer).
  * **Respostas:**
    * `200 OK`: (Schema não especificado, provavelmente `PaginatedHistoricoDocumentoList`)
* **`GET /documents/historico/{id}/`**

  * **Descrição:** Detalhes de um registro específico do histórico.
  * **Parâmetro Path:** `id` (integer).
  * **Respostas:**
    * `200 OK`: (Schema não especificado, provavelmente `HistoricoDocumento`)

---

### 7. Projetos (Projects)

#### 7.1 Projetos

* **`GET /projects/projetos/`**

  * **Descrição:** Lista projetos.
  * **Parâmetros Query:** `arquivado` (boolean), `ordering` (string), `page` (integer), `prioridade` (enum), `search` (string), `status` (enum).
  * **Respostas:**
    * `200 OK`: `PaginatedProjetoListList`
* **`POST /projects/projetos/`**

  * **Descrição:** Cria um novo projeto.
  * **Request Body:** `ProjetoRequest`
  * **Respostas:**
    * `201 Created`: `Projeto`
* **`GET /projects/projetos/{id}/`** (e `PUT`, `PATCH`, `DELETE` similar)
* **`POST /projects/projetos/{id}/add_member/`**

  * **Descrição:** Adiciona um membro a um projeto.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `ProjetoRequest` (provavelmente um schema `MembroProjetoRequest`).
  * **Respostas:**
    * `200 OK`: `Projeto`
* **`POST /projects/projetos/{id}/archive/`**

  * **Descrição:** Arquiva ou desarquiva um projeto.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `ProjetoRequest` (provavelmente um booleano para arquivar/desarquivar).
  * **Respostas:**
    * `200 OK`: `Projeto`
* **`GET /projects/projetos/{id}/membros/`**

  * **Descrição:** Lista membros de um projeto.
  * **Parâmetro Path:** `id` (integer).
  * **Respostas:**
    * `200 OK`: `Projeto` (deve retornar lista de `MembroProjeto`)
* **`POST /projects/projetos/{id}/remove_member/`**

  * **Descrição:** Remove um membro de um projeto.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `ProjetoRequest` (provavelmente um schema com ID do membro).
  * **Respostas:**
    * `200 OK`: `Projeto`
* **`GET /projects/projetos/my_projects/`**

  * **Descrição:** Retorna projetos do usuário autenticado.
  * **Respostas:**
    * `200 OK`: `Projeto` (provavelmente uma lista)
* **`GET /projects/projetos/test_connection/`**

  * **Descrição:** Endpoint para testar a conexão com a API de projetos.
  * **Respostas:**
    * `200 OK`: `Projeto` (provavelmente uma mensagem de sucesso)

#### 7.2 Sprints

* **`GET /projects/sprints/`**

  * **Descrição:** Lista sprints.
  * **Parâmetros Query:** `ordering` (string), `page` (integer), `projeto` (integer), `search` (string), `status` (enum).
  * **Respostas:**
    * `200 OK`: `PaginatedSprintList`
* **`POST /projects/sprints/`**

  * **Descrição:** Cria uma nova sprint.
  * **Request Body:** `SprintRequest`
  * **Respostas:**
    * `201 Created`: `Sprint`
* **`GET /projects/sprints/{id}/`** (e `PUT`, `PATCH`, `DELETE` similar)
* **`GET /projects/sprints/{id}/tasks/`**

  * **Descrição:** Lista tarefas de uma sprint.
  * **Parâmetro Path:** `id` (integer).
  * **Respostas:**
    * `200 OK`: `Sprint` (deve retornar lista de `Tarefa`)

---

### 8. Métricas de Projetos (Antigo endpoint?)

* **`GET /projetos/{project_id}/metricas/`**
  * **Descrição:** Retorna métricas específicas de um projeto.
  * **Parâmetro Path:** `project_id` (integer).
  * **Respostas:**
    * `200 OK`: (Corpo da resposta não especificado)
  * _Nota: Este endpoint parece usar um path diferente (`/projetos/` em vez de `/projects/`). Verificar consistência._

---

### 9. Riscos (Risks)

#### 9.1 Histórico de Riscos

* **`GET /risks/historico/`**

  * **Descrição:** Lista o histórico de riscos (somente leitura).
  * **Parâmetros Query:** `alterado_por` (integer), `page` (integer), `risco` (integer).
  * **Respostas:**
    * `200 OK`: `PaginatedHistoricoRiscoList`
* **`GET /risks/historico/{id}/`**

  * **Descrição:** Detalhes de um registro do histórico de riscos.
  * **Parâmetro Path:** `id` (integer).
  * **Respostas:**
    * `200 OK`: `HistoricoRisco`

#### 9.2 Riscos

* **`GET /risks/riscos/`**

  * **Descrição:** Lista riscos.
  * **Parâmetros Query:** `impacto` (enum), `ordering` (string), `page` (integer), `probabilidade` (enum), `projeto` (integer), `responsavel_mitigacao` (integer), `search` (string), `status` (enum).
  * **Respostas:**
    * `200 OK`: `PaginatedRiscoListList`
* **`POST /risks/riscos/`**

  * **Descrição:** Cria um novo risco.
  * **Request Body:** `RiscoRequest`
  * **Respostas:**
    * `201 Created`: `Risco`
* **`GET /risks/riscos/{id}/`** (e `PUT`, `PATCH`, `DELETE` similar)
* **`POST /risks/riscos/{id}/atualizar_status/`**

  * **Descrição:** Atualiza o status de um risco.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `RiscoRequest` (provavelmente apenas o campo de status).
  * **Respostas:**
    * `200 OK`: `Risco`
* **`GET /risks/riscos/{id}/historico/`**

  * **Descrição:** Retorna o histórico de alterações de um risco.
  * **Parâmetro Path:** `id` (integer).
  * **Respostas:**
    * `200 OK`: `Risco` (deve retornar `HistoricoRisco` ou similar)
* **`DELETE /risks/riscos/excluir_varios/`**

  * **Descrição:** Exclui múltiplos riscos.
  * **Respostas:**
    * `204 No Content`

---

### 10. Saúde da API (Saude)

* **`GET /saude/`**

  * **Descrição:** Verifica se a API está funcionando.
  * **Respostas:**
    * `200 OK`: (Corpo da resposta não especificado, geralmente uma mensagem de status)
* **`GET /saude/detalhes/`**

  * **Descrição:** Endpoint simples para verificar se a API está funcionando (não requer autenticação).
  * **Respostas:**
    * `200 OK`: (Corpo da resposta não especificado)

---

### 11. Tarefas (Tasks)

#### 11.1 Atribuições de Tarefas

* **`GET /tasks/atribuicoes/`**

  * **Descrição:** Lista atribuições de tarefas.
  * **Parâmetros Query:** `page` (integer), `tarefa` (integer), `usuario` (integer).
  * **Respostas:**
    * `200 OK`: `PaginatedAtribuicaoTarefaList`
* **`POST /tasks/atribuicoes/`** (e `GET /{id}/`, `PUT /{id}/`, `PATCH /{id}/`, `DELETE /{id}/` similar)

#### 11.2 Comentários de Tarefas

* **`GET /tasks/comentarios/`**

  * **Descrição:** Lista comentários de tarefas.
  * **Parâmetros Query:** `autor` (integer), `page` (integer), `tarefa` (integer).
  * **Respostas:**
    * `200 OK`: `PaginatedComentarioTarefaList`
* **`POST /tasks/comentarios/`** (e `GET /{id}/`, `PUT /{id}/`, `PATCH /{id}/`, `DELETE /{id}/` similar)

#### 11.3 Tarefas

* **`GET /tasks/tarefas/`**

  * **Descrição:** Lista tarefas.
  * **Parâmetros Query:** `ordering` (string), `page` (integer), `prioridade` (enum), `projeto` (integer), `search` (string), `sprint` (integer), `status` (enum).
  * **Respostas:**
    * `200 OK`: `PaginatedTarefaListList`
* **`POST /tasks/tarefas/`**

  * **Descrição:** Cria uma nova tarefa.
  * **Request Body:** `TarefaRequest`
  * **Respostas:**
    * `201 Created`: `Tarefa`
* **`GET /tasks/tarefas/{id}/`** (e `PUT`, `PATCH`, `DELETE` similar)
* **`POST /tasks/tarefas/{id}/adicionar_comentario/`**

  * **Descrição:** Adiciona um comentário a uma tarefa.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `TarefaRequest` (provavelmente `ComentarioTarefaRequest`).
  * **Respostas:**
    * `200 OK`: `Tarefa`
* **`POST /tasks/tarefas/{id}/associar_sprint/`**

  * **Descrição:** Associa uma tarefa a uma sprint.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `TarefaRequest` (provavelmente ID da sprint).
  * **Respostas:**
    * `200 OK`: `Tarefa`
* **`POST /tasks/tarefas/{id}/atribuir_responsavel/`**

  * **Descrição:** Atribui um usuário como responsável pela tarefa.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `TarefaRequest` (provavelmente ID do usuário).
  * **Respostas:**
    * `200 OK`: `Tarefa`
* **`POST /tasks/tarefas/{id}/atualizar_status/`**

  * **Descrição:** Atualiza o status de uma tarefa.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `TarefaRequest` (provavelmente apenas o campo status).
  * **Respostas:**
    * `200 OK`: `Tarefa`
* **`POST /tasks/tarefas/{id}/remover_responsavel/`**

  * **Descrição:** Remove um usuário como responsável pela tarefa.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `TarefaRequest` (provavelmente ID do usuário a ser removido).
  * **Respostas:**
    * `200 OK`: `Tarefa`

---

### 12. Equipes (Teams)

#### 12.1 Equipes

* **`GET /teams/equipes/`**

  * **Descrição:** Lista equipes.
  * **Parâmetros Query:** `ordering` (string), `page` (integer), `search` (string).
  * **Respostas:**
    * `200 OK`: `PaginatedEquipeListList`
* **`POST /teams/equipes/`**

  * **Descrição:** Cria uma nova equipe.
  * **Request Body:** `EquipeRequest`
  * **Respostas:**
    * `201 Created`: `Equipe`
* **`GET /teams/equipes/{id}/`** (e `PUT`, `PATCH`, `DELETE` similar)
* **`POST /teams/equipes/{id}/adicionar_membro/`**

  * **Descrição:** Adiciona um membro a uma equipe.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `EquipeRequest` (provavelmente `MembroEquipeRequest`).
  * **Respostas:**
    * `200 OK`: `Equipe`
* **`POST /teams/equipes/{id}/atualizar_papel_membro/`**

  * **Descrição:** Atualiza o papel de um membro da equipe.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `EquipeRequest` (provavelmente ID do membro e novo papel).
  * **Respostas:**
    * `200 OK`: `Equipe`
* **`GET /teams/equipes/{id}/membros/`**

  * **Descrição:** Lista membros de uma equipe.
  * **Parâmetro Path:** `id` (integer).
  * **Respostas:**
    * `200 OK`: `Equipe` (deve retornar lista de `MembroEquipe`)
* **`POST /teams/equipes/{id}/remover_membro/`**

  * **Descrição:** Remove um membro de uma equipe.
  * **Parâmetro Path:** `id` (integer).
  * **Request Body:** `EquipeRequest` (provavelmente ID do membro).
  * **Respostas:**
    * `200 OK`: `Equipe`
* **`GET /teams/equipes/usuarios_disponiveis/`**

  * **Descrição:** Lista usuários disponíveis para adicionar a uma equipe.
  * **Respostas:**
    * `200 OK`: `Equipe` (deve retornar lista de `User`)

#### 12.2 Membros de Equipe

* **`GET /teams/membros/`**

  * **Descrição:** Lista membros de equipe.
  * **Parâmetros Query:** `equipe` (integer), `page` (integer), `papel` (enum), `usuario` (integer).
  * **Respostas:**
    * `200 OK`: `PaginatedMembroEquipeList`
* **`POST /teams/membros/`** (e `GET /{id}/`, `PUT /{id}/`, `PATCH /{id}/`, `DELETE /{id}/` similar)

#### 12.3 Permissões de Equipe

* **`GET /teams/permissoes/`**

  * **Descrição:** Lista permissões de equipe.
  * **Parâmetros Query:** `equipe` (integer), `modulo` (enum), `page` (integer), `papel` (enum), `permissao` (enum).
  * **Respostas:**
    * `200 OK`: `PaginatedPermissaoEquipeList`
* **`POST /teams/permissoes/`** (e `GET /{id}/`, `PUT /{id}/`, `PATCH /{id}/`, `DELETE /{id}/` similar)

---

### 13. Usuário (Específico)

* **`GET /usuario/dashboard/`**
  * **Descrição:** Retorna dados específicos para o dashboard do usuário.
  * **Respostas:**
    * `200 OK`: (Corpo da resposta não especificado)

---

## Data Models (Schemas)

Esta seção detalha os principais modelos de dados usados pela API.

*(Devido à grande quantidade de schemas, listarei apenas alguns exemplos. Uma documentação completa listaria todos os schemas de `components.schemas`)*

### User

* `id` (integer, readOnly)
* `username` (string, maxLength: 30)
* `email` (string, format: email, maxLength: 254)
* `full_name` (string, maxLength: 100)
* `role` (RoleEnum)
* `is_active` (boolean)
* `date_joined` (string, format: date-time, readOnly)
* `profile` (UserProfile)
* `access_profiles` (array of UserAccessProfile, readOnly)

### TokenObtainPairRequest

* `username` (string, writeOnly)
* `password` (string, writeOnly)

### TokenObtainPair

* `access` (string, readOnly)
* `refresh` (string, readOnly)

### Projeto

* `id` (integer, readOnly)
* `titulo` (string, maxLength: 100)
* `descricao` (string)
* `data_inicio` (string, format: date)
* `data_fim` (string, format: date)
* `status` (Status477Enum)
* `status_display` (string, readOnly)
* `prioridade` (PrioridadeEnum)
* `prioridade_display` (string, readOnly)
* `criado_por` (integer, readOnly, nullable)
* `criado_em` (string, format: date-time, readOnly)
* `atualizado_em` (string, format: date-time, readOnly)
* `arquivado` (boolean)
* `membros` (array of MembroProjeto, readOnly)
* `sprints_count` (string, readOnly)
* `tasks_count` (string, readOnly)
* `progresso` (string, readOnly)

### Tarefa

* `id` (integer, readOnly)
* `titulo` (string, maxLength: 200)
* `descricao` (string)
* `projeto` (integer)
* `sprint` (integer, nullable)
* `data_inicio` (string, format: date)
* `data_termino` (string, format: date)
* `prioridade` (PrioridadeEnum)
* `status` (StatusBbcEnum)
* `criado_por` (User, readOnly)
* `criado_em` (string, format: date-time, readOnly)
* `atualizado_em` (string, format: date-time, readOnly)
* `atribuicoes` (string, readOnly) - _Nota: Verifique se isso não deveria ser um array de `AtribuicaoTarefa`_

### Enums Comuns:

* **PrioridadeEnum:** `BAIXA`, `MEDIA`, `ALTA`
* **Status477Enum (Projeto):** `PLANEJADO`, `EM_ANDAMENTO`, `PAUSADO`, `CONCLUIDO`, `CANCELADO`
* **StatusBbcEnum (Tarefa):** `A_FAZER`, `EM_ANDAMENTO`, `FEITO`
* **RoleEnum (Usuário):** `ADMIN`, `PROJECT_MANAGER`, `TEAM_MEMBER`
* ... (e muitos outros enums definidos na especificação)

---

Esta documentação simplificada deve ajudar a entender a estrutura e os principais recursos da API Planify. Para detalhes completos sobre cada campo de request/response e todos os schemas, consulte a especificação OpenAPI original.
