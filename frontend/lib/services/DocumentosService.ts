/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Comentario } from '../models/Comentario';
import type { ComentarioRequest } from '../models/ComentarioRequest';
import type { Documento } from '../models/Documento';
import type { DocumentoRequest } from '../models/DocumentoRequest';
import type { HistoricoDocumento } from '../models/HistoricoDocumento';
import type { PaginatedComentarioList } from '../models/PaginatedComentarioList';
import type { PaginatedDocumentoListList } from '../models/PaginatedDocumentoListList';
import type { PaginatedHistoricoDocumentoList } from '../models/PaginatedHistoricoDocumentoList';
import type { PatchedComentarioRequest } from '../models/PatchedComentarioRequest';
import type { PatchedDocumentoRequest } from '../models/PatchedDocumentoRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DocumentosService {
    /**
     * Listar documentos
     * Retorna a lista de todos os documentos com filtros opcionais.
     * @param enviadoPor Filtrar por ID do usuário que enviou
     * @param ordering Campo para ordenação (ex: data_upload, -titulo)
     * @param page A page number within the paginated result set.
     * @param projeto Filtrar por projeto (ID)
     * @param search Termo de busca para título, descrição ou tipo de arquivo
     * @param tarefa Filtrar por tarefa (ID)
     * @param texto Buscar por texto no título ou descrição
     * @param tipo Filtrar por tipo de documento
     * @param tipoArquivo Filtrar por tipo MIME do arquivo (ex: application/pdf)
     * @returns PaginatedDocumentoListList Lista de documentos recuperada com sucesso
     * @throws ApiError
     */
    public static apiDocumentsList(
        enviadoPor?: number,
        ordering?: string,
        page?: number,
        projeto?: number,
        search?: string,
        tarefa?: number,
        texto?: string,
        tipo?: 'ATA' | 'DESIGN' | 'MANUAL' | 'OUTRO' | 'RELATORIO' | 'REQUISITO',
        tipoArquivo?: string,
    ): CancelablePromise<PaginatedDocumentoListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/',
            query: {
                'enviado_por': enviadoPor,
                'ordering': ordering,
                'page': page,
                'projeto': projeto,
                'search': search,
                'tarefa': tarefa,
                'texto': texto,
                'tipo': tipo,
                'tipo_arquivo': tipoArquivo,
            },
        });
    }
    /**
     * Criar documento
     * Cria um novo documento no sistema.
     * @param requestBody
     * @returns Documento Documento criado com sucesso
     * @throws ApiError
     */
    public static apiDocumentsCreate(
        requestBody: DocumentoRequest,
    ): CancelablePromise<Documento> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/documents/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Dados inválidos`,
            },
        });
    }
    /**
     * Obter documento
     * Retorna os detalhes de um documento específico.
     * @param id A unique integer value identifying this Documento.
     * @returns Documento Detalhes do documento recuperados com sucesso
     * @throws ApiError
     */
    public static apiDocumentsRetrieve(
        id: number,
    ): CancelablePromise<Documento> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/{id}/',
            path: {
                'id': id,
            },
            errors: {
                404: `Documento não encontrado`,
            },
        });
    }
    /**
     * Atualizar documento
     * Atualiza todos os campos de um documento existente.
     * @param id A unique integer value identifying this Documento.
     * @param requestBody
     * @returns Documento Documento atualizado com sucesso
     * @throws ApiError
     */
    public static apiDocumentsUpdate(
        id: number,
        requestBody: DocumentoRequest,
    ): CancelablePromise<Documento> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/documents/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Dados inválidos`,
                404: `Documento não encontrado`,
            },
        });
    }
    /**
     * Atualizar documento parcialmente
     * Atualiza parcialmente um documento existente.
     * @param id A unique integer value identifying this Documento.
     * @param requestBody
     * @returns Documento Documento atualizado parcialmente com sucesso
     * @throws ApiError
     */
    public static apiDocumentsPartialUpdate(
        id: number,
        requestBody?: PatchedDocumentoRequest,
    ): CancelablePromise<Documento> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/documents/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Dados inválidos`,
                404: `Documento não encontrado`,
            },
        });
    }
    /**
     * Excluir documento
     * Remove um documento do sistema.
     * @param id A unique integer value identifying this Documento.
     * @returns void
     * @throws ApiError
     */
    public static apiDocumentsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/documents/{id}/',
            path: {
                'id': id,
            },
            errors: {
                404: `Documento não encontrado`,
            },
        });
    }
    /**
     * Adicionar comentário ao documento
     * Adiciona um novo comentário a um documento específico.
     * @param id A unique integer value identifying this Documento.
     * @param requestBody
     * @returns Comentario Comentário adicionado com sucesso
     * @throws ApiError
     */
    public static apiDocumentsAdicionarComentarioCreate(
        id: number,
        requestBody?: any,
    ): CancelablePromise<Comentario> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/documents/{id}/adicionar_comentario/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Dados inválidos (ex: texto não fornecido)`,
                404: `Documento não encontrado`,
            },
        });
    }
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
    /**
     * Histórico do documento
     * Retorna o histórico de versões do documento.
     * @param id A unique integer value identifying this Documento.
     * @returns PaginatedHistoricoDocumentoList Histórico de versões recuperado com sucesso
     * @throws ApiError
     */
    public static apiDocumentsHistoricoRetrieve2(
        id: number,
    ): CancelablePromise<PaginatedHistoricoDocumentoList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/{id}/historico/',
            path: {
                'id': id,
            },
            errors: {
                404: `Documento não encontrado`,
            },
        });
    }
    /**
     * Listar comentários de documentos
     * Retorna a lista de todos os comentários associados a documentos.
     * @param autor Filtrar por ID do autor do comentário
     * @param documento Filtrar por ID do documento ao qual o comentário pertence
     * @param ordering Campo para ordenação (ex: criado_em, -criado_em)
     * @param page A page number within the paginated result set.
     * @returns PaginatedComentarioList Lista de comentários recuperada com sucesso
     * @throws ApiError
     */
    public static apiDocumentsComentariosList(
        autor?: number,
        documento?: number,
        ordering?: string,
        page?: number,
    ): CancelablePromise<PaginatedComentarioList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/comentarios/',
            query: {
                'autor': autor,
                'documento': documento,
                'ordering': ordering,
                'page': page,
            },
        });
    }
    /**
     * Criar um novo comentário
     * Cria um novo comentário para um documento. O autor é automaticamente definido como o usuário autenticado.
     * @param requestBody
     * @returns Comentario Comentário criado com sucesso
     * @throws ApiError
     */
    public static apiDocumentsComentariosCreate(
        requestBody: ComentarioRequest,
    ): CancelablePromise<Comentario> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/documents/comentarios/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Dados inválidos`,
            },
        });
    }
    /**
     * Detalhes de um comentário
     * Retorna os detalhes de um comentário específico.
     * @param id A unique integer value identifying this Comentário.
     * @returns Comentario Detalhes do comentário recuperados com sucesso
     * @throws ApiError
     */
    public static apiDocumentsComentariosRetrieve(
        id: number,
    ): CancelablePromise<Comentario> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/documents/comentarios/{id}/',
            path: {
                'id': id,
            },
            errors: {
                404: `Comentário não encontrado`,
            },
        });
    }
    /**
     * Atualizar um comentário
     * Atualiza um comentário existente. Somente o autor do comentário ou um administrador pode atualizá-lo.
     * @param id A unique integer value identifying this Comentário.
     * @param requestBody
     * @returns Comentario Comentário atualizado com sucesso
     * @throws ApiError
     */
    public static apiDocumentsComentariosUpdate(
        id: number,
        requestBody: ComentarioRequest,
    ): CancelablePromise<Comentario> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/documents/comentarios/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Dados inválidos`,
                403: `Permissão negada para atualizar o comentário`,
                404: `Comentário não encontrado`,
            },
        });
    }
    /**
     * Atualizar parcialmente um comentário
     * Atualiza parcialmente um comentário existente. Somente o autor ou um administrador pode atualizá-lo.
     * @param id A unique integer value identifying this Comentário.
     * @param requestBody
     * @returns Comentario Comentário atualizado parcialmente com sucesso
     * @throws ApiError
     */
    public static apiDocumentsComentariosPartialUpdate(
        id: number,
        requestBody?: PatchedComentarioRequest,
    ): CancelablePromise<Comentario> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/documents/comentarios/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Dados inválidos`,
                403: `Permissão negada para atualizar o comentário`,
                404: `Comentário não encontrado`,
            },
        });
    }
    /**
     * Excluir um comentário
     * Remove um comentário do sistema. Somente o autor ou um administrador pode excluí-lo.
     * @param id A unique integer value identifying this Comentário.
     * @returns void
     * @throws ApiError
     */
    public static apiDocumentsComentariosDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/documents/comentarios/{id}/',
            path: {
                'id': id,
            },
            errors: {
                403: `Permissão negada para excluir o comentário`,
                404: `Comentário não encontrado`,
            },
        });
    }
    /**
     * Listar histórico de alterações de documentos
     * Retorna a lista de todas as alterações registradas para os documentos.
     * @param alteradoPor Filtrar por ID do usuário que realizou a alteração
     * @param documento Filtrar por ID do documento
     * @param page A page number within the paginated result set.
     * @returns PaginatedHistoricoDocumentoList Lista de histórico de documentos recuperada com sucesso
     * @throws ApiError
     */
    public static apiDocumentsHistoricoList(
        alteradoPor?: number,
        documento?: number,
        page?: number,
    ): CancelablePromise<PaginatedHistoricoDocumentoList> {
        return __request(OpenAPI, {
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
    public static apiDocumentsHistoricoRetrieve(
        id: number,
    ): CancelablePromise<HistoricoDocumento> {
        return __request(OpenAPI, {
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
