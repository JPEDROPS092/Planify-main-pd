Suíte de testes de API (canônica)
=================================

Esta é a única suíte de testes do backend. As cópias antigas em
projects/tests, costs/tests, communications/tests e documents/tests eram
scaffold desatualizado (contrato/campos obsoletos) e foram removidas — o
histórico permanece no git.

Stack real (multi-tenant)
-------------------------
Os testes rodam contra PostgreSQL com django_tenants e exercitam o caminho
HTTP completo (TenantMainMiddleware por host + JWT Bearer + PermissionMiddleware
+ RLS), em vez de force_authenticate (que ignora o middleware). A base está em
tests/tenant_base.py:

  - TenantAPITestCase    -> usuário comum com TenantMembership ativa (papel
                            owner por padrão); use para endpoints de negócio.
  - SuperuserAPITestCase -> superusuário via JWT; use para endpoints
                            administrativos (ex.: /api/users/).

Cada classe cria um schema de tenant de teste próprio (uma vez por classe) e o
APIClient já vem autenticado e roteado para o domínio do tenant.

Como rodar
----------
Requer o PostgreSQL de desenvolvimento de pé (docker compose up -d). O usuário
do banco precisa poder criar database/schema (CREATE) para o banco de teste.

  # primeira execução (cria o banco de teste e os schemas):
  python -m pytest tests/ --create-db

  # execuções seguintes (reaproveita o banco de teste, mais rápido):
  python -m pytest tests/ --reuse-db

Não use USE_SQLITE=True aqui: django_tenants e o isolamento por schema só
existem no backend PostgreSQL.
