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
