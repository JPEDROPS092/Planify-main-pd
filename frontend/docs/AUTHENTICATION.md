# Sistema de Autenticação Integrado

## Visão Geral

Este sistema integra **Nuxt 3**, **Vue Query (@tanstack/vue-query)** e **Orval** para fornecer uma solução completa de autenticação. O composable `useAuth` encapsula toda a lógica de autenticação e utiliza hooks gerados pelo Orval para comunicação com a API.

## Arquitetura

### 1. **Composable `useAuth`** (`/composables/useAuth.ts`)
- Encapsula toda a lógica de autenticação
- Utiliza hooks do Orval para comunicação com API
- Gerencia estado reativo do usuário
- Trata tokens automaticamente
- Fornece feedback via toast/console

### 2. **Plugin Vue Query** (`/plugins/vue-query.ts`)
- Configura QueryClient global
- Define opções padrão para queries e mutations
- Gerencia cache e retry automático

### 3. **Plugin API Interceptor** (`/plugins/api-interceptor.client.ts`)
- Intercepta requisições HTTP automaticamente
- Adiciona token de autorização
- Trata refresh automático de tokens
- Faz logout em caso de falha de autenticação

## Como Usar

### 1. **Em Componentes de Autenticação**

#### Login
```vue
<script setup>
const { login, isLoggingIn } = useAuth()

const handleLogin = async () => {
  try {
    await login({
      username: 'usuario',
      password: 'senha'
    })
    // Sucesso - usuário redirecionado automaticamente
  } catch (error) {
    // Erro já tratado no composable
  }
}
</script>

<template>
  <form @submit.prevent="handleLogin">
    <!-- campos do formulário -->
    <button :disabled="isLoggingIn" type="submit">
      {{ isLoggingIn ? 'Entrando...' : 'Entrar' }}
    </button>
  </form>
</template>
```

#### Registro
```vue
<script setup>
const { register, isRegistering } = useAuth()

const handleRegister = async () => {
  try {
    await register({
      username: 'novo_usuario',
      email: 'email@exemplo.com',
      first_name: 'Nome',
      last_name: 'Sobrenome',
      password: 'senha',
      role: 'USER'
    })
    // Sucesso - usuário pode fazer login
  } catch (error) {
    // Erro já tratado no composable
  }
}
</script>
```

#### Logout
```vue
<script setup>
const { logout, user } = useAuth()

const handleLogout = async () => {
  await logout()
  // Usuário redirecionado para login automaticamente
}
</script>

<template>
  <div>
    <span>Olá, {{ user?.first_name }}!</span>
    <button @click="handleLogout">Sair</button>
  </div>
</template>
```

### 2. **Em Páginas/Layouts**

#### Verificar Autenticação
```vue
<script setup>
const { user, isAuthenticated, isLoadingUser, checkAuthStatus } = useAuth()

// Verificar status de autenticação ao carregar
onMounted(async () => {
  if (process.client) {
    const isAuth = await checkAuthStatus()
    if (!isAuth) {
      await navigateTo('/login')
    }
  }
})
</script>

<template>
  <div v-if="isLoadingUser">
    Carregando...
  </div>
  <div v-else-if="isAuthenticated">
    <!-- Conteúdo autenticado -->
    <h1>Bem-vindo, {{ user?.first_name }}!</h1>
  </div>
  <div v-else>
    <!-- Usuário não autenticado -->
    <NuxtLink to="/login">Fazer Login</NuxtLink>
  </div>
</template>
```

#### Queries Condicionais
```vue
<script setup>
const { isAuthenticated } = useAuth()

// Só executar query se usuário estiver autenticado
const { data: projects, isLoading } = useQuery({
  queryKey: ['my-projects'],
  queryFn: () => api.getProjects(),
  enabled: isAuthenticated // ← Importante!
})
</script>
```

### 3. **Estado Reativo Disponível**

```vue
<script setup>
const {
  // Estado do usuário
  user,                    // Dados do usuário atual
  isAuthenticated,         // Boolean reativo
  isLoadingUser,          // Loading dos dados do usuário
  userError,              // Erro ao buscar usuário
  
  // Estados de loading
  isLoggingIn,            // Loading do login
  isRegistering,          // Loading do registro
  isRefreshing,           // Loading do refresh token
  
  // Ações
  login,                  // Função de login
  register,               // Função de registro
  logout,                 // Função de logout
  refreshToken,           // Refresh manual do token
  verifyToken,            // Verificar se token é válido
  checkAuthStatus         // Verificar e renovar autenticação
} = useAuth()
</script>
```

## Benefícios da Implementação

### 1. **DRY (Don't Repeat Yourself)**
- Lógica de autenticação centralizada
- Reutilização em qualquer componente
- Evita duplicação de código

### 2. **Type Safety**
- TypeScript completo
- Tipos gerados pelo Orval
- IntelliSense em todos os componentes

### 3. **Estado Reativo**
- Vue Query gerencia cache automaticamente
- Estado sincronizado em toda aplicação
- Updates automáticos quando dados mudam

### 4. **Gestão Automática de Tokens**
- Refresh automático quando token expira
- Logout automático em caso de falha
- Headers de autorização adicionados automaticamente

### 5. **Experiência do Usuário**
- Loading states apropriados
- Feedback visual via toast
- Navegação automática
- Persistência de sessão

## Fluxo de Autenticação

1. **Login**: usuário envia credenciais → API retorna tokens → tokens salvos no localStorage → queries invalidadas → dados do usuário buscados
2. **Navegação**: interceptor adiciona token automaticamente → API responde → se 401, tenta refresh → se falhar, logout
3. **Refresh**: token expira → interceptor detecta 401 → chama refresh → novo token salvo → requisição repetida
4. **Logout**: tokens removidos → cache limpo → redirecionamento para login

## Próximos Passos

1. **Implementar sistema de toast real** (ex: vue-toastification)
2. **Adicionar middleware de rota** para proteção automática
3. **Implementar persistência segura** (httpOnly cookies)
4. **Adicionar testes unitários** para o composable
5. **Configurar refresh automático** baseado em tempo
