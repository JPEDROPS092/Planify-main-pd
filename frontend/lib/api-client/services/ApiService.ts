/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AccessProfile } from '../models/AccessProfile';
import type { AccessProfileRequest } from '../models/AccessProfileRequest';
import type { Activation } from '../models/Activation';
import type { ActivationRequest } from '../models/ActivationRequest';
import type { Alerta } from '../models/Alerta';
import type { AlertaRequest } from '../models/AlertaRequest';
import type { AtribuicaoTarefa } from '../models/AtribuicaoTarefa';
import type { AtribuicaoTarefaRequest } from '../models/AtribuicaoTarefaRequest';
import type { Categoria } from '../models/Categoria';
import type { CategoriaRequest } from '../models/CategoriaRequest';
import type { ChatMensagem } from '../models/ChatMensagem';
import type { ChatMensagemRequest } from '../models/ChatMensagemRequest';
import type { ComentarioTarefa } from '../models/ComentarioTarefa';
import type { ComentarioTarefaRequest } from '../models/ComentarioTarefaRequest';
import type { ConfiguracaoNotificacao } from '../models/ConfiguracaoNotificacao';
import type { ConfiguracaoNotificacaoRequest } from '../models/ConfiguracaoNotificacaoRequest';
import type { Custo } from '../models/Custo';
import type { CustomTokenObtainPairRequest } from '../models/CustomTokenObtainPairRequest';
import type { CustoRequest } from '../models/CustoRequest';
import type { Equipe } from '../models/Equipe';
import type { EquipeRequest } from '../models/EquipeRequest';
import type { HistoricoRisco } from '../models/HistoricoRisco';
import type { MembroEquipe } from '../models/MembroEquipe';
import type { MembroEquipeRequest } from '../models/MembroEquipeRequest';
import type { MembroProjeto } from '../models/MembroProjeto';
import type { MembroProjetoRequest } from '../models/MembroProjetoRequest';
import type { Notificacao } from '../models/Notificacao';
import type { NotificacaoRequest } from '../models/NotificacaoRequest';
import type { OrcamentoProjeto } from '../models/OrcamentoProjeto';
import type { OrcamentoProjetoRequest } from '../models/OrcamentoProjetoRequest';
import type { OrcamentoTarefa } from '../models/OrcamentoTarefa';
import type { OrcamentoTarefaRequest } from '../models/OrcamentoTarefaRequest';
import type { PaginatedAccessProfileList } from '../models/PaginatedAccessProfileList';
import type { PaginatedAlertaList } from '../models/PaginatedAlertaList';
import type { PaginatedAtribuicaoTarefaList } from '../models/PaginatedAtribuicaoTarefaList';
import type { PaginatedCategoriaList } from '../models/PaginatedCategoriaList';
import type { PaginatedChatMensagemList } from '../models/PaginatedChatMensagemList';
import type { PaginatedComentarioTarefaList } from '../models/PaginatedComentarioTarefaList';
import type { PaginatedConfiguracaoNotificacaoList } from '../models/PaginatedConfiguracaoNotificacaoList';
import type { PaginatedCustoListList } from '../models/PaginatedCustoListList';
import type { PaginatedEquipeListList } from '../models/PaginatedEquipeListList';
import type { PaginatedHistoricoRiscoList } from '../models/PaginatedHistoricoRiscoList';
import type { PaginatedHistoricoStatusTarefaList } from '../models/PaginatedHistoricoStatusTarefaList';
import type { PaginatedMembroEquipeList } from '../models/PaginatedMembroEquipeList';
import type { PaginatedMembroProjetoList } from '../models/PaginatedMembroProjetoList';
import type { PaginatedNotificacaoList } from '../models/PaginatedNotificacaoList';
import type { PaginatedOrcamentoProjetoList } from '../models/PaginatedOrcamentoProjetoList';
import type { PaginatedOrcamentoTarefaList } from '../models/PaginatedOrcamentoTarefaList';
import type { PaginatedPermissaoEquipeList } from '../models/PaginatedPermissaoEquipeList';
import type { PaginatedPermissionList } from '../models/PaginatedPermissionList';
import type { PaginatedProjetoListList } from '../models/PaginatedProjetoListList';
import type { PaginatedRiscoListList } from '../models/PaginatedRiscoListList';
import type { PaginatedTarefaListList } from '../models/PaginatedTarefaListList';
import type { PaginatedUserList } from '../models/PaginatedUserList';
import type { PaginatedUserProfileList } from '../models/PaginatedUserProfileList';
import type { PatchedAccessProfileRequest } from '../models/PatchedAccessProfileRequest';
import type { PatchedAlertaRequest } from '../models/PatchedAlertaRequest';
import type { PatchedAtribuicaoTarefaRequest } from '../models/PatchedAtribuicaoTarefaRequest';
import type { PatchedCategoriaRequest } from '../models/PatchedCategoriaRequest';
import type { PatchedChatMensagemRequest } from '../models/PatchedChatMensagemRequest';
import type { PatchedComentarioTarefaRequest } from '../models/PatchedComentarioTarefaRequest';
import type { PatchedConfiguracaoNotificacaoRequest } from '../models/PatchedConfiguracaoNotificacaoRequest';
import type { PatchedCustoRequest } from '../models/PatchedCustoRequest';
import type { PatchedEquipeRequest } from '../models/PatchedEquipeRequest';
import type { PatchedMembroEquipeRequest } from '../models/PatchedMembroEquipeRequest';
import type { PatchedNotificacaoRequest } from '../models/PatchedNotificacaoRequest';
import type { PatchedOrcamentoProjetoRequest } from '../models/PatchedOrcamentoProjetoRequest';
import type { PatchedOrcamentoTarefaRequest } from '../models/PatchedOrcamentoTarefaRequest';
import type { PatchedPermissaoEquipeRequest } from '../models/PatchedPermissaoEquipeRequest';
import type { PatchedPermissionRequest } from '../models/PatchedPermissionRequest';
import type { PatchedProjetoRequest } from '../models/PatchedProjetoRequest';
import type { PatchedRiscoRequest } from '../models/PatchedRiscoRequest';
import type { PatchedTarefaRequest } from '../models/PatchedTarefaRequest';
import type { PatchedUserProfileRequest } from '../models/PatchedUserProfileRequest';
import type { PatchedUserRequest } from '../models/PatchedUserRequest';
import type { PermissaoEquipe } from '../models/PermissaoEquipe';
import type { PermissaoEquipeRequest } from '../models/PermissaoEquipeRequest';
import type { Permission } from '../models/Permission';
import type { PermissionRequest } from '../models/PermissionRequest';
import type { Projeto } from '../models/Projeto';
import type { ProjetoRequest } from '../models/ProjetoRequest';
import type { ResetPassword } from '../models/ResetPassword';
import type { ResetPasswordRequest } from '../models/ResetPasswordRequest';
import type { Risco } from '../models/Risco';
import type { RiscoRequest } from '../models/RiscoRequest';
import type { SendEmailReset } from '../models/SendEmailReset';
import type { SendEmailResetRequest } from '../models/SendEmailResetRequest';
import type { SetNewPassword } from '../models/SetNewPassword';
import type { SetNewPasswordRequest } from '../models/SetNewPasswordRequest';
import type { SetPasswordRetype } from '../models/SetPasswordRetype';
import type { SetPasswordRetypeRequest } from '../models/SetPasswordRetypeRequest';
import type { SetUsername } from '../models/SetUsername';
import type { SetUsernameRequest } from '../models/SetUsernameRequest';
import type { Tarefa } from '../models/Tarefa';
import type { TarefaRequest } from '../models/TarefaRequest';
import type { TokenRefresh } from '../models/TokenRefresh';
import type { TokenRefreshRequest } from '../models/TokenRefreshRequest';
import type { User } from '../models/User';
import type { UserCreate } from '../models/UserCreate';
import type { UserCreateRequest } from '../models/UserCreateRequest';
import type { UsernameResetConfirm } from '../models/UsernameResetConfirm';
import type { UsernameResetConfirmRequest } from '../models/UsernameResetConfirmRequest';
import type { UserProfile } from '../models/UserProfile';
import type { UserProfileRequest } from '../models/UserProfileRequest';
import type { UserRequest } from '../models/UserRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ApiService {
    /**
     * ViewSet para gerenciamento de perfis de acesso.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedAccessProfileList
     * @throws ApiError
     */
    public static apiAuthAccessProfilesList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedAccessProfileList> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de perfis de acesso.
     * @param requestBody
     * @returns AccessProfile
     * @throws ApiError
     */
    public static apiAuthAccessProfilesCreate(
        requestBody: AccessProfileRequest,
    ): CancelablePromise<AccessProfile> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/access-profiles/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de perfis de acesso.
     * @param id A unique integer value identifying this access profile.
     * @returns AccessProfile
     * @throws ApiError
     */
    public static apiAuthAccessProfilesRetrieve(
        id: number,
    ): CancelablePromise<AccessProfile> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/access-profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de perfis de acesso.
     * @param id A unique integer value identifying this access profile.
     * @param requestBody
     * @returns AccessProfile
     * @throws ApiError
     */
    public static apiAuthAccessProfilesUpdate(
        id: number,
        requestBody: AccessProfileRequest,
    ): CancelablePromise<AccessProfile> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de perfis de acesso.
     * @param id A unique integer value identifying this access profile.
     * @param requestBody
     * @returns AccessProfile
     * @throws ApiError
     */
    public static apiAuthAccessProfilesPartialUpdate(
        id: number,
        requestBody?: PatchedAccessProfileRequest,
    ): CancelablePromise<AccessProfile> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de perfis de acesso.
     * @param id A unique integer value identifying this access profile.
     * @returns void
     * @throws ApiError
     */
    public static apiAuthAccessProfilesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/auth/access-profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de permissões.
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
     * @returns PaginatedPermissionList
     * @throws ApiError
     */
    public static apiAuthPermissionsList(
        accessProfile?: number,
        action?: 'APPROVE' | 'ASSIGN' | 'COMMENT' | 'CREATE' | 'DELETE' | 'EDIT' | 'EXPORT' | 'IMPORT' | 'VIEW',
        module?: 'APPROVALS' | 'COMMUNICATIONS' | 'COSTS' | 'DASHBOARD' | 'DOCUMENTS' | 'NOTIFICATIONS' | 'PROJECTS' | 'REPORTS' | 'RESOURCES' | 'RISKS' | 'SETTINGS' | 'TASKS' | 'TEAMS' | 'USERS',
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedPermissionList> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de permissões.
     * @param requestBody
     * @returns Permission
     * @throws ApiError
     */
    public static apiAuthPermissionsCreate(
        requestBody: PermissionRequest,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/permissions/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de permissões.
     * @param id A unique integer value identifying this permission.
     * @returns Permission
     * @throws ApiError
     */
    public static apiAuthPermissionsRetrieve(
        id: number,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/permissions/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de permissões.
     * @param id A unique integer value identifying this permission.
     * @param requestBody
     * @returns Permission
     * @throws ApiError
     */
    public static apiAuthPermissionsUpdate(
        id: number,
        requestBody: PermissionRequest,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de permissões.
     * @param id A unique integer value identifying this permission.
     * @param requestBody
     * @returns Permission
     * @throws ApiError
     */
    public static apiAuthPermissionsPartialUpdate(
        id: number,
        requestBody?: PatchedPermissionRequest,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de permissões.
     * @param id A unique integer value identifying this permission.
     * @returns void
     * @throws ApiError
     */
    public static apiAuthPermissionsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/auth/permissions/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserProfileList
     * @throws ApiError
     */
    public static apiAuthProfilesList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserProfileList> {
        return __request(OpenAPI, {
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
     * @param requestBody
     * @returns UserProfile
     * @throws ApiError
     */
    public static apiAuthProfilesCreate(
        requestBody?: UserProfileRequest,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/profiles/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id
     * @returns UserProfile
     * @throws ApiError
     */
    public static apiAuthProfilesRetrieve(
        id: string,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id
     * @param requestBody
     * @returns UserProfile
     * @throws ApiError
     */
    public static apiAuthProfilesUpdate(
        id: string,
        requestBody?: UserProfileRequest,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
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
     * @param id
     * @param requestBody
     * @returns UserProfile
     * @throws ApiError
     */
    public static apiAuthProfilesPartialUpdate(
        id: string,
        requestBody?: PatchedUserProfileRequest,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
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
     * @param id
     * @returns void
     * @throws ApiError
     */
    public static apiAuthProfilesDestroy(
        id: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/auth/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Takes a set of user credentials and returns an access and refresh JSON web
     * token pair to prove the authentication of those credentials.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static apiAuthTokenCreate(
        requestBody: CustomTokenObtainPairRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/token/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Takes a refresh type JSON web token and returns an access type JSON web
     * token if the refresh token is valid.
     * @param requestBody
     * @returns TokenRefresh
     * @throws ApiError
     */
    public static apiAuthTokenRefreshCreate(
        requestBody: TokenRefreshRequest,
    ): CancelablePromise<TokenRefresh> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/token/refresh/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de usuários.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public static apiAuthUsersList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserList> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de usuários.
     * @param requestBody
     * @returns UserCreate
     * @throws ApiError
     */
    public static apiAuthUsersCreate(
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
     * ViewSet para gerenciamento de usuários.
     * @param id A unique integer value identifying this user.
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersRetrieve(
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
     * ViewSet para gerenciamento de usuários.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersUpdate(
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
     * ViewSet para gerenciamento de usuários.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersPartialUpdate(
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
     * ViewSet para gerenciamento de usuários.
     * @param id A unique integer value identifying this user.
     * @returns void
     * @throws ApiError
     */
    public static apiAuthUsersDestroy(
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
     * Ativa um usuário.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersActivateCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
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
     * Desativa um usuário.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersDeactivateCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
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
     * Redefine a senha do usuário para uma senha temporária e envia por e-mail.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersResetPasswordCreate2(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
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
     * Desbloqueia um usuário após tentativas de login malsucedidas.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersUnlockCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
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
    /**
     * @param requestBody
     * @returns Activation
     * @throws ApiError
     */
    public static apiAuthUsersActivationCreate(
        requestBody: ActivationRequest,
    ): CancelablePromise<Activation> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/activation/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Altera a senha do usuário autenticado.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersChangePasswordCreate(
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/change_password/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retorna as informações do usuário autenticado.
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersMeRetrieve(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/users/me/',
        });
    }
    /**
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersMeUpdate(
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/auth/users/me/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersMePartialUpdate(
        requestBody?: PatchedUserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/auth/users/me/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @returns void
     * @throws ApiError
     */
    public static apiAuthUsersMeDestroy(): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/auth/users/me/',
        });
    }
    /**
     * Retorna as permissões do usuário autenticado.
     * @returns User
     * @throws ApiError
     */
    public static apiAuthUsersPermissionsRetrieve(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/auth/users/permissions/',
        });
    }
    /**
     * @param requestBody
     * @returns ResetPassword
     * @throws ApiError
     */
    public static apiAuthUsersResendActivationCreate(
        requestBody: ResetPasswordRequest,
    ): CancelablePromise<ResetPassword> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/resend_activation/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns ResetPassword
     * @throws ApiError
     */
    public static apiAuthUsersResetPasswordCreate(
        requestBody: ResetPasswordRequest,
    ): CancelablePromise<ResetPassword> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/reset_password/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns SetNewPassword
     * @throws ApiError
     */
    public static apiAuthUsersResetPasswordConfirmCreate(
        requestBody: SetNewPasswordRequest,
    ): CancelablePromise<SetNewPassword> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/reset_password_confirm/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns SendEmailReset
     * @throws ApiError
     */
    public static apiAuthUsersResetUsernameCreate(
        requestBody: SendEmailResetRequest,
    ): CancelablePromise<SendEmailReset> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/reset_username/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns UsernameResetConfirm
     * @throws ApiError
     */
    public static apiAuthUsersResetUsernameConfirmCreate(
        requestBody: UsernameResetConfirmRequest,
    ): CancelablePromise<UsernameResetConfirm> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/reset_username_confirm/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns SetPasswordRetype
     * @throws ApiError
     */
    public static apiAuthUsersSetPasswordCreate(
        requestBody: SetPasswordRetypeRequest,
    ): CancelablePromise<SetPasswordRetype> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/set_password/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns SetUsername
     * @throws ApiError
     */
    public static apiAuthUsersSetUsernameCreate(
        requestBody: SetUsernameRequest,
    ): CancelablePromise<SetUsername> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/users/set_username/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de configurações de notificações.
     *
     * Permite criar, listar, atualizar e excluir configurações de notificações do usuário.
     * Cada usuário pode ter suas próprias configurações para diferentes tipos de notificações.
     *
     * Endpoints:
     * - GET /configuracoes-notificacao/ - Lista configurações do usuário
     * - POST /configuracoes-notificacao/ - Cria uma nova configuração
     * - GET /configuracoes-notificacao/{id}/ - Obtém detalhes de uma configuração
     * - PUT/PATCH /configuracoes-notificacao/{id}/ - Atualiza uma configuração
     * - DELETE /configuracoes-notificacao/{id}/ - Remove uma configuração
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedConfiguracaoNotificacaoList
     * @throws ApiError
     */
    public static apiCommunicationsConfiguracoesList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedConfiguracaoNotificacaoList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/configuracoes/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de configurações de notificações.
     *
     * Permite criar, listar, atualizar e excluir configurações de notificações do usuário.
     * Cada usuário pode ter suas próprias configurações para diferentes tipos de notificações.
     *
     * Endpoints:
     * - GET /configuracoes-notificacao/ - Lista configurações do usuário
     * - POST /configuracoes-notificacao/ - Cria uma nova configuração
     * - GET /configuracoes-notificacao/{id}/ - Obtém detalhes de uma configuração
     * - PUT/PATCH /configuracoes-notificacao/{id}/ - Atualiza uma configuração
     * - DELETE /configuracoes-notificacao/{id}/ - Remove uma configuração
     * @param requestBody
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static apiCommunicationsConfiguracoesCreate(
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
     * ViewSet para gerenciamento de configurações de notificações.
     *
     * Permite criar, listar, atualizar e excluir configurações de notificações do usuário.
     * Cada usuário pode ter suas próprias configurações para diferentes tipos de notificações.
     *
     * Endpoints:
     * - GET /configuracoes-notificacao/ - Lista configurações do usuário
     * - POST /configuracoes-notificacao/ - Cria uma nova configuração
     * - GET /configuracoes-notificacao/{id}/ - Obtém detalhes de uma configuração
     * - PUT/PATCH /configuracoes-notificacao/{id}/ - Atualiza uma configuração
     * - DELETE /configuracoes-notificacao/{id}/ - Remove uma configuração
     * @param id A unique integer value identifying this Configuração de Notificação.
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static apiCommunicationsConfiguracoesRetrieve(
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
     * ViewSet para gerenciamento de configurações de notificações.
     *
     * Permite criar, listar, atualizar e excluir configurações de notificações do usuário.
     * Cada usuário pode ter suas próprias configurações para diferentes tipos de notificações.
     *
     * Endpoints:
     * - GET /configuracoes-notificacao/ - Lista configurações do usuário
     * - POST /configuracoes-notificacao/ - Cria uma nova configuração
     * - GET /configuracoes-notificacao/{id}/ - Obtém detalhes de uma configuração
     * - PUT/PATCH /configuracoes-notificacao/{id}/ - Atualiza uma configuração
     * - DELETE /configuracoes-notificacao/{id}/ - Remove uma configuração
     * @param id A unique integer value identifying this Configuração de Notificação.
     * @param requestBody
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static apiCommunicationsConfiguracoesUpdate(
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
     * ViewSet para gerenciamento de configurações de notificações.
     *
     * Permite criar, listar, atualizar e excluir configurações de notificações do usuário.
     * Cada usuário pode ter suas próprias configurações para diferentes tipos de notificações.
     *
     * Endpoints:
     * - GET /configuracoes-notificacao/ - Lista configurações do usuário
     * - POST /configuracoes-notificacao/ - Cria uma nova configuração
     * - GET /configuracoes-notificacao/{id}/ - Obtém detalhes de uma configuração
     * - PUT/PATCH /configuracoes-notificacao/{id}/ - Atualiza uma configuração
     * - DELETE /configuracoes-notificacao/{id}/ - Remove uma configuração
     * @param id A unique integer value identifying this Configuração de Notificação.
     * @param requestBody
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static apiCommunicationsConfiguracoesPartialUpdate(
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
     * ViewSet para gerenciamento de configurações de notificações.
     *
     * Permite criar, listar, atualizar e excluir configurações de notificações do usuário.
     * Cada usuário pode ter suas próprias configurações para diferentes tipos de notificações.
     *
     * Endpoints:
     * - GET /configuracoes-notificacao/ - Lista configurações do usuário
     * - POST /configuracoes-notificacao/ - Cria uma nova configuração
     * - GET /configuracoes-notificacao/{id}/ - Obtém detalhes de uma configuração
     * - PUT/PATCH /configuracoes-notificacao/{id}/ - Atualiza uma configuração
     * - DELETE /configuracoes-notificacao/{id}/ - Remove uma configuração
     * @param id A unique integer value identifying this Configuração de Notificação.
     * @returns void
     * @throws ApiError
     */
    public static apiCommunicationsConfiguracoesDestroy(
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
     * Retorna a configuração do usuário atual ou cria uma padrão se não existir.
     * @returns ConfiguracaoNotificacao
     * @throws ApiError
     */
    public static apiCommunicationsConfiguracoesMinhaConfiguracaoRetrieve(): CancelablePromise<ConfiguracaoNotificacao> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/configuracoes/minha_configuracao/',
        });
    }
    /**
     * ViewSet para gerenciamento de mensagens de chat.
     *
     * Permite criar, listar, atualizar e excluir mensagens de chat em projetos.
     * Inclui funcionalidades para marcar mensagens como lidas e filtrar mensagens não lidas.
     *
     * Endpoints:
     * - GET /chat-mensagens/ - Lista todas as mensagens (com filtros)
     * - POST /chat-mensagens/ - Cria uma nova mensagem
     * - GET /chat-mensagens/{id}/ - Obtém detalhes de uma mensagem
     * - PUT/PATCH /chat-mensagens/{id}/ - Atualiza uma mensagem
     * - DELETE /chat-mensagens/{id}/ - Remove uma mensagem
     * - POST /chat-mensagens/{id}/marcar_como_lida/ - Marca uma mensagem como lida
     * - GET /chat-mensagens/mensagens_nao_lidas/ - Lista mensagens não lidas
     * @param autor
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param projeto
     * @returns PaginatedChatMensagemList
     * @throws ApiError
     */
    public static apiCommunicationsMensagensList(
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
     * ViewSet para gerenciamento de mensagens de chat.
     *
     * Permite criar, listar, atualizar e excluir mensagens de chat em projetos.
     * Inclui funcionalidades para marcar mensagens como lidas e filtrar mensagens não lidas.
     *
     * Endpoints:
     * - GET /chat-mensagens/ - Lista todas as mensagens (com filtros)
     * - POST /chat-mensagens/ - Cria uma nova mensagem
     * - GET /chat-mensagens/{id}/ - Obtém detalhes de uma mensagem
     * - PUT/PATCH /chat-mensagens/{id}/ - Atualiza uma mensagem
     * - DELETE /chat-mensagens/{id}/ - Remove uma mensagem
     * - POST /chat-mensagens/{id}/marcar_como_lida/ - Marca uma mensagem como lida
     * - GET /chat-mensagens/mensagens_nao_lidas/ - Lista mensagens não lidas
     * @param requestBody
     * @returns ChatMensagem
     * @throws ApiError
     */
    public static apiCommunicationsMensagensCreate(
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
     * ViewSet para gerenciamento de mensagens de chat.
     *
     * Permite criar, listar, atualizar e excluir mensagens de chat em projetos.
     * Inclui funcionalidades para marcar mensagens como lidas e filtrar mensagens não lidas.
     *
     * Endpoints:
     * - GET /chat-mensagens/ - Lista todas as mensagens (com filtros)
     * - POST /chat-mensagens/ - Cria uma nova mensagem
     * - GET /chat-mensagens/{id}/ - Obtém detalhes de uma mensagem
     * - PUT/PATCH /chat-mensagens/{id}/ - Atualiza uma mensagem
     * - DELETE /chat-mensagens/{id}/ - Remove uma mensagem
     * - POST /chat-mensagens/{id}/marcar_como_lida/ - Marca uma mensagem como lida
     * - GET /chat-mensagens/mensagens_nao_lidas/ - Lista mensagens não lidas
     * @param id A unique integer value identifying this Mensagem de Chat.
     * @returns ChatMensagem
     * @throws ApiError
     */
    public static apiCommunicationsMensagensRetrieve(
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
     * ViewSet para gerenciamento de mensagens de chat.
     *
     * Permite criar, listar, atualizar e excluir mensagens de chat em projetos.
     * Inclui funcionalidades para marcar mensagens como lidas e filtrar mensagens não lidas.
     *
     * Endpoints:
     * - GET /chat-mensagens/ - Lista todas as mensagens (com filtros)
     * - POST /chat-mensagens/ - Cria uma nova mensagem
     * - GET /chat-mensagens/{id}/ - Obtém detalhes de uma mensagem
     * - PUT/PATCH /chat-mensagens/{id}/ - Atualiza uma mensagem
     * - DELETE /chat-mensagens/{id}/ - Remove uma mensagem
     * - POST /chat-mensagens/{id}/marcar_como_lida/ - Marca uma mensagem como lida
     * - GET /chat-mensagens/mensagens_nao_lidas/ - Lista mensagens não lidas
     * @param id A unique integer value identifying this Mensagem de Chat.
     * @param requestBody
     * @returns ChatMensagem
     * @throws ApiError
     */
    public static apiCommunicationsMensagensUpdate(
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
     * ViewSet para gerenciamento de mensagens de chat.
     *
     * Permite criar, listar, atualizar e excluir mensagens de chat em projetos.
     * Inclui funcionalidades para marcar mensagens como lidas e filtrar mensagens não lidas.
     *
     * Endpoints:
     * - GET /chat-mensagens/ - Lista todas as mensagens (com filtros)
     * - POST /chat-mensagens/ - Cria uma nova mensagem
     * - GET /chat-mensagens/{id}/ - Obtém detalhes de uma mensagem
     * - PUT/PATCH /chat-mensagens/{id}/ - Atualiza uma mensagem
     * - DELETE /chat-mensagens/{id}/ - Remove uma mensagem
     * - POST /chat-mensagens/{id}/marcar_como_lida/ - Marca uma mensagem como lida
     * - GET /chat-mensagens/mensagens_nao_lidas/ - Lista mensagens não lidas
     * @param id A unique integer value identifying this Mensagem de Chat.
     * @param requestBody
     * @returns ChatMensagem
     * @throws ApiError
     */
    public static apiCommunicationsMensagensPartialUpdate(
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
     * ViewSet para gerenciamento de mensagens de chat.
     *
     * Permite criar, listar, atualizar e excluir mensagens de chat em projetos.
     * Inclui funcionalidades para marcar mensagens como lidas e filtrar mensagens não lidas.
     *
     * Endpoints:
     * - GET /chat-mensagens/ - Lista todas as mensagens (com filtros)
     * - POST /chat-mensagens/ - Cria uma nova mensagem
     * - GET /chat-mensagens/{id}/ - Obtém detalhes de uma mensagem
     * - PUT/PATCH /chat-mensagens/{id}/ - Atualiza uma mensagem
     * - DELETE /chat-mensagens/{id}/ - Remove uma mensagem
     * - POST /chat-mensagens/{id}/marcar_como_lida/ - Marca uma mensagem como lida
     * - GET /chat-mensagens/mensagens_nao_lidas/ - Lista mensagens não lidas
     * @param id A unique integer value identifying this Mensagem de Chat.
     * @returns void
     * @throws ApiError
     */
    public static apiCommunicationsMensagensDestroy(
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
     * @returns ChatMensagem
     * @throws ApiError
     */
    public static apiCommunicationsMensagensMarcarComoLidaCreate(
        id: number,
        requestBody: ChatMensagemRequest,
    ): CancelablePromise<ChatMensagem> {
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
     * @returns ChatMensagem
     * @throws ApiError
     */
    public static apiCommunicationsMensagensMensagensNaoLidasRetrieve(): CancelablePromise<ChatMensagem> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/mensagens/mensagens_nao_lidas/',
        });
    }
    /**
     * ViewSet para gerenciamento de notificações.
     *
     * Permite criar, listar, atualizar e excluir notificações do sistema.
     * Inclui funcionalidades para marcar notificações como lidas e filtrar notificações não lidas.
     *
     * Endpoints:
     * - GET /notificacoes/ - Lista notificações do usuário
     * - GET /notificacoes/{id}/ - Obtém detalhes de uma notificação
     * - POST /notificacoes/{id}/marcar_como_lida/ - Marca uma notificação como lida
     * - POST /notificacoes/marcar_todas_como_lidas/ - Marca todas as notificações como lidas
     * - GET /notificacoes/nao_lidas/ - Lista notificações não lidas
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
    public static apiCommunicationsNotificacoesList(
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
     * ViewSet para gerenciamento de notificações.
     *
     * Permite criar, listar, atualizar e excluir notificações do sistema.
     * Inclui funcionalidades para marcar notificações como lidas e filtrar notificações não lidas.
     *
     * Endpoints:
     * - GET /notificacoes/ - Lista notificações do usuário
     * - GET /notificacoes/{id}/ - Obtém detalhes de uma notificação
     * - POST /notificacoes/{id}/marcar_como_lida/ - Marca uma notificação como lida
     * - POST /notificacoes/marcar_todas_como_lidas/ - Marca todas as notificações como lidas
     * - GET /notificacoes/nao_lidas/ - Lista notificações não lidas
     * @param requestBody
     * @returns Notificacao
     * @throws ApiError
     */
    public static apiCommunicationsNotificacoesCreate(
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
     * ViewSet para gerenciamento de notificações.
     *
     * Permite criar, listar, atualizar e excluir notificações do sistema.
     * Inclui funcionalidades para marcar notificações como lidas e filtrar notificações não lidas.
     *
     * Endpoints:
     * - GET /notificacoes/ - Lista notificações do usuário
     * - GET /notificacoes/{id}/ - Obtém detalhes de uma notificação
     * - POST /notificacoes/{id}/marcar_como_lida/ - Marca uma notificação como lida
     * - POST /notificacoes/marcar_todas_como_lidas/ - Marca todas as notificações como lidas
     * - GET /notificacoes/nao_lidas/ - Lista notificações não lidas
     * @param id A unique integer value identifying this Notificação.
     * @returns Notificacao
     * @throws ApiError
     */
    public static apiCommunicationsNotificacoesRetrieve(
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
     * ViewSet para gerenciamento de notificações.
     *
     * Permite criar, listar, atualizar e excluir notificações do sistema.
     * Inclui funcionalidades para marcar notificações como lidas e filtrar notificações não lidas.
     *
     * Endpoints:
     * - GET /notificacoes/ - Lista notificações do usuário
     * - GET /notificacoes/{id}/ - Obtém detalhes de uma notificação
     * - POST /notificacoes/{id}/marcar_como_lida/ - Marca uma notificação como lida
     * - POST /notificacoes/marcar_todas_como_lidas/ - Marca todas as notificações como lidas
     * - GET /notificacoes/nao_lidas/ - Lista notificações não lidas
     * @param id A unique integer value identifying this Notificação.
     * @param requestBody
     * @returns Notificacao
     * @throws ApiError
     */
    public static apiCommunicationsNotificacoesUpdate(
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
     * ViewSet para gerenciamento de notificações.
     *
     * Permite criar, listar, atualizar e excluir notificações do sistema.
     * Inclui funcionalidades para marcar notificações como lidas e filtrar notificações não lidas.
     *
     * Endpoints:
     * - GET /notificacoes/ - Lista notificações do usuário
     * - GET /notificacoes/{id}/ - Obtém detalhes de uma notificação
     * - POST /notificacoes/{id}/marcar_como_lida/ - Marca uma notificação como lida
     * - POST /notificacoes/marcar_todas_como_lidas/ - Marca todas as notificações como lidas
     * - GET /notificacoes/nao_lidas/ - Lista notificações não lidas
     * @param id A unique integer value identifying this Notificação.
     * @param requestBody
     * @returns Notificacao
     * @throws ApiError
     */
    public static apiCommunicationsNotificacoesPartialUpdate(
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
     * ViewSet para gerenciamento de notificações.
     *
     * Permite criar, listar, atualizar e excluir notificações do sistema.
     * Inclui funcionalidades para marcar notificações como lidas e filtrar notificações não lidas.
     *
     * Endpoints:
     * - GET /notificacoes/ - Lista notificações do usuário
     * - GET /notificacoes/{id}/ - Obtém detalhes de uma notificação
     * - POST /notificacoes/{id}/marcar_como_lida/ - Marca uma notificação como lida
     * - POST /notificacoes/marcar_todas_como_lidas/ - Marca todas as notificações como lidas
     * - GET /notificacoes/nao_lidas/ - Lista notificações não lidas
     * @param id A unique integer value identifying this Notificação.
     * @returns void
     * @throws ApiError
     */
    public static apiCommunicationsNotificacoesDestroy(
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
     * @returns Notificacao
     * @throws ApiError
     */
    public static apiCommunicationsNotificacoesMarcarComoLidaCreate(
        id: number,
        requestBody: NotificacaoRequest,
    ): CancelablePromise<Notificacao> {
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
     * @returns Notificacao
     * @throws ApiError
     */
    public static apiCommunicationsNotificacoesMarcarTodasComoLidasCreate(
        requestBody: NotificacaoRequest,
    ): CancelablePromise<Notificacao> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/communications/notificacoes/marcar_todas_como_lidas/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retorna apenas as notificações não lidas do usuário.
     *
     * Suporta filtros adicionais por tipo e prioridade através de parâmetros na query string.
     *
     * Args:
     * request: Objeto de requisição
     *
     * Returns:
     * Response: Lista de notificações não lidas filtradas
     * @returns Notificacao
     * @throws ApiError
     */
    public static apiCommunicationsNotificacoesNaoLidasRetrieve(): CancelablePromise<Notificacao> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/communications/notificacoes/nao_lidas/',
        });
    }
    /**
     * ViewSet para gerenciamento de alertas de orçamento.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param projeto
     * @param status * `ATIVO` - Ativo
     * * `RESOLVIDO` - Resolvido
     * * `IGNORADO` - Ignorado
     * @param tarefa
     * @param tipo * `PROJETO` - Projeto
     * * `TAREFA` - Tarefa
     * @returns PaginatedAlertaList
     * @throws ApiError
     */
    public static apiCostsAlertasList(
        ordering?: string,
        page?: number,
        projeto?: number,
        status?: 'ATIVO' | 'IGNORADO' | 'RESOLVIDO',
        tarefa?: number,
        tipo?: 'PROJETO' | 'TAREFA',
    ): CancelablePromise<PaginatedAlertaList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/alertas/',
            query: {
                'ordering': ordering,
                'page': page,
                'projeto': projeto,
                'status': status,
                'tarefa': tarefa,
                'tipo': tipo,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de alertas de orçamento.
     * @param requestBody
     * @returns Alerta
     * @throws ApiError
     */
    public static apiCostsAlertasCreate(
        requestBody: AlertaRequest,
    ): CancelablePromise<Alerta> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/alertas/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de alertas de orçamento.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @returns Alerta
     * @throws ApiError
     */
    public static apiCostsAlertasRetrieve(
        id: number,
    ): CancelablePromise<Alerta> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/alertas/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de alertas de orçamento.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @param requestBody
     * @returns Alerta
     * @throws ApiError
     */
    public static apiCostsAlertasUpdate(
        id: number,
        requestBody: AlertaRequest,
    ): CancelablePromise<Alerta> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/costs/alertas/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de alertas de orçamento.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @param requestBody
     * @returns Alerta
     * @throws ApiError
     */
    public static apiCostsAlertasPartialUpdate(
        id: number,
        requestBody?: PatchedAlertaRequest,
    ): CancelablePromise<Alerta> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/costs/alertas/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de alertas de orçamento.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @returns void
     * @throws ApiError
     */
    public static apiCostsAlertasDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/costs/alertas/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Marca um alerta como ignorado.
     * Opcionalmente, pode incluir uma justificativa para ignorar o alerta.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @param requestBody
     * @returns Alerta
     * @throws ApiError
     */
    public static apiCostsAlertasIgnorarCreate(
        id: number,
        requestBody: AlertaRequest,
    ): CancelablePromise<Alerta> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/alertas/{id}/ignorar/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Marca um alerta como resolvido.
     * Opcionalmente, pode incluir uma observação sobre a resolução.
     * @param id A unique integer value identifying this Alerta de Orçamento.
     * @param requestBody
     * @returns Alerta
     * @throws ApiError
     */
    public static apiCostsAlertasResolverCreate(
        id: number,
        requestBody: AlertaRequest,
    ): CancelablePromise<Alerta> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/alertas/{id}/resolver/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retorna apenas os alertas pendentes (status ATIVO).
     * Permite filtrar por projeto, tarefa e tipo.
     * @returns Alerta
     * @throws ApiError
     */
    public static apiCostsAlertasPendentesRetrieve(): CancelablePromise<Alerta> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/alertas/pendentes/',
        });
    }
    /**
     * ViewSet para gerenciamento de categorias de custos.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedCategoriaList
     * @throws ApiError
     */
    public static apiCostsCategoriasList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedCategoriaList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/categorias/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de categorias de custos.
     * @param requestBody
     * @returns Categoria
     * @throws ApiError
     */
    public static apiCostsCategoriasCreate(
        requestBody: CategoriaRequest,
    ): CancelablePromise<Categoria> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/categorias/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de categorias de custos.
     * @param id A unique integer value identifying this Categoria.
     * @returns Categoria
     * @throws ApiError
     */
    public static apiCostsCategoriasRetrieve(
        id: number,
    ): CancelablePromise<Categoria> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/categorias/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de categorias de custos.
     * @param id A unique integer value identifying this Categoria.
     * @param requestBody
     * @returns Categoria
     * @throws ApiError
     */
    public static apiCostsCategoriasUpdate(
        id: number,
        requestBody: CategoriaRequest,
    ): CancelablePromise<Categoria> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/costs/categorias/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de categorias de custos.
     * @param id A unique integer value identifying this Categoria.
     * @param requestBody
     * @returns Categoria
     * @throws ApiError
     */
    public static apiCostsCategoriasPartialUpdate(
        id: number,
        requestBody?: PatchedCategoriaRequest,
    ): CancelablePromise<Categoria> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/costs/categorias/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de categorias de custos.
     * @param id A unique integer value identifying this Categoria.
     * @returns void
     * @throws ApiError
     */
    public static apiCostsCategoriasDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/costs/categorias/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de custos.
     * Permite criar, listar, atualizar e excluir custos.
     * @param categoria
     * @param data
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param projeto
     * @param search A search term.
     * @param tarefa
     * @param tipo * `FIXO` - Custo Fixo
     * * `VARIAVEL` - Custo Variável
     * * `RECORRENTE` - Custo Recorrente
     * @returns PaginatedCustoListList
     * @throws ApiError
     */
    public static apiCostsCustosList(
        categoria?: number,
        data?: string,
        ordering?: string,
        page?: number,
        projeto?: number,
        search?: string,
        tarefa?: number,
        tipo?: 'FIXO' | 'RECORRENTE' | 'VARIAVEL',
    ): CancelablePromise<PaginatedCustoListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/',
            query: {
                'categoria': categoria,
                'data': data,
                'ordering': ordering,
                'page': page,
                'projeto': projeto,
                'search': search,
                'tarefa': tarefa,
                'tipo': tipo,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de custos.
     * Permite criar, listar, atualizar e excluir custos.
     * @param requestBody
     * @returns Custo
     * @throws ApiError
     */
    public static apiCostsCustosCreate(
        requestBody: CustoRequest,
    ): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/custos/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de custos.
     * Permite criar, listar, atualizar e excluir custos.
     * @param id A unique integer value identifying this Custo.
     * @returns Custo
     * @throws ApiError
     */
    public static apiCostsCustosRetrieve(
        id: number,
    ): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de custos.
     * Permite criar, listar, atualizar e excluir custos.
     * @param id A unique integer value identifying this Custo.
     * @param requestBody
     * @returns Custo
     * @throws ApiError
     */
    public static apiCostsCustosUpdate(
        id: number,
        requestBody: CustoRequest,
    ): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/costs/custos/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de custos.
     * Permite criar, listar, atualizar e excluir custos.
     * @param id A unique integer value identifying this Custo.
     * @param requestBody
     * @returns Custo
     * @throws ApiError
     */
    public static apiCostsCustosPartialUpdate(
        id: number,
        requestBody?: PatchedCustoRequest,
    ): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/costs/custos/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de custos.
     * Permite criar, listar, atualizar e excluir custos.
     * @param id A unique integer value identifying this Custo.
     * @returns void
     * @throws ApiError
     */
    public static apiCostsCustosDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/costs/custos/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Endpoint para dashboard financeiro: retorna dados resumidos de custos.
     * Inclui total gasto, gasto mensal, top categorias e alertas recentes.
     * @returns Custo
     * @throws ApiError
     */
    public static apiCostsCustosDashboardRetrieve(): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/dashboard/',
        });
    }
    /**
     * Gera um relatório de gastos mensais para análise de tendências.
     * Agrupa os custos por mês e retorna série temporal.
     * @returns Custo
     * @throws ApiError
     */
    public static apiCostsCustosRelatorioMensalRetrieve(): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/relatorio_mensal/',
        });
    }
    /**
     * Gera um relatório de gastos por categoria.
     * Utiliza anotações para calcular percentuais diretamente no banco de dados.
     * @returns Custo
     * @throws ApiError
     */
    public static apiCostsCustosRelatorioPorCategoriaRetrieve(): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/relatorio_por_categoria/',
        });
    }
    /**
     * Gera um relatório de gastos por projeto.
     * @returns Custo
     * @throws ApiError
     */
    public static apiCostsCustosRelatorioPorProjetoRetrieve(): CancelablePromise<Custo> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/custos/relatorio_por_projeto/',
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de projetos.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param page A page number within the paginated result set.
     * @param projeto
     * @returns PaginatedOrcamentoProjetoList
     * @throws ApiError
     */
    public static apiCostsOrcamentosProjetoList(
        page?: number,
        projeto?: number,
    ): CancelablePromise<PaginatedOrcamentoProjetoList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-projeto/',
            query: {
                'page': page,
                'projeto': projeto,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de projetos.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param requestBody
     * @returns OrcamentoProjeto
     * @throws ApiError
     */
    public static apiCostsOrcamentosProjetoCreate(
        requestBody: OrcamentoProjetoRequest,
    ): CancelablePromise<OrcamentoProjeto> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/orcamentos-projeto/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de projetos.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param id A unique integer value identifying this Orçamento de Projeto.
     * @returns OrcamentoProjeto
     * @throws ApiError
     */
    public static apiCostsOrcamentosProjetoRetrieve(
        id: number,
    ): CancelablePromise<OrcamentoProjeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-projeto/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de projetos.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param id A unique integer value identifying this Orçamento de Projeto.
     * @param requestBody
     * @returns OrcamentoProjeto
     * @throws ApiError
     */
    public static apiCostsOrcamentosProjetoUpdate(
        id: number,
        requestBody: OrcamentoProjetoRequest,
    ): CancelablePromise<OrcamentoProjeto> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/costs/orcamentos-projeto/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de projetos.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param id A unique integer value identifying this Orçamento de Projeto.
     * @param requestBody
     * @returns OrcamentoProjeto
     * @throws ApiError
     */
    public static apiCostsOrcamentosProjetoPartialUpdate(
        id: number,
        requestBody?: PatchedOrcamentoProjetoRequest,
    ): CancelablePromise<OrcamentoProjeto> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/costs/orcamentos-projeto/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de projetos.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param id A unique integer value identifying this Orçamento de Projeto.
     * @returns void
     * @throws ApiError
     */
    public static apiCostsOrcamentosProjetoDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/costs/orcamentos-projeto/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Permite ajustar o orçamento de um projeto com justificativa.
     * Mantém histórico da alteração no campo de observações.
     * @param id A unique integer value identifying this Orçamento de Projeto.
     * @param requestBody
     * @returns OrcamentoProjeto
     * @throws ApiError
     */
    public static apiCostsOrcamentosProjetoAjustarOrcamentoCreate(
        id: number,
        requestBody: OrcamentoProjetoRequest,
    ): CancelablePromise<OrcamentoProjeto> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/orcamentos-projeto/{id}/ajustar_orcamento/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retorna a lista de projetos que ainda não possuem orçamento definido.
     * @returns OrcamentoProjeto
     * @throws ApiError
     */
    public static apiCostsOrcamentosProjetoProjetosSemOrcamentoRetrieve(): CancelablePromise<OrcamentoProjeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-projeto/projetos_sem_orcamento/',
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de tarefas.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param page A page number within the paginated result set.
     * @param tarefa
     * @param tarefaProjeto
     * @returns PaginatedOrcamentoTarefaList
     * @throws ApiError
     */
    public static apiCostsOrcamentosTarefaList(
        page?: number,
        tarefa?: number,
        tarefaProjeto?: number,
    ): CancelablePromise<PaginatedOrcamentoTarefaList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-tarefa/',
            query: {
                'page': page,
                'tarefa': tarefa,
                'tarefa__projeto': tarefaProjeto,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de tarefas.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param requestBody
     * @returns OrcamentoTarefa
     * @throws ApiError
     */
    public static apiCostsOrcamentosTarefaCreate(
        requestBody: OrcamentoTarefaRequest,
    ): CancelablePromise<OrcamentoTarefa> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/orcamentos-tarefa/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de tarefas.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param id A unique integer value identifying this Orçamento de Tarefa.
     * @returns OrcamentoTarefa
     * @throws ApiError
     */
    public static apiCostsOrcamentosTarefaRetrieve(
        id: number,
    ): CancelablePromise<OrcamentoTarefa> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-tarefa/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de tarefas.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param id A unique integer value identifying this Orçamento de Tarefa.
     * @param requestBody
     * @returns OrcamentoTarefa
     * @throws ApiError
     */
    public static apiCostsOrcamentosTarefaUpdate(
        id: number,
        requestBody: OrcamentoTarefaRequest,
    ): CancelablePromise<OrcamentoTarefa> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/costs/orcamentos-tarefa/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de tarefas.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param id A unique integer value identifying this Orçamento de Tarefa.
     * @param requestBody
     * @returns OrcamentoTarefa
     * @throws ApiError
     */
    public static apiCostsOrcamentosTarefaPartialUpdate(
        id: number,
        requestBody?: PatchedOrcamentoTarefaRequest,
    ): CancelablePromise<OrcamentoTarefa> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/costs/orcamentos-tarefa/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de orçamentos de tarefas.
     * Inclui anotações para calcular campos derivados diretamente no banco de dados.
     * @param id A unique integer value identifying this Orçamento de Tarefa.
     * @returns void
     * @throws ApiError
     */
    public static apiCostsOrcamentosTarefaDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/costs/orcamentos-tarefa/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Permite ajustar o orçamento de uma tarefa com justificativa.
     * Mantém histórico da alteração no campo de observações.
     * @param id A unique integer value identifying this Orçamento de Tarefa.
     * @param requestBody
     * @returns OrcamentoTarefa
     * @throws ApiError
     */
    public static apiCostsOrcamentosTarefaAjustarOrcamentoCreate(
        id: number,
        requestBody: OrcamentoTarefaRequest,
    ): CancelablePromise<OrcamentoTarefa> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/costs/orcamentos-tarefa/{id}/ajustar_orcamento/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retorna a lista de tarefas que ainda não possuem orçamento definido.
     * @returns OrcamentoTarefa
     * @throws ApiError
     */
    public static apiCostsOrcamentosTarefaTarefasSemOrcamentoRetrieve(): CancelablePromise<OrcamentoTarefa> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/costs/orcamentos-tarefa/tarefas_sem_orcamento/',
        });
    }
    /**
     * Listar projetos
     * Retorna uma lista paginada de projetos.
     * @param arquivado
     * @param atrasado Filtra projetos atrasados (data_fim < hoje e status != CONCLUIDO)
     * @param dataFimAntesAfter Filtra projetos com data de fim antes da data especificada
     * @param dataFimAntesBefore Filtra projetos com data de fim antes da data especificada
     * @param dataFimAposAfter Filtra projetos com data de fim após a data especificada
     * @param dataFimAposBefore Filtra projetos com data de fim após a data especificada
     * @param dataInicioAntesAfter Filtra projetos com data de início antes da data especificada
     * @param dataInicioAntesBefore Filtra projetos com data de início antes da data especificada
     * @param dataInicioAposAfter Filtra projetos com data de início após a data especificada
     * @param dataInicioAposBefore Filtra projetos com data de início após a data especificada
     * @param descricao Filtra por descrição (case insensitive)
     * @param membro Filtra projetos que contenham o membro especificado (ID do usuário)
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param prioridade Filtra por prioridade (pode ser múltiplas, separadas por vírgula)
     * @param search A search term.
     * @param status Filtra por status (pode ser múltiplos, separados por vírgula)
     * @param titulo Filtra por título (case insensitive)
     * @returns PaginatedProjetoListList
     * @throws ApiError
     */
    public static apiProjectsList(
        arquivado?: boolean,
        atrasado?: boolean,
        dataFimAntesAfter?: string,
        dataFimAntesBefore?: string,
        dataFimAposAfter?: string,
        dataFimAposBefore?: string,
        dataInicioAntesAfter?: string,
        dataInicioAntesBefore?: string,
        dataInicioAposAfter?: string,
        dataInicioAposBefore?: string,
        descricao?: string,
        membro?: string,
        ordering?: string,
        page?: number,
        prioridade?: string,
        search?: string,
        status?: string,
        titulo?: string,
    ): CancelablePromise<PaginatedProjetoListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/',
            query: {
                'arquivado': arquivado,
                'atrasado': atrasado,
                'data_fim_antes_after': dataFimAntesAfter,
                'data_fim_antes_before': dataFimAntesBefore,
                'data_fim_apos_after': dataFimAposAfter,
                'data_fim_apos_before': dataFimAposBefore,
                'data_inicio_antes_after': dataInicioAntesAfter,
                'data_inicio_antes_before': dataInicioAntesBefore,
                'data_inicio_apos_after': dataInicioAposAfter,
                'data_inicio_apos_before': dataInicioAposBefore,
                'descricao': descricao,
                'membro': membro,
                'ordering': ordering,
                'page': page,
                'prioridade': prioridade,
                'search': search,
                'status': status,
                'titulo': titulo,
            },
        });
    }
    /**
     * Criar novo projeto
     * Cria um novo projeto.
     * @param requestBody
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsCreate(
        requestBody: ProjetoRequest,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Obter detalhes do projeto
     * Retorna informações detalhadas de um projeto específico.
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Atualizar projeto
     * Atualiza todos os campos de um projeto existente.
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsUpdate(
        id: number,
        requestBody: ProjetoRequest,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/projects/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualizar projeto parcialmente
     * Atualiza parcialmente um projeto existente.
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsPartialUpdate(
        id: number,
        requestBody?: PatchedProjetoRequest,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/projects/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Excluir projeto
     * Remove um projeto existente.
     * @param id A unique integer value identifying this Projeto.
     * @returns void
     * @throws ApiError
     */
    public static apiProjectsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/projects/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Adicionar membro ao projeto
     * Adiciona um novo membro ao projeto com o papel especificado.
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns MembroProjeto
     * @throws ApiError
     */
    public static apiProjectsAdicionarMembroCreate(
        id: number,
        requestBody: MembroProjetoRequest,
    ): CancelablePromise<MembroProjeto> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects/{id}/adicionar_membro/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Arquiva ou desarquiva um projeto.
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsArchiveCreate(
        id: number,
        requestBody: ProjetoRequest,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects/{id}/archive/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Criar nova sprint no projeto
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsCriarSprintCreate(
        id: number,
        requestBody: ProjetoRequest,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects/{id}/criar_sprint/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Criar nova tarefa no projeto
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsCriarTarefaCreate(
        id: number,
        requestBody: ProjetoRequest,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects/{id}/criar_tarefa/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Criar múltiplas tarefas no projeto
     * @param id A unique integer value identifying this Projeto.
     * @param requestBody
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsCriarTarefasMultiplasCreate(
        id: number,
        requestBody: ProjetoRequest,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects/{id}/criar_tarefas_multiplas/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Dashboard do projeto
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsDashboardRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{id}/dashboard/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Exportar dados do projeto
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsExportarRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{id}/exportar/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Visualização Gantt do projeto
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsGanttRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{id}/gantt/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Histórico de status do projeto
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsHistoricoStatusRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{id}/historico_status/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Visualização Kanban do projeto
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsKanbanRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{id}/kanban/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar membros do projeto
     * Retorna todos os membros associados ao projeto.
     * @param id A unique integer value identifying this Projeto.
     * @param arquivado
     * @param atrasado Filtra projetos atrasados (data_fim < hoje e status != CONCLUIDO)
     * @param dataFimAntesAfter Filtra projetos com data de fim antes da data especificada
     * @param dataFimAntesBefore Filtra projetos com data de fim antes da data especificada
     * @param dataFimAposAfter Filtra projetos com data de fim após a data especificada
     * @param dataFimAposBefore Filtra projetos com data de fim após a data especificada
     * @param dataInicioAntesAfter Filtra projetos com data de início antes da data especificada
     * @param dataInicioAntesBefore Filtra projetos com data de início antes da data especificada
     * @param dataInicioAposAfter Filtra projetos com data de início após a data especificada
     * @param dataInicioAposBefore Filtra projetos com data de início após a data especificada
     * @param descricao Filtra por descrição (case insensitive)
     * @param membro Filtra projetos que contenham o membro especificado (ID do usuário)
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param prioridade Filtra por prioridade (pode ser múltiplas, separadas por vírgula)
     * @param search A search term.
     * @param status Filtra por status (pode ser múltiplos, separados por vírgula)
     * @param titulo Filtra por título (case insensitive)
     * @returns PaginatedMembroProjetoList
     * @throws ApiError
     */
    public static apiProjectsListarMembrosList(
        id: number,
        arquivado?: boolean,
        atrasado?: boolean,
        dataFimAntesAfter?: string,
        dataFimAntesBefore?: string,
        dataFimAposAfter?: string,
        dataFimAposBefore?: string,
        dataInicioAntesAfter?: string,
        dataInicioAntesBefore?: string,
        dataInicioAposAfter?: string,
        dataInicioAposBefore?: string,
        descricao?: string,
        membro?: string,
        ordering?: string,
        page?: number,
        prioridade?: string,
        search?: string,
        status?: string,
        titulo?: string,
    ): CancelablePromise<PaginatedMembroProjetoList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{id}/listar_membros/',
            path: {
                'id': id,
            },
            query: {
                'arquivado': arquivado,
                'atrasado': atrasado,
                'data_fim_antes_after': dataFimAntesAfter,
                'data_fim_antes_before': dataFimAntesBefore,
                'data_fim_apos_after': dataFimAposAfter,
                'data_fim_apos_before': dataFimAposBefore,
                'data_inicio_antes_after': dataInicioAntesAfter,
                'data_inicio_antes_before': dataInicioAntesBefore,
                'data_inicio_apos_after': dataInicioAposAfter,
                'data_inicio_apos_before': dataInicioAposBefore,
                'descricao': descricao,
                'membro': membro,
                'ordering': ordering,
                'page': page,
                'prioridade': prioridade,
                'search': search,
                'status': status,
                'titulo': titulo,
            },
        });
    }
    /**
     * Lista os membros do projeto.
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsMembrosRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{id}/membros/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Métricas Detalhadas do Projeto
     * Retorna métricas detalhadas sobre o projeto, incluindo progresso, custos, prazos e qualidade.
     * @param id A unique integer value identifying this Projeto.
     * @returns any
     * @throws ApiError
     */
    public static apiProjectsMetricsRetrieve(
        id: number,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{id}/metrics/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Remover membro do projeto
     * Remove um membro do projeto pelo ID.
     * @param id A unique integer value identifying this Projeto.
     * @param membroId ID do membro a ser removido
     * @returns void
     * @throws ApiError
     */
    public static apiProjectsRemoverMembroDestroy(
        id: number,
        membroId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/projects/{id}/remover_membro/',
            path: {
                'id': id,
            },
            query: {
                'membro_id': membroId,
            },
        });
    }
    /**
     * Listar sprints do projeto
     * @param id A unique integer value identifying this Projeto.
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsSprintsRetrieve(
        id: number,
    ): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{id}/sprints/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Retorna os projetos dos quais o usuário é membro.
     * @returns Projeto
     * @throws ApiError
     */
    public static apiProjectsMyProjectsRetrieve(): CancelablePromise<Projeto> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/my_projects/',
        });
    }
    /**
     * ViewSet para visualização do histórico de riscos.
     * Somente leitura.
     * @param alteradoPor
     * @param page A page number within the paginated result set.
     * @param risco
     * @returns PaginatedHistoricoRiscoList
     * @throws ApiError
     */
    public static apiRisksHistoricoList(
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
     * ViewSet para visualização do histórico de riscos.
     * Somente leitura.
     * @param id A unique integer value identifying this Histórico de Risco.
     * @returns HistoricoRisco
     * @throws ApiError
     */
    public static apiRisksHistoricoRetrieve(
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
     * ViewSet para gerenciamento de riscos.
     * Permite criar, listar, atualizar e excluir riscos.
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
     * @returns PaginatedRiscoListList
     * @throws ApiError
     */
    public static apiRisksRiscosList(
        impacto?: 'ALTO' | 'BAIXO' | 'MEDIO',
        ordering?: string,
        page?: number,
        probabilidade?: 'ALTA' | 'BAIXA' | 'MEDIA',
        projeto?: number,
        responsavelMitigacao?: number,
        search?: string,
        status?: 'ACEITO' | 'ELIMINADO' | 'EM_ANALISE' | 'IDENTIFICADO' | 'MITIGADO',
    ): CancelablePromise<PaginatedRiscoListList> {
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
     * ViewSet para gerenciamento de riscos.
     * Permite criar, listar, atualizar e excluir riscos.
     * @param requestBody
     * @returns Risco
     * @throws ApiError
     */
    public static apiRisksRiscosCreate(
        requestBody: RiscoRequest,
    ): CancelablePromise<Risco> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/risks/riscos/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de riscos.
     * Permite criar, listar, atualizar e excluir riscos.
     * @param id A unique integer value identifying this Risco.
     * @returns Risco
     * @throws ApiError
     */
    public static apiRisksRiscosRetrieve(
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
     * ViewSet para gerenciamento de riscos.
     * Permite criar, listar, atualizar e excluir riscos.
     * @param id A unique integer value identifying this Risco.
     * @param requestBody
     * @returns Risco
     * @throws ApiError
     */
    public static apiRisksRiscosUpdate(
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
     * ViewSet para gerenciamento de riscos.
     * Permite criar, listar, atualizar e excluir riscos.
     * @param id A unique integer value identifying this Risco.
     * @param requestBody
     * @returns Risco
     * @throws ApiError
     */
    public static apiRisksRiscosPartialUpdate(
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
     * ViewSet para gerenciamento de riscos.
     * Permite criar, listar, atualizar e excluir riscos.
     * @param id A unique integer value identifying this Risco.
     * @returns void
     * @throws ApiError
     */
    public static apiRisksRiscosDestroy(
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
     * Atualiza o status de um risco.
     * @param id A unique integer value identifying this Risco.
     * @param requestBody
     * @returns Risco
     * @throws ApiError
     */
    public static apiRisksRiscosAtualizarStatusCreate(
        id: number,
        requestBody: RiscoRequest,
    ): CancelablePromise<Risco> {
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
     * Retorna o histórico de alterações do risco.
     * @param id A unique integer value identifying this Risco.
     * @returns Risco
     * @throws ApiError
     */
    public static apiRisksRiscosHistoricoRetrieve(
        id: number,
    ): CancelablePromise<Risco> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/risks/riscos/{id}/historico/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Exclui múltiplos riscos de uma vez.
     * @returns void
     * @throws ApiError
     */
    public static apiRisksRiscosExcluirVariosDestroy(): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/risks/riscos/excluir_varios/',
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
    public static apiTasksAtribuicoesList(
        ordering?: string,
        page?: number,
        tarefa?: number,
        usuario?: number,
    ): CancelablePromise<PaginatedAtribuicaoTarefaList> {
        return __request(OpenAPI, {
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
    public static apiTasksAtribuicoesCreate(
        requestBody: AtribuicaoTarefaRequest,
    ): CancelablePromise<AtribuicaoTarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksAtribuicoesRetrieve(
        id: number,
    ): CancelablePromise<AtribuicaoTarefa> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/tasks/atribuicoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de atribuições de tarefas a usuários.
     *
     * Permite criar, listar, visualizar e remover atribuições de tarefas a usuários.
     * O usuário que faz a atribuição é automaticamente registrado.
     * @param id A unique integer value identifying this Atribuição de Tarefa.
     * @param requestBody
     * @returns AtribuicaoTarefa
     * @throws ApiError
     */
    public static apiTasksAtribuicoesUpdate(
        id: number,
        requestBody: AtribuicaoTarefaRequest,
    ): CancelablePromise<AtribuicaoTarefa> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/tasks/atribuicoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de atribuições de tarefas a usuários.
     *
     * Permite criar, listar, visualizar e remover atribuições de tarefas a usuários.
     * O usuário que faz a atribuição é automaticamente registrado.
     * @param id A unique integer value identifying this Atribuição de Tarefa.
     * @param requestBody
     * @returns AtribuicaoTarefa
     * @throws ApiError
     */
    public static apiTasksAtribuicoesPartialUpdate(
        id: number,
        requestBody?: PatchedAtribuicaoTarefaRequest,
    ): CancelablePromise<AtribuicaoTarefa> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/tasks/atribuicoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Remover atribuição
     * Remove a atribuição de uma tarefa a um usuário.
     * @param id A unique integer value identifying this Atribuição de Tarefa.
     * @returns void
     * @throws ApiError
     */
    public static apiTasksAtribuicoesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
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
    public static apiTasksComentariosList(
        autor?: number,
        ordering?: string,
        page?: number,
        search?: string,
        tarefa?: number,
    ): CancelablePromise<PaginatedComentarioTarefaList> {
        return __request(OpenAPI, {
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
    public static apiTasksComentariosCreate(
        requestBody: ComentarioTarefaRequest,
    ): CancelablePromise<ComentarioTarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksComentariosRetrieve(
        id: number,
    ): CancelablePromise<ComentarioTarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksComentariosUpdate(
        id: number,
        requestBody: ComentarioTarefaRequest,
    ): CancelablePromise<ComentarioTarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksComentariosPartialUpdate(
        id: number,
        requestBody?: PatchedComentarioTarefaRequest,
    ): CancelablePromise<ComentarioTarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksComentariosDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/tasks/comentarios/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Listar tarefas
     * Retorna uma lista paginada de tarefas com opções de filtragem e ordenação.
     * @param atrasada Filtrar tarefas atrasadas
     * @param dataInicioAntesAfter Filtra tarefas com data de início antes da data especificada
     * @param dataInicioAntesBefore Filtra tarefas com data de início antes da data especificada
     * @param dataInicioAposAfter Filtra tarefas com data de início após a data especificada
     * @param dataInicioAposBefore Filtra tarefas com data de início após a data especificada
     * @param dataTerminoAntesAfter Filtra tarefas com data de término antes da data especificada
     * @param dataTerminoAntesBefore Filtra tarefas com data de término antes da data especificada
     * @param dataTerminoAposAfter Filtra tarefas com data de término após a data especificada
     * @param dataTerminoAposBefore Filtra tarefas com data de término após a data especificada
     * @param descricao Filtra por descrição (case insensitive)
     * @param minhasTarefas Filtrar minhas tarefas
     * @param ordering Ordenar resultados (ex: -data_termino)
     * @param page A page number within the paginated result set.
     * @param prioridade Filtrar por prioridade (separadas por vírgula)
     * @param projeto Filtrar por ID do projeto
     * @param responsavel Filtrar por ID do usuário responsável
     * @param search A search term.
     * @param semResponsavel Filtra tarefas sem responsáveis atribuídos
     * @param semSprint Filtrar tarefas sem sprint
     * @param sprint Filtrar por ID da sprint
     * @param status Filtrar por status (separados por vírgula)
     * @param titulo Filtra por título (case insensitive)
     * @returns PaginatedTarefaListList
     * @throws ApiError
     */
    public static apiTasksTarefasList(
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
        responsavel?: number,
        search?: string,
        semResponsavel?: boolean,
        semSprint?: boolean,
        sprint?: number,
        status?: string,
        titulo?: string,
    ): CancelablePromise<PaginatedTarefaListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/tasks/tarefas/',
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
     * Criar tarefa
     * Cria uma nova tarefa com os dados fornecidos.
     * @param requestBody
     * @returns Tarefa
     * @throws ApiError
     */
    public static apiTasksTarefasCreate(
        requestBody: TarefaRequest,
    ): CancelablePromise<Tarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksTarefasRetrieve(
        id: number,
    ): CancelablePromise<Tarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksTarefasUpdate(
        id: number,
        requestBody: TarefaRequest,
    ): CancelablePromise<Tarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksTarefasPartialUpdate(
        id: number,
        requestBody?: PatchedTarefaRequest,
    ): CancelablePromise<Tarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksTarefasDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
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
    public static apiTasksTarefasAdicionarComentarioCreate(
        id: number,
        requestBody?: {
            /**
             * Texto do comentário
             */
            texto: string;
        },
    ): CancelablePromise<ComentarioTarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksTarefasAssociarSprintCreate(
        id: number,
        requestBody?: {
            /**
             * ID da sprint a ser associada. Use 0 ou null para remover a associação.
             */
            sprint_id: number | null;
        },
    ): CancelablePromise<Tarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksTarefasAtribuirResponsavelCreate(
        id: number,
        requestBody?: {
            /**
             * ID do usuário a ser atribuído como responsável
             */
            usuario_id: number;
        },
    ): CancelablePromise<AtribuicaoTarefa> {
        return __request(OpenAPI, {
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
    public static apiTasksTarefasAtualizarStatusCreate(
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
        return __request(OpenAPI, {
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
    public static apiTasksTarefasHistoricoStatusList(
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
        return __request(OpenAPI, {
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
    public static apiTasksTarefasRemoverResponsavelCreate(
        id: number,
        requestBody?: {
            /**
             * ID do usuário a ser removido da tarefa
             */
            usuario_id: number;
        },
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/tasks/tarefas/{id}/remover_responsavel/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de equipes.
     * Permite criar, listar, atualizar e excluir equipes.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedEquipeListList
     * @throws ApiError
     */
    public static apiTeamsEquipesList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedEquipeListList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/equipes/',
            query: {
                'ordering': ordering,
                'page': page,
                'search': search,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de equipes.
     * Permite criar, listar, atualizar e excluir equipes.
     * @param requestBody
     * @returns Equipe
     * @throws ApiError
     */
    public static apiTeamsEquipesCreate(
        requestBody: EquipeRequest,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/teams/equipes/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de equipes.
     * Permite criar, listar, atualizar e excluir equipes.
     * @param id A unique integer value identifying this Equipe.
     * @returns Equipe
     * @throws ApiError
     */
    public static apiTeamsEquipesRetrieve(
        id: number,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/equipes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de equipes.
     * Permite criar, listar, atualizar e excluir equipes.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns Equipe
     * @throws ApiError
     */
    public static apiTeamsEquipesUpdate(
        id: number,
        requestBody: EquipeRequest,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/teams/equipes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de equipes.
     * Permite criar, listar, atualizar e excluir equipes.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns Equipe
     * @throws ApiError
     */
    public static apiTeamsEquipesPartialUpdate(
        id: number,
        requestBody?: PatchedEquipeRequest,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/teams/equipes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de equipes.
     * Permite criar, listar, atualizar e excluir equipes.
     * @param id A unique integer value identifying this Equipe.
     * @returns void
     * @throws ApiError
     */
    public static apiTeamsEquipesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/teams/equipes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Adiciona um membro à equipe.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns Equipe
     * @throws ApiError
     */
    public static apiTeamsEquipesAdicionarMembroCreate(
        id: number,
        requestBody: EquipeRequest,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/teams/equipes/{id}/adicionar_membro/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Atualiza o papel de um membro da equipe.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns Equipe
     * @throws ApiError
     */
    public static apiTeamsEquipesAtualizarPapelMembroCreate(
        id: number,
        requestBody: EquipeRequest,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/teams/equipes/{id}/atualizar_papel_membro/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retorna a lista de membros da equipe.
     * @param id A unique integer value identifying this Equipe.
     * @returns Equipe
     * @throws ApiError
     */
    public static apiTeamsEquipesMembrosRetrieve(
        id: number,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/equipes/{id}/membros/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Remove um membro da equipe.
     * @param id A unique integer value identifying this Equipe.
     * @param requestBody
     * @returns Equipe
     * @throws ApiError
     */
    public static apiTeamsEquipesRemoverMembroCreate(
        id: number,
        requestBody: EquipeRequest,
    ): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/teams/equipes/{id}/remover_membro/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retorna a lista de usuários disponíveis para adicionar a uma equipe.
     * @returns Equipe
     * @throws ApiError
     */
    public static apiTeamsEquipesUsuariosDisponiveisRetrieve(): CancelablePromise<Equipe> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/equipes/usuarios_disponiveis/',
        });
    }
    /**
     * ViewSet para gerenciamento de membros de equipe.
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
    public static apiTeamsMembrosList(
        equipe?: number,
        page?: number,
        papel?: 'ANALISTA' | 'DESIGN' | 'DEV' | 'PO' | 'QA' | 'SM',
        usuario?: number,
    ): CancelablePromise<PaginatedMembroEquipeList> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de membros de equipe.
     * @param requestBody
     * @returns MembroEquipe
     * @throws ApiError
     */
    public static apiTeamsMembrosCreate(
        requestBody: MembroEquipeRequest,
    ): CancelablePromise<MembroEquipe> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/teams/membros/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de membros de equipe.
     * @param id A unique integer value identifying this Membro da Equipe.
     * @returns MembroEquipe
     * @throws ApiError
     */
    public static apiTeamsMembrosRetrieve(
        id: number,
    ): CancelablePromise<MembroEquipe> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/membros/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de membros de equipe.
     * @param id A unique integer value identifying this Membro da Equipe.
     * @param requestBody
     * @returns MembroEquipe
     * @throws ApiError
     */
    public static apiTeamsMembrosUpdate(
        id: number,
        requestBody: MembroEquipeRequest,
    ): CancelablePromise<MembroEquipe> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de membros de equipe.
     * @param id A unique integer value identifying this Membro da Equipe.
     * @param requestBody
     * @returns MembroEquipe
     * @throws ApiError
     */
    public static apiTeamsMembrosPartialUpdate(
        id: number,
        requestBody?: PatchedMembroEquipeRequest,
    ): CancelablePromise<MembroEquipe> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de membros de equipe.
     * @param id A unique integer value identifying this Membro da Equipe.
     * @returns void
     * @throws ApiError
     */
    public static apiTeamsMembrosDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/teams/membros/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de permissões de equipe.
     * @param equipe
     * @param modulo * `TAREFAS` - Tarefas
     * * `SPRINTS` - Sprints
     * * `DOCUMENTOS` - Documentos
     * * `RISCOS` - Riscos
     * * `CUSTOS` - Custos
     * @param page A page number within the paginated result set.
     * @param papel * `PO` - Product Owner
     * * `SM` - Scrum Master
     * * `DEV` - Desenvolvedor
     * * `QA` - Analista de Qualidade
     * * `DESIGN` - Designer
     * * `ANALISTA` - Analista
     * @param permissao * `VISUALIZAR` - Visualizar
     * * `CRIAR` - Criar
     * * `EDITAR` - Editar
     * * `EXCLUIR` - Excluir
     * @returns PaginatedPermissaoEquipeList
     * @throws ApiError
     */
    public static apiTeamsPermissoesList(
        equipe?: number,
        modulo?: 'CUSTOS' | 'DOCUMENTOS' | 'RISCOS' | 'SPRINTS' | 'TAREFAS',
        page?: number,
        papel?: 'ANALISTA' | 'DESIGN' | 'DEV' | 'PO' | 'QA' | 'SM',
        permissao?: 'CRIAR' | 'EDITAR' | 'EXCLUIR' | 'VISUALIZAR',
    ): CancelablePromise<PaginatedPermissaoEquipeList> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/permissoes/',
            query: {
                'equipe': equipe,
                'modulo': modulo,
                'page': page,
                'papel': papel,
                'permissao': permissao,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de permissões de equipe.
     * @param requestBody
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public static apiTeamsPermissoesCreate(
        requestBody: PermissaoEquipeRequest,
    ): CancelablePromise<PermissaoEquipe> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/teams/permissoes/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de permissões de equipe.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public static apiTeamsPermissoesRetrieve(
        id: number,
    ): CancelablePromise<PermissaoEquipe> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/teams/permissoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de permissões de equipe.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @param requestBody
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public static apiTeamsPermissoesUpdate(
        id: number,
        requestBody: PermissaoEquipeRequest,
    ): CancelablePromise<PermissaoEquipe> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/teams/permissoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de permissões de equipe.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @param requestBody
     * @returns PermissaoEquipe
     * @throws ApiError
     */
    public static apiTeamsPermissoesPartialUpdate(
        id: number,
        requestBody?: PatchedPermissaoEquipeRequest,
    ): CancelablePromise<PermissaoEquipe> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/teams/permissoes/{id}/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de permissões de equipe.
     * @param id A unique integer value identifying this Permissão de Equipe.
     * @returns void
     * @throws ApiError
     */
    public static apiTeamsPermissoesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/teams/permissoes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de perfis de acesso.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedAccessProfileList
     * @throws ApiError
     */
    public static apiUsersAccessProfilesList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedAccessProfileList> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de perfis de acesso.
     * @param requestBody
     * @returns AccessProfile
     * @throws ApiError
     */
    public static apiUsersAccessProfilesCreate(
        requestBody: AccessProfileRequest,
    ): CancelablePromise<AccessProfile> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/access-profiles/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de perfis de acesso.
     * @param id A unique integer value identifying this access profile.
     * @returns AccessProfile
     * @throws ApiError
     */
    public static apiUsersAccessProfilesRetrieve(
        id: number,
    ): CancelablePromise<AccessProfile> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/access-profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de perfis de acesso.
     * @param id A unique integer value identifying this access profile.
     * @param requestBody
     * @returns AccessProfile
     * @throws ApiError
     */
    public static apiUsersAccessProfilesUpdate(
        id: number,
        requestBody: AccessProfileRequest,
    ): CancelablePromise<AccessProfile> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de perfis de acesso.
     * @param id A unique integer value identifying this access profile.
     * @param requestBody
     * @returns AccessProfile
     * @throws ApiError
     */
    public static apiUsersAccessProfilesPartialUpdate(
        id: number,
        requestBody?: PatchedAccessProfileRequest,
    ): CancelablePromise<AccessProfile> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de perfis de acesso.
     * @param id A unique integer value identifying this access profile.
     * @returns void
     * @throws ApiError
     */
    public static apiUsersAccessProfilesDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/users/access-profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de permissões.
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
     * @returns PaginatedPermissionList
     * @throws ApiError
     */
    public static apiUsersPermissionsList(
        accessProfile?: number,
        action?: 'APPROVE' | 'ASSIGN' | 'COMMENT' | 'CREATE' | 'DELETE' | 'EDIT' | 'EXPORT' | 'IMPORT' | 'VIEW',
        module?: 'APPROVALS' | 'COMMUNICATIONS' | 'COSTS' | 'DASHBOARD' | 'DOCUMENTS' | 'NOTIFICATIONS' | 'PROJECTS' | 'REPORTS' | 'RESOURCES' | 'RISKS' | 'SETTINGS' | 'TASKS' | 'TEAMS' | 'USERS',
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedPermissionList> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de permissões.
     * @param requestBody
     * @returns Permission
     * @throws ApiError
     */
    public static apiUsersPermissionsCreate(
        requestBody: PermissionRequest,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/permissions/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de permissões.
     * @param id A unique integer value identifying this permission.
     * @returns Permission
     * @throws ApiError
     */
    public static apiUsersPermissionsRetrieve(
        id: number,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/permissions/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de permissões.
     * @param id A unique integer value identifying this permission.
     * @param requestBody
     * @returns Permission
     * @throws ApiError
     */
    public static apiUsersPermissionsUpdate(
        id: number,
        requestBody: PermissionRequest,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de permissões.
     * @param id A unique integer value identifying this permission.
     * @param requestBody
     * @returns Permission
     * @throws ApiError
     */
    public static apiUsersPermissionsPartialUpdate(
        id: number,
        requestBody?: PatchedPermissionRequest,
    ): CancelablePromise<Permission> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de permissões.
     * @param id A unique integer value identifying this permission.
     * @returns void
     * @throws ApiError
     */
    public static apiUsersPermissionsDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/users/permissions/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserProfileList
     * @throws ApiError
     */
    public static apiUsersProfilesList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserProfileList> {
        return __request(OpenAPI, {
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
     * @param requestBody
     * @returns UserProfile
     * @throws ApiError
     */
    public static apiUsersProfilesCreate(
        requestBody?: UserProfileRequest,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/profiles/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param id
     * @returns UserProfile
     * @throws ApiError
     */
    public static apiUsersProfilesRetrieve(
        id: string,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id
     * @param requestBody
     * @returns UserProfile
     * @throws ApiError
     */
    public static apiUsersProfilesUpdate(
        id: string,
        requestBody?: UserProfileRequest,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
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
     * @param id
     * @param requestBody
     * @returns UserProfile
     * @throws ApiError
     */
    public static apiUsersProfilesPartialUpdate(
        id: string,
        requestBody?: PatchedUserProfileRequest,
    ): CancelablePromise<UserProfile> {
        return __request(OpenAPI, {
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
     * @param id
     * @returns void
     * @throws ApiError
     */
    public static apiUsersProfilesDestroy(
        id: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/users/profiles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Takes a set of user credentials and returns an access and refresh JSON web
     * token pair to prove the authentication of those credentials.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public static apiUsersTokenCreate(
        requestBody: CustomTokenObtainPairRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/token/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Takes a refresh type JSON web token and returns an access type JSON web
     * token if the refresh token is valid.
     * @param requestBody
     * @returns TokenRefresh
     * @throws ApiError
     */
    public static apiUsersTokenRefreshCreate(
        requestBody: TokenRefreshRequest,
    ): CancelablePromise<TokenRefresh> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/token/refresh/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de usuários.
     * @param ordering Which field to use when ordering the results.
     * @param page A page number within the paginated result set.
     * @param search A search term.
     * @returns PaginatedUserList
     * @throws ApiError
     */
    public static apiUsersUsersList(
        ordering?: string,
        page?: number,
        search?: string,
    ): CancelablePromise<PaginatedUserList> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de usuários.
     * @param requestBody
     * @returns UserCreate
     * @throws ApiError
     */
    public static apiUsersUsersCreate(
        requestBody: UserCreateRequest,
    ): CancelablePromise<UserCreate> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/users/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * ViewSet para gerenciamento de usuários.
     * @param id A unique integer value identifying this user.
     * @returns User
     * @throws ApiError
     */
    public static apiUsersUsersRetrieve(
        id: number,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/users/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * ViewSet para gerenciamento de usuários.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiUsersUsersUpdate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de usuários.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiUsersUsersPartialUpdate(
        id: number,
        requestBody?: PatchedUserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
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
     * ViewSet para gerenciamento de usuários.
     * @param id A unique integer value identifying this user.
     * @returns void
     * @throws ApiError
     */
    public static apiUsersUsersDestroy(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/users/users/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * Ativa um usuário.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiUsersUsersActivateCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
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
     * Desativa um usuário.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiUsersUsersDeactivateCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
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
     * Redefine a senha do usuário para uma senha temporária e envia por e-mail.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiUsersUsersResetPasswordCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/users/{id}/reset_password/',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Desbloqueia um usuário após tentativas de login malsucedidas.
     * @param id A unique integer value identifying this user.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiUsersUsersUnlockCreate(
        id: number,
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
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
     * Altera a senha do usuário autenticado.
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public static apiUsersUsersChangePasswordCreate(
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users/users/change_password/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * Retorna as informações do usuário autenticado.
     * @returns User
     * @throws ApiError
     */
    public static apiUsersUsersMeRetrieve(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/users/me/',
        });
    }
    /**
     * Retorna as permissões do usuário autenticado.
     * @returns User
     * @throws ApiError
     */
    public static apiUsersUsersPermissionsRetrieve(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/users/permissions/',
        });
    }
}
