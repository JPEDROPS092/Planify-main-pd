/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Alerta } from '../models/Alerta';
import type { AlertaRequest } from '../models/AlertaRequest';
import type { Categoria } from '../models/Categoria';
import type { CategoriaRequest } from '../models/CategoriaRequest';
import type { Custo } from '../models/Custo';
import type { CustoRequest } from '../models/CustoRequest';
import type { OrcamentoProjeto } from '../models/OrcamentoProjeto';
import type { OrcamentoProjetoRequest } from '../models/OrcamentoProjetoRequest';
import type { OrcamentoTarefa } from '../models/OrcamentoTarefa';
import type { OrcamentoTarefaRequest } from '../models/OrcamentoTarefaRequest';
import type { PaginatedAlertaList } from '../models/PaginatedAlertaList';
import type { PaginatedCategoriaList } from '../models/PaginatedCategoriaList';
import type { PaginatedCustoListList } from '../models/PaginatedCustoListList';
import type { PaginatedOrcamentoProjetoList } from '../models/PaginatedOrcamentoProjetoList';
import type { PaginatedOrcamentoTarefaList } from '../models/PaginatedOrcamentoTarefaList';
import type { PatchedAlertaRequest } from '../models/PatchedAlertaRequest';
import type { PatchedCategoriaRequest } from '../models/PatchedCategoriaRequest';
import type { PatchedCustoRequest } from '../models/PatchedCustoRequest';
import type { PatchedOrcamentoProjetoRequest } from '../models/PatchedOrcamentoProjetoRequest';
import type { PatchedOrcamentoTarefaRequest } from '../models/PatchedOrcamentoTarefaRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CustoService {
    /**
     * Listar alertas
     * Retorna uma lista paginada de alertas.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param projeto
     * @param status * `ATIVO` - Ativo
     * * `RESOLVIDO` - Resolvido
     * * `IGNORADO` - Ignorado
     * @param tarefa
     * @param tipo * `PROJETO` - Projeto
     * * `TAREFA` - Tarefa
     * @returns PaginatedAlertaList
     * @throws ApiError
     */
    public static costsAlertasList(
        ordering?: string,
        page?: number,
        projeto?: number,
        status?: 'ATIVO' | 'IGNORADO' | 'RESOLVIDO',
        tarefa?: number,
        tipo?: 'PROJETO' | 'TAREFA',
    ): CancelablePromise<PaginatedAlertaList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/alertas/',
            query: {
                'ordering': ordering,
                'page': page,
                'projeto': projeto,
                'status': status,
                'tarefa': tarefa,
                'tipo': tipo,
            },
        });
    }
    /**
     * Criar nova alerta
     * Cria uma novo alerta.
     * @param requestBody
     * @returns Alerta
     * @throws ApiError
     */
    public static costsAlertasCreate(
        requestBody: AlertaRequest,
    ): CancelablePromise<Alerta> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/alertas/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes da alerta
     * Retorna informações detalhadas de uma alerta específica.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @returns Alerta
     * @throws ApiError
     */
    public static costsAlertasRetrieve(
        id: number,
    ): CancelablePromise<Alerta> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/alertas/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar alerta
     * Atualiza todos os campos de uma alerta existente.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @param requestBody
     * @returns Alerta
     * @throws ApiError
     */
    public static costsAlertasUpdate(
        id: number,
        requestBody: AlertaRequest,
    ): CancelablePromise<Alerta> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/costs/alertas/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar alerta parcialmente
     * Atualiza parcialmente uma alerta existente.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @param requestBody
     * @returns Alerta
     * @throws ApiError
     */
    public static costsAlertasPartialUpdate(
        id: number,
        requestBody?: PatchedAlertaRequest,
    ): CancelablePromise<Alerta> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/costs/alertas/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir alerta
     * Remove uma alerta existente.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @returns void
     * @throws ApiError
     */
    public static costsAlertasDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/costs/alertas/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Marcar alertas como ignorado
     * Marca um alerta como ignorado.
     * Opcionalmente, pode incluir uma justificativa para ignorar o alerta.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static costsAlertasIgnorarCreate(
        id: number,
        requestBody: AlertaRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/alertas/{id}/ignorar/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Marcar alertas como resolvido
     * Marca um alerta como resolvido.
     * Opcionalmente, pode incluir uma observação sobre a resolução.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static costsAlertasResolverCreate(
        id: number,
        requestBody: AlertaRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/alertas/{id}/resolver/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Listar alertas com status ATIVO
     * Retorna apenas os alertas pendentes (status ATIVO).
     * Permite filtrar por projeto, tarefa e tipo.
     * @returns any No response body
     * @throws ApiError
     */
    public static costsAlertasPendentesRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/alertas/pendentes/',
        });
    }
    /**
     * Listar categorias
     * Retorna uma lista paginada de categorias.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedCategoriaList
     * @throws ApiError
     */
    public static costsCategoriasList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedCategoriaList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/categorias/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * Criar nova categoria
     * Cria uma novo categoria.
     * @param requestBody
     * @returns Categoria
     * @throws ApiError
     */
    public static costsCategoriasCreate(
        requestBody: CategoriaRequest,
    ): CancelablePromise<Categoria> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/categorias/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes da categoria
     * Retorna informações detalhadas de uma categoria específica.
     * @param id A unique integer value identifying this Categoria.
     * @returns Categoria
     * @throws ApiError
     */
    public static costsCategoriasRetrieve(
        id: number,
    ): CancelablePromise<Categoria> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/categorias/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar categoria
     * Atualiza todos os campos de uma categoria existente.
     * @param id A unique integer value identifying this Categoria.
     * @param requestBody
     * @returns Categoria
     * @throws ApiError
     */
    public static costsCategoriasUpdate(
        id: number,
        requestBody: CategoriaRequest,
    ): CancelablePromise<Categoria> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/costs/categorias/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar categoria parcialmente
     * Atualiza parcialmente uma categoria existente.
     * @param id A unique integer value identifying this Categoria.
     * @param requestBody
     * @returns Categoria
     * @throws ApiError
     */
    public static costsCategoriasPartialUpdate(
        id: number,
        requestBody?: PatchedCategoriaRequest,
    ): CancelablePromise<Categoria> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/costs/categorias/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir categoria
     * Remove uma categoria existente.
     * @param id A unique integer value identifying this Categoria.
     * @returns void
     * @throws ApiError
     */
    public static costsCategoriasDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/costs/categorias/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar custos
     * Retorna uma lista paginada de custos.
     * @param categoria
     * @param data
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param projeto
     * @param search A search term.
     * @param tarefa
     * @param tipo * `FIXO` - Custo Fixo
     * * `VARIAVEL` - Custo Variável
     * * `RECORRENTE` - Custo Recorrente
     * @returns PaginatedCustoListList
     * @throws ApiError
     */
    public static costsCustosList(
        categoria?: number,
        data?: string,
        ordering?: string,
        page?: number,
        projeto?: number,
        search?: string,
        tarefa?: number,
        tipo?: 'FIXO' | 'RECORRENTE' | 'VARIAVEL',
    ): CancelablePromise<PaginatedCustoListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/',
            query: {
                'categoria': categoria,
                'data': data,
                'ordering': ordering,
                'page': page,
                'projeto': projeto,
                'search': search,
                'tarefa': tarefa,
                'tipo': tipo,
            },
        });
    }
    /**
     * Criar novo custo
     * Cria um novo custo.
     * @param requestBody
     * @returns Custo
     * @throws ApiError
     */
    public static costsCustosCreate(
        requestBody: CustoRequest,
    ): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/custos/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do custo
     * Retorna informações detalhadas de um custo específico.
     * @param id A unique integer value identifying this Custo.
     * @returns Custo
     * @throws ApiError
     */
    public static costsCustosRetrieve(
        id: number,
    ): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar custo
     * Atualiza todos os campos de um custo existente.
     * @param id A unique integer value identifying this Custo.
     * @param requestBody
     * @returns Custo
     * @throws ApiError
     */
    public static costsCustosUpdate(
        id: number,
        requestBody: CustoRequest,
    ): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/costs/custos/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar custo parcialmente
     * Atualiza parcialmente um custo existente.
     * @param id A unique integer value identifying this Custo.
     * @param requestBody
     * @returns Custo
     * @throws ApiError
     */
    public static costsCustosPartialUpdate(
        id: number,
        requestBody?: PatchedCustoRequest,
    ): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/costs/custos/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir custo
     * Remove um custo existente.
     * @param id A unique integer value identifying this Custo.
     * @returns void
     * @throws ApiError
     */
    public static costsCustosDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/costs/custos/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Dashboard financeiro
     * Endpoint para dashboard financeiro: retorna dados resumidos de custos.
     * Inclui total gasto, gasto mensal, top categorias e alertas recentes.
     * @returns any No response body
     * @throws ApiError
     */
    public static costsCustosDashboardRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/dashboard/',
        });
    }
    /**
     * Relatório de gastos mensais
     * Gera um relatório de gastos mensais para análise de tendências.
     * Agrupa os custos por mês e retorna série temporal.
     * @returns any No response body
     * @throws ApiError
     */
    public static costsCustosRelatorioMensalRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/relatorio_mensal/',
        });
    }
    /**
     * Relatório de gastos por categoria
     * Gera um relatório de gastos por categoria.
     * Utiliza anotações para calcular percentuais diretamente no banco de dados.
     * @returns any No response body
     * @throws ApiError
     */
    public static costsCustosRelatorioPorCategoriaRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/relatorio_por_categoria/',
        });
    }
    /**
     * Relatório de gastos por projeto
     * Gera um relatório de gastos por projeto.
     * @returns any No response body
     * @throws ApiError
     */
    public static costsCustosRelatorioPorProjetoRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/relatorio_por_projeto/',
        });
    }
    /**
     * Listar custos
     * Retorna uma lista paginada de custos.
     * @param page A page number within the paginated result set.
     * @param projeto
     * @returns PaginatedOrcamentoProjetoList
     * @throws ApiError
     */
    public static costsOrcamentosProjetoList(
        page?: number,
        projeto?: number,
    ): CancelablePromise<PaginatedOrcamentoProjetoList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-projeto/',
            query: {
                'page': page,
                'projeto': projeto,
            },
        });
    }
    /**
     * Criar novo custo
     * Cria um novo custo.
     * @param requestBody
     * @returns OrcamentoProjeto
     * @throws ApiError
     */
    public static costsOrcamentosProjetoCreate(
        requestBody: OrcamentoProjetoRequest,
    ): CancelablePromise<OrcamentoProjeto> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/orcamentos-projeto/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do custo
     * Retorna informações detalhadas de um custo específico.
     * @param id A unique integer value identifying this Orçamento de Projeto.
     * @returns OrcamentoProjeto
     * @throws ApiError
     */
    public static costsOrcamentosProjetoRetrieve(
        id: number,
    ): CancelablePromise<OrcamentoProjeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-projeto/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar custo
     * Atualiza todos os campos de um custo existente.
     * @param id A unique integer value identifying this Orçamento de Projeto.
     * @param requestBody
     * @returns OrcamentoProjeto
     * @throws ApiError
     */
    public static costsOrcamentosProjetoUpdate(
        id: number,
        requestBody: OrcamentoProjetoRequest,
    ): CancelablePromise<OrcamentoProjeto> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/costs/orcamentos-projeto/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar custo parcialmente
     * Atualiza parcialmente um custo existente.
     * @param id A unique integer value identifying this Orçamento de Projeto.
     * @param requestBody
     * @returns OrcamentoProjeto
     * @throws ApiError
     */
    public static costsOrcamentosProjetoPartialUpdate(
        id: number,
        requestBody?: PatchedOrcamentoProjetoRequest,
    ): CancelablePromise<OrcamentoProjeto> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/costs/orcamentos-projeto/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir custo
     * Remove um custo existente.
     * @param id A unique integer value identifying this Orçamento de Projeto.
     * @returns void
     * @throws ApiError
     */
    public static costsOrcamentosProjetoDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/costs/orcamentos-projeto/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Ajustar orçamento de um projeto
     * Permite ajustar o orçamento de um projeto com justificativa.
     * Mantém histórico da alteração no campo de observações.
     * @param id A unique integer value identifying this Orçamento de Projeto.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static costsOrcamentosProjetoAjustarOrcamentoCreate(
        id: number,
        requestBody: OrcamentoProjetoRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/orcamentos-projeto/{id}/ajustar_orcamento/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Listar projetos sem orçamento definido
     * Retorna a lista de projetos que ainda não possuem orçamento definido.
     * @returns any No response body
     * @throws ApiError
     */
    public static costsOrcamentosProjetoProjetosSemOrcamentoRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-projeto/projetos_sem_orcamento/',
        });
    }
    /**
     * Listar tarefas
     * Retorna uma lista paginada de tarefas.
     * @param page A page number within the paginated result set.
     * @param tarefa
     * @param tarefaProjeto
     * @returns PaginatedOrcamentoTarefaList
     * @throws ApiError
     */
    public static costsOrcamentosTarefaList(
        page?: number,
        tarefa?: number,
        tarefaProjeto?: number,
    ): CancelablePromise<PaginatedOrcamentoTarefaList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-tarefa/',
            query: {
                'page': page,
                'tarefa': tarefa,
                'tarefa__projeto': tarefaProjeto,
            },
        });
    }
    /**
     * Criar nova tarefa
     * Cria uma novo tarefa.
     * @param requestBody
     * @returns OrcamentoTarefa
     * @throws ApiError
     */
    public static costsOrcamentosTarefaCreate(
        requestBody: OrcamentoTarefaRequest,
    ): CancelablePromise<OrcamentoTarefa> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/orcamentos-tarefa/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes da tarefa
     * Retorna informações detalhadas de uma tarefa específica.
     * @param id A unique integer value identifying this Orçamento de Tarefa.
     * @returns OrcamentoTarefa
     * @throws ApiError
     */
    public static costsOrcamentosTarefaRetrieve(
        id: number,
    ): CancelablePromise<OrcamentoTarefa> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-tarefa/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar tarefa
     * Atualiza todos os campos de uma tarefa existente.
     * @param id A unique integer value identifying this Orçamento de Tarefa.
     * @param requestBody
     * @returns OrcamentoTarefa
     * @throws ApiError
     */
    public static costsOrcamentosTarefaUpdate(
        id: number,
        requestBody: OrcamentoTarefaRequest,
    ): CancelablePromise<OrcamentoTarefa> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/costs/orcamentos-tarefa/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar tarefa parcialmente
     * Atualiza parcialmente uma tarefa existente.
     * @param id A unique integer value identifying this Orçamento de Tarefa.
     * @param requestBody
     * @returns OrcamentoTarefa
     * @throws ApiError
     */
    public static costsOrcamentosTarefaPartialUpdate(
        id: number,
        requestBody?: PatchedOrcamentoTarefaRequest,
    ): CancelablePromise<OrcamentoTarefa> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/costs/orcamentos-tarefa/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir tarefa
     * Remove uma tarefa existente.
     * @param id A unique integer value identifying this Orçamento de Tarefa.
     * @returns void
     * @throws ApiError
     */
    public static costsOrcamentosTarefaDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/costs/orcamentos-tarefa/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Ajustar orçamento de uma tarefas
     * Permite ajustar o orçamento de uma tarefa com justificativa.
     * Mantém histórico da alteração no campo de observações.
     * @param id A unique integer value identifying this Orçamento de Tarefa.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static costsOrcamentosTarefaAjustarOrcamentoCreate(
        id: number,
        requestBody: OrcamentoTarefaRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/orcamentos-tarefa/{id}/ajustar_orcamento/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Listar tarefas sem orçamento
     * Retorna a lista de tarefas que ainda não possuem orçamento definido.
     * @returns any No response body
     * @throws ApiError
     */
    public static costsOrcamentosTarefaTarefasSemOrcamentoRetrieve(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-tarefa/tarefas_sem_orcamento/',
        });
    }
}
