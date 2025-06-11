/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Documento } from '../models/Documento';
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
    public static apiDocumentsAssociarTarefaCreate(
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
}
