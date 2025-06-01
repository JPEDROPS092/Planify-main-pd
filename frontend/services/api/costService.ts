/**
 * Serviço de custos
 * Gerado a partir da especificação OpenAPI
 */
import { createFetchClient } from './auth';
import { createFormData } from './config';
import type {
  Custo,
  CustoRequest,
  Categoria,
  CategoriaRequest,
  Alerta,
  AlertaRequest,
  PaginatedResponse,
} from './types';

// Função para obter a instância do cliente fetch apenas quando necessário
const getApi = () => {
  return createFetchClient();
};

/**
 * Listar custos
 * @param params Parâmetros de paginação e filtro
 */
export async function listCustos(params?: {
  categoria?: number;
  data_fim?: string;
  data_inicio?: string;
  ordering?: string;
  page?: number;
  projeto?: number;
  search?: string;
  tarefa?: number;
  tipo?: string;
}): Promise<PaginatedResponse<Custo>> {
  const queryParams = new URLSearchParams();

  if (params?.categoria)
    queryParams.append('categoria', params.categoria.toString());
  if (params?.data_fim) queryParams.append('data_fim', params.data_fim);
  if (params?.data_inicio)
    queryParams.append('data_inicio', params.data_inicio);
  if (params?.ordering) queryParams.append('ordering', params.ordering);
  if (params?.page) queryParams.append('page', params.page.toString());
  if (params?.projeto) queryParams.append('projeto', params.projeto.toString());
  if (params?.search) queryParams.append('search', params.search);
  if (params?.tarefa) queryParams.append('tarefa', params.tarefa.toString());
  if (params?.tipo) queryParams.append('tipo', params.tipo);

  const queryString = queryParams.toString();
  const url = `/api/costs/custos/${queryString ? `?${queryString}` : ''}`;

  return getApi()<PaginatedResponse<Custo>>(url, {
    method: 'GET',
  });
}

/**
 * Criar um novo custo
 * @param payload Dados do custo
 */
export async function createCusto(payload: CustoRequest): Promise<Custo> {
  // Se houver um comprovante, usar FormData
  if (payload.comprovante) {
    const formData = createFormData(payload);

    return getApi()<Custo>('/api/costs/custos/', {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': undefined, // O navegador definirá automaticamente com o boundary correto
      },
    });
  }

  return getApi()<Custo>('/api/costs/custos/', {
    method: 'POST',
    body: payload,
  });
}

/**
 * Obter detalhes de um custo
 * @param id ID do custo
 */
export async function retrieveCusto(id: number): Promise<Custo> {
  return getApi()<Custo>(`/api/costs/custos/${id}/`, {
    method: 'GET',
  });
}

/**
 * Atualizar um custo
 * @param id ID do custo
 * @param payload Dados do custo
 */
export async function updateCusto(
  id: number,
  payload: CustoRequest
): Promise<Custo> {
  // Se houver um comprovante, usar FormData
  if (payload.comprovante) {
    const formData = createFormData(payload);

    return getApi()<Custo>(`/api/costs/custos/${id}/`, {
      method: 'PUT',
      body: formData,
      headers: {
        'Content-Type': undefined, // O navegador definirá automaticamente com o boundary correto
      },
    });
  }

  return getApi()<Custo>(`/api/costs/custos/${id}/`, {
    method: 'PUT',
    body: payload,
  });
}

/**
 * Atualizar parcialmente um custo
 * @param id ID do custo
 * @param payload Dados parciais do custo
 */
export async function partialUpdateCusto(
  id: number,
  payload: Partial<CustoRequest>
): Promise<Custo> {
  // Se houver um comprovante, usar FormData
  if (payload.comprovante) {
    const formData = createFormData(payload);

    return getApi()<Custo>(`/api/costs/custos/${id}/`, {
      method: 'PATCH',
      body: formData,
      headers: {
        'Content-Type': undefined, // O navegador definirá automaticamente com o boundary correto
      },
    });
  }

  return getApi()<Custo>(`/api/costs/custos/${id}/`, {
    method: 'PATCH',
    body: payload,
  });
}

/**
 * Excluir um custo
 * @param id ID do custo
 */
export async function destroyCusto(id: number): Promise<void> {
  return getApi()<void>(`/api/costs/custos/${id}/`, {
    method: 'DELETE',
  });
}

/**
 * Listar categorias de custos
 * @param params Parâmetros de paginação e filtro
 */
export async function listCategorias(params?: {
  ordering?: string;
  page?: number;
  search?: string;
}): Promise<PaginatedResponse<Categoria>> {
  const queryParams = new URLSearchParams();

  if (params?.ordering) queryParams.append('ordering', params.ordering);
  if (params?.page) queryParams.append('page', params.page.toString());
  if (params?.search) queryParams.append('search', params.search);

  const queryString = queryParams.toString();
  const url = `/api/costs/categorias/${queryString ? `?${queryString}` : ''}`;

  return getApi()<PaginatedResponse<Categoria>>(url, {
    method: 'GET',
  });
}

/**
 * Criar uma nova categoria de custo
 * @param payload Dados da categoria
 */
export async function createCategoria(
  payload: CategoriaRequest
): Promise<Categoria> {
  return getApi()<Categoria>('/api/costs/categorias/', {
    method: 'POST',
    body: payload,
  });
}

/**
 * Obter detalhes de uma categoria de custo
 * @param id ID da categoria
 */
export async function retrieveCategoria(id: number): Promise<Categoria> {
  return getApi()<Categoria>(`/api/costs/categorias/${id}/`, {
    method: 'GET',
  });
}

/**
 * Atualizar uma categoria de custo
 * @param id ID da categoria
 * @param payload Dados da categoria
 */
export async function updateCategoria(
  id: number,
  payload: CategoriaRequest
): Promise<Categoria> {
  return getApi()<Categoria>(`/api/costs/categorias/${id}/`, {
    method: 'PUT',
    body: payload,
  });
}

/**
 * Atualizar parcialmente uma categoria de custo
 * @param id ID da categoria
 * @param payload Dados parciais da categoria
 */
export async function partialUpdateCategoria(
  id: number,
  payload: Partial<CategoriaRequest>
): Promise<Categoria> {
  return getApi()<Categoria>(`/api/costs/categorias/${id}/`, {
    method: 'PATCH',
    body: payload,
  });
}

/**
 * Excluir uma categoria de custo
 * @param id ID da categoria
 */
export async function destroyCategoria(id: number): Promise<void> {
  return getApi()<void>(`/api/costs/categorias/${id}/`, {
    method: 'DELETE',
  });
}

/**
 * Listar alertas de orçamento
 * @param params Parâmetros de paginação e filtro
 */
export async function listAlertas(params?: {
  ordering?: string;
  page?: number;
  projeto?: number;
  status?: string;
  tarefa?: number;
  tipo?: string;
}): Promise<PaginatedResponse<Alerta>> {
  const queryParams = new URLSearchParams();

  if (params?.ordering) queryParams.append('ordering', params.ordering);
  if (params?.page) queryParams.append('page', params.page.toString());
  if (params?.projeto) queryParams.append('projeto', params.projeto.toString());
  if (params?.status) queryParams.append('status', params.status);
  if (params?.tarefa) queryParams.append('tarefa', params.tarefa.toString());
  if (params?.tipo) queryParams.append('tipo', params.tipo);

  const queryString = queryParams.toString();
  const url = `/api/costs/alertas/${queryString ? `?${queryString}` : ''}`;

  return getApi()<PaginatedResponse<Alerta>>(url, {
    method: 'GET',
  });
}

/**
 * Criar um novo alerta de orçamento
 * @param payload Dados do alerta
 */
export async function createAlerta(payload: AlertaRequest): Promise<Alerta> {
  return getApi()<Alerta>('/api/costs/alertas/', {
    method: 'POST',
    body: payload,
  });
}

/**
 * Obter detalhes de um alerta de orçamento
 * @param id ID do alerta
 */
export async function retrieveAlerta(id: number): Promise<Alerta> {
  return getApi()<Alerta>(`/api/costs/alertas/${id}/`, {
    method: 'GET',
  });
}

/**
 * Atualizar um alerta de orçamento
 * @param id ID do alerta
 * @param payload Dados do alerta
 */
export async function updateAlerta(
  id: number,
  payload: AlertaRequest
): Promise<Alerta> {
  return getApi()<Alerta>(`/api/costs/alertas/${id}/`, {
    method: 'PUT',
    body: payload,
  });
}

/**
 * Atualizar parcialmente um alerta de orçamento
 * @param id ID do alerta
 * @param payload Dados parciais do alerta
 */
export async function partialUpdateAlerta(
  id: number,
  payload: Partial<AlertaRequest>
): Promise<Alerta> {
  return getApi()<Alerta>(`/api/costs/alertas/${id}/`, {
    method: 'PATCH',
    body: payload,
  });
}

/**
 * Excluir um alerta de orçamento
 * @param id ID do alerta
 */
export async function destroyAlerta(id: number): Promise<void> {
  return getApi()<void>(`/api/costs/alertas/${id}/`, {
    method: 'DELETE',
  });
}

/**
 * Resolver um alerta de orçamento
 * @param id ID do alerta
 */
export async function resolverAlerta(id: number): Promise<Alerta> {
  return getApi()<Alerta>(`/api/costs/alertas/${id}/resolver/`, {
    method: 'POST',
  });
}

/**
 * Listar orçamentos de projeto
 * @param params Parâmetros de paginação e filtro
 */
export async function listOrcamentosProjeto(params?: {
  ordering?: string;
  page?: number;
  projeto?: number;
}): Promise<PaginatedResponse<any>> {
  const queryParams = new URLSearchParams();

  if (params?.ordering) queryParams.append('ordering', params.ordering);
  if (params?.page) queryParams.append('page', params.page.toString());
  if (params?.projeto) queryParams.append('projeto', params.projeto.toString());

  const queryString = queryParams.toString();
  const url = `/api/costs/orcamentos-projeto/${queryString ? `?${queryString}` : ''}`;

  return getApi()<PaginatedResponse<any>>(url, {
    method: 'GET',
  });
}

/**
 * Criar um novo orçamento de projeto
 * @param payload Dados do orçamento
 */
export async function createOrcamentoProjeto(payload: any): Promise<any> {
  return getApi()<any>('/api/costs/orcamentos-projeto/', {
    method: 'POST',
    body: payload,
  });
}

/**
 * Obter detalhes de um orçamento de projeto
 * @param id ID do orçamento
 */
export async function retrieveOrcamentoProjeto(id: number): Promise<any> {
  return getApi()<any>(`/api/costs/orcamentos-projeto/${id}/`, {
    method: 'GET',
  });
}

/**
 * Atualizar um orçamento de projeto
 * @param id ID do orçamento
 * @param payload Dados do orçamento
 */
export async function updateOrcamentoProjeto(
  id: number,
  payload: any
): Promise<any> {
  return getApi()<any>(`/api/costs/orcamentos-projeto/${id}/`, {
    method: 'PUT',
    body: payload,
  });
}

/**
 * Atualizar parcialmente um orçamento de projeto
 * @param id ID do orçamento
 * @param payload Dados parciais do orçamento
 */
export async function partialUpdateOrcamentoProjeto(
  id: number,
  payload: any
): Promise<any> {
  return getApi()<any>(`/api/costs/orcamentos-projeto/${id}/`, {
    method: 'PATCH',
    body: payload,
  });
}

/**
 * Excluir um orçamento de projeto
 * @param id ID do orçamento
 */
export async function destroyOrcamentoProjeto(id: number): Promise<void> {
  return getApi()<void>(`/api/costs/orcamentos-projeto/${id}/`, {
    method: 'DELETE',
  });
}

/**
 * Obter projetos sem orçamento
 */
export async function retrieveProjetosSemOrcamento(): Promise<any[]> {
  return getApi()<any[]>(
    '/api/costs/orcamentos-projeto/projetos_sem_orcamento/',
    {
      method: 'GET',
    }
  );
}
