/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AccessProfileRequest } from '../types/AccessProfileRequest';
import type { MembroEquipe } from '../types/MembroEquipe';
import type { MembroEquipeRequest } from '../types/MembroEquipeRequest';
import type { PaginatedMembroEquipeList } from '../types/PaginatedMembroEquipeList';
import type { PaginatedUserList } from '../types/PaginatedUserList';
import type { PatchedAccessProfileRequest } from '../types/PatchedAccessProfileRequest';
import type { PatchedMembroEquipeRequest } from '../types/PatchedMembroEquipeRequest';
import type { PatchedPermissionRequest } from '../types/PatchedPermissionRequest';
import type { PatchedUserProfileRequest } from '../types/PatchedUserProfileRequest';
import type { PatchedUserRequest } from '../types/PatchedUserRequest';
import type { PermissionRequest } from '../types/PermissionRequest';
import type { User } from '../types/User';
import type { UserCreate } from '../types/UserCreate';
import type { UserCreateRequest } from '../types/UserCreateRequest';
import type { UserProfileRequest } from '../types/UserProfileRequest';
import type { UserRequest } from '../types/UserRequest';
import type { CancelablePromise } from '../api/core/CancelablePromise';
import type { BaseHttpRequest } from '../api/core/BaseHttpRequest';
export class AuthService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Listar perfis de acesso
     * Retorna uma lista paginada de perfis de acesso.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public apiAuthAccessProfilesList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/auth/access-profiles/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * Criar novo perfil de acesso
     * Cria um novo perfil de acesso.
     * @param requestBody
     * @returns UserCreate
     * @throws ApiError
     */
    public apiAuthAccessProfilesCreate(
        requestBody: AccessProfileRequest,
    ): CancelablePromise<UserCreate> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/auth/access-profiles/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do perfil de acesso
     * Retorna informações detalhadas de um perfil de acesso específico.
     * @param id A unique integer value identifying this access profile.
     * @returns User
     * @throws ApiError
     */
    public apiAuthAccessProfilesRetrieve(
        id: number,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/auth/access-profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar perfil de acesso
     * Atualiza todos os campos de um perfil de acesso existente.
     * @param id A unique integer value identifying this access profile.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiAuthAccessProfilesUpdate(
        id: number,
        requestBody: AccessProfileRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/auth/access-profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar perfil de acesso parcialmente
     * Atualiza parcialmente um perfil de acesso existente.
     * @param id A unique integer value identifying this access profile.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiAuthAccessProfilesPartialUpdate(
        id: number,
        requestBody?: PatchedAccessProfileRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/auth/access-profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir perfil de acesso
     * Remove um perfil de acesso existente.
     * @param id A unique integer value identifying this access profile.
     * @returns void
     * @throws ApiError
     */
    public apiAuthAccessProfilesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/auth/access-profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar permissões
     * Retorna uma lista paginada de permissões.
     * @param accessProfile
     * @param action * `VIEW` - View
     * * `CREATE` - Create
     * * `EDIT` - Edit
     * * `DELETE` - Delete
     * * `APPROVE` - Approve
     * * `ASSIGN` - Assign
     * * `EXPORT` - Export
     * * `IMPORT` - Import
     * * `COMMENT` - Comment
     * @param module * `PROJECTS` - Projects
     * * `TASKS` - Tasks
     * * `TEAMS` - Teams
     * * `RESOURCES` - Resources
     * * `COMMUNICATIONS` - Communications
     * * `RISKS` - Risks
     * * `COSTS` - Costs
     * * `DOCUMENTS` - Documents
     * * `REPORTS` - Reports
     * * `USERS` - Users
     * * `SETTINGS` - Settings
     * * `DASHBOARD` - Dashboard
     * * `NOTIFICATIONS` - Notifications
     * * `APPROVALS` - Approvals
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public apiAuthPermissionsList(
        accessProfile?: number,
        action?: 'APPROVE' | 'ASSIGN' | 'COMMENT' | 'CREATE' | 'DELETE' | 'EDIT' | 'EXPORT' | 'IMPORT' | 'VIEW',
        module?: 'APPROVALS' | 'COMMUNICATIONS' | 'COSTS' | 'DASHBOARD' | 'DOCUMENTS' | 'NOTIFICATIONS' | 'PROJECTS' | 'REPORTS' | 'RESOURCES' | 'RISKS' | 'SETTINGS' | 'TASKS' | 'TEAMS' | 'USERS',
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/auth/permissions/',
            query: {
                'access_profile': accessProfile,
                'action': action,
                'module': module,
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * Criar nova permissão
     * Cria uma nova permissão.
     * @param requestBody
     * @returns UserCreate
     * @throws ApiError
     */
    public apiAuthPermissionsCreate(
        requestBody: PermissionRequest,
    ): CancelablePromise<UserCreate> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/auth/permissions/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do permissão
     * Retorna informações detalhadas de uma permissão específica.
     * @param id A unique integer value identifying this permission.
     * @returns User
     * @throws ApiError
     */
    public apiAuthPermissionsRetrieve(
        id: number,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/auth/permissions/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar permissão
     * Atualiza todos os campos de uma permissão existente.
     * @param id A unique integer value identifying this permission.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiAuthPermissionsUpdate(
        id: number,
        requestBody: PermissionRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/auth/permissions/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar permissão parcialmente
     * Atualiza parcialmente uma permissão existente.
     * @param id A unique integer value identifying this permission.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiAuthPermissionsPartialUpdate(
        id: number,
        requestBody?: PatchedPermissionRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/auth/permissions/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir permissão
     * Remove uma permissão existente.
     * @param id A unique integer value identifying this permission.
     * @returns void
     * @throws ApiError
     */
    public apiAuthPermissionsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/auth/permissions/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar perfis
     * Retorna uma lista paginada de perfis.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public apiAuthProfilesList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/auth/profiles/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * Criar novo perfil
     * Cria um novo perfil.
     * @param requestBody
     * @returns UserCreate
     * @throws ApiError
     */
    public apiAuthProfilesCreate(
        requestBody?: UserProfileRequest,
    ): CancelablePromise<UserCreate> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/auth/profiles/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do perfil
     * Retorna informações detalhadas de um perfil específico.
     * @param id A unique integer value identifying this user profile.
     * @returns User
     * @throws ApiError
     */
    public apiAuthProfilesRetrieve(
        id: number,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/auth/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar perfil
     * Atualiza todos os campos de um perfil existente.
     * @param id A unique integer value identifying this user profile.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiAuthProfilesUpdate(
        id: number,
        requestBody?: UserProfileRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/auth/profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar perfil parcialmente
     * Atualiza parcialmente um perfil existente.
     * @param id A unique integer value identifying this user profile.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiAuthProfilesPartialUpdate(
        id: number,
        requestBody?: PatchedUserProfileRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/auth/profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir perfil
     * Remove um perfil existente.
     * @param id A unique integer value identifying this user profile.
     * @returns void
     * @throws ApiError
     */
    public apiAuthProfilesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/auth/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar usuários
     * Retorna uma lista paginada de usuários.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public apiAuthUsersList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/auth/users/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
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
    public apiAuthUsersCreate(
        requestBody: UserCreateRequest,
    ): CancelablePromise<UserCreate> {
        return this.httpRequest.request({
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
    public apiAuthUsersRetrieve(
        id: number,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
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
    public apiAuthUsersUpdate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
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
    public apiAuthUsersPartialUpdate(
        id: number,
        requestBody?: PatchedUserRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
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
    public apiAuthUsersDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/auth/users/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Ativar usuário
     * Ativa um usuário.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiAuthUsersActivateCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
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
     * Desativa um usuário.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiAuthUsersDeactivateCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
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
     * Redefinir senha de usuário específico
     * Redefine a senha do usuário para uma senha temporária e envia por e-mail.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiAuthUsersResetUserPasswordCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/auth/users/{id}/reset_user_password/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Desbloqueia um usuário
     * Desbloqueia um usuário após tentativas de login malsucedidas.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiAuthUsersUnlockCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/auth/users/{id}/unlock/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Alterar a minha senha
     * Altera a senha do usuário autenticado.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiAuthUsersChangePasswordCreate(
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/auth/users/change_password/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retornar minhas informações
     * Retorna as informações do usuário autenticado.
     * @returns any No response body
     * @throws ApiError
     */
    public apiAuthUsersMeRetrieve(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/auth/users/me/',
        });
    }
    /**
     * Retornar minhas permissões
     * Retorna as permissões do usuário autenticado.
     * @returns any No response body
     * @throws ApiError
     */
    public apiAuthUsersPermissionsRetrieve(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/auth/users/permissions/',
        });
    }
    /**
     * Listar membros de equipe
     * Retorna uma lista paginada de membros de equipe.
     * @param equipe
     * @param page A page number within the paginated result set.
     * @param papel * `PO` - Product Owner
     * * `SM` - Scrum Master
     * * `DEV` - Desenvolvedor
     * * `QA` - Analista de Qualidade
     * * `DESIGN` - Designer
     * * `ANALISTA` - Analista
     * @param usuario
     * @returns PaginatedMembroEquipeList
     * @throws ApiError
     */
    public apiTeamsMembrosList(
        equipe?: number,
        page?: number,
        papel?: 'ANALISTA' | 'DESIGN' | 'DEV' | 'PO' | 'QA' | 'SM',
        usuario?: number,
    ): CancelablePromise<PaginatedMembroEquipeList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/teams/membros/',
            query: {
                'equipe': equipe,
                'page': page,
                'papel': papel,
                'usuario': usuario,
            },
        });
    }
    /**
     * Criar novo membro de equipe
     * Cria um novo membro de equipe.
     * @param requestBody
     * @returns MembroEquipe
     * @throws ApiError
     */
    public apiTeamsMembrosCreate(
        requestBody: MembroEquipeRequest,
    ): CancelablePromise<MembroEquipe> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/teams/membros/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do membros de equipe
     * Retorna informações detalhadas de um membro de equipe específico.
     * @param id A unique integer value identifying this Membro da Equipe.
     * @returns MembroEquipe
     * @throws ApiError
     */
    public apiTeamsMembrosRetrieve(
        id: number,
    ): CancelablePromise<MembroEquipe> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/teams/membros/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar membro de equipe
     * Atualiza todos os campos de um membro de equipe existente.
     * @param id A unique integer value identifying this Membro da Equipe.
     * @param requestBody
     * @returns MembroEquipe
     * @throws ApiError
     */
    public apiTeamsMembrosUpdate(
        id: number,
        requestBody: MembroEquipeRequest,
    ): CancelablePromise<MembroEquipe> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/teams/membros/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar membro de equipe parcialmente
     * Atualiza parcialmente um membro de equipe existente.
     * @param id A unique integer value identifying this Membro da Equipe.
     * @param requestBody
     * @returns MembroEquipe
     * @throws ApiError
     */
    public apiTeamsMembrosPartialUpdate(
        id: number,
        requestBody?: PatchedMembroEquipeRequest,
    ): CancelablePromise<MembroEquipe> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/teams/membros/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir membro de equipe
     * Remove um membro de equipe existente.
     * @param id A unique integer value identifying this Membro da Equipe.
     * @returns void
     * @throws ApiError
     */
    public apiTeamsMembrosDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/teams/membros/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar perfis de acesso
     * Retorna uma lista paginada de perfis de acesso.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public apiUsersAccessProfilesList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/access-profiles/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * Criar novo perfil de acesso
     * Cria um novo perfil de acesso.
     * @param requestBody
     * @returns UserCreate
     * @throws ApiError
     */
    public apiUsersAccessProfilesCreate(
        requestBody: AccessProfileRequest,
    ): CancelablePromise<UserCreate> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/users/access-profiles/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do perfil de acesso
     * Retorna informações detalhadas de um perfil de acesso específico.
     * @param id A unique integer value identifying this access profile.
     * @returns User
     * @throws ApiError
     */
    public apiUsersAccessProfilesRetrieve(
        id: number,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/access-profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar perfil de acesso
     * Atualiza todos os campos de um perfil de acesso existente.
     * @param id A unique integer value identifying this access profile.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiUsersAccessProfilesUpdate(
        id: number,
        requestBody: AccessProfileRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/users/access-profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar perfil de acesso parcialmente
     * Atualiza parcialmente um perfil de acesso existente.
     * @param id A unique integer value identifying this access profile.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiUsersAccessProfilesPartialUpdate(
        id: number,
        requestBody?: PatchedAccessProfileRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/users/access-profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir perfil de acesso
     * Remove um perfil de acesso existente.
     * @param id A unique integer value identifying this access profile.
     * @returns void
     * @throws ApiError
     */
    public apiUsersAccessProfilesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/users/access-profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar permissões
     * Retorna uma lista paginada de permissões.
     * @param accessProfile
     * @param action * `VIEW` - View
     * * `CREATE` - Create
     * * `EDIT` - Edit
     * * `DELETE` - Delete
     * * `APPROVE` - Approve
     * * `ASSIGN` - Assign
     * * `EXPORT` - Export
     * * `IMPORT` - Import
     * * `COMMENT` - Comment
     * @param module * `PROJECTS` - Projects
     * * `TASKS` - Tasks
     * * `TEAMS` - Teams
     * * `RESOURCES` - Resources
     * * `COMMUNICATIONS` - Communications
     * * `RISKS` - Risks
     * * `COSTS` - Costs
     * * `DOCUMENTS` - Documents
     * * `REPORTS` - Reports
     * * `USERS` - Users
     * * `SETTINGS` - Settings
     * * `DASHBOARD` - Dashboard
     * * `NOTIFICATIONS` - Notifications
     * * `APPROVALS` - Approvals
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public apiUsersPermissionsList(
        accessProfile?: number,
        action?: 'APPROVE' | 'ASSIGN' | 'COMMENT' | 'CREATE' | 'DELETE' | 'EDIT' | 'EXPORT' | 'IMPORT' | 'VIEW',
        module?: 'APPROVALS' | 'COMMUNICATIONS' | 'COSTS' | 'DASHBOARD' | 'DOCUMENTS' | 'NOTIFICATIONS' | 'PROJECTS' | 'REPORTS' | 'RESOURCES' | 'RISKS' | 'SETTINGS' | 'TASKS' | 'TEAMS' | 'USERS',
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/permissions/',
            query: {
                'access_profile': accessProfile,
                'action': action,
                'module': module,
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * Criar nova permissão
     * Cria uma nova permissão.
     * @param requestBody
     * @returns UserCreate
     * @throws ApiError
     */
    public apiUsersPermissionsCreate(
        requestBody: PermissionRequest,
    ): CancelablePromise<UserCreate> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/users/permissions/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do permissão
     * Retorna informações detalhadas de uma permissão específica.
     * @param id A unique integer value identifying this permission.
     * @returns User
     * @throws ApiError
     */
    public apiUsersPermissionsRetrieve(
        id: number,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/permissions/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar permissão
     * Atualiza todos os campos de uma permissão existente.
     * @param id A unique integer value identifying this permission.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiUsersPermissionsUpdate(
        id: number,
        requestBody: PermissionRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/users/permissions/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar permissão parcialmente
     * Atualiza parcialmente uma permissão existente.
     * @param id A unique integer value identifying this permission.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiUsersPermissionsPartialUpdate(
        id: number,
        requestBody?: PatchedPermissionRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/users/permissions/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir permissão
     * Remove uma permissão existente.
     * @param id A unique integer value identifying this permission.
     * @returns void
     * @throws ApiError
     */
    public apiUsersPermissionsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/users/permissions/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar perfis
     * Retorna uma lista paginada de perfis.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public apiUsersProfilesList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/profiles/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * Criar novo perfil
     * Cria um novo perfil.
     * @param requestBody
     * @returns UserCreate
     * @throws ApiError
     */
    public apiUsersProfilesCreate(
        requestBody?: UserProfileRequest,
    ): CancelablePromise<UserCreate> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/users/profiles/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do perfil
     * Retorna informações detalhadas de um perfil específico.
     * @param id A unique integer value identifying this user profile.
     * @returns User
     * @throws ApiError
     */
    public apiUsersProfilesRetrieve(
        id: number,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar perfil
     * Atualiza todos os campos de um perfil existente.
     * @param id A unique integer value identifying this user profile.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiUsersProfilesUpdate(
        id: number,
        requestBody?: UserProfileRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/users/profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar perfil parcialmente
     * Atualiza parcialmente um perfil existente.
     * @param id A unique integer value identifying this user profile.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiUsersProfilesPartialUpdate(
        id: number,
        requestBody?: PatchedUserProfileRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/users/profiles/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir perfil
     * Remove um perfil existente.
     * @param id A unique integer value identifying this user profile.
     * @returns void
     * @throws ApiError
     */
    public apiUsersProfilesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/users/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar usuários
     * Retorna uma lista paginada de usuários.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public apiUsersUsersList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/users/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
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
    public apiUsersUsersCreate(
        requestBody: UserCreateRequest,
    ): CancelablePromise<UserCreate> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/users/users/',
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
    public apiUsersUsersRetrieve(
        id: number,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/users/{id}/',
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
    public apiUsersUsersUpdate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/users/users/{id}/',
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
    public apiUsersUsersPartialUpdate(
        id: number,
        requestBody?: PatchedUserRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/users/users/{id}/',
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
    public apiUsersUsersDestroy(
        id: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/users/users/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Ativar usuário
     * Ativa um usuário.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiUsersUsersActivateCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/users/users/{id}/activate/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Desativar usuário
     * Desativa um usuário.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiUsersUsersDeactivateCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/users/users/{id}/deactivate/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Redefinir senha de usuário específico
     * Redefine a senha do usuário para uma senha temporária e envia por e-mail.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiUsersUsersResetUserPasswordCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/users/users/{id}/reset_user_password/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Desbloqueia um usuário
     * Desbloqueia um usuário após tentativas de login malsucedidas.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiUsersUsersUnlockCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/users/users/{id}/unlock/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Alterar a minha senha
     * Altera a senha do usuário autenticado.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiUsersUsersChangePasswordCreate(
        requestBody: UserRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/users/users/change_password/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retornar minhas informações
     * Retorna as informações do usuário autenticado.
     * @returns any No response body
     * @throws ApiError
     */
    public apiUsersUsersMeRetrieve(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/users/me/',
        });
    }
    /**
     * Retornar minhas permissões
     * Retorna as permissões do usuário autenticado.
     * @returns any No response body
     * @throws ApiError
     */
    public apiUsersUsersPermissionsRetrieve(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/users/users/permissions/',
        });
    }
}
