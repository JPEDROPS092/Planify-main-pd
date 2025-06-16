/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GanttResponse } from '../models/GanttResponse';
import type { KanbanResponse } from '../models/KanbanResponse';
import type { MembroProjeto } from '../models/MembroProjeto';
import type { MembroProjetoRequest } from '../models/MembroProjetoRequest';
import type { PaginatedMembroProjetoList } from '../models/PaginatedMembroProjetoList';
import type { PaginatedProjetoList } from '../models/PaginatedProjetoList';
import type { PaginatedProjetoListList } from '../models/PaginatedProjetoListList';
import type { PatchedKanbanResponseRequest } from '../models/PatchedKanbanResponseRequest';
import type { PatchedProjetoRequest } from '../models/PatchedProjetoRequest';
import type { Projeto } from '../models/Projeto';
import type { ProjetoDashboardResponse } from '../models/ProjetoDashboardResponse';
import type { ProjetoRequest } from '../models/ProjetoRequest';
import type { Tarefa } from '../models/Tarefa';
import type { TarefaCreateRequest } from '../models/TarefaCreateRequest';
import type { TarefasBulkCreateRequest } from '../models/TarefasBulkCreateRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class ProjetosService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Listar projetos
     * Retorna uma lista paginada de projetos.
     * @param arquivado
     * @param atrasado Filtra projetos atrasados (data_fim < hoje e status != CONCLUIDO)
     * @param dataFimAntesAfter Filtra projetos com data de fim antes da data especificada
     * @param dataFimAntesBefore Filtra projetos com data de fim antes da data especificada
     * @param dataFimAposAfter Filtra projetos com data de fim após a data especificada
     * @param dataFimAposBefore Filtra projetos com data de fim após a data especificada
     * @param dataInicioAntesAfter Filtra projetos com data de início antes da data especificada
     * @param dataInicioAntesBefore Filtra projetos com data de início antes da data especificada
     * @param dataInicioAposAfter Filtra projetos com data de início após a data especificada
     * @param dataInicioAposBefore Filtra projetos com data de início após a data especificada
     * @param descricao Filtra por descrição (case insensitive)
     * @param membro Filtra projetos que contenham o membro especificado (ID do usuário)
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param prioridade Filtra por prioridade (pode ser múltiplas, separadas por vírgula)
     * @param search A search term.
     * @param status Filtra por status (pode ser múltiplos, separados por vírgula)
     * @param titulo Filtra por título (case insensitive)
     * @returns PaginatedProjetoListList
     * @throws ApiError
     */
    public apiProjectsList(
        arquivado?: boolean,
        atrasado?: boolean,
        dataFimAntesAfter?: string,
        dataFimAntesBefore?: string,
        dataFimAposAfter?: string,
        dataFimAposBefore?: string,
        dataInicioAntesAfter?: string,
        dataInicioAntesBefore?: string,
        dataInicioAposAfter?: string,
        dataInicioAposBefore?: string,
        descricao?: string,
        membro?: string,
        ordering?: string,
        page?: number,
        prioridade?: string,
        search?: string,
        status?: string,
        titulo?: string,
    ): CancelablePromise<PaginatedProjetoListList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/',
            query: {
                'arquivado': arquivado,
                'atrasado': atrasado,
                'data_fim_antes_after': dataFimAntesAfter,
                'data_fim_antes_before': dataFimAntesBefore,
                'data_fim_apos_after': dataFimAposAfter,
                'data_fim_apos_before': dataFimAposBefore,
                'data_inicio_antes_after': dataInicioAntesAfter,
                'data_inicio_antes_before': dataInicioAntesBefore,
                'data_inicio_apos_after': dataInicioAposAfter,
                'data_inicio_apos_before': dataInicioAposBefore,
                'descricao': descricao,
                'membro': membro,
                'ordering': ordering,
                'page': page,
                'prioridade': prioridade,
                'search': search,
                'status': status,
                'titulo': titulo,
            },
        });
    }
    /**
     * Criar novo projeto
     * Cria um novo projeto.
     * @param requestBody
     * @returns Projeto
     * @throws ApiError
     */
    public apiProjectsCreate(
        requestBody: ProjetoRequest,
    ): CancelablePromise<Projeto> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/projects/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do projeto
     * Retorna informações detalhadas de um projeto específico.
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public apiProjectsRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar projeto
     * Atualiza todos os campos de um projeto existente.
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns Projeto
     * @throws ApiError
     */
    public apiProjectsUpdate(
        id: number,
        requestBody: ProjetoRequest,
    ): CancelablePromise<Projeto> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/projects/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar projeto parcialmente
     * Atualiza parcialmente um projeto existente.
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns Projeto
     * @throws ApiError
     */
    public apiProjectsPartialUpdate(
        id: number,
        requestBody?: PatchedProjetoRequest,
    ): CancelablePromise<Projeto> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/projects/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir projeto
     * Remove um projeto existente.
     * @param id A unique integer value identifying this Projeto.
     * @returns void
     * @throws ApiError
     */
    public apiProjectsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/projects/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Adicionar membro ao projeto
     * Adiciona um novo membro ao projeto com o papel especificado.
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns MembroProjeto
     * @throws ApiError
     */
    public apiProjectsAdicionarMembroCreate(
        id: number,
        requestBody: MembroProjetoRequest,
    ): CancelablePromise<MembroProjeto> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/projects/{id}/adicionar_membro/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Arquivar projeto
     * Arquiva ou desarquiva um projeto.
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns any
     * @throws ApiError
     */
    public apiProjectsArchiveCreate(
        id: number,
        requestBody: ProjetoRequest,
    ): CancelablePromise<Record<string, any>> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/projects/{id}/archive/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Criar Sprint no projeto
     * Cria uma nova sprint para um projeto.
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns Projeto
     * @throws ApiError
     */
    public apiProjectsCriarSprintCreate(
        id: number,
        requestBody: ProjetoRequest,
    ): CancelablePromise<Projeto> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/projects/{id}/criar_sprint/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Exportar dados do projeto
     * Exporta os dados do projeto.
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public apiProjectsExportProjectRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/{id}/export_project/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Histórico de status do projeto
     * Visualizar o histórico de mudanças de status do projeto.
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public apiProjectsHistoricoStatusRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/{id}/historico_status/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar membros do projeto
     * Retorna todos os membros associados ao projeto.
     * @param id A unique integer value identifying this Projeto.
     * @param arquivado
     * @param atrasado Filtra projetos atrasados (data_fim < hoje e status != CONCLUIDO)
     * @param dataFimAntesAfter Filtra projetos com data de fim antes da data especificada
     * @param dataFimAntesBefore Filtra projetos com data de fim antes da data especificada
     * @param dataFimAposAfter Filtra projetos com data de fim após a data especificada
     * @param dataFimAposBefore Filtra projetos com data de fim após a data especificada
     * @param dataInicioAntesAfter Filtra projetos com data de início antes da data especificada
     * @param dataInicioAntesBefore Filtra projetos com data de início antes da data especificada
     * @param dataInicioAposAfter Filtra projetos com data de início após a data especificada
     * @param dataInicioAposBefore Filtra projetos com data de início após a data especificada
     * @param descricao Filtra por descrição (case insensitive)
     * @param membro Filtra projetos que contenham o membro especificado (ID do usuário)
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param prioridade Filtra por prioridade (pode ser múltiplas, separadas por vírgula)
     * @param search A search term.
     * @param status Filtra por status (pode ser múltiplos, separados por vírgula)
     * @param titulo Filtra por título (case insensitive)
     * @returns PaginatedMembroProjetoList
     * @throws ApiError
     */
    public apiProjectsListarMembrosList(
        id: number,
        arquivado?: boolean,
        atrasado?: boolean,
        dataFimAntesAfter?: string,
        dataFimAntesBefore?: string,
        dataFimAposAfter?: string,
        dataFimAposBefore?: string,
        dataInicioAntesAfter?: string,
        dataInicioAntesBefore?: string,
        dataInicioAposAfter?: string,
        dataInicioAposBefore?: string,
        descricao?: string,
        membro?: string,
        ordering?: string,
        page?: number,
        prioridade?: string,
        search?: string,
        status?: string,
        titulo?: string,
    ): CancelablePromise<PaginatedMembroProjetoList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/{id}/listar_membros/',
            path: {
                'id': id,
            },
            query: {
                'arquivado': arquivado,
                'atrasado': atrasado,
                'data_fim_antes_after': dataFimAntesAfter,
                'data_fim_antes_before': dataFimAntesBefore,
                'data_fim_apos_after': dataFimAposAfter,
                'data_fim_apos_before': dataFimAposBefore,
                'data_inicio_antes_after': dataInicioAntesAfter,
                'data_inicio_antes_before': dataInicioAntesBefore,
                'data_inicio_apos_after': dataInicioAposAfter,
                'data_inicio_apos_before': dataInicioAposBefore,
                'descricao': descricao,
                'membro': membro,
                'ordering': ordering,
                'page': page,
                'prioridade': prioridade,
                'search': search,
                'status': status,
                'titulo': titulo,
            },
        });
    }
    /**
     * Métricas Detalhadas do Projeto
     * Retorna métricas detalhadas sobre o projeto, incluindo progresso, custos, prazos e qualidade.
     * @param id A unique integer value identifying this Projeto.
     * @returns any
     * @throws ApiError
     */
    public apiProjectsMetricsRetrieve(
        id: number,
    ): CancelablePromise<Record<string, any>> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/{id}/metrics/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Remover membro do projeto
     * Remove um membro do projeto pelo ID.
     * @param id A unique integer value identifying this Projeto.
     * @param membroId ID do membro a ser removido
     * @returns void
     * @throws ApiError
     */
    public apiProjectsRemoverMembroDestroy(
        id: number,
        membroId: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/projects/{id}/remover_membro/',
            path: {
                'id': id,
            },
            query: {
                'membro_id': membroId,
            },
        });
    }
    /**
     * Sprints do projeto
     * Listar sprints do projeto.
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public apiProjectsSprintsRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/{id}/sprints/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Dashboard do projeto
     * Fornece dados para o dashboard de um projeto específico, incluindo visualizações Kanban e Gantt
     * @param projetoId
     * @param projetoId ID do projeto
     * @returns ProjetoDashboardResponse
     * @throws ApiError
     */
    public apiProjectsDashboardRetrieve(
        projetoId: number,
        projetoId: number,
    ): CancelablePromise<ProjetoDashboardResponse> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/{projeto_id}/dashboard/',
            path: {
                'projeto_id': projetoId,
            },
            query: {
                'projeto_id': projetoId,
            },
        });
    }
    /**
     * Exportar dados do projeto
     * Exporta dados detalhados de um projeto específico em formatos CSV ou JSON. O usuário deve ser membro do projeto ou um administrador para acessá-lo. É possível selecionar diferentes seções de dados para incluir na exportação, como informações básicas do projeto, lista de tarefas, equipe, riscos e custos.
     * @param projetoId ID do projeto a ser exportado.
     * @param format Formato de exportação desejado. Opções: "csv" ou "json".
     * @param includeCosts Define se os custos associados ao projeto devem ser incluídos.
     * @param includeProject Define se os dados básicos do projeto devem ser incluídos.
     * @param includeRisks Define se os riscos associados ao projeto devem ser incluídos.
     * @param includeTasks Define se as tarefas (incluindo dados para Kanban e Gantt) do projeto devem ser incluídas.
     * @param includeTeam Define se os dados da equipe do projeto devem ser incluídos.
     * @returns binary
     * @throws ApiError
     */
    public apiProjectsExportarRetrieve(
        projetoId: number,
        format: string = 'csv',
        includeCosts: boolean = false,
        includeProject: boolean = true,
        includeRisks: boolean = false,
        includeTasks: boolean = true,
        includeTeam: boolean = false,
    ): CancelablePromise<Blob> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/{projeto_id}/exportar/',
            path: {
                'projeto_id': projetoId,
            },
            query: {
                'format': format,
                'include_costs': includeCosts,
                'include_project': includeProject,
                'include_risks': includeRisks,
                'include_tasks': includeTasks,
                'include_team': includeTeam,
            },
        });
    }
    /**
     * Visualização Gantt do projeto
     * Fornece dados para a visualização Gantt de um projeto, com tarefas e suas dependências
     * @param projetoId
     * @param projetoId ID do projeto
     * @returns GanttResponse
     * @throws ApiError
     */
    public apiProjectsGanttRetrieve(
        projetoId: number,
        projetoId: number,
    ): CancelablePromise<GanttResponse> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/{projeto_id}/gantt/',
            path: {
                'projeto_id': projetoId,
            },
            query: {
                'projeto_id': projetoId,
            },
        });
    }
    /**
     * Visualização Kanban do projeto
     * Fornece dados para a visualização Kanban de um projeto, com tarefas agrupadas por status
     * @param projetoId
     * @returns KanbanResponse
     * @throws ApiError
     */
    public apiProjectsKanbanRetrieve(
        projetoId: number,
    ): CancelablePromise<KanbanResponse> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/{projeto_id}/kanban/',
            path: {
                'projeto_id': projetoId,
            },
        });
    }
    /**
     * Atualizar Kanban do projeto
     * Atualiza os quadro Kanban de um projeto existente.
     * @param projetoId
     * @param requestBody
     * @returns KanbanResponse
     * @throws ApiError
     */
    public apiProjectsKanbanPartialUpdate(
        projetoId: number,
        requestBody?: PatchedKanbanResponseRequest,
    ): CancelablePromise<KanbanResponse> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/projects/{projeto_id}/kanban/',
            path: {
                'projeto_id': projetoId,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Criar tarefa no projeto
     * Cria uma nova tarefa no contexto de um projeto específico
     * @param projetoId
     * @param projetoId ID do projeto
     * @param requestBody
     * @returns Tarefa
     * @throws ApiError
     */
    public apiProjectsTarefasCriarCreate(
        projetoId: number,
        projetoId: number,
        requestBody: TarefaCreateRequest,
    ): CancelablePromise<Tarefa> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/projects/{projeto_id}/tarefas/criar/',
            path: {
                'projeto_id': projetoId,
            },
            query: {
                'projeto_id': projetoId,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Criar múltiplas tarefas no projeto
     * Cria múltiplas tarefas em lote no contexto de um projeto específico
     * @param projetoId
     * @param projetoId ID do projeto
     * @param requestBody
     * @returns any
     * @throws ApiError
     */
    public apiProjectsTarefasCriarMultiplasCreate(
        projetoId: number,
        projetoId: number,
        requestBody: TarefasBulkCreateRequest,
    ): CancelablePromise<Record<string, any>> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/projects/{projeto_id}/tarefas/criar-multiplas/',
            path: {
                'projeto_id': projetoId,
            },
            query: {
                'projeto_id': projetoId,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Listar meus projetos
     * Retorna os projetos dos quais o usuário é membro.
     * @param arquivado
     * @param atrasado Filtra projetos atrasados (data_fim < hoje e status != CONCLUIDO)
     * @param dataFimAntesAfter Filtra projetos com data de fim antes da data especificada
     * @param dataFimAntesBefore Filtra projetos com data de fim antes da data especificada
     * @param dataFimAposAfter Filtra projetos com data de fim após a data especificada
     * @param dataFimAposBefore Filtra projetos com data de fim após a data especificada
     * @param dataInicioAntesAfter Filtra projetos com data de início antes da data especificada
     * @param dataInicioAntesBefore Filtra projetos com data de início antes da data especificada
     * @param dataInicioAposAfter Filtra projetos com data de início após a data especificada
     * @param dataInicioAposBefore Filtra projetos com data de início após a data especificada
     * @param descricao Filtra por descrição (case insensitive)
     * @param membro Filtra projetos que contenham o membro especificado (ID do usuário)
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param prioridade Filtra por prioridade (pode ser múltiplas, separadas por vírgula)
     * @param search A search term.
     * @param status Filtra por status (pode ser múltiplos, separados por vírgula)
     * @param titulo Filtra por título (case insensitive)
     * @returns PaginatedProjetoList
     * @throws ApiError
     */
    public apiProjectsMyProjectsList(
        arquivado?: boolean,
        atrasado?: boolean,
        dataFimAntesAfter?: string,
        dataFimAntesBefore?: string,
        dataFimAposAfter?: string,
        dataFimAposBefore?: string,
        dataInicioAntesAfter?: string,
        dataInicioAntesBefore?: string,
        dataInicioAposAfter?: string,
        dataInicioAposBefore?: string,
        descricao?: string,
        membro?: string,
        ordering?: string,
        page?: number,
        prioridade?: string,
        search?: string,
        status?: string,
        titulo?: string,
    ): CancelablePromise<PaginatedProjetoList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/projects/my_projects/',
            query: {
                'arquivado': arquivado,
                'atrasado': atrasado,
                'data_fim_antes_after': dataFimAntesAfter,
                'data_fim_antes_before': dataFimAntesBefore,
                'data_fim_apos_after': dataFimAposAfter,
                'data_fim_apos_before': dataFimAposBefore,
                'data_inicio_antes_after': dataInicioAntesAfter,
                'data_inicio_antes_before': dataInicioAntesBefore,
                'data_inicio_apos_after': dataInicioAposAfter,
                'data_inicio_apos_before': dataInicioAposBefore,
                'descricao': descricao,
                'membro': membro,
                'ordering': ordering,
                'page': page,
                'prioridade': prioridade,
                'search': search,
                'status': status,
                'titulo': titulo,
            },
        });
    }
}
