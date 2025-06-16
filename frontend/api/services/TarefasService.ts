/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ComentarioTarefa } from '../models/ComentarioTarefa';
import type { Documento } from '../models/Documento';
import type { PaginatedHistoricoStatusTarefaList } from '../models/PaginatedHistoricoStatusTarefaList';
import type { PaginatedTarefaListList } from '../models/PaginatedTarefaListList';
import type { PatchedTarefaRequest } from '../models/PatchedTarefaRequest';
import type { Tarefa } from '../models/Tarefa';
import type { TarefaRequest } from '../models/TarefaRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class TarefasService {
    /**
     * Associar documento a uma tarefa
     * Associa ou desassocia um documento a uma tarefa específica. Forneça 'tarefa_id' para associar, ou 'tarefa_id: 0' (ou nulo) para desassociar.
     * @param id A unique integer value identifying this Documento.
     * @param requestBody
     * @returns Documento Documento associado/desassociado com sucesso
     * @throws ApiError
     */
    public static documentsAssociarTarefaCreate(
        id: number,
        requestBody?: any,
    ): CancelablePromise<Documento> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/documents/{id}/associar_tarefa/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Dados inválidos (ex: tarefa_id não fornecido)`,
                404: `Documento ou Tarefa não encontrada`,
            },
        });
    }
    /**
     * Listar tarefas
     * Retorna uma lista paginada de tarefas com opções de filtragem e ordenação.
     * @param atrasada Filtrar tarefas atrasadas
     * @param dataInicioAntesAfter Filtra tarefas com data de início antes da data especificada
     * @param dataInicioAntesBefore Filtra tarefas com data de início antes da data especificada
     * @param dataInicioAposAfter Filtra tarefas com data de início após a data especificada
     * @param dataInicioAposBefore Filtra tarefas com data de início após a data especificada
     * @param dataTerminoAntesAfter Filtra tarefas com data de término antes da data especificada
     * @param dataTerminoAntesBefore Filtra tarefas com data de término antes da data especificada
     * @param dataTerminoAposAfter Filtra tarefas com data de término após a data especificada
     * @param dataTerminoAposBefore Filtra tarefas com data de término após a data especificada
     * @param descricao Filtra por descrição (case insensitive)
     * @param minhasTarefas Filtrar minhas tarefas
     * @param ordering Ordenar resultados (ex: -data_termino)
     * @param page A page number within the paginated result set.
     * @param prioridade Filtrar por prioridade (separadas por vírgula)
     * @param projeto Filtrar por ID do projeto
     * @param responsavel Filtrar por ID do usuário responsável
     * @param search A search term.
     * @param semResponsavel Filtra tarefas sem responsáveis atribuídos
     * @param semSprint Filtrar tarefas sem sprint
     * @param sprint Filtrar por ID da sprint
     * @param status Filtrar por status (separados por vírgula)
     * @param titulo Filtra por título (case insensitive)
     * @returns PaginatedTarefaListList
     * @throws ApiError
     */
    public static tasksTarefasList(
        atrasada?: boolean,
        dataInicioAntesAfter?: string,
        dataInicioAntesBefore?: string,
        dataInicioAposAfter?: string,
        dataInicioAposBefore?: string,
        dataTerminoAntesAfter?: string,
        dataTerminoAntesBefore?: string,
        dataTerminoAposAfter?: string,
        dataTerminoAposBefore?: string,
        descricao?: string,
        minhasTarefas?: boolean,
        ordering?: string,
        page?: number,
        prioridade?: string,
        projeto?: number,
        responsavel?: number,
        search?: string,
        semResponsavel?: boolean,
        semSprint?: boolean,
        sprint?: number,
        status?: string,
        titulo?: string,
    ): CancelablePromise<PaginatedTarefaListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/tasks/tarefas/',
            query: {
                'atrasada': atrasada,
                'data_inicio_antes_after': dataInicioAntesAfter,
                'data_inicio_antes_before': dataInicioAntesBefore,
                'data_inicio_apos_after': dataInicioAposAfter,
                'data_inicio_apos_before': dataInicioAposBefore,
                'data_termino_antes_after': dataTerminoAntesAfter,
                'data_termino_antes_before': dataTerminoAntesBefore,
                'data_termino_apos_after': dataTerminoAposAfter,
                'data_termino_apos_before': dataTerminoAposBefore,
                'descricao': descricao,
                'minhas_tarefas': minhasTarefas,
                'ordering': ordering,
                'page': page,
                'prioridade': prioridade,
                'projeto': projeto,
                'responsavel': responsavel,
                'search': search,
                'sem_responsavel': semResponsavel,
                'sem_sprint': semSprint,
                'sprint': sprint,
                'status': status,
                'titulo': titulo,
            },
        });
    }
    /**
     * Criar tarefa
     * Cria uma nova tarefa com os dados fornecidos.
     * @param requestBody
     * @returns Tarefa
     * @throws ApiError
     */
    public static tasksTarefasCreate(
        requestBody: TarefaRequest,
    ): CancelablePromise<Tarefa> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/tasks/tarefas/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes da tarefa
     * Retorna informações detalhadas de uma tarefa específica.
     * @param id A unique integer value identifying this Tarefa.
     * @returns Tarefa
     * @throws ApiError
     */
    public static tasksTarefasRetrieve(
        id: number,
    ): CancelablePromise<Tarefa> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/tasks/tarefas/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar tarefa
     * Atualiza todos os campos de uma tarefa existente.
     * @param id A unique integer value identifying this Tarefa.
     * @param requestBody
     * @returns Tarefa
     * @throws ApiError
     */
    public static tasksTarefasUpdate(
        id: number,
        requestBody: TarefaRequest,
    ): CancelablePromise<Tarefa> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/tasks/tarefas/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar tarefa parcialmente
     * Atualiza parcialmente os campos de uma tarefa existente.
     * @param id A unique integer value identifying this Tarefa.
     * @param requestBody
     * @returns Tarefa
     * @throws ApiError
     */
    public static tasksTarefasPartialUpdate(
        id: number,
        requestBody?: PatchedTarefaRequest,
    ): CancelablePromise<Tarefa> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/tasks/tarefas/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir tarefa
     * Remove permanentemente uma tarefa.
     * @param id A unique integer value identifying this Tarefa.
     * @returns void
     * @throws ApiError
     */
    public static tasksTarefasDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/tasks/tarefas/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Adicionar comentário à tarefa
     * Adiciona um novo comentário à tarefa.
     * @param id A unique integer value identifying this Tarefa.
     * @param requestBody
     * @returns ComentarioTarefa
     * @throws ApiError
     */
    public static tasksTarefasAdicionarComentarioCreate(
        id: number,
        requestBody?: {
            /**
             * Texto do comentário
             */
            texto: string;
        },
    ): CancelablePromise<ComentarioTarefa> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/tasks/tarefas/{id}/adicionar_comentario/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Associar tarefa a uma sprint
     * Associa a tarefa a uma sprint ou remove a associação existente.
     * @param id A unique integer value identifying this Tarefa.
     * @param requestBody
     * @returns Tarefa
     * @throws ApiError
     */
    public static tasksTarefasAssociarSprintCreate(
        id: number,
        requestBody?: {
            /**
             * ID da sprint a ser associada. Use 0 ou null para remover a associação.
             */
            sprint_id: number | null;
        },
    ): CancelablePromise<Tarefa> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/tasks/tarefas/{id}/associar_sprint/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar status da tarefa
     * Atualiza o status de uma tarefa e registra a alteração no histórico.
     * @param id A unique integer value identifying this Tarefa.
     * @param requestBody
     * @returns Tarefa
     * @throws ApiError
     */
    public static tasksTarefasAtualizarStatusCreate(
        id: number,
        requestBody?: {
            /**
             * Novo status da tarefa (A_FAZER, EM_ANDAMENTO, FEITO, BLOQUEADO, CANCELADO)
             */
            status: string;
            /**
             * Comentário opcional sobre a mudança de status
             */
            comentario?: string;
        },
    ): CancelablePromise<Tarefa> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/tasks/tarefas/{id}/atualizar_status/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter histórico de status da tarefa
     * Retorna o histórico de alterações de status da tarefa.
     * @param id A unique integer value identifying this Tarefa.
     * @param atrasada Filtra tarefas atrasadas (data_termino < hoje e status != FEITO)
     * @param dataInicioAntesAfter Filtra tarefas com data de início antes da data especificada
     * @param dataInicioAntesBefore Filtra tarefas com data de início antes da data especificada
     * @param dataInicioAposAfter Filtra tarefas com data de início após a data especificada
     * @param dataInicioAposBefore Filtra tarefas com data de início após a data especificada
     * @param dataTerminoAntesAfter Filtra tarefas com data de término antes da data especificada
     * @param dataTerminoAntesBefore Filtra tarefas com data de término antes da data especificada
     * @param dataTerminoAposAfter Filtra tarefas com data de término após a data especificada
     * @param dataTerminoAposBefore Filtra tarefas com data de término após a data especificada
     * @param descricao Filtra por descrição (case insensitive)
     * @param minhasTarefas Filtra tarefas do usuário autenticado
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param prioridade Filtra por prioridade (pode ser múltiplas, separadas por vírgula)
     * @param projeto
     * @param responsavel Filtra tarefas pelo ID do usuário responsável
     * @param search A search term.
     * @param semResponsavel Filtra tarefas sem responsáveis atribuídos
     * @param semSprint Filtra tarefas que não estão associadas a nenhuma sprint
     * @param sprint
     * @param status Filtra por status (pode ser múltiplos, separados por vírgula)
     * @param titulo Filtra por título (case insensitive)
     * @returns PaginatedHistoricoStatusTarefaList
     * @throws ApiError
     */
    public static tasksTarefasHistoricoStatusList(
        id: number,
        atrasada?: boolean,
        dataInicioAntesAfter?: string,
        dataInicioAntesBefore?: string,
        dataInicioAposAfter?: string,
        dataInicioAposBefore?: string,
        dataTerminoAntesAfter?: string,
        dataTerminoAntesBefore?: string,
        dataTerminoAposAfter?: string,
        dataTerminoAposBefore?: string,
        descricao?: string,
        minhasTarefas?: boolean,
        ordering?: string,
        page?: number,
        prioridade?: string,
        projeto?: number,
        responsavel?: string,
        search?: string,
        semResponsavel?: boolean,
        semSprint?: boolean,
        sprint?: number,
        status?: string,
        titulo?: string,
    ): CancelablePromise<PaginatedHistoricoStatusTarefaList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/tasks/tarefas/{id}/historico_status/',
            path: {
                'id': id,
            },
            query: {
                'atrasada': atrasada,
                'data_inicio_antes_after': dataInicioAntesAfter,
                'data_inicio_antes_before': dataInicioAntesBefore,
                'data_inicio_apos_after': dataInicioAposAfter,
                'data_inicio_apos_before': dataInicioAposBefore,
                'data_termino_antes_after': dataTerminoAntesAfter,
                'data_termino_antes_before': dataTerminoAntesBefore,
                'data_termino_apos_after': dataTerminoAposAfter,
                'data_termino_apos_before': dataTerminoAposBefore,
                'descricao': descricao,
                'minhas_tarefas': minhasTarefas,
                'ordering': ordering,
                'page': page,
                'prioridade': prioridade,
                'projeto': projeto,
                'responsavel': responsavel,
                'search': search,
                'sem_responsavel': semResponsavel,
                'sem_sprint': semSprint,
                'sprint': sprint,
                'status': status,
                'titulo': titulo,
            },
        });
    }
}
