# Documentação da API Planify

## Índice

Esta documentação está organizada em várias partes para facilitar a consulta e manutenção:

1. [Parte 1: Autenticação e Usuários](./API_DOCUMENTATION.md)
   - Introdução e Base URL
   - Autenticação JWT
   - Configuração de Interceptors
   - Endpoints de Usuários

2. [Parte 2: Projetos, Sprints, Tarefas e Equipes](./API_DOCUMENTATION_PART2.md)
   - Endpoints de Projetos
   - Endpoints de Sprints
   - Endpoints de Tarefas
   - Endpoints de Equipes

3. [Parte 3: Comunicações, Documentos e Custos](./API_DOCUMENTATION_PART3.md)
   - Configurações de Notificação
   - Mensagens de Chat
   - Notificações
   - Documentos
   - Custos
   - Orçamentos e Alertas

4. [Parte 4: Riscos e Dashboard](./API_DOCUMENTATION_PART4.md)
   - Riscos
   - Estratégias de Mitigação
   - Métricas do Dashboard
   - Gráficos e Visualizações
   - Boas Práticas de Integração

## Como Usar Esta Documentação

Esta documentação fornece:

1. **Interfaces TypeScript** para todos os tipos de dados usados na API
2. **Funções de serviço** para interagir com cada endpoint da API
3. **Exemplos de código** para implementação no frontend
4. **Boas práticas** para tratamento de erros e gerenciamento de estado

Recomendamos que você:

- Use os serviços de API localizados em `/frontend/services/api/` para todas as interações com o backend
- Implemente o interceptor Axios conforme descrito na [Parte 4](./API_DOCUMENTATION_PART4.md) para gerenciar tokens de autenticação
- Utilize os composables para tratamento de erros e estados de loading

## Estrutura de Diretórios da API

Os serviços de API estão organizados da seguinte forma:

```
/frontend/services/api/
  ├── client/
  │   └── apiService.ts       # Serviço base para chamadas à API
  ├── endpoints/              # Endpoints brutos da API
  │   ├── auth.ts
  │   ├── projects.ts
  │   └── ...
  └── services/               # Serviços de alto nível para uso no frontend
      ├── userService.ts
      ├── projectService.ts
      ├── taskService.ts
      └── ...
```

## Atualizações e Manutenção

Esta documentação deve ser mantida atualizada conforme a API evolui. Ao adicionar novos endpoints ou modificar existentes, certifique-se de:

1. Atualizar as interfaces TypeScript correspondentes
2. Adicionar ou modificar as funções de serviço
3. Documentar quaisquer mudanças de comportamento
4. Atualizar exemplos de código quando necessário

## Referências Adicionais

- [Backend API Specification](/backend/Planify_API.MD) - Especificação completa da API no backend
- [Nuxt.js Documentation](https://nuxt.com/docs) - Documentação do Nuxt.js para integração frontend
- [Axios Documentation](https://axios-http.com/docs/intro) - Documentação do Axios para requisições HTTP
