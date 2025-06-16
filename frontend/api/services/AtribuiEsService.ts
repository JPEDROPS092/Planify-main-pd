/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AtribuicaoTarefa } from '../models/AtribuicaoTarefa';
import type { AtribuicaoTarefaRequest } from '../models/AtribuicaoTarefaRequest';
import type { PaginatedAtribuicaoTarefaList } from '../models/PaginatedAtribuicaoTarefaList';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AtribuiEsService {
    /**
     * Listar atribuições de tarefas
     * Retorna uma lista de atribuições de tarefas a usuários.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param tarefa Filtrar por ID da tarefa
     * @param usuario Filtrar por ID do usuário
     * @returns PaginatedAtribuicaoTarefaList
     * @throws ApiError
     */
    public static tasksAtribuicoesList(
        ordering?: string,
        page?: number,
        tarefa?: number,
        usuario?: number,
    ): CancelablePromise<PaginatedAtribuicaoTarefaList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/tasks/atribuicoes/',
            query: {
                'ordering': ordering,
                'page': page,
                'tarefa': tarefa,
                'usuario': usuario,
            },
        });
    }
    /**
     * Criar atribuição de tarefa
     * Atribui uma tarefa a um usuário.
     * @param requestBody
     * @returns AtribuicaoTarefa
     * @throws ApiError
     */
    public static tasksAtribuicoesCreate(
        requestBody: AtribuicaoTarefaRequest,
    ): CancelablePromise<AtribuicaoTarefa> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/tasks/atribuicoes/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes de atribuição
     * Retorna informações detalhadas de uma atribuição específica.
     * @param id A unique integer value identifying this Atribuição de Tarefa.
     * @returns AtribuicaoTarefa
     * @throws ApiError
     */
    public static tasksAtribuicoesRetrieve(
        id: number,
    ): CancelablePromise<AtribuicaoTarefa> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/tasks/atribuicoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Remover atribuição
     * Remove a atribuição de uma tarefa a um usuário.
     * @param id A unique integer value identifying this Atribuição de Tarefa.
     * @returns void
     * @throws ApiError
     */
    public static tasksAtribuicoesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/tasks/atribuicoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atribuir responsável à tarefa
     * Atribui um usuário como responsável pela tarefa.
     * @param id A unique integer value identifying this Tarefa.
     * @param requestBody
     * @returns AtribuicaoTarefa
     * @throws ApiError
     */
    public static tasksTarefasAtribuirResponsavelCreate(
        id: number,
        requestBody?: {
            /**
             * ID do usuário a ser atribuído como responsável
             */
            usuario_id: number;
        },
    ): CancelablePromise<AtribuicaoTarefa> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/tasks/tarefas/{id}/atribuir_responsavel/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Remover responsável da tarefa
     * Remove um usuário como responsável pela tarefa.
     * @param id A unique integer value identifying this Tarefa.
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public static tasksTarefasRemoverResponsavelCreate(
        id: number,
        requestBody?: {
            /**
             * ID do usuário a ser removido da tarefa
             */
            usuario_id: number;
        },
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/tasks/tarefas/{id}/remover_responsavel/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
}
