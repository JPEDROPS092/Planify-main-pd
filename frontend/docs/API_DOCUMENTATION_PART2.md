## Projetos

### Listar Projetos

```typescript
// services/api/services/projectService.ts
import { useApiService } from '../client/apiService';

export interface Projeto {
  id: number;
  titulo: string;
  descricao: string;
  data_inicio: string;
  data_fim: string;
  status: 'PLANEJADO' | 'EM_ANDAMENTO' | 'PAUSADO' | 'CONCLUIDO' | 'CANCELADO';
  status_display: string;
  prioridade: 'BAIXA' | 'MEDIA' | 'ALTA';
  prioridade_display: string;
  criado_por: number | null;
  criado_em: string;
  atualizado_em: string;
  arquivado: boolean;
  membros: MembroProjeto[];
  sprints_count: string;
  tasks_count: string;
  progresso: string;
}

export interface MembroProjeto {
  id: number;
  usuario: number;
  papel: string;
  projeto: number;
  data_adicao: string;
}

export interface ProjetoListParams {
  page?: number;
  search?: string;
  ordering?: string;
  status?: 'PLANEJADO' | 'EM_ANDAMENTO' | 'PAUSADO' | 'CONCLUIDO' | 'CANCELADO';
  prioridade?: 'BAIXA' | 'MEDIA' | 'ALTA';
  arquivado?: boolean;
}

export interface PaginatedProjetoList {
  count: number;
  next: string | null;
  previous: string | null;
  results: Projeto[];
}

export const listProjetos = async (params: ProjetoListParams = {}): Promise<PaginatedProjetoList> => {
  const api = useApiService();
  const response = await api.get<PaginatedProjetoList>('/projects/projetos/', { params });
  return response.data;
};
```

### Obter Projeto por ID

```typescript
// services/api/services/projectService.ts
export const getProjeto = async (id: number): Promise<Projeto> => {
  const api = useApiService();
  const response = await api.get<Projeto>(`/projects/projetos/${id}/`);
  return response.data;
};
```

### Criar Projeto

```typescript
// services/api/services/projectService.ts
export interface CreateProjetoRequest {
  titulo: string;
  descricao: string;
  data_inicio: string;
  data_fim: string;
  status: 'PLANEJADO' | 'EM_ANDAMENTO' | 'PAUSADO' | 'CONCLUIDO' | 'CANCELADO';
  prioridade: 'BAIXA' | 'MEDIA' | 'ALTA';
}

export const createProjeto = async (projeto: CreateProjetoRequest): Promise<Projeto> => {
  const api = useApiService();
  const response = await api.post<Projeto>('/projects/projetos/', projeto);
  return response.data;
};
```

### Atualizar Projeto

```typescript
// services/api/services/projectService.ts
export interface UpdateProjetoRequest {
  titulo?: string;
  descricao?: string;
  data_inicio?: string;
  data_fim?: string;
  status?: 'PLANEJADO' | 'EM_ANDAMENTO' | 'PAUSADO' | 'CONCLUIDO' | 'CANCELADO';
  prioridade?: 'BAIXA' | 'MEDIA' | 'ALTA';
}

export const updateProjeto = async (id: number, projeto: UpdateProjetoRequest): Promise<Projeto> => {
  const api = useApiService();
  const response = await api.patch<Projeto>(`/projects/projetos/${id}/`, projeto);
  return response.data;
};
```

### Excluir Projeto

```typescript
// services/api/services/projectService.ts
export const deleteProjeto = async (id: number): Promise<void> => {
  const api = useApiService();
  await api.delete(`/projects/projetos/${id}/`);
};
```

### Gerenciar Membros do Projeto

```typescript
// services/api/services/projectService.ts
export interface AddMembroRequest {
  usuario: number;
  papel: string;
}

export const addMembro = async (projetoId: number, membro: AddMembroRequest): Promise<Projeto> => {
  const api = useApiService();
  const response = await api.post<Projeto>(`/projects/projetos/${projetoId}/add_member/`, membro);
  return response.data;
};

export const removeMembro = async (projetoId: number, usuarioId: number): Promise<Projeto> => {
  const api = useApiService();
  const response = await api.post<Projeto>(`/projects/projetos/${projetoId}/remove_member/`, { usuario: usuarioId });
  return response.data;
};

export const getMembrosProjeto = async (projetoId: number): Promise<MembroProjeto[]> => {
  const api = useApiService();
  const response = await api.get<MembroProjeto[]>(`/projects/projetos/${projetoId}/membros/`);
  return response.data;
};
```

### Arquivar/Desarquivar Projeto

```typescript
// services/api/services/projectService.ts
export const arquivarProjeto = async (projetoId: number, arquivar: boolean): Promise<Projeto> => {
  const api = useApiService();
  const response = await api.post<Projeto>(`/projects/projetos/${projetoId}/archive/`, { arquivado: arquivar });
  return response.data;
};
```

### Obter Métricas do Projeto

```typescript
// services/api/services/projectService.ts
export interface ProjetoMetricas {
  tarefas_por_status: Record<string, number>;
  progresso_geral: number;
  // Outros campos conforme a resposta da API
}

export const getProjetoMetricas = async (projetoId: number): Promise<ProjetoMetricas> => {
  const api = useApiService();
  const response = await api.get<ProjetoMetricas>(`/projetos/${projetoId}/metricas/`);
  return response.data;
};
```

### Sprints

```typescript
// services/api/services/sprintService.ts
import { useApiService } from '../client/apiService';

export interface Sprint {
  id: number;
  nome: string;
  descricao: string;
  projeto: number;
  data_inicio: string;
  data_fim: string;
  status: 'PLANEJADO' | 'EM_ANDAMENTO' | 'CONCLUIDO';
  criado_por: number;
  criado_em: string;
  atualizado_em: string;
}

export interface SprintListParams {
  page?: number;
  search?: string;
  ordering?: string;
  projeto?: number;
  status?: 'PLANEJADO' | 'EM_ANDAMENTO' | 'CONCLUIDO';
}

export interface PaginatedSprintList {
  count: number;
  next: string | null;
  previous: string | null;
  results: Sprint[];
}

export const listSprints = async (params: SprintListParams = {}): Promise<PaginatedSprintList> => {
  const api = useApiService();
  const response = await api.get<PaginatedSprintList>('/projects/sprints/', { params });
  return response.data;
};

export const getSprint = async (id: number): Promise<Sprint> => {
  const api = useApiService();
  const response = await api.get<Sprint>(`/projects/sprints/${id}/`);
  return response.data;
};

export interface CreateSprintRequest {
  nome: string;
  descricao: string;
  projeto: number;
  data_inicio: string;
  data_fim: string;
  status: 'PLANEJADO' | 'EM_ANDAMENTO' | 'CONCLUIDO';
}

export const createSprint = async (sprint: CreateSprintRequest): Promise<Sprint> => {
  const api = useApiService();
  const response = await api.post<Sprint>('/projects/sprints/', sprint);
  return response.data;
};

export interface UpdateSprintRequest {
  nome?: string;
  descricao?: string;
  data_inicio?: string;
  data_fim?: string;
  status?: 'PLANEJADO' | 'EM_ANDAMENTO' | 'CONCLUIDO';
}

export const updateSprint = async (id: number, sprint: UpdateSprintRequest): Promise<Sprint> => {
  const api = useApiService();
  const response = await api.patch<Sprint>(`/projects/sprints/${id}/`, sprint);
  return response.data;
};

export const deleteSprint = async (id: number): Promise<void> => {
  const api = useApiService();
  await api.delete(`/projects/sprints/${id}/`);
};

export const getSprintTasks = async (sprintId: number): Promise<Tarefa[]> => {
  const api = useApiService();
  const response = await api.get<Tarefa[]>(`/projects/sprints/${sprintId}/tasks/`);
  return response.data;
};
```

## Tarefas

### Listar Tarefas

```typescript
// services/api/services/taskService.ts
import { useApiService } from '../client/apiService';

export interface Tarefa {
  id: number;
  titulo: string;
  descricao: string;
  projeto: number;
  sprint: number | null;
  data_inicio: string;
  data_termino: string;
  prioridade: 'BAIXA' | 'MEDIA' | 'ALTA';
  status: 'A_FAZER' | 'EM_ANDAMENTO' | 'FEITO';
  criado_por: User;
  criado_em: string;
  atualizado_em: string;
  atribuicoes: AtribuicaoTarefa[];
}

export interface AtribuicaoTarefa {
  id: number;
  usuario: number;
  tarefa: number;
  data_atribuicao: string;
}

export interface TarefaListParams {
  page?: number;
  search?: string;
  ordering?: string;
  projeto?: number;
  sprint?: number;
  status?: 'A_FAZER' | 'EM_ANDAMENTO' | 'FEITO';
  prioridade?: 'BAIXA' | 'MEDIA' | 'ALTA';
}

export interface PaginatedTarefaList {
  count: number;
  next: string | null;
  previous: string | null;
  results: Tarefa[];
}

export const listTarefas = async (params: TarefaListParams = {}): Promise<PaginatedTarefaList> => {
  const api = useApiService();
  const response = await api.get<PaginatedTarefaList>('/tasks/tarefas/', { params });
  return response.data;
};
```

### Obter Tarefa por ID

```typescript
// services/api/services/taskService.ts
export const getTarefa = async (id: number): Promise<Tarefa> => {
  const api = useApiService();
  const response = await api.get<Tarefa>(`/tasks/tarefas/${id}/`);
  return response.data;
};
```

### Criar Tarefa

```typescript
// services/api/services/taskService.ts
export interface CreateTarefaRequest {
  titulo: string;
  descricao: string;
  projeto: number;
  sprint?: number | null;
  data_inicio: string;
  data_termino: string;
  prioridade: 'BAIXA' | 'MEDIA' | 'ALTA';
  status: 'A_FAZER' | 'EM_ANDAMENTO' | 'FEITO';
}

export const createTarefa = async (tarefa: CreateTarefaRequest): Promise<Tarefa> => {
  const api = useApiService();
  const response = await api.post<Tarefa>('/tasks/tarefas/', tarefa);
  return response.data;
};
```

### Atualizar Tarefa

```typescript
// services/api/services/taskService.ts
export interface UpdateTarefaRequest {
  titulo?: string;
  descricao?: string;
  sprint?: number | null;
  data_inicio?: string;
  data_termino?: string;
  prioridade?: 'BAIXA' | 'MEDIA' | 'ALTA';
  status?: 'A_FAZER' | 'EM_ANDAMENTO' | 'FEITO';
}

export const updateTarefa = async (id: number, tarefa: UpdateTarefaRequest): Promise<Tarefa> => {
  const api = useApiService();
  const response = await api.patch<Tarefa>(`/tasks/tarefas/${id}/`, tarefa);
  return response.data;
};
```

### Excluir Tarefa

```typescript
// services/api/services/taskService.ts
export const deleteTarefa = async (id: number): Promise<void> => {
  const api = useApiService();
  await api.delete(`/tasks/tarefas/${id}/`);
};
```

### Gerenciar Responsáveis

```typescript
// services/api/services/taskService.ts
export const atribuirResponsavel = async (tarefaId: number, usuarioId: number): Promise<Tarefa> => {
  const api = useApiService();
  const response = await api.post<Tarefa>(`/tasks/tarefas/${tarefaId}/atribuir_responsavel/`, { usuario: usuarioId });
  return response.data;
};

export const removerResponsavel = async (tarefaId: number, usuarioId: number): Promise<Tarefa> => {
  const api = useApiService();
  const response = await api.post<Tarefa>(`/tasks/tarefas/${tarefaId}/remover_responsavel/`, { usuario: usuarioId });
  return response.data;
};
```

### Atualizar Status da Tarefa

```typescript
// services/api/services/taskService.ts
export const atualizarStatusTarefa = async (tarefaId: number, status: 'A_FAZER' | 'EM_ANDAMENTO' | 'FEITO'): Promise<Tarefa> => {
  const api = useApiService();
  const response = await api.post<Tarefa>(`/tasks/tarefas/${tarefaId}/atualizar_status/`, { status });
  return response.data;
};
```

### Associar Tarefa a Sprint

```typescript
// services/api/services/taskService.ts
export const associarSprint = async (tarefaId: number, sprintId: number): Promise<Tarefa> => {
  const api = useApiService();
  const response = await api.post<Tarefa>(`/tasks/tarefas/${tarefaId}/associar_sprint/`, { sprint: sprintId });
  return response.data;
};
```

### Comentários de Tarefas

```typescript
// services/api/services/taskService.ts
export interface ComentarioTarefa {
  id: number;
  texto: string;
  tarefa: number;
  autor: number;
  data_criacao: string;
}

export interface ComentarioTarefaListParams {
  page?: number;
  tarefa?: number;
  autor?: number;
}

export interface PaginatedComentarioTarefaList {
  count: number;
  next: string | null;
  previous: string | null;
  results: ComentarioTarefa[];
}

export const listComentariosTarefa = async (params: ComentarioTarefaListParams = {}): Promise<PaginatedComentarioTarefaList> => {
  const api = useApiService();
  const response = await api.get<PaginatedComentarioTarefaList>('/tasks/comentarios/', { params });
  return response.data;
};

export interface CreateComentarioTarefaRequest {
  texto: string;
  tarefa: number;
}

export const createComentarioTarefa = async (comentario: CreateComentarioTarefaRequest): Promise<ComentarioTarefa> => {
  const api = useApiService();
  const response = await api.post<ComentarioTarefa>('/tasks/comentarios/', comentario);
  return response.data;
};

export const adicionarComentarioTarefa = async (tarefaId: number, texto: string): Promise<Tarefa> => {
  const api = useApiService();
  const response = await api.post<Tarefa>(`/tasks/tarefas/${tarefaId}/adicionar_comentario/`, { texto });
  return response.data;
};
```

## Equipes

### Listar Equipes

```typescript
// services/api/services/teamService.ts
import { useApiService } from '../client/apiService';

export interface Equipe {
  id: number;
  nome: string;
  descricao: string;
  criado_por: number;
  criado_em: string;
  atualizado_em: string;
  membros: MembroEquipe[];
}

export interface MembroEquipe {
  id: number;
  usuario: number;
  equipe: number;
  papel: 'LIDER' | 'MEMBRO';
  data_adicao: string;
}

export interface EquipeListParams {
  page?: number;
  search?: string;
  ordering?: string;
}

export interface PaginatedEquipeList {
  count: number;
  next: string | null;
  previous: string | null;
  results: Equipe[];
}

export const listEquipes = async (params: EquipeListParams = {}): Promise<PaginatedEquipeList> => {
  const api = useApiService();
  const response = await api.get<PaginatedEquipeList>('/teams/equipes/', { params });
  return response.data;
};
```

### Obter Equipe por ID

```typescript
// services/api/services/teamService.ts
export const getEquipe = async (id: number): Promise<Equipe> => {
  const api = useApiService();
  const response = await api.get<Equipe>(`/teams/equipes/${id}/`);
  return response.data;
};
```

### Criar Equipe

```typescript
// services/api/services/teamService.ts
export interface CreateEquipeRequest {
  nome: string;
  descricao: string;
}

export const createEquipe = async (equipe: CreateEquipeRequest): Promise<Equipe> => {
  const api = useApiService();
  const response = await api.post<Equipe>('/teams/equipes/', equipe);
  return response.data;
};
```

### Atualizar Equipe

```typescript
// services/api/services/teamService.ts
export interface UpdateEquipeRequest {
  nome?: string;
  descricao?: string;
}

export const updateEquipe = async (id: number, equipe: UpdateEquipeRequest): Promise<Equipe> => {
  const api = useApiService();
  const response = await api.patch<Equipe>(`/teams/equipes/${id}/`, equipe);
  return response.data;
};
```

### Excluir Equipe

```typescript
// services/api/services/teamService.ts
export const deleteEquipe = async (id: number): Promise<void> => {
  const api = useApiService();
  await api.delete(`/teams/equipes/${id}/`);
};
```

### Gerenciar Membros da Equipe

```typescript
// services/api/services/teamService.ts
export interface AddMembroEquipeRequest {
  usuario: number;
  papel: 'LIDER' | 'MEMBRO';
}

export const adicionarMembroEquipe = async (equipeId: number, membro: AddMembroEquipeRequest): Promise<Equipe> => {
  const api = useApiService();
  const response = await api.post<Equipe>(`/teams/equipes/${equipeId}/adicionar_membro/`, membro);
  return response.data;
};

export const removerMembroEquipe = async (equipeId: number, usuarioId: number): Promise<Equipe> => {
  const api = useApiService();
  const response = await api.post<Equipe>(`/teams/equipes/${equipeId}/remover_membro/`, { usuario: usuarioId });
  return response.data;
};

export const atualizarPapelMembro = async (equipeId: number, usuarioId: number, papel: 'LIDER' | 'MEMBRO'): Promise<Equipe> => {
  const api = useApiService();
  const response = await api.post<Equipe>(`/teams/equipes/${equipeId}/atualizar_papel_membro/`, { usuario: usuarioId, papel });
  return response.data;
};

export const getMembrosEquipe = async (equipeId: number): Promise<MembroEquipe[]> => {
  const api = useApiService();
  const response = await api.get<MembroEquipe[]>(`/teams/equipes/${equipeId}/membros/`);
  return response.data;
};

export const getUsuariosDisponiveis = async (): Promise<User[]> => {
  const api = useApiService();
  const response = await api.get<User[]>('/teams/equipes/usuarios_disponiveis/');
  return response.data;
};
```
