/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AtribuicaoTarefa } from '../models/AtribuicaoTarefa';
import type { AtribuicaoTarefaRequest } from '../models/AtribuicaoTarefaRequest';
import type { PatchedAtribuicaoTarefaRequest } from '../models/PatchedAtribuicaoTarefaRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class TasksService {
    /**
     * ViewSet para gerenciamento de atribuições de tarefas a usuários.
     *
     * Permite criar, listar, visualizar e remover atribuições de tarefas a usuários.
     * O usuário que faz a atribuição é automaticamente registrado.
     * @param id A unique integer value identifying this Atribuição de Tarefa.
     * @param requestBody
     * @returns AtribuicaoTarefa
     * @throws ApiError
     */
    public static tasksAtribuicoesUpdate(
        id: number,
        requestBody: AtribuicaoTarefaRequest,
    ): CancelablePromise<AtribuicaoTarefa> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/tasks/atribuicoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de atribuições de tarefas a usuários.
     *
     * Permite criar, listar, visualizar e remover atribuições de tarefas a usuários.
     * O usuário que faz a atribuição é automaticamente registrado.
     * @param id A unique integer value identifying this Atribuição de Tarefa.
     * @param requestBody
     * @returns AtribuicaoTarefa
     * @throws ApiError
     */
    public static tasksAtribuicoesPartialUpdate(
        id: number,
        requestBody?: PatchedAtribuicaoTarefaRequest,
    ): CancelablePromise<AtribuicaoTarefa> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/tasks/atribuicoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
}
