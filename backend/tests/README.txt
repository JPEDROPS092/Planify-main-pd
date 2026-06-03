Suíte de testes de API (canônica)
=================================

Esta é a única suíte de testes do backend. As cópias antigas em
projects/tests, costs/tests, communications/tests e documents/tests eram
scaffold desatualizado (contrato/campos obsoletos) e foram removidas — o
histórico permanece no git.

Stack real (multi-tenant shared schema)
---------------------------------------
A partir de 2026-06-03 o isolamento é por `tenant_id` num único schema
PostgreSQL (sem django_tenants/schema/subdomínio). Os testes exercitam o
caminho HTTP completo — PermissionMiddleware (JWT Bearer + resolve o tenant
pela TenantMembership ativa + ativa o contexto de tenant da thread) +
TenantDatabaseRLSMiddleware + TenantManager/apply_tenant_rls — em vez de
force_authenticate (que ignora o middleware). A base está em
tests/tenant_base.py:

  - TenantAPITestCase    -> usuário comum com TenantMembership ativa (papel
                            owner por padrão); use para endpoints de negócio.
  - SuperuserAPITestCase -> superusuário via JWT; use para endpoints
                            administrativos (ex.: /api/users/).

O tenant de teste é uma linha customers.Client comum (self.tenant). A base
mantém o contexto de tenant ativo durante o teste, de modo que os
Model.objects.create(...) feitos no setUp/teste são carimbados com tenant_id
e as leituras ficam escopadas; o self.client restaura esse escopo após cada
request (o middleware o desativa ao fim de cada chamada).

Como rodar
----------
Requer o PostgreSQL de desenvolvimento de pé (docker compose up -d postgres).
O usuário do banco precisa poder criar database (CREATE) para o banco de teste.

  # primeira execução (cria o banco de teste):
  python -m pytest tests/ --create-db

  # execuções seguintes (reaproveita o banco de teste, mais rápido):
  python -m pytest tests/ --reuse-db

Não use USE_SQLITE=True aqui: o stack multi-tenant é validado em PostgreSQL.
Rode os testes com a role dona do banco (não app_user): a RLS nativa é inócua
para ela e não atrapalha a criação de fixtures.
