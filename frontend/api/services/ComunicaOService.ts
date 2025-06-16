/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ChatMensagem } from '../models/ChatMensagem';
import type { ChatMensagemRequest } from '../models/ChatMensagemRequest';
import type { ConfiguracaoNotificacao } from '../models/ConfiguracaoNotificacao';
import type { ConfiguracaoNotificacaoRequest } from '../models/ConfiguracaoNotificacaoRequest';
import type { Notificacao } from '../models/Notificacao';
import type { NotificacaoRequest } from '../models/NotificacaoRequest';
import type { PaginatedChatMensagemList } from '../models/PaginatedChatMensagemList';
import type { PaginatedConfiguracaoNotificacaoList } from '../models/PaginatedConfiguracaoNotificacaoList';
import type { PaginatedNotificacaoList } from '../models/PaginatedNotificacaoList';
import type { PatchedChatMensagemRequest } from '../models/PatchedChatMensagemRequest';
import type { PatchedConfiguracaoNotificacaoRequest } from '../models/PatchedConfiguracaoNotificacaoRequest';
import type { PatchedNotificacaoRequest } from '../models/PatchedNotificacaoRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ComunicaOService {
    /**
     * Listar configurações
     * Retorna uma lista paginada de configurações.
     * @param page A page number within the paginated result set.
     * @returns PaginatedConfiguracaoNotificacaoList
     * @throws ApiError
     */
    public static communicationsConfiguracoesList(
        page?: number,
    ): CancelablePromise<PaginatedConfiguracaoNotificacaoList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/configuracoes/',
            query: {
                'page': page,
            },
        });
    }
    /**
     * Criar nova configuração
     * Cria um nova configuração.
     * @param requestBody
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static communicationsConfiguracoesCreate(
        requestBody: ConfiguracaoNotificacaoRequest,
    ): CancelablePromise<ConfiguracaoNotificacao> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/communications/configuracoes/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes da configuração
     * Retorna informações detalhadas de uma configuração específica.
     * @param id A unique integer value identifying this Configuração de Notificação.
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static communicationsConfiguracoesRetrieve(
        id: number,
    ): CancelablePromise<ConfiguracaoNotificacao> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/configuracoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar configuração
     * Atualiza todos os campos de uma configuração existente.
     * @param id A unique integer value identifying this Configuração de Notificação.
     * @param requestBody
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static communicationsConfiguracoesUpdate(
        id: number,
        requestBody: ConfiguracaoNotificacaoRequest,
    ): CancelablePromise<ConfiguracaoNotificacao> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/communications/configuracoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar configuração parcialmente
     * Atualiza parcialmente uma configuração existente.
     * @param id A unique integer value identifying this Configuração de Notificação.
     * @param requestBody
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static communicationsConfiguracoesPartialUpdate(
        id: number,
        requestBody?: PatchedConfiguracaoNotificacaoRequest,
    ): CancelablePromise<ConfiguracaoNotificacao> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/communications/configuracoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir configuração
     * Remove uma configuração existente.
     * @param id A unique integer value identifying this Configuração de Notificação.
     * @returns void
     * @throws ApiError
     */
    public static communicationsConfiguracoesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/communications/configuracoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Ver minha configuração
     * Retorna a configuração do usuário atual ou cria uma padrão se não existir.
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static communicationsConfiguracoesMinhaConfiguracaoRetrieve(): CancelablePromise<ConfiguracaoNotificacao> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/configuracoes/minha_configuracao/',
        });
    }
    /**
     * Listar mensagens
     * Retorna uma lista paginada de mensagens.
     * @param autor
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param projeto
     * @returns PaginatedChatMensagemList
     * @throws ApiError
     */
    public static communicationsMensagensList(
        autor?: number,
        ordering?: string,
        page?: number,
        projeto?: number,
    ): CancelablePromise<PaginatedChatMensagemList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/mensagens/',
            query: {
                'autor': autor,
                'ordering': ordering,
                'page': page,
                'projeto': projeto,
            },
        });
    }
    /**
     * Criar nova mensagem
     * Cria um nova mensagem.
     * @param requestBody
     * @returns ChatMensagem
     * @throws ApiError
     */
    public static communicationsMensagensCreate(
        requestBody: ChatMensagemRequest,
    ): CancelablePromise<ChatMensagem> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/communications/mensagens/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes da mensagem
     * Retorna informações detalhadas de uma mensagem específica.
     * @param id A unique integer value identifying this Mensagem de Chat.
     * @returns ChatMensagem
     * @throws ApiError
     */
    public static communicationsMensagensRetrieve(
        id: number,
    ): CancelablePromise<ChatMensagem> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/mensagens/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar mensagem
     * Atualiza todos os campos de uma mensagem existente.
     * @param id A unique integer value identifying this Mensagem de Chat.
     * @param requestBody
     * @returns ChatMensagem
     * @throws ApiError
     */
    public static communicationsMensagensUpdate(
        id: number,
        requestBody: ChatMensagemRequest,
    ): CancelablePromise<ChatMensagem> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/communications/mensagens/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar mensagem parcialmente
     * Atualiza parcialmente uma mensagem existente.
     * @param id A unique integer value identifying this Mensagem de Chat.
     * @param requestBody
     * @returns ChatMensagem
     * @throws ApiError
     */
    public static communicationsMensagensPartialUpdate(
        id: number,
        requestBody?: PatchedChatMensagemRequest,
    ): CancelablePromise<ChatMensagem> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/communications/mensagens/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir mensagem
     * Remove uma mensagem existente.
     * @param id A unique integer value identifying this Mensagem de Chat.
     * @returns void
     * @throws ApiError
     */
    public static communicationsMensagensDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/communications/mensagens/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Marcar mensagem como lida
     * Marca uma mensagem como lida pelo usuário atual.
     *
     * Args:
     * request: Objeto de requisição
     * pk: ID da mensagem a ser marcada como lida
     *
     * Returns:
     * Response: Detalhes do registro de leitura ou mensagem de status
     * @param id A unique integer value identifying this Mensagem de Chat.
     * @param requestBody
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static communicationsMensagensMarcarComoLidaCreate(
        id: number,
        requestBody: ChatMensagemRequest,
    ): CancelablePromise<ConfiguracaoNotificacao> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/communications/mensagens/{id}/marcar_como_lida/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Listar mensagens não lidas
     * Retorna as mensagens não lidas pelo usuário atual.
     *
     * Suporta filtro por projeto através do parâmetro 'projeto' na query string.
     * Exclui mensagens enviadas pelo próprio usuário, pois estas não precisam ser lidas.
     *
     * Args:
     * request: Objeto de requisição
     *
     * Returns:
     * Response: Lista de mensagens não lidas
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static communicationsMensagensMensagensNaoLidasRetrieve(): CancelablePromise<ConfiguracaoNotificacao> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/mensagens/mensagens_nao_lidas/',
        });
    }
    /**
     * Listar notificações
     * Retorna uma lista paginada de notificações.
     * @param lida
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param prioridade Nível de prioridade da notificação
     *
     * * `BAIXA` - Baixa
     * * `MEDIA` - Média
     * * `ALTA` - Alta
     * @param projeto
     * @param tarefa
     * @param tipo Tipo de objeto relacionado à notificação
     *
     * * `TAREFA` - Tarefa
     * * `PROJETO` - Projeto
     * * `EQUIPE` - Equipe
     * * `RISCO` - Risco
     * * `DOCUMENTO` - Documento
     * * `SISTEMA` - Sistema
     * @returns PaginatedNotificacaoList
     * @throws ApiError
     */
    public static communicationsNotificacoesList(
        lida?: boolean,
        ordering?: string,
        page?: number,
        prioridade?: 'ALTA' | 'BAIXA' | 'MEDIA',
        projeto?: number,
        tarefa?: number,
        tipo?: 'DOCUMENTO' | 'EQUIPE' | 'PROJETO' | 'RISCO' | 'SISTEMA' | 'TAREFA',
    ): CancelablePromise<PaginatedNotificacaoList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/notificacoes/',
            query: {
                'lida': lida,
                'ordering': ordering,
                'page': page,
                'prioridade': prioridade,
                'projeto': projeto,
                'tarefa': tarefa,
                'tipo': tipo,
            },
        });
    }
    /**
     * Criar nova notificação
     * Cria um nova notificação.
     * @param requestBody
     * @returns Notificacao
     * @throws ApiError
     */
    public static communicationsNotificacoesCreate(
        requestBody: NotificacaoRequest,
    ): CancelablePromise<Notificacao> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/communications/notificacoes/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes da notificação
     * Retorna informações detalhadas de uma notificação específica.
     * @param id A unique integer value identifying this Notificação.
     * @returns Notificacao
     * @throws ApiError
     */
    public static communicationsNotificacoesRetrieve(
        id: number,
    ): CancelablePromise<Notificacao> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/notificacoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar notificação
     * Atualiza todos os campos de uma notificação existente.
     * @param id A unique integer value identifying this Notificação.
     * @param requestBody
     * @returns Notificacao
     * @throws ApiError
     */
    public static communicationsNotificacoesUpdate(
        id: number,
        requestBody: NotificacaoRequest,
    ): CancelablePromise<Notificacao> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/communications/notificacoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar notificação parcialmente
     * Atualiza parcialmente uma notificação existente.
     * @param id A unique integer value identifying this Notificação.
     * @param requestBody
     * @returns Notificacao
     * @throws ApiError
     */
    public static communicationsNotificacoesPartialUpdate(
        id: number,
        requestBody?: PatchedNotificacaoRequest,
    ): CancelablePromise<Notificacao> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/communications/notificacoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir notificação
     * Remove uma notificação existente.
     * @param id A unique integer value identifying this Notificação.
     * @returns void
     * @throws ApiError
     */
    public static communicationsNotificacoesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/communications/notificacoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Marcar notificação como lida
     * Marca uma notificação como lida.
     *
     * Define o campo 'lida' como True e registra a data/hora em 'lida_em'.
     *
     * Args:
     * request: Objeto de requisição
     * pk: ID da notificação a ser marcada como lida
     *
     * Returns:
     * Response: Detalhes da notificação atualizada ou mensagem de status
     * @param id A unique integer value identifying this Notificação.
     * @param requestBody
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static communicationsNotificacoesMarcarComoLidaCreate(
        id: number,
        requestBody: NotificacaoRequest,
    ): CancelablePromise<ConfiguracaoNotificacao> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/communications/notificacoes/{id}/marcar_como_lida/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Marcar todas as notificações como lidas
     * Marca todas as notificações não lidas do usuário como lidas.
     *
     * Atualiza em massa todas as notificações não lidas do usuário atual,
     * definindo 'lida' como True e 'lida_em' como a data/hora atual.
     *
     * Args:
     * request: Objeto de requisição
     *
     * Returns:
     * Response: Mensagem de confirmação com o número de notificações atualizadas
     * @param requestBody
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static communicationsNotificacoesMarcarTodasComoLidasCreate(
        requestBody: NotificacaoRequest,
    ): CancelablePromise<ConfiguracaoNotificacao> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/communications/notificacoes/marcar_todas_como_lidas/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Listar notificações não lidas
     * Retorna apenas as notificações não lidas do usuário.
     *
     * Suporta filtros adicionais por tipo e prioridade através de parâmetros na query string.
     *
     * Args:
     * request: Objeto de requisição
     *
     * Returns:
     * Response: Lista de notificações não lidas filtradas
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static communicationsNotificacoesNaoLidasRetrieve(): CancelablePromise<ConfiguracaoNotificacao> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/notificacoes/nao_lidas/',
        });
    }
}
