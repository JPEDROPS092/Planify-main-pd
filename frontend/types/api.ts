/**
 * Este arquivo contém tipos simplificados para demonstração.
 * Em um cenário real, você usaria o comando:
 * npm run generate-api-types
 * para gerar tipos completos baseados no schema OpenAPI.
 */

// Tipos genéricos
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
  total_pages: number;
  current_page: number;
}

// Tipos de autenticação
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface RefreshTokenRequest {
  refresh: string;
}

export interface RefreshTokenResponse {
  access: string;
}

// Tipos de usuário
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  date_joined: string;
  last_login: string;
}

// Tipos de projeto
export interface Projeto {
  id: number;
  titulo: string;
  descricao: string;
  data_inicio: string;
  data_fim_previsto: string;
  data_fim_real: string | null;
  status: string;
  status_display: string;
  criado_por: number;
  criado_por_nome: string;
  created_at: string;
  updated_at: string;
  membros: MembroProjeto[];
}

export interface ProjetoRequest {
  titulo: string;
  descricao?: string;
  data_inicio?: string;
  data_fim_previsto?: string;
  status?: string;
}

export interface MembroProjeto {
  id: number;
  usuario_id: number;
  usuario_nome: string;
  papel: string;
  papel_display: string;
}

// Tipos de tarefa
export interface Tarefa {
  id: number;
  titulo: string;
  descricao: string;
  projeto: number;
  projeto_titulo: string;
  status: string;
  status_display: string;
  prioridade: string;
  prioridade_display: string;
  data_inicio: string;
  data_fim_previsto: string;
  data_fim_real: string | null;
  criado_por: number;
  criado_por_nome: string;
  responsaveis: AtribuicaoTarefa[];
  created_at: string;
  updated_at: string;
}

export interface TarefaRequest {
  titulo: string;
  descricao?: string;
  projeto: number;
  status?: string;
  prioridade?: string;
  data_inicio?: string;
  data_fim_previsto?: string;
}

export interface AtribuicaoTarefa {
  id: number;
  tarefa: number;
  usuario: number;
  usuario_nome: string;
  papel: string;
}

// Tipos de kanban
export interface KanbanResponse {
  id: number;
  titulo: string;
  colunas: ColunaKanban[];
}

export interface ColunaKanban {
  id: number;
  titulo: string;
  ordem: number;
  tarefas: TarefaKanban[];
}

export interface TarefaKanban {
  id: number;
  titulo: string;
  descricao: string;
  prioridade: string;
  prioridade_display: string;
  data_fim_previsto: string;
  responsaveis: AtribuicaoTarefa[];
}

// Tipos de gantt
export interface GanttResponse {
  id: number;
  titulo: string;
  tarefas: TarefaGantt[];
}

export interface TarefaGantt {
  id: number;
  titulo: string;
  inicio: string;
  fim: string;
  progresso: number;
  dependencias: number[];
}
