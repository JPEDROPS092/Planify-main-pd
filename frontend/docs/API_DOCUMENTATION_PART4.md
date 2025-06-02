## Riscos

### Listar Riscos

```typescript
// services/api/services/riskService.ts
import { useApiService } from '../client/apiService';

export interface Risco {
  id: number;
  titulo: string;
  descricao: string;
  projeto: number;
  probabilidade: 'BAIXA' | 'MEDIA' | 'ALTA';
  impacto: 'BAIXO' | 'MEDIO' | 'ALTO';
  status: 'IDENTIFICADO' | 'ANALISADO' | 'MITIGADO' | 'MONITORADO' | 'FECHADO';
  data_identificacao: string;
  data_atualizacao: string;
  criado_por: number;
  responsavel: number | null;
}

export interface RiscoListParams {
  page?: number;
  search?: string;
  projeto?: number;
  probabilidade?: 'BAIXA' | 'MEDIA' | 'ALTA';
  impacto?: 'BAIXO' | 'MEDIO' | 'ALTO';
  status?: 'IDENTIFICADO' | 'ANALISADO' | 'MITIGADO' | 'MONITORADO' | 'FECHADO';
  criado_por?: number;
  responsavel?: number;
  ordering?: string;
}

export interface PaginatedRiscoList {
  count: number;
  next: string | null;
  previous: string | null;
  results: Risco[];
}

export const listRiscos = async (params: RiscoListParams = {}): Promise<PaginatedRiscoList> => {
  const api = useApiService();
  const response = await api.get<PaginatedRiscoList>('/risks/riscos/', { params });
  return response.data;
};
```

### Obter Risco por ID

```typescript
// services/api/services/riskService.ts
export const getRisco = async (id: number): Promise<Risco> => {
  const api = useApiService();
  const response = await api.get<Risco>(`/risks/riscos/${id}/`);
  return response.data;
};
```

### Criar Risco

```typescript
// services/api/services/riskService.ts
export interface CreateRiscoRequest {
  titulo: string;
  descricao: string;
  projeto: number;
  probabilidade: 'BAIXA' | 'MEDIA' | 'ALTA';
  impacto: 'BAIXO' | 'MEDIO' | 'ALTO';
  status: 'IDENTIFICADO' | 'ANALISADO' | 'MITIGADO' | 'MONITORADO' | 'FECHADO';
  responsavel?: number | null;
}

export const createRisco = async (risco: CreateRiscoRequest): Promise<Risco> => {
  const api = useApiService();
  const response = await api.post<Risco>('/risks/riscos/', risco);
  return response.data;
};
```

### Atualizar Risco

```typescript
// services/api/services/riskService.ts
export interface UpdateRiscoRequest {
  titulo?: string;
  descricao?: string;
  probabilidade?: 'BAIXA' | 'MEDIA' | 'ALTA';
  impacto?: 'BAIXO' | 'MEDIO' | 'ALTO';
  status?: 'IDENTIFICADO' | 'ANALISADO' | 'MITIGADO' | 'MONITORADO' | 'FECHADO';
  responsavel?: number | null;
}

export const updateRisco = async (id: number, risco: UpdateRiscoRequest): Promise<Risco> => {
  const api = useApiService();
  const response = await api.patch<Risco>(`/risks/riscos/${id}/`, risco);
  return response.data;
};
```

### Excluir Risco

```typescript
// services/api/services/riskService.ts
export const deleteRisco = async (id: number): Promise<void> => {
  const api = useApiService();
  await api.delete(`/risks/riscos/${id}/`);
};
```

### Estratégias de Mitigação

```typescript
// services/api/services/riskService.ts
export interface EstrategiaMitigacao {
  id: number;
  risco: number;
  descricao: string;
  status: 'PLANEJADA' | 'EM_ANDAMENTO' | 'CONCLUIDA' | 'CANCELADA';
  data_criacao: string;
  data_atualizacao: string;
  criado_por: number;
  responsavel: number | null;
}

export interface EstrategiaMitigacaoListParams {
  page?: number;
  risco?: number;
  status?: 'PLANEJADA' | 'EM_ANDAMENTO' | 'CONCLUIDA' | 'CANCELADA';
  responsavel?: number;
  ordering?: string;
}

export interface PaginatedEstrategiaMitigacaoList {
  count: number;
  next: string | null;
  previous: string | null;
  results: EstrategiaMitigacao[];
}

export const listEstrategiasMitigacao = async (params: EstrategiaMitigacaoListParams = {}): Promise<PaginatedEstrategiaMitigacaoList> => {
  const api = useApiService();
  const response = await api.get<PaginatedEstrategiaMitigacaoList>('/risks/estrategias-mitigacao/', { params });
  return response.data;
};

export interface CreateEstrategiaMitigacaoRequest {
  risco: number;
  descricao: string;
  status: 'PLANEJADA' | 'EM_ANDAMENTO' | 'CONCLUIDA' | 'CANCELADA';
  responsavel?: number | null;
}

export const createEstrategiaMitigacao = async (estrategia: CreateEstrategiaMitigacaoRequest): Promise<EstrategiaMitigacao> => {
  const api = useApiService();
  const response = await api.post<EstrategiaMitigacao>('/risks/estrategias-mitigacao/', estrategia);
  return response.data;
};

export interface UpdateEstrategiaMitigacaoRequest {
  descricao?: string;
  status?: 'PLANEJADA' | 'EM_ANDAMENTO' | 'CONCLUIDA' | 'CANCELADA';
  responsavel?: number | null;
}

export const updateEstrategiaMitigacao = async (id: number, estrategia: UpdateEstrategiaMitigacaoRequest): Promise<EstrategiaMitigacao> => {
  const api = useApiService();
  const response = await api.patch<EstrategiaMitigacao>(`/risks/estrategias-mitigacao/${id}/`, estrategia);
  return response.data;
};

export const deleteEstrategiaMitigacao = async (id: number): Promise<void> => {
  const api = useApiService();
  await api.delete(`/risks/estrategias-mitigacao/${id}/`);
};
```

### Histórico de Riscos

```typescript
// services/api/services/riskService.ts
export interface HistoricoRisco {
  id: number;
  risco: number;
  alterado_por: number;
  data_alteracao: string;
  tipo_alteracao: 'CRIACAO' | 'ATUALIZACAO' | 'EXCLUSAO';
  detalhes: string;
}

export interface HistoricoRiscoListParams {
  page?: number;
  risco?: number;
  alterado_por?: number;
}

export interface PaginatedHistoricoRiscoList {
  count: number;
  next: string | null;
  previous: string | null;
  results: HistoricoRisco[];
}

export const listHistoricoRisco = async (params: HistoricoRiscoListParams = {}): Promise<PaginatedHistoricoRiscoList> => {
  const api = useApiService();
  const response = await api.get<PaginatedHistoricoRiscoList>('/risks/historico/', { params });
  return response.data;
};

export const getHistoricoRisco = async (riscoId: number): Promise<HistoricoRisco[]> => {
  const api = useApiService();
  const response = await api.get<HistoricoRisco[]>(`/risks/riscos/${riscoId}/historico/`);
  return response.data;
};
```

### Matriz de Riscos

```typescript
// services/api/services/riskService.ts
export interface MatrizRisco {
  baixo_baixa: number;
  baixo_media: number;
  baixo_alta: number;
  medio_baixa: number;
  medio_media: number;
  medio_alta: number;
  alto_baixa: number;
  alto_media: number;
  alto_alta: number;
}

export const getMatrizRiscos = async (projetoId: number): Promise<MatrizRisco> => {
  const api = useApiService();
  const response = await api.get<MatrizRisco>(`/risks/matriz-riscos/${projetoId}/`);
  return response.data;
};
```

## Dashboard

### Métricas Gerais

```typescript
// services/api/services/dashboardService.ts
import { useApiService } from '../client/apiService';

export interface MetricasGerais {
  total_projetos: number;
  projetos_ativos: number;
  projetos_concluidos: number;
  projetos_atrasados: number;
  total_tarefas: number;
  tarefas_pendentes: number;
  tarefas_em_andamento: number;
  tarefas_concluidas: number;
  tarefas_atrasadas: number;
}

export const getMetricasGerais = async (): Promise<MetricasGerais> => {
  const api = useApiService();
  const response = await api.get<MetricasGerais>('/dashboard/metricas-gerais/');
  return response.data;
};
```

### Métricas de Projeto

```typescript
// services/api/services/dashboardService.ts
export interface MetricasProjeto {
  total_tarefas: number;
  tarefas_pendentes: number;
  tarefas_em_andamento: number;
  tarefas_concluidas: number;
  tarefas_atrasadas: number;
  porcentagem_concluido: number;
  dias_restantes: number;
  total_riscos: number;
  riscos_ativos: number;
  custo_total: number;
  orcamento_total: number;
  porcentagem_orcamento_utilizado: number;
}

export const getMetricasProjeto = async (projetoId: number): Promise<MetricasProjeto> => {
  const api = useApiService();
  const response = await api.get<MetricasProjeto>(`/dashboard/metricas-projeto/${projetoId}/`);
  return response.data;
};
```

### Gráfico de Burndown

```typescript
// services/api/services/dashboardService.ts
export interface PontoBurndown {
  data: string;
  tarefas_restantes: number;
  tarefas_ideais: number;
}

export interface GraficoBurndown {
  sprint: number;
  titulo_sprint: string;
  data_inicio: string;
  data_fim: string;
  pontos: PontoBurndown[];
}

export const getGraficoBurndown = async (sprintId: number): Promise<GraficoBurndown> => {
  const api = useApiService();
  const response = await api.get<GraficoBurndown>(`/dashboard/grafico-burndown/${sprintId}/`);
  return response.data;
};
```

### Gráfico de Velocidade

```typescript
// services/api/services/dashboardService.ts
export interface PontoVelocidade {
  sprint: number;
  titulo_sprint: string;
  pontos_planejados: number;
  pontos_concluidos: number;
}

export interface GraficoVelocidade {
  projeto: number;
  titulo_projeto: string;
  pontos: PontoVelocidade[];
}

export const getGraficoVelocidade = async (projetoId: number): Promise<GraficoVelocidade> => {
  const api = useApiService();
  const response = await api.get<GraficoVelocidade>(`/dashboard/grafico-velocidade/${projetoId}/`);
  return response.data;
};
```

### Distribuição de Tarefas

```typescript
// services/api/services/dashboardService.ts
export interface DistribuicaoTarefas {
  pendentes: number;
  em_andamento: number;
  concluidas: number;
  bloqueadas: number;
  atrasadas: number;
}

export const getDistribuicaoTarefas = async (projetoId?: number): Promise<DistribuicaoTarefas> => {
  const api = useApiService();
  const params = projetoId ? { projeto: projetoId } : {};
  const response = await api.get<DistribuicaoTarefas>('/dashboard/distribuicao-tarefas/', { params });
  return response.data;
};
```

### Distribuição de Custos

```typescript
// services/api/services/dashboardService.ts
export interface CategoriaCustoDistribuicao {
  categoria: string;
  valor: number;
  porcentagem: number;
}

export interface DistribuicaoCustos {
  projeto: number;
  titulo_projeto: string;
  custo_total: number;
  categorias: CategoriaCustoDistribuicao[];
}

export const getDistribuicaoCustos = async (projetoId: number): Promise<DistribuicaoCustos> => {
  const api = useApiService();
  const response = await api.get<DistribuicaoCustos>(`/dashboard/distribuicao-custos/${projetoId}/`);
  return response.data;
};
```

### Calendário de Tarefas

```typescript
// services/api/services/dashboardService.ts
export interface EventoCalendario {
  id: number;
  titulo: string;
  data_inicio: string;
  data_fim: string;
  tipo: 'TAREFA' | 'SPRINT' | 'PROJETO';
  status: string;
  projeto: number;
  projeto_titulo: string;
  cor: string;
}

export interface CalendarioTarefas {
  eventos: EventoCalendario[];
}

export interface CalendarioParams {
  data_inicio?: string;
  data_fim?: string;
  projeto?: number;
  usuario?: number;
}

export const getCalendarioTarefas = async (params: CalendarioParams = {}): Promise<CalendarioTarefas> => {
  const api = useApiService();
  const response = await api.get<CalendarioTarefas>('/dashboard/calendario-tarefas/', { params });
  return response.data;
};
```

### Atividades Recentes

```typescript
// services/api/services/dashboardService.ts
export interface AtividadeRecente {
  id: number;
  tipo: 'PROJETO' | 'TAREFA' | 'SPRINT' | 'DOCUMENTO' | 'RISCO' | 'CUSTO';
  acao: 'CRIACAO' | 'ATUALIZACAO' | 'EXCLUSAO' | 'COMENTARIO';
  descricao: string;
  usuario: number;
  usuario_nome: string;
  projeto: number | null;
  projeto_titulo: string | null;
  data: string;
}

export interface AtividadesRecentesParams {
  page?: number;
  projeto?: number;
  usuario?: number;
  tipo?: 'PROJETO' | 'TAREFA' | 'SPRINT' | 'DOCUMENTO' | 'RISCO' | 'CUSTO';
  acao?: 'CRIACAO' | 'ATUALIZACAO' | 'EXCLUSAO' | 'COMENTARIO';
}

export interface PaginatedAtividadesRecentesList {
  count: number;
  next: string | null;
  previous: string | null;
  results: AtividadeRecente[];
}

export const getAtividadesRecentes = async (params: AtividadesRecentesParams = {}): Promise<PaginatedAtividadesRecentesList> => {
  const api = useApiService();
  const response = await api.get<PaginatedAtividadesRecentesList>('/dashboard/atividades-recentes/', { params });
  return response.data;
};
```

## Integração com o Frontend

### Configuração do Interceptor Axios

Para garantir que todas as requisições à API incluam o token de autenticação e lidem com erros de forma consistente, configure um interceptor Axios no seu frontend:

```typescript
// plugins/axios.ts
import axios from 'axios';
import { useAuth } from '~/stores/composables/useAuth';

export default defineNuxtPlugin(async (nuxtApp) => {
  const auth = useAuth();
  const config = useRuntimeConfig();
  
  const api = axios.create({
    baseURL: config.public.apiBaseUrl || '/api',
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  // Interceptor de requisição para adicionar token de autenticação
  api.interceptors.request.use(
    (config) => {
      const token = auth.getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
  
  // Interceptor de resposta para lidar com erros e renovação de token
  api.interceptors.response.use(
    (response) => {
      return response;
    },
    async (error) => {
      const originalRequest = error.config;
      
      // Se o erro for 401 (Não autorizado) e não for uma tentativa de renovação de token
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        
        try {
          // Tentar renovar o token
          await auth.refreshToken();
          
          // Atualizar o token na requisição original
          const token = auth.getToken();
          if (token) {
            originalRequest.headers.Authorization = `Bearer ${token}`;
          }
          
          // Reenviar a requisição original
          return api(originalRequest);
        } catch (refreshError) {
          // Se a renovação falhar, fazer logout
          auth.logout();
          return Promise.reject(refreshError);
        }
      }
      
      return Promise.reject(error);
    }
  );
  
  // Disponibilizar a instância axios para o aplicativo
  nuxtApp.provide('api', api);
});
```

### Exemplo de Uso em Componente Vue

Exemplo de como usar os serviços de API em um componente Vue:

```vue
<template>
  <div>
    <h1>Projetos</h1>
    <div v-if="loading">Carregando...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <ul>
        <li v-for="projeto in projetos" :key="projeto.id">
          {{ projeto.titulo }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { listProjetos } from '~/services/api/services/projectService';

const projetos = ref([]);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    const response = await listProjetos();
    projetos.value = response.results;
  } catch (err) {
    error.value = 'Erro ao carregar projetos. Por favor, tente novamente.';
    console.error(err);
  } finally {
    loading.value = false;
  }
});
</script>
```

## Boas Práticas

### Tratamento de Erros

Implemente um tratamento de erros consistente em toda a aplicação:

```typescript
// composables/useApiError.ts
import { ref } from 'vue';
import { AxiosError } from 'axios';

export function useApiError() {
  const error = ref<string | null>(null);
  const validationErrors = ref<Record<string, string[]>>({});
  
  const handleError = (err: unknown) => {
    if (err instanceof AxiosError) {
      if (err.response) {
        // Erro de resposta da API
        const status = err.response.status;
        const data = err.response.data;
        
        if (status === 400 && typeof data === 'object') {
          // Erros de validação
          validationErrors.value = data;
          error.value = 'Por favor, corrija os erros no formulário.';
        } else if (status === 401) {
          error.value = 'Sessão expirada. Por favor, faça login novamente.';
        } else if (status === 403) {
          error.value = 'Você não tem permissão para realizar esta ação.';
        } else if (status === 404) {
          error.value = 'Recurso não encontrado.';
        } else if (status === 500) {
          error.value = 'Erro no servidor. Por favor, tente novamente mais tarde.';
        } else {
          error.value = data.detail || 'Ocorreu um erro. Por favor, tente novamente.';
        }
      } else if (err.request) {
        // Sem resposta do servidor
        error.value = 'Não foi possível conectar ao servidor. Verifique sua conexão.';
      } else {
        // Erro na configuração da requisição
        error.value = 'Erro ao configurar a requisição.';
      }
    } else {
      // Erro genérico
      error.value = 'Ocorreu um erro inesperado.';
    }
    
    console.error('API Error:', err);
  };
  
  const clearErrors = () => {
    error.value = null;
    validationErrors.value = {};
  };
  
  const getFieldError = (field: string): string | null => {
    return validationErrors.value[field]?.[0] || null;
  };
  
  return {
    error,
    validationErrors,
    handleError,
    clearErrors,
    getFieldError
  };
}
```

### Composable para Loading

Crie um composable para gerenciar estados de loading:

```typescript
// composables/useLoading.ts
import { ref } from 'vue';

export function useLoading() {
  const isLoading = ref(false);
  
  const withLoading = async <T>(fn: () => Promise<T>): Promise<T> => {
    isLoading.value = true;
    try {
      return await fn();
    } finally {
      isLoading.value = false;
    }
  };
  
  return {
    isLoading,
    withLoading
  };
}
```

### Paginação

Implemente um composable para gerenciar paginação:

```typescript
// composables/usePagination.ts
import { ref, computed } from 'vue';

export function usePagination<T>(
  fetchFn: (page: number) => Promise<{ count: number; results: T[] }>,
  itemsPerPage = 10
) {
  const currentPage = ref(1);
  const totalItems = ref(0);
  const items = ref<T[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  
  const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage));
  
  const fetchPage = async (page: number) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await fetchFn(page);
      items.value = response.results;
      totalItems.value = response.count;
      currentPage.value = page;
    } catch (err) {
      error.value = 'Erro ao carregar dados. Por favor, tente novamente.';
      console.error(err);
    } finally {
      loading.value = false;
    }
  };
  
  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      fetchPage(currentPage.value + 1);
    }
  };
  
  const prevPage = () => {
    if (currentPage.value > 1) {
      fetchPage(currentPage.value - 1);
    }
  };
  
  const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
      fetchPage(page);
    }
  };
  
  // Carregar a primeira página inicialmente
  fetchPage(1);
  
  return {
    currentPage,
    totalItems,
    totalPages,
    items,
    loading,
    error,
    nextPage,
    prevPage,
    goToPage,
    refresh: () => fetchPage(currentPage.value)
  };
}
```

## Conclusão

Esta documentação fornece uma visão completa da API Planify, incluindo todos os endpoints disponíveis, estruturas de dados, exemplos de código TypeScript para integração com o frontend, e boas práticas para implementação.

Para implementar a integração com a API no frontend:

1. Configure o interceptor Axios para gerenciar tokens de autenticação
2. Utilize os serviços de API para cada módulo do sistema
3. Implemente tratamento de erros consistente
4. Utilize composables para gerenciar estados de loading e paginação
5. Mantenha a tipagem TypeScript para garantir segurança de tipos

Seguindo estas diretrizes, você terá uma integração robusta e eficiente entre o frontend e a API backend do Planify.
