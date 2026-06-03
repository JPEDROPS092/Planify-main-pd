from django.contrib import admin

# `core` é um app SHARED (schema public). O admin do Django roda no schema
# resolvido pelo host da requisição. Por isso este módulo NÃO consulta models
# tenant (Projeto, Tarefa, etc.): no schema public essas tabelas não existem e a
# consulta quebraria a página inicial do admin.
#
# Histórico: havia um override de `admin.site.index` que agregava métricas de
# projetos/tarefas a cada carga do admin. Além de acoplar um app shared a models
# tenant (e quebrar `/admin/` no host público com ProgrammingError), o template
# do admin não renderizava nenhuma daquelas variáveis de contexto — era código
# morto. As métricas de negócio são expostas pelos endpoints de dashboard
# tenant-scoped em `core/views.py` (`/api/dashboard/`, `/api/user/dashboard/`),
# que aplicam RLS e rodam no schema do tenant.
admin.site.site_header = 'Planify - Administração'
admin.site.site_title = 'Planify - Sistema de Gerenciamento de Projetos'
admin.site.index_title = 'Dashboard'
