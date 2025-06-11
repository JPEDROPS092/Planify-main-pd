/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Comentario } from '../models/Comentario';
import type { ComentarioRequest } from '../models/ComentarioRequest';
import type { PaginatedComentarioList } from '../models/PaginatedComentarioList';
import type { PatchedComentarioRequest } from '../models/PatchedComentarioRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ComentRiosService {
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
}
