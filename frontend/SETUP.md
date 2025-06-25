# Planify - Sistema de Gerenciamento de Projetos

Este é um projeto de frontend para o Planify, um sistema completo de gerenciamento de projetos. O frontend foi desenvolvido com Nuxt.js e TanStack Query para consumir a API RESTful do backend.

## Tecnologias Utilizadas

- **Nuxt.js**: Framework Vue.js para desenvolvimento de aplicações web
- **TanStack Query**: Biblioteca para gerenciamento de estado e cache de requisições
- **Axios**: Cliente HTTP para realizar requisições à API
- **Tailwind CSS**: Framework CSS para estilização
- **Shadcn UI**: Componentes estilizados com Tailwind
- **Iconify**: Biblioteca de ícones

## Estrutura do Projeto

```
├── components/          # Componentes reutilizáveis
├── composables/         # Composables Vue (hooks)
├── layouts/             # Layouts da aplicação
│   ├── default.vue      # Layout padrão com sidebar
│   └── auth.vue         # Layout para páginas de autenticação
├── pages/               # Páginas da aplicação
│   ├── index.vue        # Dashboard principal
│   ├── login.vue        # Página de login
│   ├── projects/        # Páginas relacionadas a projetos
│   └── ...              # Outras páginas
├── plugins/             # Plugins do Nuxt
│   └── vue-query.ts     # Configuração do TanStack Query
├── services/            # Serviços para comunicação com a API
│   ├── authService.ts   # Serviço de autenticação
│   ├── projectService.ts# Serviço de projetos
│   └── ...              # Outros serviços
├── types/               # Definições de tipos TypeScript
│   └── api.ts           # Tipos gerados a partir do schema OpenAPI
├── app.vue              # Componente raiz
├── nuxt.config.ts       # Configuração do Nuxt
└── package.json         # Dependências e scripts
```

## Início Rápido

1. Instale as dependências:

```bash
npm install
```

2. Configure o arquivo `.env` na raiz do projeto:

```
API_BASE_URL=http://localhost:8000/api/
```

3. Gere os tipos TypeScript a partir do schema OpenAPI:

```bash
npm run generate-api-types
```

4. Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

## Recursos Implementados

- ✅ Autenticação (login/logout) com JWT
- ✅ Refresh automático de tokens
- ✅ Dashboard com visão geral dos projetos
- ✅ Gerenciamento de projetos (CRUD)
- ✅ Interface responsiva com Tailwind CSS
- ✅ Componentes reutilizáveis com Shadcn UI
- ✅ Ícones com Iconify

## Integração com TanStack Query

O projeto utiliza TanStack Query para gerenciar o estado e cache das requisições à API. Principais benefícios:

- Gerenciamento automático de cache
- Revalidação de dados
- Estados de carregamento e erro
- Updates otimistas
- Paginação
- Suporte para SSR

## Autenticação

O sistema utiliza JWT para autenticação:

1. O usuário faz login e recebe tokens de acesso e refresh
2. O token de acesso é armazenado no localStorage e usado em todas as requisições
3. Quando o token expira, o sistema tenta obter um novo usando o refresh token
4. Se o refresh falhar, o usuário é redirecionado para a página de login

## Rotas Principais

- `/`: Dashboard principal
- `/login`: Tela de login
- `/projects`: Lista de projetos
- `/projects/:id`: Detalhes do projeto
- `/projects/:id/kanban`: Visualização Kanban do projeto
- `/projects/:id/gantt`: Visualização Gantt do projeto

## Scripts

- `npm run dev`: Inicia o servidor de desenvolvimento
- `npm run build`: Gera a versão de produção
- `npm run generate`: Gera o site estático
- `npm run generate-api-types`: Gera tipos TypeScript a partir do schema OpenAPI
