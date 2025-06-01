/**
 * API de Projetos
 * Implementação direta das chamadas de API para projetos
 */
import { useApiService } from '~/composables/useApiService';
import { PaginatedResponse, ProjetoList, Projeto, ProjetoRequest } from './types';

// Função para obter a instância da API
const getApi = () => {
  const { api } = useApiService();
  return api;
};

// Listar projetos com paginação e filtros
export const listProjetos = async (params?: {
  page?: number;
  ordering?: string;
  arquivado?: boolean;
  gerente?: number;
  search?: string;
  status?: string;
}): Promise<PaginatedResponse<ProjetoList>> => {
  const api = getApi();
  const queryParams = new URLSearchParams();
  
  if (params?.page) queryParams.append('page', params.page.toString());
  if (params?.ordering) queryParams.append('ordering', params.ordering);
  if (params?.arquivado !== undefined) queryParams.append('arquivado', params.arquivado.toString());
  if (params?.gerente) queryParams.append('gerente', params.gerente.toString());
  if (params?.search) queryParams.append('search', params.search);
  if (params?.status) queryParams.append('status', params.status);
  
  const url = `/api/projetos/${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
  const response = await api.get(url);
  return response.data;
};

// Criar um novo projeto
export const createProjeto = async (payload: ProjetoRequest): Promise<Projeto> => {
  const api = getApi();
  const response = await api.post('/api/projetos/', payload);
  return response.data;
};

// Obter detalhes de um projeto
export const retrieveProjeto = async (id: number): Promise<Projeto> => {
  const api = getApi();
  const response = await api.get(`/api/projetos/${id}/`);
  return response.data;
};

// Atualizar um projeto
export const updateProjeto = async (id: number, payload: ProjetoRequest): Promise<Projeto> => {
  const api = getApi();
  const response = await api.put(`/api/projetos/${id}/`, payload);
  return response.data;
};

// Atualizar parcialmente um projeto
export const partialUpdateProjeto = async (id: number, payload: Partial<ProjetoRequest>): Promise<Projeto> => {
  const api = getApi();
  const response = await api.patch(`/api/projetos/${id}/`, payload);
  return response.data;
};

// Excluir um projeto
export const destroyProjeto = async (id: number): Promise<void> => {
  const api = getApi();
  await api.delete(`/api/projetos/${id}/`);
};

// Arquivar ou desarquivar um projeto
export const archiveProjeto = async (id: number, payload: { arquivado: boolean }): Promise<Projeto> => {
  const api = getApi();
  const response = await api.patch(`/api/projetos/${id}/arquivar/`, payload);
  return response.data;
};

// Listar sprints de um projeto
export const listSprints = async (params?: {
  page?: number;
  ordering?: string;
  projeto?: number;
  search?: string;
  status?: string;
}): Promise<PaginatedResponse<any>> => {
  const api = getApi();
  const queryParams = new URLSearchParams();
  
  if (params?.page) queryParams.append('page', params.page.toString());
  if (params?.ordering) queryParams.append('ordering', params.ordering);
  if (params?.projeto) queryParams.append('projeto', params.projeto.toString());
  if (params?.search) queryParams.append('search', params.search);
  if (params?.status) queryParams.append('status', params.status);
  
  const url = `/api/sprints/${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
  const response = await api.get(url);
  return response.data;
};

// Outras operações de sprint
export const createSprint = async (payload: any): Promise<any> => {
  const api = getApi();
  const response = await api.post('/api/sprints/', payload);
  return response.data;
};

export const retrieveSprint = async (id: number): Promise<any> => {
  const api = getApi();
  const response = await api.get(`/api/sprints/${id}/`);
  return response.data;
};

export const updateSprint = async (id: number, payload: any): Promise<any> => {
  const api = getApi();
  const response = await api.put(`/api/sprints/${id}/`, payload);
  return response.data;
};

export const partialUpdateSprint = async (id: number, payload: any): Promise<any> => {
  const api = getApi();
  const response = await api.patch(`/api/sprints/${id}/`, payload);
  return response.data;
};

export const destroySprint = async (id: number): Promise<void> => {
  const api = getApi();
  await api.delete(`/api/sprints/${id}/`);
};
