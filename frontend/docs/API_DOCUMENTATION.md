# Documentação da API Planify para Frontend

## Introdução

Esta documentação fornece detalhes completos para implementação da API Planify no frontend. Ela contém informações sobre endpoints, parâmetros, payloads e respostas para facilitar a integração com o backend.

**Base URL:** `/api/` (todos os endpoints são relativos a esta base)

## Índice

1. [Autenticação](#autenticação)
2. [Usuários](#usuários)
3. [Projetos](#projetos)
4. [Tarefas](#tarefas)
5. [Equipes](#equipes)
6. [Comunicações](#comunicações)
7. [Documentos](#documentos)
8. [Custos](#custos)
9. [Riscos](#riscos)
10. [Dashboard](#dashboard)

## Autenticação

A API Planify utiliza autenticação JWT (JSON Web Token) para proteger seus endpoints. Aqui está como implementar:

### Obter Token de Acesso

```typescript
// services/api/endpoints/auth.ts
import { useApiService } from '../client/apiService';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface TokenResponse {
  access: string;
  refresh: string;
}

export const login = async (credentials: LoginCredentials): Promise<TokenResponse> => {
  const api = useApiService();
  const response = await api.post<TokenResponse>('/auth/token/', credentials);
  return response.data;
};
```

### Renovar Token

```typescript
// services/api/endpoints/auth.ts
export interface RefreshTokenRequest {
  refresh: string;
}

export interface RefreshTokenResponse {
  access: string;
}

export const refreshToken = async (refreshToken: string): Promise<RefreshTokenResponse> => {
  const api = useApiService();
  const response = await api.post<RefreshTokenResponse>('/auth/token/refresh/', { refresh: refreshToken });
  return response.data;
};
```

### Configuração de Interceptores

Para incluir automaticamente o token de acesso em todas as requisições e lidar com a renovação de tokens expirados:

```typescript
// services/api/client/interceptors.ts
import axios, { AxiosInstance } from 'axios';
import { refreshToken } from '../endpoints/auth';

export const setupInterceptors = (instance: AxiosInstance, getToken: () => string, setToken: (token: string) => void, getRefreshToken: () => string) => {
  // Interceptor de requisição para adicionar o token
  instance.interceptors.request.use(
    (config) => {
      const token = getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Interceptor de resposta para lidar com tokens expirados
  instance.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;
      
      // Se o erro for 401 (Não Autorizado) e não for uma tentativa de refresh
      if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url.includes('auth/token/refresh')) {
        originalRequest._retry = true;
        
        try {
          const refreshTokenValue = getRefreshToken();
          const response = await refreshToken(refreshTokenValue);
          setToken(response.access);
          
          // Atualiza o token na requisição original e tenta novamente
          originalRequest.headers.Authorization = `Bearer ${response.access}`;
          return axios(originalRequest);
        } catch (refreshError) {
          // Se falhar ao renovar o token, redirecionar para login
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
      
      return Promise.reject(error);
    }
  );
};
```

## Usuários

### Obter Usuário Atual

```typescript
// services/api/services/userService.ts
import { useApiService } from '../client/apiService';

export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: 'ADMIN' | 'PROJECT_MANAGER' | 'TEAM_MEMBER';
  is_active: boolean;
  date_joined: string;
  profile: UserProfile;
  access_profiles: UserAccessProfile[];
}

export interface UserProfile {
  avatar: string | null;
  bio: string | null;
  telefone: string | null;
}

export interface UserAccessProfile {
  id: number;
  name: string;
  permissions: string[];
}

export const retrieveAuthUsersMe = async (): Promise<User> => {
  const api = useApiService();
  const response = await api.get<User>('/auth/users/me/');
  return response.data;
};
```

### Listar Usuários

```typescript
// services/api/services/userService.ts
export interface UserListParams {
  page?: number;
  search?: string;
  ordering?: string;
}

export interface PaginatedUserList {
  count: number;
  next: string | null;
  previous: string | null;
  results: User[];
}

export const listUsers = async (params: UserListParams = {}): Promise<PaginatedUserList> => {
  const api = useApiService();
  const response = await api.get<PaginatedUserList>('/auth/users/', { params });
  return response.data;
};
```

### Atualizar Usuário

```typescript
// services/api/services/userService.ts
export interface UpdateUserRequest {
  username?: string;
  email?: string;
  full_name?: string;
}

export const updateCurrentUser = async (userData: UpdateUserRequest): Promise<User> => {
  const api = useApiService();
  const response = await api.patch<User>('/auth/users/me/', userData);
  return response.data;
};
```

### Redefinir Senha

```typescript
// services/api/services/userService.ts
export interface ResetPasswordRequest {
  email: string;
}

export const resetPassword = async (data: ResetPasswordRequest): Promise<void> => {
  const api = useApiService();
  await api.post('/auth/users/reset_password/', data);
};

export interface SetNewPasswordRequest {
  uid: string;
  token: string;
  new_password: string;
  re_new_password: string;
}

export const confirmResetPassword = async (data: SetNewPasswordRequest): Promise<void> => {
  const api = useApiService();
  await api.post('/auth/users/reset_password_confirm/', data);
};
```
