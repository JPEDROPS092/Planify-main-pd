# Documentação do Fluxo de Autenticação do Planify

Este documento descreve o fluxo de autenticação completo do Planify, incluindo login, registro, recuperação e redefinição de senha.

## Arquitetura

O sistema de autenticação do Planify é composto por:

1. **Composable `useAuth`**: Gerencia o estado de autenticação e fornece métodos para interagir com a API de autenticação.
2. **Middleware de Autenticação**: Protege rotas e gerencia redirecionamentos.
3. **Sistema de Notificações**: Fornece feedback visual durante operações de autenticação.
4. **Páginas de Autenticação**: Interface para interação do usuário.

## Composable useAuth

Localizado em `~/stores/composables/useAuth.ts`, este composable:

- Gerencia o estado de autenticação (`isAuthenticated`, `user`)
- Fornece métodos para autenticação (`login`, `register`, `logout`, `forgotPassword`, `resetPassword`)
- Gerencia tokens de autenticação
- Verifica permissões do usuário

## Middleware

### auth.ts

Protege rotas que exigem autenticação:

- Verifica se o usuário está autenticado
- Redireciona para `/auth/login` se não estiver
- Preserva a rota original no parâmetro `redirect` para redirecionamento após login

### guest-only.ts

Protege rotas públicas de autenticação:

- Verifica se o usuário está autenticado
- Redireciona para `/dashboard` se estiver
- Aplicado às rotas `/auth/login`, `/auth/registro`, `/auth/esqueci-senha`, `/auth/reset-password`

## Sistema de Notificações

O composable `useNotification` fornece:

- Métodos para exibir notificações (`success`, `error`, `info`, `loading`)
- Método `withLoading` para envolver promessas com notificações automáticas
- Configurações personalizáveis para mensagens e títulos

### Método withLoading

```typescript
const response = await notification.withLoading(
  promiseFunction(),
  {
    loadingMessage: 'Carregando...',
    loadingTitle: 'Título do Loading',
    successMessage: 'Operação concluída com sucesso!',
    errorMessage: 'Ocorreu um erro. Tente novamente.'
  }
);
```

## Páginas de Autenticação

### Login (`/auth/login`)

- Formulário de login com validação
- Usa `withLoading` para feedback visual
- Suporte para redirecionamento após login usando parâmetro `redirect`

### Registro (`/auth/registro`)

- Formulário de registro com validação
- Usa `withLoading` para feedback visual
- Tradução de mensagens de erro da API
- Redirecionamento para login após registro bem-sucedido

### Esqueci Senha (`/auth/esqueci-senha`)

- Formulário para solicitar recuperação de senha
- Usa `withLoading` para feedback visual
- Redirecionamento para login após envio bem-sucedido

### Redefinição de Senha (`/auth/reset-password`)

- Formulário para redefinir senha com token e email da URL
- Usa `withLoading` para feedback visual
- Validação de senhas
- Redirecionamento para login após redefinição bem-sucedida

## Layout

Todas as páginas de autenticação usam o layout `auth.vue`, que fornece:

- Design consistente
- Responsividade
- Suporte para tema claro/escuro

## Fluxo de Autenticação

1. **Login**:
   - Usuário acessa `/auth/login`
   - Preenche credenciais e submete
   - Recebe feedback visual durante o processo
   - É redirecionado para dashboard ou rota original

2. **Registro**:
   - Usuário acessa `/auth/registro`
   - Preenche dados e submete
   - Recebe feedback visual durante o processo
   - É redirecionado para login após sucesso

3. **Recuperação de Senha**:
   - Usuário acessa `/auth/esqueci-senha`
   - Informa email e submete
   - Recebe feedback visual durante o processo
   - É redirecionado para login após sucesso

4. **Redefinição de Senha**:
   - Usuário acessa `/auth/reset-password` com token e email na URL
   - Informa nova senha e submete
   - Recebe feedback visual durante o processo
   - É redirecionado para login após sucesso

## Testes

Um script de teste manual está disponível em `frontend/tests/auth-flow-test.js`. Este script contém um checklist para testar todas as funcionalidades do fluxo de autenticação.

Para executar os testes:

1. Inicie o servidor de desenvolvimento: `cd frontend && npm run dev`
2. Execute o script: `node tests/auth-flow-test.js`
3. Siga os passos de cada teste manualmente

## Boas Práticas

1. **Tratamento de Erros**: Todas as operações de autenticação têm tratamento de erros robusto.
2. **Feedback Visual**: Uso consistente de notificações para feedback.
3. **Validação**: Validação de formulários antes do envio.
4. **Redirecionamento**: Preservação da rota original após login.
5. **Segurança**: Proteção de rotas com middleware.

## Próximos Passos

1. Implementar testes automatizados com Cypress ou Playwright
2. Adicionar autenticação com provedores externos (Google, GitHub)
3. Implementar verificação de email após registro
4. Adicionar proteção contra ataques de força bruta
