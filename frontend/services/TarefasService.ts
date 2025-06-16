/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AtribuicaoTarefa } from '../models/AtribuicaoTarefa';
import type { AtribuicaoTarefaRequest } from '../models/AtribuicaoTarefaRequest';
import type { ComentarioTarefa } from '../models/ComentarioTarefa';
import type { ComentarioTarefaRequest } from '../models/ComentarioTarefaRequest';
import type { Documento } from '../models/Documento';
import type { PaginatedAtribuicaoTarefaList } from '../models/PaginatedAtribuicaoTarefaList';
import type { PaginatedComentarioTarefaList } from '../models/PaginatedComentarioTarefaList';
import type { PaginatedHistoricoStatusTarefaList } from '../models/PaginatedHistoricoStatusTarefaList';
import type { PatchedComentarioTarefaRequest } from '../models/PatchedComentarioTarefaRequest';
import type { PatchedTarefaRequest } from '../models/PatchedTarefaRequest';
import type { Tarefa } from '../models/Tarefa';
import type { TarefaRequest } from '../models/TarefaRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class TarefasService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Associar documento a uma tarefa
     * Associa ou desassocia um documento a uma tarefa específica. Forneça 'tarefa_id' para associar, ou 'tarefa_id: 0' (ou nulo) para desassociar.
     * @param id A unique integer value identifying this Documento.
     * @param requestBody
     * @returns Documento Documento associado/desassociado com sucesso
     * @throws ApiError
     */
    public apiDocumentsAssociarTarefaCreate(
        id: number,
        requestBody?: any,
    ): CancelablePromise<Documento> {
        return this.httpRequest.request({
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
     * Listar atribuições de tarefas
     * Retorna uma lista de atribuições de tarefas a usuários.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param tarefa Filtrar por ID da tarefa
     * @param usuario Filtrar por ID do usuário
     * @returns PaginatedAtribuicaoTarefaList
     * @throws ApiError
     */
    public apiTasksAtribuicoesList(
        ordering?: string,
        page?: number,
        tarefa?: number,
        usuario?: number,
    ): CancelablePromise<PaginatedAtribuicaoTarefaList> {
        return this.httpRequest.request({
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
    public apiTasksAtribuicoesCreate(
        requestBody: AtribuicaoTarefaRequest,
    ): CancelablePromise<AtribuicaoTarefa> {
        return this.httpRequest.request({
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
    public apiTasksAtribuicoesRetrieve(
        id: number,
    ): CancelablePromise<AtribuicaoTarefa> {
        return this.httpRequest.request({
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
    public apiTasksAtribuicoesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/tasks/atribuicoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar comentários de tarefas
     * Retorna uma lista de comentários de tarefas.
     * @param autor Filtrar por ID do autor
     * @param ordering Ordenar resultados (ex: -criado_em)
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @param tarefa Filtrar por ID da tarefa
     * @returns PaginatedComentarioTarefaList
     * @throws ApiError
     */
    public apiTasksComentariosList(
        autor?: number,
        ordering?: string,
        page?: number,
        search?: string,
        tarefa?: number,
    ): CancelablePromise<PaginatedComentarioTarefaList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/tasks/comentarios/',
            query: {
                'autor': autor,
                'ordering': ordering,
                'page': page,
                'search': search,
                'tarefa': tarefa,
            },
        });
    }
    /**
     * Criar comentário
     * Adiciona um novo comentário a uma tarefa.
     * @param requestBody
     * @returns ComentarioTarefa
     * @throws ApiError
     */
    public apiTasksComentariosCreate(
        requestBody: ComentarioTarefaRequest,
    ): CancelablePromise<ComentarioTarefa> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/tasks/comentarios/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes de comentário
     * Retorna informações detalhadas de um comentário específico.
     * @param id A unique integer value identifying this Comentário.
     * @returns ComentarioTarefa
     * @throws ApiError
     */
    public apiTasksComentariosRetrieve(
        id: number,
    ): CancelablePromise<ComentarioTarefa> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/tasks/comentarios/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar comentário
     * Atualiza o texto de um comentário existente.
     * @param id A unique integer value identifying this Comentário.
     * @param requestBody
     * @returns ComentarioTarefa
     * @throws ApiError
     */
    public apiTasksComentariosUpdate(
        id: number,
        requestBody: ComentarioTarefaRequest,
    ): CancelablePromise<ComentarioTarefa> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/tasks/comentarios/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar comentário parcialmente
     * Atualiza parcialmente o texto de um comentário existente.
     * @param id A unique integer value identifying this Comentário.
     * @param requestBody
     * @returns ComentarioTarefa
     * @throws ApiError
     */
    public apiTasksComentariosPartialUpdate(
        id: number,
        requestBody?: PatchedComentarioTarefaRequest,
    ): CancelablePromise<ComentarioTarefa> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/tasks/comentarios/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir comentário
     * Remove permanentemente um comentário.
     * @param id A unique integer value identifying this Comentário.
     * @returns void
     * @throws ApiError
     */
    public apiTasksComentariosDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/tasks/comentarios/{id}/',
            path: {
                'id': id,
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
    public apiTasksTarefasCreate(
        requestBody: TarefaRequest,
    ): CancelablePromise<Tarefa> {
        return this.httpRequest.request({
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
    public apiTasksTarefasRetrieve(
        id: number,
    ): CancelablePromise<Tarefa> {
        return this.httpRequest.request({
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
    public apiTasksTarefasUpdate(
        id: number,
        requestBody: TarefaRequest,
    ): CancelablePromise<Tarefa> {
        return this.httpRequest.request({
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
    public apiTasksTarefasPartialUpdate(
        id: number,
        requestBody?: PatchedTarefaRequest,
    ): CancelablePromise<Tarefa> {
        return this.httpRequest.request({
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
    public apiTasksTarefasDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
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
    public apiTasksTarefasAdicionarComentarioCreate(
        id: number,
        requestBody?: {
            /**
             * Texto do comentário
             */
            texto: string;
        },
    ): CancelablePromise<ComentarioTarefa> {
        return this.httpRequest.request({
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
    public apiTasksTarefasAssociarSprintCreate(
        id: number,
        requestBody?: {
            /**
             * ID da sprint a ser associada. Use 0 ou null para remover a associação.
             */
            sprint_id: number | null;
        },
    ): CancelablePromise<Tarefa> {
        return this.httpRequest.request({
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
     * Atribuir responsável à tarefa
     * Atribui um usuário como responsável pela tarefa.
     * @param id A unique integer value identifying this Tarefa.
     * @param requestBody
     * @returns AtribuicaoTarefa
     * @throws ApiError
     */
    public apiTasksTarefasAtribuirResponsavelCreate(
        id: number,
        requestBody?: {
            /**
             * ID do usuário a ser atribuído como responsável
             */
            usuario_id: number;
        },
    ): CancelablePromise<AtribuicaoTarefa> {
        return this.httpRequest.request({
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
     * Atualizar status da tarefa
     * Atualiza o status de uma tarefa e registra a alteração no histórico.
     * @param id A unique integer value identifying this Tarefa.
     * @param requestBody
     * @returns Tarefa
     * @throws ApiError
     */
    public apiTasksTarefasAtualizarStatusCreate(
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
        return this.httpRequest.request({
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
    public apiTasksTarefasHistoricoStatusList(
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
        return this.httpRequest.request({
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
    /**
     * Remover responsável da tarefa
     * Remove um usuário como responsável pela tarefa.
     * @param id A unique integer value identifying this Tarefa.
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public apiTasksTarefasRemoverResponsavelCreate(
        id: number,
        requestBody?: {
            /**
             * ID do usuário a ser removido da tarefa
             */
            usuario_id: number;
        },
    ): CancelablePromise<void> {
        return this.httpRequest.request({
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
