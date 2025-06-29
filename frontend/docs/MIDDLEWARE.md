# Middleware no Planify-Fe

Este documento descreve a estrutura de middleware usada no projeto Planify-Fe.

## Estrutura de Middleware

```
middleware/
├── auth.ts           # Protege rotas autenticadas
├── guest.ts          # Redireciona usuários logados
├── admin.ts          # Valida permissões de admin
├── team-member.ts    # Valida se usuário pertence à equipe
├── project-access.ts # Valida acesso a projeto específico
└── load-user-data.ts # Carrega dados críticos do usuário
```

## Middleware vs Interceptors

### Interceptors (Axios) - Lidam com:
- Renovar token automaticamente
- Logout em caso de token inválido
- Adição de headers de autenticação

### Middleware - Lidam com:
- Proteção de rotas ANTES de carregar componente
- Validação de permissões de acesso à página
- Redirecionamentos baseados em estado do usuário
- Carregamento de dados essenciais antes da página

## Como Usar nos Layouts/Páginas

### Layout Protegido
```vue
<!-- layouts/dashboard.vue -->
<script setup lang="ts">
// Aplicar middleware a todas as páginas que usam este layout
definePageMeta({
  middleware: ['auth', 'load-user-data']
})
</script>
```

### Página Específica com Múltiplas Validações
```vue
<!-- pages/admin/usuarios.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: ['auth', 'admin']
})

// Agora pode usar os composables do Orval com segurança
const { data: usuarios } = useUsuáriosUsuáriosListQuery()
</script>
```

### Página de Login
```vue
<!-- pages/login.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: ['guest'], // Redireciona se já logado
  layout: 'auth'
})

const { login, isLoggingIn } = useAuth()
</script>
```

### Página de Projeto
```vue
<!-- pages/projetos/[id]/index.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: ['auth', 'project-access'] // Protege rota + valida acesso ao projeto
})

// Agora pode usar composables com segurança
// Middleware já garantiu que usuário tem acesso
const route = useRoute()
const projectId = route.params.id

const { data: project } = useProjectsProjectsRetrieveQuery({ 
  id: projectId 
})
</script>
```

## Resumo

O Orval + Vue Query são excelentes para:
- Gerenciar requisições HTTP
- Cache de dados
- Loading states
- Tratamento de erros de API

Middleware são essenciais para:
- Proteção de rotas
- Validação de permissões
- Redirecionamentos
- Carregamento de dados críticos
- Validação de parâmetros de rota

Eles trabalham juntos:
1. **Middleware** protege a rota e valida acesso
2. **Composables do Orval** fazem as requisições necessárias
3. **Vue Query** gerencia cache e estados
4. **Interceptors** lidam com erros globais de API
