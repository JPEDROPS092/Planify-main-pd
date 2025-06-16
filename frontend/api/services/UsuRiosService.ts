/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaginatedUserList } from '../models/PaginatedUserList';
import type { PatchedUserRequest } from '../models/PatchedUserRequest';
import type { User } from '../models/User';
import type { UserCreate } from '../models/UserCreate';
import type { UserCreateRequest } from '../models/UserCreateRequest';
import type { UserRequest } from '../models/UserRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UsuRiosService {
    /**
     * Listar usuários
     * Retorna uma lista paginada de usuários.
     * @param page A page number within the paginated result set.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public static authUsersList(
        page?: number,
    ): CancelablePromise<PaginatedUserList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/users/',
            query: {
                'page': page,
            },
        });
    }
    /**
     * Criar novo usuário
     * Cria um novo usuário.
     * @param requestBody
     * @returns UserCreate
     * @throws ApiError
     */
    public static authUsersCreate(
        requestBody: UserCreateRequest,
    ): CancelablePromise<UserCreate> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do usuário
     * Retorna informações detalhadas de um usuário específico.
     * @param id A unique integer value identifying this user.
     * @returns User
     * @throws ApiError
     */
    public static authUsersRetrieve(
        id: number,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/users/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar usuário
     * Atualiza todos os campos de um usuário existente.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static authUsersUpdate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/auth/users/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar usuário parcialmente
     * Atualiza parcialmente um usuário existente.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static authUsersPartialUpdate(
        id: number,
        requestBody?: PatchedUserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/auth/users/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir usuário
     * Remove um usuário existente.
     * @param id A unique integer value identifying this user.
     * @returns void
     * @throws ApiError
     */
    public static authUsersDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/auth/users/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Ativar usuário
     * Ativa um usuário inativo.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static authUsersActivateCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/{id}/activate/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Desativar usuário
     * Desativa um usuário ativo.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static authUsersDeactivateCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/{id}/deactivate/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Redefinir senha
     * Redefine a senha do usuário para uma senha temporária.
     * @param id
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static authUsersResetPasswordCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/{id}/reset-password/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Redefinir senha
     * Redefine a senha do usuário para uma senha temporária.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static authUsersResetPasswordCreate2(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/{id}/reset_password/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Desbloquear usuário
     * Desbloqueia um usuário após tentativas de login malsucedidas.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static authUsersUnlockCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/{id}/unlock/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
}
