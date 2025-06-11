/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class SaDeDoSistemaService {
    /**
     * Verificação de Saúde Simples
     * Endpoint simples para verificar se a API está operacional. Retorna 'ok' se estiver tudo certo.
     * @returns any API está operacional.
     * @throws ApiError
     */
    public static verificacaoSaudeSimples(): CancelablePromise<{
        status?: string;
    }> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/health/',
        });
    }
    /**
     * Verificação de Saúde Detalhada
     * Endpoint para verificar o estado da API, incluindo versão e ambiente. Não requer autenticação.
     * @returns any API está operacional com detalhes.
     * @throws ApiError
     */
    public static verificacaoSaudeDetalhada(): CancelablePromise<{
        status?: string;
        versao?: string;
        ambiente?: string;
        data_hora?: string;
    }> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/health/detailed/',
        });
    }
}
