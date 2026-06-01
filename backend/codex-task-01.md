# Codex Task 01: Plano de Refatoração Multi-Tenant do Backend

**Projeto:** Planify

## Objetivo

Planejar e executar, em fases, a refatoração do backend do Planify para uma arquitetura SaaS multi-tenant usando PostgreSQL, `django-tenants` e, em etapa posterior, uma camada de autenticação mais robusta com `django-allauth` e/ou `django-tenant-users`.

**Objetivo técnico:** garantir isolamento forte de dados por empresa, mantendo usuários, permissões, administração, API e testes coerentes com o novo modelo.

## Contexto Atual

### Stack

- Django
- Django REST Framework
- Simple JWT
- Djoser
- SQLite em desenvolvimento

### Domínios

- `users`
- `projects`
- `tasks`
- `teams`
- `risks`
- `costs`
- `documents`
- `communications`
- `core`

### Problema

Os dados estão no mesmo banco/schema sem fronteira formal de tenant/empresa, aumentando o risco de vazamento de dados entre clientes e dificultando backup, auditoria, restauração e manutenção por cliente.

## Decisão Arquitetural

- PostgreSQL como banco principal.
- `django-tenants` para isolamento por schema.
- Um app de tenants, chamado `customers` ou `tenants`.
- Schema `public` para dados compartilhados.
- Um schema por empresa/cliente para dados de negócio.
- Usuário global com associação a uma ou mais empresas.
- Autenticação atual mantida na primeira fase para reduzir risco.
- Avaliação posterior de `django-allauth` e `django-tenant-users`.

## Resultado Esperado

- Cada empresa terá seu próprio schema no PostgreSQL.
- Projetos, tarefas, equipes, riscos, custos, documentos e comunicações ficarão isolados por tenant.
- Usuários poderão acessar apenas tenants permitidos.
- APIs resolverão o tenant por domínio/subdomínio.
- Testes cobrirão criação de tenant, migrações, autenticação e isolamento de dados.
- O admin Django funcionará respeitando o contexto de tenant.
- A documentação explicará como criar, migrar, testar e operar tenants.

## Fases

### Fase 0: Preparação e Baseline

**Checklist**

- [ ] Criar branch específica para a refatoração.
- [ ] Rodar `python manage.py check` e registrar estado atual.
- [ ] Rodar testes existentes com `pytest` e registrar falhas atuais.
- [ ] Gerar backup do `backend/db.sqlite3`.
- [ ] Exportar dump dos dados atuais, se existirem dados importantes.
- [ ] Confirmar versão do Python e dependências atuais.
- [ ] Registrar endpoints principais que precisam continuar funcionando.
- [ ] Registrar modelos customizados de usuário, permissão e perfis.

**Entregáveis**

- Relatório curto do estado atual.
- Lista de falhas conhecidas antes da refatoração.
- Backup local do banco atual.

### Fase 1: Review Completo do Banco e dos Domínios

**Checklist**

- [ ] Mapear todos os models por app.
- [ ] Listar campos, tipos, `ForeignKey`, `ManyToMany`, `OneToOne` e constraints.
- [ ] Identificar models de negócio.
- [ ] Identificar models de autenticação, permissão e configuração global.
- [ ] Identificar models que podem ficar no schema `public`.
- [ ] Identificar models que devem ficar dentro de cada tenant.
- [ ] Criar mapa textual ou diagrama ER dos relacionamentos.
- [ ] Identificar dependências circulares e relacionamentos entre apps.
- [ ] Identificar modelos que apontam para `settings.AUTH_USER_MODEL`.
- [ ] Classificar cada tabela como global/pública, tenant ou híbrida.

**Entregáveis**

- Documento `docs/database-review.md`.
- Tabela de models por escopo: public, tenant ou híbrido.
- Lista de riscos de migração.

### Fase 2: Desenho da Nova Arquitetura

**Checklist**

- [ ] Definir `SHARED_APPS` e `TENANT_APPS`.
- [ ] Definir `INSTALLED_APPS` compatibilizado com `django-tenants`.
- [ ] Decidir nome do app de tenants: `customers` ou `tenants`.
- [ ] Decidir nomes dos models: `Client`, `Tenant`, `Domain`.
- [ ] Escolher resolução de tenant por subdomínio, como `empresa.planify.com`.
- [ ] Definir comportamento local: `empresa.localhost` ou host customizado.
- [ ] Decidir se usuário continua global e pode pertencer a várias empresas.
- [ ] Definir roles por tenant: `owner`, `admin`, `manager`, `member`, `viewer`.

**Entregáveis**

- Documento `docs/multi-tenant-architecture.md`.
- Decisão formal sobre usuário global vs usuário por tenant.
- Decisão formal sobre subdomínios.

### Fase 3: Migração para PostgreSQL

**Checklist**

- [ ] Adicionar dependências de PostgreSQL, como `psycopg` ou `psycopg2-binary`.
- [ ] Criar banco local PostgreSQL para desenvolvimento.
- [ ] Configurar `DATABASES` via variáveis de ambiente.
- [ ] Remover dependência direta de SQLite da configuração principal.
- [ ] Rodar `python manage.py migrate` em banco PostgreSQL limpo.
- [ ] Rodar `python manage.py check` e testes.
- [ ] Documentar setup PostgreSQL no README do backend.

**Entregáveis**

- Backend funcionando em PostgreSQL.
- README atualizado.
- Testes ou checks executados contra PostgreSQL.

### Fase 4: Introdução do django-tenants

**Checklist**

- [ ] Instalar `django-tenants`.
- [ ] Criar app `customers` ou `tenants`.
- [ ] Criar model de tenant herdando `TenantMixin`.
- [ ] Criar model de domínio herdando `DomainMixin`.
- [ ] Configurar `TENANT_MODEL`, `TENANT_DOMAIN_MODEL` e `DATABASE_ROUTERS`.
- [ ] Configurar middleware `TenantMainMiddleware`.
- [ ] Separar `SHARED_APPS`, `TENANT_APPS` e `INSTALLED_APPS`.
- [ ] Rodar migrações shared e tenant.
- [ ] Criar tenant de desenvolvimento e validar acesso.

**Entregáveis**

- Tenant inicial criado.
- Projeto sobe com middleware de tenant.
- Admin acessível no contexto correto.
- Comandos de migração documentados.

### Fase 5: Classificação e Movimentação dos Apps

**Checklist**

- [ ] Mover apps globais para `SHARED_APPS`.
- [ ] Mover apps de negócio para `TENANT_APPS`.
- [ ] Revisar imports e referências entre apps shared e tenant.
- [ ] Ajustar serializers e views que assumem banco único.
- [ ] Ajustar admin que registra models tenant.
- [ ] Revisar signals, managers e querysets.

**Entregáveis**

- Apps organizados entre shared e tenant.
- Admin sem erro de registro ou schema.
- API principal funcionando dentro de um tenant.

### Fase 6: Membership, Permissões e Isolamento

**Checklist**

- [ ] Criar modelo de membership usuário-tenant.
- [ ] Definir roles por tenant.
- [ ] Adaptar middleware/permissões para validar membership no tenant atual.
- [ ] Garantir que usuário autenticado sem acesso ao tenant receba `403`.
- [ ] Garantir que usuário autenticado em tenant A não acesse tenant B.
- [ ] Revisar permissões DRF e serializers que expõem usuários.

**Entregáveis**

- Usuário com acesso controlado por tenant.
- Testes de acesso negado entre tenants.
- Permissões documentadas.

### Fase 7: Refatoração de Autenticação

**Checklist**

- [ ] Revisar fluxos atuais de login, cadastro, reset e troca de senha.
- [ ] Mapear endpoints Djoser usados pelo frontend.
- [ ] Decidir se Djoser será mantido ou removido.
- [ ] Avaliar `django-allauth` e/ou `django-tenant-users`.
- [ ] Definir convites para entrada em tenant.
- [ ] Definir fluxo de primeiro usuário owner do tenant.
- [ ] Definir estratégia futura para SSO/SAML/OIDC.

**Entregáveis**

- ADR sobre estratégia de auth.
- Plano de migração de endpoints do frontend.
- Implementação incremental sem quebrar login atual.

### Fase 8: Migração de Dados Existentes

**Checklist**

- [ ] Definir tenant destino para dados atuais.
- [ ] Criar script de migração de dados.
- [ ] Migrar usuários globais.
- [ ] Migrar dados de negócio para schema do tenant destino.
- [ ] Validar contagens antes/depois por tabela.
- [ ] Validar integridade referencial.
- [ ] Validar arquivos de media/documentos e históricos.

**Entregáveis**

- Script de migração versionado.
- Relatório de contagens antes/depois.
- Plano de rollback.

### Fase 9: Testes

**Checklist**

- [ ] Criar tenant em teste; criar dois tenants em teste.
- [ ] Verificar schema ativo por request.
- [ ] Garantir que listagem de tenant A não retorna dados do tenant B.
- [ ] Garantir isolamento: tarefas, custos, riscos e documentos.
- [ ] Usuário membro acessa tenant permitido; não membro recebe `403`.
- [ ] Testes de regressão: Projects, Tasks, Teams, Risks, Costs, Documents, Communications, Users.

**Entregáveis**

- Suite de testes multi-tenant.
- Cobertura mínima para isolamento entre tenants.
- Documentação de como rodar testes tenant.

### Fase 10: Admin, Docs e Operação

**Checklist**

- [ ] Ajustar Django Admin para contexto multi-tenant.
- [ ] Criar comandos para criar, listar e migrar tenants.
- [ ] Documentar processo de onboarding de nova empresa.
- [ ] Documentar backup/restauração por tenant.
- [ ] Documentar estratégia de domínios.
- [ ] Atualizar Swagger/OpenAPI e README do backend.

**Entregáveis**

- Guia operacional de tenants.
- README atualizado.
- Comandos administrativos documentados.

### Fase 11: Observabilidade e Segurança

**Checklist**

- [ ] Garantir logs com identificador do tenant.
- [ ] Garantir auditoria de ações sensíveis.
- [ ] Revisar CORS, `ALLOWED_HOSTS`, cookies, JWT e HTTPS para produção.
- [ ] Definir rate limiting.
- [ ] Definir backup por tenant.
- [ ] Definir monitoramento de migrations por tenant.

**Entregáveis**

- Checklist de segurança para produção.
- Logs com tenant.
- Plano de backup/restauração.

### Fase 12: Frontend e Integração

**Checklist**

- [ ] Definir como o frontend escolhe ou recebe o tenant.
- [ ] Ajustar URLs por subdomínio.
- [ ] Ajustar login para contexto de empresa.
- [ ] Ajustar armazenamento de token considerando tenant.
- [ ] Ajustar telas de administração de organização.
- [ ] Testar fluxo completo: cadastro, login, criar projeto, criar tarefa.

**Entregáveis**

- Frontend consumindo API tenant-aware.
- Fluxo de troca/acesso de empresa documentado.

## Ordem de Execução

1. Fazer review completo do banco e relacionamentos.
2. Documentar classificação public/tenant/híbrido.
3. Migrar ambiente para PostgreSQL.
4. Introduzir `django-tenants` com tenant mínimo.
5. Separar apps em shared e tenant.
6. Ajustar permissões e membership.
7. Criar testes de isolamento.
8. Migrar dados existentes.
9. Revisar auth e decidir `allauth`/`tenant-users`.
10. Atualizar frontend.
11. Preparar operação, backup e produção.

## Critérios de Aceite

- [ ] `python manage.py check` passa.
- [ ] Migrações shared passam.
- [ ] Migrações tenant passam.
- [ ] Pelo menos dois tenants podem existir simultaneamente.
- [ ] Dados de tenant A não aparecem em tenant B.
- [ ] Usuário sem membership não acessa tenant.
- [ ] Admin funciona no contexto esperado.
- [ ] Swagger/docs continuam acessíveis.
- [ ] Testes principais passam.
- [ ] README e docs operacionais estão atualizados.

## Riscos Principais

- Quebra de autenticação atual.
- Frontend dependendo de endpoints Djoser atuais.
- Models shared importando models tenant.
- Dados históricos sem tenant claro.
- Notificações e permissões misturando escopos.
- Admin Django registrando models no schema errado.
- Testes existentes assumindo banco único.
- Complexidade de migrações em todos os tenants.

## Recomendação Final

Não iniciar pela troca para `django-allauth`. Primeiro estabilizar PostgreSQL e `django-tenants` com a autenticação atual. Depois, com isolamento por tenant validado, executar a refatoração de auth como uma segunda frente controlada.
