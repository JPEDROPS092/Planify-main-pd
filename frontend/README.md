# Guia de Integração de API: Conectando Frontend com Backend Django usando TanStack Query no Nuxt

## Sumário

1. [Introdução](#introducao)
2. [Configuração OpenAPI do Backend](#configuracao-openapi-do-backend)
3. [Geração de Documentação da API](#geracao-de-documentacao-da-api)
4. [Integração Frontend com Nuxt + TanStack Query](#integracao-frontend-com-nuxt-tanstack-query)
5. [Fluxo de Autenticação](#fluxo-de-autenticacao)
6. [Segurança de Tipos](#seguranca-de-tipos)
7. [Melhores Práticas](#melhores-praticas)
8. [Componentes UI com Shadcn](#componentes-ui-com-shadcn)

## Introdução

Este guia explica como integrar o backend Planify com uma aplicação **Nuxt** usando a especificação **OpenAPI** e **TanStack Query** para gerenciamento eficiente de requisições, cache e estados de carregamento. Além disso, utilizamos **Shadcn UI** e ícones para criar uma interface moderna e atraente.

## Configuração OpenAPI do Backend

* Use `drf-spectacular` no Django REST Framework para gerar a documentação OpenAPI.
* Exemplo de settings:

```python
INSTALLED_APPS += ["drf_spectacular"]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Planify API',
    'DESCRIPTION': 'Sistema de Gerenciamento de Projetos',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

* Adicione as rotas da schema:

```python
urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

## Geração de Documentação da API

No backend:

```bash
python manage.py spectacular --file schema.yaml
```

Use o arquivo `schema.yaml` para gerar tipos no frontend.

## Integração Frontend com Nuxt + TanStack Query

### Instalação dos pacotes necessários

```bash
# TanStack Query e Axios
npm install @tanstack/vue-query axios

# Shadcn UI com Nuxt
npm install shadcn-nuxt @nuxtjs/tailwindcss -D

# Ícones
npm install @iconify/vue
```

### Configuração no Nuxt

1️⃣ Crie o plugin `plugins/vue-query.ts`:

```typescript
import { VueQueryPlugin, QueryClient, dehydrate, hydrate } from '@tanstack/vue-query';

export default defineNuxtPlugin((nuxtApp) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5, // 5 minutos
        retry: 2,
        refetchOnWindowFocus: false,
      },
    },
  });
  
  nuxtApp.vueApp.use(VueQueryPlugin, { queryClient });

  // Suporte para SSR
  if (process.server) {
    nuxtApp.payload.vueQueryState = dehydrate(queryClient);
  }
  
  if (process.client && nuxtApp.payload.vueQueryState) {
    hydrate(queryClient, nuxtApp.payload.vueQueryState);
  }
});
```

2️⃣ Configure o `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  plugins: ['~/plugins/vue-query'],
  modules: ['@nuxtjs/tailwindcss', 'shadcn-nuxt'],
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000/api/',
    },
  },
  shadcn: {
    prefix: '', // prefixo para componentes shadcn
    componentDir: './components/ui' // diretório onde os componentes serão gerados
  },
  tailwindcss: {
    exposeConfig: true,
    config: {
      darkMode: 'class',
      content: [
        './components/**/*.{js,vue,ts}',
        './layouts/**/*.vue',
        './pages/**/*.vue',
        './plugins/**/*.{js,ts}',
        './app.vue',
        './components/ui/**/*.{js,vue,ts}'
      ],
      theme: {
        extend: {
          colors: {
            'primary': {
              DEFAULT: '#3D7DF8',
              '50': '#EBF1FE',
              '100': '#D6E4FD',
              '200': '#ADC9FB',
              '300': '#85AFF9',
              '400': '#5C94F7',
              '500': '#3D7DF8',
              '600': '#0F5AE8',
              '700': '#0C46B6',
              '800': '#093384',
              '900': '#051F52'
            },
          }
        }
      }
    }
  }
});
```

3️⃣ Crie os serviços de API:

```typescript
// composables/useApiClient.ts
import axios, { AxiosInstance } from 'axios';
import { useToast } from '~/composables/useToast';

export const useApiClient = (): AxiosInstance => {
  const config = useRuntimeConfig();
  const router = useRouter();
  const { toast } = useToast();
  
  const apiClient = axios.create({
    baseURL: config.public.apiBase,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Adicionar token de autenticação
  apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  // Tratamento de erros e refresh token
  apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;
      
      // Se o erro for 401 e não for uma tentativa de refresh token
      if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== 'auth/token/refresh/') {
        originalRequest._retry = true;
        
        try {
          const refreshToken = localStorage.getItem('refreshToken');
          
          if (!refreshToken) {
            throw new Error('No refresh token');
          }
          
          // Tenta obter um novo token de acesso
          const response = await axios.post(`${config.public.apiBase}auth/token/refresh/`, {
            refresh: refreshToken
          });
          
          const { access } = response.data;
          localStorage.setItem('accessToken', access);
          
          // Reenviar a requisição original
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return apiClient(originalRequest);
        } catch (err) {
          // Se falhar, logout e redireciona para login
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          
          toast({
            title: 'Sessão expirada',
            description: 'Por favor, faça login novamente.',
            variant: 'destructive'
          });
          
          router.push('/login');
          return Promise.reject(error);
        }
      }
      
      // Para outros erros, exibe mensagem
      if (error.response?.data?.detail) {
        toast({
          title: 'Erro',
          description: error.response.data.detail,
          variant: 'destructive'
        });
      } else if (error.message) {
        toast({
          title: 'Erro',
          description: error.message,
          variant: 'destructive'
        });
      }
      
      return Promise.reject(error);
    }
  );

  return apiClient;
};
```

4️⃣ Exemplo de serviço para Projetos:

```typescript
// services/projectService.ts
import { useApiClient } from '~/composables/useApiClient';
import type { Projeto, ProjetoRequest, PaginatedProjetoList } from '~/types/api';

export const useProjectService = () => {
  const apiClient = useApiClient();
  
  return {
    getProjects: async (page = 1): Promise<PaginatedProjetoList> => {
      const response = await apiClient.get('/projects/', {
        params: { page }
      });
      return response.data;
    },
    
    getProject: async (id: string): Promise<Projeto> => {
      const response = await apiClient.get(`/projects/${id}/`);
      return response.data;
    },
    
    createProject: async (project: ProjetoRequest): Promise<Projeto> => {
      const response = await apiClient.post('/projects/', project);
      return response.data;
    },
    
    updateProject: async (id: string, project: ProjetoRequest): Promise<Projeto> => {
      const response = await apiClient.put(`/projects/${id}/`, project);
      return response.data;
    },
    
    deleteProject: async (id: string): Promise<void> => {
      await apiClient.delete(`/projects/${id}/`);
    },
    
    getProjectDashboard: async (id: string): Promise<any> => {
      const response = await apiClient.get(`/projects/${id}/dashboard/`);
      return response.data;
    },
    
    getProjectKanban: async (id: string): Promise<any> => {
      const response = await apiClient.get(`/projects/${id}/kanban/`);
      return response.data;
    },
    
    getProjectGantt: async (id: string): Promise<any> => {
      const response = await apiClient.get(`/projects/${id}/gantt/`);
      return response.data;
    },
    
    addMember: async (id: string, data: any): Promise<any> => {
      const response = await apiClient.post(`/projects/${id}/adicionar_membro/`, data);
      return response.data;
    },
    
    removeMember: async (id: string, data: any): Promise<any> => {
      const response = await apiClient.delete(`/projects/${id}/remover_membro/`, {
        data
      });
      return response.data;
    }
  };
};
```

5️⃣ Exemplo de uso com TanStack Query:

```vue
<!-- pages/projects/index.vue -->
<script setup lang="ts">
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useProjectService } from '~/services/projectService';
import { Icon } from '@iconify/vue';

const projectService = useProjectService();
const queryClient = useQueryClient();
const router = useRouter();

// Estado para formulário de novo projeto
const newProject = ref({
  titulo: '',
  descricao: '',
  data_inicio: '',
  data_fim_previsto: ''
});

// Consulta para carregar projetos
const { data: projects, isLoading, error } = useQuery({
  queryKey: ['projects'],
  queryFn: () => projectService.getProjects()
});

// Mutação para criar projeto
const createProjectMutation = useMutation({
  mutationFn: (project) => projectService.createProject(project),
  onSuccess: () => {
    // Invalidar a consulta para recarregar a lista de projetos
    queryClient.invalidateQueries({ queryKey: ['projects'] });
    // Limpar formulário
    newProject.value = {
      titulo: '',
      descricao: '',
      data_inicio: '',
      data_fim_previsto: ''
    };
  }
});

// Mutação para excluir projeto
const deleteProjectMutation = useMutation({
  mutationFn: (id: string) => projectService.deleteProject(id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['projects'] });
  }
});

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString();
};

const handleCreateProject = () => {
  createProjectMutation.mutate(newProject.value);
};

const navigateToProject = (id: string) => {
  router.push(`/projects/${id}`);
};
</script>

<template>
  <div class="container mx-auto py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold">Projetos</h1>
      
      <!-- Botão para abrir modal de novo projeto -->
      <Button @click="showModal = true">
        <Icon icon="lucide:plus" class="mr-2 h-4 w-4" />
        Novo Projeto
      </Button>
    </div>
    
    <!-- Estado de carregamento -->
    <div v-if="isLoading" class="flex justify-center my-12">
      <div class="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full"></div>
    </div>
    
    <!-- Estado de erro -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 p-4 rounded-lg my-6">
      <p class="text-red-600">{{ error.message }}</p>
    </div>
    
    <!-- Lista de projetos -->
    <div v-else-if="projects?.results?.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="project in projects.results" :key="project.id" 
           class="border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
        <div class="p-6">
          <div class="flex justify-between items-start">
            <h2 class="text-xl font-semibold text-gray-900">{{ project.titulo }}</h2>
            
            <DropdownMenu>
              <DropdownMenuTrigger>
                <Button variant="ghost" size="icon">
                  <Icon icon="lucide:more-vertical" class="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              
              <DropdownMenuContent>
                <DropdownMenuItem @click="navigateToProject(project.id)">
                  <Icon icon="lucide:edit" class="mr-2 h-4 w-4" />
                  Editar
                </DropdownMenuItem>
                <DropdownMenuItem @click="navigateToProject(`${project.id}/kanban`)">
                  <Icon icon="lucide:layout-kanban" class="mr-2 h-4 w-4" />
                  Kanban
                </DropdownMenuItem>
                <DropdownMenuItem @click="navigateToProject(`${project.id}/gantt`)">
                  <Icon icon="lucide:gantt-chart" class="mr-2 h-4 w-4" />
                  Gantt
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem @click="deleteProjectMutation.mutate(project.id)" class="text-red-600">
                  <Icon icon="lucide:trash-2" class="mr-2 h-4 w-4" />
                  Excluir
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          
          <p class="text-gray-500 mt-2">{{ project.descricao }}</p>
          
          <div class="mt-4 flex justify-between text-sm">
            <div>
              <Icon icon="lucide:calendar" class="inline-block mr-1" />
              <span>{{ formatDate(project.data_inicio) }}</span>
            </div>
            <div>
              <Icon icon="lucide:flag" class="inline-block mr-1" />
              <span>{{ formatDate(project.data_fim_previsto) }}</span>
            </div>
          </div>
          
          <div class="mt-4 flex justify-between items-center">
            <Badge :variant="project.status === 'ATIVO' ? 'default' : project.status === 'CONCLUIDO' ? 'success' : 'secondary'">
              {{ project.status_display }}
            </Badge>
            
            <div class="flex -space-x-2">
              <Avatar v-for="(member, index) in project.membros?.slice(0, 3)" :key="index" class="border-2 border-white">
                <AvatarImage :src="`https://api.dicebear.com/7.x/initials/svg?seed=${member.usuario_nome}`" />
                <AvatarFallback>{{ member.usuario_nome.substring(0, 2) }}</AvatarFallback>
              </Avatar>
              
              <div v-if="project.membros?.length > 3" class="flex items-center justify-center w-8 h-8 rounded-full bg-gray-200 text-xs border-2 border-white">
                +{{ project.membros.length - 3 }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Estado vazio -->
    <div v-else class="bg-gray-50 p-12 rounded-lg text-center">
      <Icon icon="lucide:folder" class="mx-auto h-12 w-12 text-gray-400" />
      <h3 class="mt-4 text-lg font-medium text-gray-900">Nenhum projeto encontrado</h3>
      <p class="mt-2 text-gray-500">Comece criando seu primeiro projeto.</p>
      <Button class="mt-4" @click="showModal = true">
        <Icon icon="lucide:plus" class="mr-2 h-4 w-4" />
        Criar Projeto
      </Button>
    </div>
    
    <!-- Modal de criação de projeto -->
    <Dialog :open="showModal" @update:open="showModal = $event">
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Criar Novo Projeto</DialogTitle>
          <DialogDescription>
            Preencha os detalhes para criar um novo projeto.
          </DialogDescription>
        </DialogHeader>
        
        <div class="space-y-4 py-4">
          <div class="space-y-2">
            <Label for="titulo">Título</Label>
            <Input id="titulo" v-model="newProject.titulo" placeholder="Nome do projeto" />
          </div>
          
          <div class="space-y-2">
            <Label for="descricao">Descrição</Label>
            <Textarea id="descricao" v-model="newProject.descricao" placeholder="Descreva o projeto" />
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <Label for="data_inicio">Data de início</Label>
              <Input id="data_inicio" v-model="newProject.data_inicio" type="date" />
            </div>
            
            <div class="space-y-2">
              <Label for="data_fim_previsto">Previsão de término</Label>
              <Input id="data_fim_previsto" v-model="newProject.data_fim_previsto" type="date" />
            </div>
          </div>
        </div>
        
        <DialogFooter>
          <Button variant="outline" @click="showModal = false">Cancelar</Button>
          <Button :disabled="createProjectMutation.isLoading" @click="handleCreateProject">
            <Icon v-if="createProjectMutation.isLoading" icon="lucide:loader-2" class="mr-2 h-4 w-4 animate-spin" />
            Criar Projeto
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>
```

## Fluxo de Autenticação

Aqui está um exemplo de componente de login:

```vue
<!-- pages/login.vue -->
<script setup lang="ts">
import { useMutation } from '@tanstack/vue-query';
import { useApiClient } from '~/composables/useApiClient';
import { Icon } from '@iconify/vue';
import { useToast } from '~/composables/useToast';

const apiClient = useApiClient();
const router = useRouter();
const { toast } = useToast();

const form = ref({
  username: '',
  password: '',
});

const loginMutation = useMutation({
  mutationFn: async (credentials) => {
    const response = await apiClient.post('/auth/login/', credentials);
    return response.data;
  },
  onSuccess: (data) => {
    // Armazenar tokens
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);
    
    toast({
      title: 'Login realizado com sucesso',
      description: 'Bem-vindo ao Planify',
    });
    
    // Redirecionar para a página inicial
    router.push('/');
  },
  onError: (error) => {
    console.error('Erro de login:', error);
  }
});

const handleSubmit = () => {
  loginMutation.mutate(form.value);
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <Card class="w-full max-w-md">
      <CardHeader class="text-center">
        <div class="mx-auto mb-4">
          <Icon icon="lucide:layout-dashboard" class="h-12 w-12 text-primary" />
        </div>
        <CardTitle class="text-2xl">Planify</CardTitle>
        <CardDescription>
          Faça login para acessar a plataforma
        </CardDescription>
      </CardHeader>
      
      <CardContent>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="space-y-2">
            <Label for="username">Usuário</Label>
            <Input id="username" v-model="form.username" placeholder="Digite seu nome de usuário" />
          </div>
          
          <div class="space-y-2">
            <Label for="password">Senha</Label>
            <Input id="password" v-model="form.password" type="password" placeholder="Digite sua senha" />
          </div>
          
          <Button type="submit" class="w-full" :disabled="loginMutation.isLoading">
            <Icon v-if="loginMutation.isLoading" icon="lucide:loader-2" class="mr-2 h-4 w-4 animate-spin" />
            Entrar
          </Button>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
```

## Segurança de Tipos

Gere tipos a partir do OpenAPI:

```bash
# Instale openapi-typescript
npm install --save-dev openapi-typescript

# Gere os tipos
npx openapi-typescript schema.yaml -o types/api.ts
```

## Melhores Práticas

✅ **Configurações do QueryClient:**

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutos
      retry: 2,
      refetchOnWindowFocus: false,
      refetchOnReconnect: 'always',
    },
    mutations: {
      retry: 1,
    },
  },
});
```

✅ **Updates Otimistas:**

```typescript
// Exemplo de atualização otimista
const updateTaskMutation = useMutation({
  mutationFn: (task) => taskService.updateTask(task.id, task),
  // Atualização otimista
  onMutate: async (newTask) => {
    // Cancelar consultas em andamento para evitar sobrescrever a atualização otimista
    await queryClient.cancelQueries({ queryKey: ['tasks', newTask.id] });
    
    // Backup do valor antigo
    const previousTask = queryClient.getQueryData(['tasks', newTask.id]);
    
    // Atualizar cache otimisticamente
    queryClient.setQueryData(['tasks', newTask.id], newTask);
    
    // Retornar contexto com backup
    return { previousTask };
  },
  // Em caso de erro, reverter para o valor anterior
  onError: (err, newTask, context) => {
    queryClient.setQueryData(['tasks', newTask.id], context.previousTask);
  },
  // Revalidar após mutação bem-sucedida
  onSettled: (_, __, variables) => {
    queryClient.invalidateQueries({ queryKey: ['tasks', variables.id] });
  },
});
```

✅ **Invalidação de Cache Inteligente:**

```typescript
// Ao criar uma nova tarefa
createTaskMutation.mutate(newTask, {
  onSuccess: (data) => {
    // Invalidar apenas consultas afetadas
    queryClient.invalidateQueries({ 
      queryKey: ['tasks', { projectId: data.projeto }]
    });
    // Não é necessário invalidar todas as consultas de tarefas
  }
});
```

✅ **Centralização de Erros no Interceptor:**

Nosso interceptor de API já implementa:
- Refresh automático de tokens
- Tratamento centralizado de erros com toast
- Redirecionamento para login em caso de falha de autenticação

## Componentes UI com Shadcn

Shadcn UI fornece componentes estilizados com Tailwind CSS. Instale componentes específicos:

```bash
npx shadcn-nuxt@latest add button
npx shadcn-nuxt@latest add card
npx shadcn-nuxt@latest add input
npx shadcn-nuxt@latest add avatar
npx shadcn-nuxt@latest add badge
npx shadcn-nuxt@latest add dialog
npx shadcn-nuxt@latest add dropdown-menu
npx shadcn-nuxt@latest add tabs
npx shadcn-nuxt@latest add toast
npx shadcn-nuxt@latest add select
npx shadcn-nuxt@latest add textarea
```

Crie um composable para toast:

```typescript
// composables/useToast.ts
import { useToast as useShadcnToast } from '~/components/ui/toast/use-toast';

export const useToast = () => {
  return useShadcnToast();
};
```

### Layout da Aplicação

```vue
<!-- layouts/default.vue -->
<script setup lang="ts">
import { Icon } from '@iconify/vue';

const router = useRouter();
const route = useRoute();

const user = ref({
  name: 'John Doe',
  email: 'john@example.com',
  avatar: 'https://api.dicebear.com/7.x/initials/svg?seed=JD'
});

const navigation = [
  { name: 'Dashboard', href: '/', icon: 'lucide:home' },
  { name: 'Projetos', href: '/projects', icon: 'lucide:briefcase' },
  { name: 'Tarefas', href: '/tasks', icon: 'lucide:check-square' },
  { name: 'Equipes', href: '/teams', icon: 'lucide:users' },
  { name: 'Documentos', href: '/documents', icon: 'lucide:file-text' },
  { name: 'Finanças', href: '/finances', icon: 'lucide:dollar-sign' },
  { name: 'Riscos', href: '/risks', icon: 'lucide:alert-triangle' },
];

const logout = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  router.push('/login');
};

const isActive = (path) => {
  return route.path === path || route.path.startsWith(`${path}/`);
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <div class="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
      <div class="flex-1 flex flex-col min-h-0 bg-white border-r border-gray-200">
        <div class="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
          <div class="flex items-center flex-shrink-0 px-4 mb-5">
            <Icon icon="lucide:layout-dashboard" class="h-8 w-8 text-primary mr-2" />
            <span class="text-xl font-semibold text-gray-900">Planify</span>
          </div>
          
          <nav class="mt-5 flex-1 px-2 space-y-1">
            <a v-for="item in navigation" :key="item.name"
               :href="item.href"
               :class="[
                 isActive(item.href)
                   ? 'bg-primary-50 text-primary'
                   : 'text-gray-600 hover:bg-gray-50',
                 'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
               ]">
              <Icon :icon="item.icon" class="mr-3 h-5 w-5" :class="isActive(item.href) ? 'text-primary' : 'text-gray-400'" />
              {{ item.name }}
            </a>
          </nav>
        </div>
        
        <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
          <DropdownMenu>
            <DropdownMenuTrigger class="flex-shrink-0 w-full group block">
              <div class="flex items-center">
                <div>
                  <Avatar>
                    <AvatarImage :src="user.avatar" />
                    <AvatarFallback>{{ user.name.substring(0, 2) }}</AvatarFallback>
                  </Avatar>
                </div>
                <div class="ml-3 flex-1">
                  <p class="text-sm font-medium text-gray-700 group-hover:text-gray-900">
                    {{ user.name }}
                  </p>
                  <p class="text-xs font-medium text-gray-500 group-hover:text-gray-700">
                    {{ user.email }}
                  </p>
                </div>
                <Icon icon="lucide:chevron-up" class="h-4 w-4 text-gray-400" />
              </div>
            </DropdownMenuTrigger>
            
            <DropdownMenuContent align="end" class="w-56">
              <DropdownMenuLabel>Minha Conta</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <Icon icon="lucide:user" class="mr-2 h-4 w-4" />
                Perfil
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Icon icon="lucide:settings" class="mr-2 h-4 w-4" />
                Configurações
              </DropdownMenuItem>
              <DropdownMenuItem @click="logout">
                <Icon icon="lucide:log-out" class="mr-2 h-4 w-4" />
                Sair
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </div>
    
    <!-- Main content -->
    <div class="md:pl-64 flex flex-col flex-1">
      <div class="sticky top-0 z-10 md:hidden pl-1 pt-1 sm:pl-3 sm:pt-3 bg-white border-b">
        <Button variant="ghost" size="icon" class="-ml-0.5 -mt-0.5 h-12 w-12 inline-flex items-center justify-center rounded-md hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary">
          <span class="sr-only">Abrir menu</span>
          <Icon icon="lucide:menu" class="h-6 w-6" />
        </Button>
      </div>
      
      <main class="flex-1">
        <slot />
      </main>
    </div>
  </div>
  
  <Toaster />
</template>
```

### Exemplo de Página de Dashboard

```vue
<!-- pages/index.vue -->
<script setup lang="ts">
import { useQuery } from '@tanstack/vue-query';
import { useApiClient } from '~/composables/useApiClient';
import { Icon } from '@iconify/vue';

const apiClient = useApiClient();

// Função para buscar dados do dashboard
const fetchDashboardData = async () => {
  const response = await apiClient.get('/projects/my_projects/');
  return response.data;
};

// Consulta para carregar dados do dashboard
const { data: dashboard, isLoading } = useQuery({
  queryKey: ['dashboard'],
  queryFn: fetchDashboardData
});

// Consulta para carregar notificações
const { data: notifications } = useQuery({
  queryKey: ['notifications'],
  queryFn: async () => {
    const response = await apiClient.get('/communications/notificacoes/nao_lidas/');
    return response.data;
  }
});

// Função para formatar data
const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
};
</script>

<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <h1 class="text-2xl font-semibold text-gray-900">Dashboard</h1>
    </div>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <!-- Resumo em cards -->
      <div class="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-primary-100 rounded-md p-3">
                <Icon icon="lucide:briefcase" class="h-6 w-6 text-primary" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Projetos Ativos</dt>
                  <dd>
                    <div class="text-lg font-medium text-gray-900">
                      {{ isLoading ? '...' : dashboard?.results?.filter(p => p.status === 'ATIVO').length }}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-green-100 rounded-md p-3">
                <Icon icon="lucide:check-circle" class="h-6 w-6 text-green-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Tarefas Concluídas</dt>
                  <dd>
                    <div class="text-lg font-medium text-gray-900">12</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-yellow-100 rounded-md p-3">
                <Icon icon="lucide:clock" class="h-6 w-6 text-yellow-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Prazo Médio</dt>
                  <dd>
                    <div class="text-lg font-medium text-gray-900">14 dias</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Projetos recentes e notificações -->
      <div class="mt-8 grid grid-cols-1 gap-5 lg:grid-cols-2">
        <!-- Projetos recentes -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 border-b border-gray-200 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Projetos Recentes
            </h3>
          </div>
          
          <div v-if="isLoading" class="p-4 flex justify-center">
            <div class="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
          </div>
          
          <ul v-else class="divide-y divide-gray-200">
            <li v-for="project in dashboard?.results?.slice(0, 5)" :key="project.id" class="px-4 py-4 sm:px-6 hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <Icon icon="lucide:folder" class="h-5 w-5 text-gray-400" />
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium text-gray-900">{{ project.titulo }}</p>
                    <p class="text-sm text-gray-500">
                      Atualizado em {{ formatDate(project.updated_at) }}
                    </p>
                  </div>
                </div>
                <Badge :variant="project.status === 'ATIVO' ? 'default' : project.status === 'CONCLUIDO' ? 'success' : 'secondary'">
                  {{ project.status_display }}
                </Badge>
              </div>
            </li>
            
            <li v-if="dashboard?.results?.length === 0" class="px-4 py-6 text-center text-gray-500">
              Nenhum projeto encontrado.
            </li>
          </ul>
          
          <div class="border-t border-gray-200 px-4 py-4 sm:px-6">
            <NuxtLink to="/projects" class="text-sm font-medium text-primary hover:text-primary-600">
              Ver todos os projetos
            </NuxtLink>
          </div>
        </div>
        
        <!-- Notificações -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 border-b border-gray-200 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Notificações Recentes
            </h3>
          </div>
          
          <ul class="divide-y divide-gray-200">
            <li v-for="(notification, index) in notifications?.results?.slice(0, 5)" :key="index" class="px-4 py-4 sm:px-6 hover:bg-gray-50">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <Icon 
                    :icon="notification.tipo === 'ALERTA' ? 'lucide:alert-circle' : 'lucide:bell'" 
                    :class="[
                      'h-5 w-5',
                      notification.tipo === 'ALERTA' ? 'text-red-500' : 'text-yellow-500'
                    ]" 
                  />
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">{{ notification.titulo }}</p>
                  <p class="text-sm text-gray-500">{{ notification.mensagem }}</p>
                </div>
              </div>
            </li>
            
            <li v-if="!notifications?.results?.length" class="px-4 py-6 text-center text-gray-500">
              Nenhuma notificação encontrada.
            </li>
          </ul>
          
          <div class="border-t border-gray-200 px-4 py-4 sm:px-6">
            <button class="text-sm font-medium text-primary hover:text-primary-600">
              Marcar todas como lidas
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
```

Este guia abrangente demonstra como integrar uma aplicação frontend Nuxt.js com TanStack Query a um backend Django usando OpenAPI. Os exemplos de código incluem:

1. Configuração completa do Nuxt com TanStack Query
2. Cliente de API com interceptors para autenticação
3. Serviços tipados para consumir a API
4. Componentes de UI com Shadcn e ícones
5. Exemplos de páginas (login, dashboard, lista de projetos)
6. Melhores práticas para gerenciamento de cache e atualizações otimistas

Este guia serve como uma referência completa para desenvolvedores que desejam construir aplicações modernas e performáticas conectando Nuxt.js ao Django.
