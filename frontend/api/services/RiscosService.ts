/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { HistoricoRisco } from '../models/HistoricoRisco';
import type { PaginatedHistoricoRiscoList } from '../models/PaginatedHistoricoRiscoList';
import type { PaginatedRiscoList } from '../models/PaginatedRiscoList';
import type { PatchedRiscoRequest } from '../models/PatchedRiscoRequest';
import type { Risco } from '../models/Risco';
import type { RiscoList } from '../models/RiscoList';
import type { RiscoRequest } from '../models/RiscoRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class RiscosService {
    /**
     * Listar históricos do risco
     * Retorna uma lista paginada de históricos do risco.
     * @param alteradoPor
     * @param page A page number within the paginated result set.
     * @param risco
     * @returns PaginatedHistoricoRiscoList
     * @throws ApiError
     */
    public static risksHistoricoList(
        alteradoPor?: number,
        page?: number,
        risco?: number,
    ): CancelablePromise<PaginatedHistoricoRiscoList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/risks/historico/',
            query: {
                'alterado_por': alteradoPor,
                'page': page,
                'risco': risco,
            },
        });
    }
    /**
     * Obter detalhes do histórico do risco
     * Retorna o histórico detalhado de um risco específico.
     * @param id A unique integer value identifying this Histórico de Risco.
     * @returns HistoricoRisco
     * @throws ApiError
     */
    public static risksHistoricoRetrieve(
        id: number,
    ): CancelablePromise<HistoricoRisco> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/risks/historico/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar riscos
     * Retorna uma lista paginada de riscos.
     * @param impacto * `BAIXO` - Baixo
     * * `MEDIO` - Médio
     * * `ALTO` - Alto
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param probabilidade * `BAIXA` - Baixa
     * * `MEDIA` - Média
     * * `ALTA` - Alta
     * @param projeto
     * @param responsavelMitigacao
     * @param search A search term.
     * @param status * `IDENTIFICADO` - Identificado
     * * `EM_ANALISE` - Em Análise
     * * `MITIGADO` - Mitigado
     * * `ACEITO` - Aceito
     * * `ELIMINADO` - Eliminado
     * @returns PaginatedRiscoList
     * @throws ApiError
     */
    public static risksRiscosList(
        impacto?: 'ALTO' | 'BAIXO' | 'MEDIO',
        ordering?: string,
        page?: number,
        probabilidade?: 'ALTA' | 'BAIXA' | 'MEDIA',
        projeto?: number,
        responsavelMitigacao?: number,
        search?: string,
        status?: 'ACEITO' | 'ELIMINADO' | 'EM_ANALISE' | 'IDENTIFICADO' | 'MITIGADO',
    ): CancelablePromise<PaginatedRiscoList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/risks/riscos/',
            query: {
                'impacto': impacto,
                'ordering': ordering,
                'page': page,
                'probabilidade': probabilidade,
                'projeto': projeto,
                'responsavel_mitigacao': responsavelMitigacao,
                'search': search,
                'status': status,
            },
        });
    }
    /**
     * Criar novo risco
     * Cria um novo risco.
     * @param requestBody
     * @returns RiscoList
     * @throws ApiError
     */
    public static risksRiscosCreate(
        requestBody: RiscoRequest,
    ): CancelablePromise<RiscoList> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/risks/riscos/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do risco
     * Retorna informações detalhadas de um risco específico.
     * @param id A unique integer value identifying this Risco.
     * @returns Risco
     * @throws ApiError
     */
    public static risksRiscosRetrieve(
        id: number,
    ): CancelablePromise<Risco> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/risks/riscos/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar risco
     * Atualiza todos os campos de um risco existente.
     * @param id A unique integer value identifying this Risco.
     * @param requestBody
     * @returns Risco
     * @throws ApiError
     */
    public static risksRiscosUpdate(
        id: number,
        requestBody: RiscoRequest,
    ): CancelablePromise<Risco> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/risks/riscos/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar risco parcialmente
     * Atualiza parcialmente um risco existente.
     * @param id A unique integer value identifying this Risco.
     * @param requestBody
     * @returns Risco
     * @throws ApiError
     */
    public static risksRiscosPartialUpdate(
        id: number,
        requestBody?: PatchedRiscoRequest,
    ): CancelablePromise<Risco> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/risks/riscos/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir risco
     * Remove um risco existente.
     * @param id A unique integer value identifying this Risco.
     * @returns void
     * @throws ApiError
     */
    public static risksRiscosDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/risks/riscos/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar status do risco
     * Atualiza o status de um risco.
     * @param id A unique integer value identifying this Risco.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static risksRiscosAtualizarStatusCreate(
        id: number,
        requestBody: RiscoRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/risks/riscos/{id}/atualizar_status/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retorna histórico do risco
     * Retorna o histórico de alterações do risco.
     * @param id A unique integer value identifying this Risco.
     * @returns any No response body
     * @throws ApiError
     */
    public static risksRiscosHistoricoRetrieve(
        id: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/risks/riscos/{id}/historico/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Excluir múltiplos riscos
     * Exclui múltiplos riscos de uma vez.
     * @returns any No response body
     * @throws ApiError
     */
    public static risksRiscosExcluirVariosDestroy(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/risks/riscos/excluir_varios/',
        });
    }
}
