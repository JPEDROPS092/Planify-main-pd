Okay, aqui está a tradução completa do seu guia para o português, mantendo todas as informações e a formatação Markdown:

---

# Guia de Integração de API: Conectando Frontend com Backend Django

## Sumário
1. [Introdução](#introducao)
2. [Configuração OpenAPI do Backend](#configuracao-openapi-do-backend)
3. [Geração de Documentação da API](#geracao-de-documentacao-da-api)
4. [Integração Frontend](#integracao-frontend)
   - [Integração com React](#integracao-com-react)
   - [Integração com Nuxt](#integracao-com-nuxt)
5. [Fluxo de Autenticação](#fluxo-de-autenticacao)
6. [Segurança de Tipos](#seguranca-de-tipos)
7. [Melhores Práticas](#melhores-praticas)

## Introdução

Este guia explica como integrar o backend Planify com uma aplicação frontend usando a especificação OpenAPI. Usamos `drf-spectacular` para gerar esquemas OpenAPI que podem ser consumidos por ferramentas de frontend para criar clientes de API com segurança de tipos (type-safe).

## Configuração OpenAPI do Backend

Nosso backend Django já está configurado com `drf-spectacular`. Aqui está a configuração atual em `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Configurações do Spectacular para geração OpenAPI
SPECTACULAR_SETTINGS = {
    'TITLE': 'Planify API',
    'DESCRIPTION': 'Sistema de Gerenciamento de Projetos',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/',
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    'SECURITY': [
        {
            'JWT': []
        }
    ],
    'TAGS': [
        {'name': 'Autenticação', 'description': 'Endpoints de autenticação'},
        {'name': 'Usuários', 'description': 'Gerenciamento de usuários'},
        {'name': 'Projetos', 'description': 'Gerenciamento de projetos'},
        {'name': 'Tarefas', 'description': 'Gerenciamento de tarefas'},
        {'name': 'Equipes', 'description': 'Gerenciamento de equipes'},
        {'name': 'Comunicações', 'description': 'Gerenciamento de comunicações'},
        {'name': 'Riscos', 'description': 'Gerenciamento de riscos'},
        {'name': 'Custos', 'description': 'Gerenciamento de custos'},
        {'name': 'Documentos', 'description': 'Gerenciamento de documentos'},
    ],
}
```

## Geração de Documentação da API

Para gerar o esquema OpenAPI, execute:

```bash
# Gera o esquema OpenAPI no formato YAML
python manage.py spectacular --file schema.yaml

# Opcional: Gera o esquema no formato JSON
python manage.py spectacular --file schema.json
```

O esquema será gerado na raiz do projeto. Este arquivo contém todos os endpoints da API, modelos e requisitos de autenticação.

## Integração Frontend

### Integração com React

Para aplicações React, recomendamos usar o OpenAPI TypeScript Generator ou o RTK Query com o gerador OpenAPI.

#### Opção 1: Usando OpenAPI TypeScript Generator

1. Instale os pacotes necessários:
```bash
npm install @openapitools/openapi-generator-cli
```

2. Adicione o script ao `package.json`:
```json
{
  "scripts": {
    "generate-api": "openapi-generator-cli generate -i ../backend/schema.yaml -g typescript-axios -o src/api"
  }
}
```

3. Gere o cliente da API:
```bash
npm run generate-api
```

4. Uso em componentes React:

```typescript
// src/api/apiConfig.ts
import { Configuration, DefaultApi } from './api';
import { getToken } from './auth'; // Assumindo que você tem uma função getToken

const configuration = new Configuration({
  basePath: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  accessToken: getToken // Função que retorna o token JWT
});

export const api = new DefaultApi(configuration);
```

```typescript
// Exemplo de uso em um componente
import { api } from '../api/apiConfig';
import { useState, useEffect } from 'react';
// Importe os tipos necessários da API gerada se precisar deles explicitamente
// import { Project } from './api'; // Exemplo

const ProjectsList = () => {
  const [projects, setProjects] = useState([]); // Ou useState<Project[]>([]) para tipagem

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await api.projectsList(); // Ajuste conforme o nome da sua operação
        setProjects(response.data);
      } catch (error) {
        console.error('Erro ao buscar projetos:', error);
      }
    };
    
    fetchProjects();
  }, []);

  return (
    // Seu JSX aqui
  );
};
```

#### Opção 2: Usando RTK Query

1. Instale os pacotes:
```bash
npm install @reduxjs/toolkit react-redux @rtk-query/codegen-openapi
```

2. Gere o slice da API:
```bash
npx @rtk-query/codegen-openapi openapi-config.js
```

3. Configuração (`openapi-config.js`):
```javascript
module.exports = {
  schemaFile: '../backend/schema.yaml',
  apiFile: './src/store/emptyApi.ts', // Arquivo base da API (geralmente exporta createApi)
  apiImport: 'emptySplitApi', // Nome da exportação do apiFile
  outputFile: './src/store/planifyApi.ts', // Arquivo de saída para os endpoints gerados
  exportName: 'planifyApi', // Nome da API exportada
  hooks: true, // Gerar hooks (useGetProjectsQuery, etc.)
}
```

### Integração com Nuxt

Para aplicações Nuxt 3, podemos usar o módulo OpenAPI diretamente.

1. Instale os pacotes necessários:
```bash
npm install @nuxtjs/openapi
```

2. Configure em `nuxt.config.ts`:
```typescript
export default defineNuxtConfig({
  modules: ['@nuxtjs/openapi'],
  openapi: {
    baseURL: process.env.API_BASE_URL || 'http://localhost:8000',
    endpoints: {
      planify: { // Nome do cliente API (ex: api.planify)
        path: './schema.yaml', // Caminho para o arquivo de schema local ou URL
        headers: { // Cabeçalhos padrão para este cliente
          Authorization: 'JWT {token}' // O {token} será substituído dinamicamente
        }
      }
    }
  }
})
```

3. Uso em componentes:

```vue
<script setup lang="ts">
import { useApi } from '#openapi'; // Importação automática do Nuxt

const api = useApi();

// Exemplo: Buscar projetos
// A estrutura exata de api.planify.projects.list() dependerá de como o gerador nomeia as operações.
// Pode ser algo como api.planify.listProjects() ou similar. Verifique a documentação do gerador.
const { data: projects, pending, error } = await useAsyncData('projects', () =>
  api.planify.projects.list() // Ajuste se necessário baseado no operationId do seu schema
);
</script>

<template>
  <div>
    <div v-if="pending">Carregando...</div>
    <div v-else-if="error">Erro: {{ error.message }}</div>
    <div v-else>
      <div v-for="project in projects" :key="project.id">
        {{ project.name }}
      </div>
    </div>
  </div>
</template>
```

## Fluxo de Autenticação

A API usa autenticação JWT. Veja como lidar com isso:

1. Requisição de Login:
```typescript
// Exemplo React/TypeScript
const login = async (username: string, password: string) => {
  // A chamada exata da API dependerá do operationId do seu endpoint de login
  // Ex: api.authLoginCreate({ username, password }) ou api.tokenCreate({ username, password })
  const response = await api.login({ username, password }); // Ajuste conforme necessário
  const { access, refresh } = response.data;
  
  // Armazene os tokens (use seu método de armazenamento preferido)
  localStorage.setItem('accessToken', access);
  localStorage.setItem('refreshToken', refresh);
  
  return response.data;
};
```

2. Interceptor do Axios para Atualização de Token:
```typescript
import axios from 'axios';

const apiClient = axios.create({ // Renomeado para apiClient para evitar conflito com 'api' gerado
  baseURL: process.env.NEXT_PUBLIC_API_URL
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `JWT ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Verifica se o erro é 401 e se a requisição ainda não foi tentada novamente
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        // A URL para refresh do token pode variar
        const response = await apiClient.post('/auth/token/refresh/', { // Ajuste o endpoint se necessário
          refresh: refreshToken
        });
        
        const { access } = response.data;
        localStorage.setItem('accessToken', access);
        
        // Atualiza o cabeçalho da requisição original com o novo token
        originalRequest.headers.Authorization = `JWT ${access}`;
        // Reenvia a requisição original com o novo token
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Lide com a falha na atualização do token (deslogue o usuário, redirecione para o login, etc.)
        console.error('Falha ao atualizar token:', refreshError);
        // Pode ser útil limpar os tokens e redirecionar para o login
        // localStorage.removeItem('accessToken');
        // localStorage.removeItem('refreshToken');
        // window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient; // Exporte a instância configurada do Axios
```
**Nota:** Se você estiver usando o cliente gerado pelo OpenAPI TypeScript Generator (que usa Axios internamente) ou RTK Query, a configuração do interceptor precisa ser aplicada à instância do Axios usada por esses clientes, ou você precisará lidar com a lógica de atualização de token dentro da própria configuração do cliente gerado. Para o OpenAPI TypeScript Generator, você pode passar uma instância do Axios configurada para `Configuration`. Para RTK Query, você pode usar `fetchBaseQuery` com `prepareHeaders` e lidar com a lógica de reautenticação.

## Segurança de Tipos

O cliente OpenAPI gerado fornece segurança de tipos completa para:
- Payloads de requisição
- Dados de resposta
- Parâmetros de query
- Parâmetros de path
- Respostas de erro

Exemplo com TypeScript:

```typescript
// Supondo que sua API retorna um objeto Project com esta estrutura
interface Project {
  id: number;
  name: string;
  description: string;
  start_date: string; // Ou Date, dependendo da configuração do gerador
  end_date: string;   // Ou Date
  status: 'PLANNING' | 'IN_PROGRESS' | 'COMPLETED' | 'ON_HOLD'; // Conforme definido no schema
}

// O cliente da API garantirá esses tipos.
// O tipo `Omit<Project, 'id'>` é usado para criar um projeto, pois o 'id' geralmente é gerado pelo backend.
// A estrutura exata de `requestBody` dependerá da configuração do seu schema e do gerador.
const createProject = async (projectData: Omit<Project, 'id'>) => {
  // A chamada exata da API pode variar: api.projectsCreate({ project: projectData }) ou similar
  const response = await api.projectsCreate({ requestBody: projectData }); 
  return response.data; // response.data será do tipo Project (ou o tipo de resposta definido)
};
```

## Melhores Práticas

1.  **Organização do Cliente API**
    *   Mantenha o código da API gerado separado da lógica de negócios.
    *   Crie hooks/composables personalizados para operações comuns da API.
    *   Use interfaces de resposta tipadas (fornecidas pelo gerador).

2.  **Tratamento de Erros**
    *   Implemente tratamento de erros global.
    *   Lide com a atualização de token (refresh token) de forma elegante.
    *   Mostre feedback apropriado ao usuário.

3.  **Gerenciamento de Estado**
    *   Use gerenciamento de estado apropriado (Redux, Pinia, Zustand, Context API, etc.).
    *   Faça cache das respostas da API quando apropriado (RTK Query faz isso automaticamente).
    *   Implemente atualizações otimistas para melhor UX.

4.  **Desempenho**
    *   Use paginação para grandes conjuntos de dados.
    *   Implemente cancelamento de requisições para requisições abandonadas (Axios suporta AbortController).
    *   Faça cache das respostas onde apropriado.

5.  **Segurança**
    *   **Nunca armazene tokens JWT no `localStorage` para aplicações de produção se houver alternativas mais seguras como cookies `HttpOnly`**. `localStorage` é vulnerável a ataques XSS. Se usar `localStorage` por simplicidade em desenvolvimento, esteja ciente dos riscos.
    *   Implemente proteção CSRF adequada se estiver usando autenticação baseada em cookies/sessão. Para JWT em cabeçalhos `Authorization`, CSRF é menos preocupante, mas boas práticas de segurança devem ser sempre consideradas.
    *   Use cookies `HttpOnly` e `Secure` para armazenar tokens quando possível, especialmente o refresh token.

Esta documentação fornece uma base sólida para integrar seu backend Django com aplicações frontend React ou Nuxt. A especificação OpenAPI garante a segurança de tipos e proporciona uma excelente experiência de desenvolvimento através da geração de código.

