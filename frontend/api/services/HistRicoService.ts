/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { HistoricoDocumento } from '../models/HistoricoDocumento';
import type { PaginatedHistoricoDocumentoList } from '../models/PaginatedHistoricoDocumentoList';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class HistRicoService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Listar histórico de alterações de documentos
     * Retorna a lista de todas as alterações registradas para os documentos.
     * @param alteradoPor Filtrar por ID do usuário que realizou a alteração
     * @param documento Filtrar por ID do documento
     * @param page A page number within the paginated result set.
     * @returns PaginatedHistoricoDocumentoList Lista de histórico de documentos recuperada com sucesso
     * @throws ApiError
     */
    public apiDocumentsHistoricoList(
        alteradoPor?: number,
        documento?: number,
        page?: number,
    ): CancelablePromise<PaginatedHistoricoDocumentoList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/documents/historico/',
            query: {
                'alterado_por': alteradoPor,
                'documento': documento,
                'page': page,
            },
        });
    }
    /**
     * Detalhes de um registro de histórico
     * Retorna os detalhes de um registro específico do histórico de alterações de um documento.
     * @param id A unique integer value identifying this Histórico de Documento.
     * @returns HistoricoDocumento Detalhes do registro de histórico recuperados com sucesso
     * @throws ApiError
     */
    public apiDocumentsHistoricoRetrieve(
        id: number,
    ): CancelablePromise<HistoricoDocumento> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/documents/historico/{id}/',
            path: {
                'id': id,
            },
            errors: {
                404: `Registro de histórico não encontrado`,
            },
        });
    }
}
