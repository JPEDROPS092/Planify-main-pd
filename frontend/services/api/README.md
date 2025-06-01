# Serviços de API do Planify

Este diretório contém os serviços de API gerados a partir da especificação OpenAPI 3.0.3 do Planify.

## Estrutura

Os serviços estão organizados por tags da API:

- `auth.ts` - Serviços de autenticação e gerenciamento de usuários
- `projects.ts` - Serviços de gerenciamento de projetos e sprints
- `tasks.ts` - Serviços de gerenciamento de tarefas e atribuições
- `communications.ts` - Serviços de mensagens e notificações
- `documents.ts` - Serviços de gerenciamento de documentos
- `risks.ts` - Serviços de gerenciamento de riscos
- `costs.ts` - Serviços de gerenciamento de custos, categorias e alertas
- `teams.ts` - Serviços de gerenciamento de equipes e permissões
- `types.ts` - Tipos TypeScript para todos os modelos da API
- `config.ts` - Configurações e utilitários para os serviços
- `index.ts` - Exportações de todos os serviços

## Autenticação

A autenticação é gerenciada pelo composable `useAuth` que fornece:

- Login/logout
- Armazenamento de tokens JWT
- Refresh automático de tokens
- Acesso ao usuário atual

```typescript
import { useAuth } from '~/services/api';

// No componente
const auth = useAuth();

// Login
await auth.login({ username: 'usuario', password: 'senha' });

// Verificar autenticação
if (auth.isAuthenticated.value) {
  // Usuário autenticado
  console.log(auth.user.value);
}

// Logout
auth.logout();
```

## Uso dos Serviços

Cada serviço exporta funções que correspondem aos endpoints da API:

```typescript
import { listProjetos, createProjeto, retrieveProjeto } from '~/services/api';

// Listar projetos com paginação
const response = await listProjetos({ page: 1, ordering: '-data_criacao' });
const projetos = response.results;

// Obter detalhes de um projeto
const projeto = await retrieveProjeto(1);

// Criar um novo projeto
const novoProjeto = await createProjeto({
  nome: 'Novo Projeto',
  descricao: 'Descrição do projeto',
  data_inicio: '2025-01-01',
  status: 'PENDENTE',
  gerente: 1,
});
```

## Tratamento de Erros

Os serviços lançam erros do tipo `ApiError` que contêm informações detalhadas:

```typescript
import { ApiError } from '~/services/api/config';

try {
  await createProjeto(/* ... */);
} catch (error) {
  if (error instanceof ApiError) {
    console.error(`Erro ${error.status}: ${error.friendlyMessage}`);
    console.error(error.data); // Dados detalhados do erro
  }
}
```

## Composable useApiService

Para facilitar o uso dos serviços com tratamento de loading e erros, use o composable `useApiService`:

```typescript
import { useApiService } from '~/composables/useApiService';

const apiService = useApiService();

// Executar uma operação com tratamento de loading e erros
const result = await apiService.withLoading(
  async () => {
    return await listProjetos({ page: 1 });
  },
  {
    loadingMessage: 'Carregando projetos...',
    successMessage: 'Projetos carregados com sucesso!',
    errorMessage: 'Erro ao carregar projetos.',
  }
);
```

## Uploads de Arquivos

Para endpoints que aceitam uploads de arquivos, os serviços lidam automaticamente com a criação de `FormData`:

```typescript
import { createDocumento } from '~/services/api';

// Obter arquivo do input
const fileInput = document.querySelector('input[type="file"]');
const file = fileInput.files[0];

// Criar documento com arquivo
await createDocumento({
  projeto: 1,
  titulo: 'Documento de Teste',
  tipo: 'REQUISITOS',
  arquivo: file,
});
```

## Configuração

A URL base da API é configurada através da variável de ambiente `NUXT_PUBLIC_API_BASE_URL` ou no `nuxt.config.ts`:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBaseUrl:
        process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
    },
  },
});
```

# API Services Structure Documentation

## Visão Geral

O sistema de API do Planify foi refatorado para seguir as melhores práticas de organização de código e tornar o desenvolvimento mais eficiente. Esta documentação explica a nova estrutura e como usá-la corretamente.

## Estrutura de Arquivos

```
services/api/
├── apiClient.ts           # Cliente central de API com tratamento de erros
├── config.ts              # Configurações e utilitários da API
├── index.ts               # Arquivo de exportação central
├── types.ts               # Tipos compartilhados entre serviços
├── auth.ts                # Serviço de autenticação
├── userService.ts         # Serviço de usuários
├── teamService.ts         # Serviço de equipes (composable)
├── projectService.ts      # Serviço de projetos (composable)
├── taskService.ts         # Serviço de tarefas (composable)
├── documentService.ts     # Serviço de documentos (composable)
├── riskService.ts         # Serviço de riscos (composable)
├── permissionService.ts   # Serviço de permissões
└── endpoints/             # Pasta com endpoints diretos da API
    ├── teams.ts           # Endpoints da API de equipes
    ├── projects.ts        # Endpoints da API de projetos
    ├── tasks.ts           # Endpoints da API de tarefas
    └── ...                # Outros endpoints
```

## Princípios de Design

1. **Separação de Responsabilidades**
   - `endpoints/`: Contém funções diretas para chamadas à API e definições de tipos
   - Arquivos de serviço (ex: `teamService.ts`): Composables Vue com estado reativo e lógica de negócio

2. **Cliente API Centralizado**
   - Todas as chamadas à API passam pelo `apiClient.ts`
   - Tratamento consistente de erros, autenticação e headers

3. **Tipagem Forte com TypeScript**
   - Interfaces bem definidas para todos os objetos de domínio
   - Melhor experiência de desenvolvimento com autocomplete

## Como Usar

### 1. Uso em Componentes Vue (Recomendado)

Use os composables de serviço para acesso à API em componentes Vue:

```vue
<script setup>
import { useProjectService } from '~/services/api';

const { fetchProjects, createProject, isLoading, error } = useProjectService();

// Buscar projetos
const loadProjects = async () => {
  try {
    const result = await fetchProjects();
    // Processar resultado...
  } catch (err) {
    // Erro já tratado pelo serviço
  }
};

// Criar um projeto
const handleCreateProject = async (formData) => {
  try {
    const newProject = await createProject(formData);
    // Fazer algo com o novo projeto...
  } catch (err) {
    // Erro já tratado pelo serviço
  }
};
</script>
```

### 2. Uso Direto dos Endpoints

Para casos avançados, você pode acessar os endpoints diretamente:

```ts
import { listProjects, createProject } from '~/services/api/endpoints/projects';
// ou
import { listProjects, createProject } from '~/services/api';

// Buscar projetos
const fetchData = async () => {
  try {
    const response = await listProjects({ status: 'active' });
    // Processar response.results...
  } catch (err) {
    console.error('Erro ao buscar projetos:', err);
  }
};
```

### 3. Cliente API para Casos Personalizados

```ts
import { apiClient } from '~/services/api';

// Chamada personalizada
const customApiCall = async () => {
  try {
    const data = await apiClient.get('/api/custom/endpoint/', { 
      params: { custom: 'param' } 
    });
    return data;
  } catch (err) {
    console.error('Erro na chamada personalizada:', err);
    throw err;
  }
};
```

## Boas Práticas

1. **Prefira os composables de serviço** para a maioria dos casos de uso, pois eles oferecem:
   - Estado reativo (loading, error)
   - Tratamento de erros
   - Notificações visuais
   - Cache de dados

2. **Use endpoints diretos** apenas quando:
   - Precisar de controle total sobre o ciclo de vida dos dados
   - Estiver implementando funcionalidades muito específicas
   - Estiver criando um novo serviço composable

3. **Estenda os tipos existentes** em vez de criar novos:
   ```ts
   import { Task } from '~/services/api/endpoints/tasks';
   
   interface ExtendedTask extends Task {
     customField: string;
   }
   ```

4. **Mantenha a consistência** seguindo o padrão estabelecido ao criar novos serviços

## Migração do Código Antigo

Ao migrar código existente para a nova estrutura:

1. Identifique o serviço correto a usar
2. Substitua chamadas API antigas pelos métodos composable correspondentes
3. Adapte as estruturas de dados conforme necessário
4. Remova importações redundantes ou obsoletas

# API Services Architecture

This directory contains the API service layer for the Planify application. It follows a structured architecture that separates API endpoint definitions from the service layer that components interact with.

## Directory Structure

```
services/api/
├── apiClient.ts               # Core HTTP client with authentication and error handling
├── config.ts                  # Configuration for API (tokens, URLs, etc)
├── index.ts                   # Central export point for all services
├── endpoints/                 # Direct API endpoint functions
│   ├── communications.ts      # Message and notification endpoints
│   ├── costs.ts               # Cost and budget endpoints
│   ├── documents.ts           # Document management endpoints
│   ├── projects.ts            # Project management endpoints
│   ├── risks.ts               # Risk management endpoints
│   ├── tasks.ts               # Task management endpoints
│   ├── teams.ts               # Team management endpoints
│   └── users.ts               # User management endpoints
└── services/                  # Vue composables for component use
    ├── communicationService.ts  # Message and notification services
    ├── costService.ts           # Cost management services
    ├── documentService.ts       # Document management services
    ├── projectService.ts        # Project management services
    ├── riskService.ts           # Risk management services
    ├── taskService.ts           # Task management services
    ├── teamService.ts           # Team management services
    └── userService.ts           # User management services
```

## Architecture Overview

This API service layer follows a three-tier architecture:

1. **API Client Layer** (`apiClient.ts`): Handles HTTP requests, authentication, and error handling
2. **Endpoint Layer** (`endpoints/*.ts`): Direct interfaces to backend API endpoints
3. **Service Layer** (`services/*.ts`): Vue composables that provide reactive state and methods for components

## Usage Guide

### Importing Services

Import services directly from the central export point:

```typescript
import { useProjectService, useTaskService, useCostService } from '~/services/api';
```

### Basic Usage Pattern

Services follow a consistent pattern:

```typescript
// In a Vue component
const { 
  projects,          // Reactive data
  isLoading,         // Loading state
  error,             // Error state
  fetchProjects,     // Methods to interact with API
  createProject,
  updateProject,
  deleteProject
} = useProjectService();

// Load data in onMounted
onMounted(async () => {
  await fetchProjects();
});
```

### Error Handling

All services handle errors consistently:

```typescript
try {
  await createProject(newProject);
} catch (err) {
  // Error is already stored in the service's error ref
  console.error('Failed to create project:', error.value);
}
```

## Service Structure

Each service follows a consistent structure:

1. **State**: Reactive refs for data, loading state, and errors
2. **Methods**: CRUD operations and other API interactions
3. **Computed Properties**: Derived state (filtered lists, summaries, etc.)

## Adding New Services

To add a new service:

1. Create endpoint file in `endpoints/` with proper TypeScript interfaces
2. Implement service in `services/` using the established pattern
3. Export the service in `index.ts`

## Best Practices

- **Use composables**: Always use the service composables instead of calling endpoints directly
- **TypeScript**: Use TypeScript interfaces for all data structures
- **Error handling**: Let the service handle API errors
- **Reuse**: Share types and utilities between services when appropriate
- **Documentation**: Document all services and methods with JSDoc comments

## Service Reference

### Communication Services

- `useMessageService()`: Manage messages between users
- `useNotificationService()`: Handle system notifications

### Cost Services

- `useCostService()`: Manage project costs and budgets

### Document Services

- `useDocumentService()`: Handle file uploads and document management

### Project Services

- `useProjectService()`: Create and manage projects

### Risk Services

- `useRiskService()`: Manage project risks

### Task Services

- `useTaskService()`: Handle project tasks and assignments

### Team Services

- `useTeamService()`: Manage teams and team members

### User Services

- `useUserService()`: User management and profiles
