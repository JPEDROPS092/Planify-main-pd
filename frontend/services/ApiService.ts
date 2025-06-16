/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Activation } from '../types/Activation';
import type { ActivationRequest } from '../types/ActivationRequest';
import type { AtribuicaoTarefa } from '../types/AtribuicaoTarefa';
import type { AtribuicaoTarefaRequest } from '../types/AtribuicaoTarefaRequest';
import type { CustomTokenObtainPairRequest } from '../types/CustomTokenObtainPairRequest';
import type { PaginatedTarefaListList } from '../types/PaginatedTarefaListList';
import type { PatchedAtribuicaoTarefaRequest } from '../types/PatchedAtribuicaoTarefaRequest';
import type { PatchedUserRequest } from '../types/PatchedUserRequest';
import type { ResetPassword } from '../types/ResetPassword';
import type { ResetPasswordRequest } from '../types/ResetPasswordRequest';
import type { SendEmailReset } from '../types/SendEmailReset';
import type { SendEmailResetRequest } from '../types/SendEmailResetRequest';
import type { SetNewPassword } from '../types/SetNewPassword';
import type { SetNewPasswordRequest } from '../types/SetNewPasswordRequest';
import type { SetPasswordRetype } from '../types/SetPasswordRetype';
import type { SetPasswordRetypeRequest } from '../types/SetPasswordRetypeRequest';
import type { SetUsername } from '../types/SetUsername';
import type { SetUsernameRequest } from '../types/SetUsernameRequest';
import type { TokenRefresh } from '../types/TokenRefresh';
import type { TokenRefreshRequest } from '../types/TokenRefreshRequest';
import type { User } from '../types/User';
import type { UsernameResetConfirm } from '../types/UsernameResetConfirm';
import type { UsernameResetConfirmRequest } from '../types/UsernameResetConfirmRequest';
import type { UserRequest } from '../types/UserRequest';
import type { CancelablePromise } from '../api/core/CancelablePromise';
import type { BaseHttpRequest } from '../api/core/BaseHttpRequest';
export class ApiService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Takes a set of user credentials and returns an access and refresh JSON web
     * token pair to prove the authentication of those credentials.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiAuthTokenCreate(
        requestBody: CustomTokenObtainPairRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
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
    public apiAuthTokenRefreshCreate(
        requestBody: TokenRefreshRequest,
    ): CancelablePromise<TokenRefresh> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/auth/token/refresh/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns Activation
     * @throws ApiError
     */
    public apiAuthUsersActivationCreate(
        requestBody: ActivationRequest,
    ): CancelablePromise<Activation> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/auth/users/activation/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * @param requestBody
     * @returns User
     * @throws ApiError
     */
    public apiAuthUsersMeUpdate(
        requestBody: UserRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
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
    public apiAuthUsersMePartialUpdate(
        requestBody?: PatchedUserRequest,
    ): CancelablePromise<User> {
        return this.httpRequest.request({
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
    public apiAuthUsersMeDestroy(): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/auth/users/me/',
        });
    }
    /**
     * @param requestBody
     * @returns ResetPassword
     * @throws ApiError
     */
    public apiAuthUsersResendActivationCreate(
        requestBody: ResetPasswordRequest,
    ): CancelablePromise<ResetPassword> {
        return this.httpRequest.request({
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
    public apiAuthUsersResetPasswordCreate(
        requestBody: ResetPasswordRequest,
    ): CancelablePromise<ResetPassword> {
        return this.httpRequest.request({
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
    public apiAuthUsersResetPasswordConfirmCreate(
        requestBody: SetNewPasswordRequest,
    ): CancelablePromise<SetNewPassword> {
        return this.httpRequest.request({
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
    public apiAuthUsersResetUsernameCreate(
        requestBody: SendEmailResetRequest,
    ): CancelablePromise<SendEmailReset> {
        return this.httpRequest.request({
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
    public apiAuthUsersResetUsernameConfirmCreate(
        requestBody: UsernameResetConfirmRequest,
    ): CancelablePromise<UsernameResetConfirm> {
        return this.httpRequest.request({
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
    public apiAuthUsersSetPasswordCreate(
        requestBody: SetPasswordRetypeRequest,
    ): CancelablePromise<SetPasswordRetype> {
        return this.httpRequest.request({
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
    public apiAuthUsersSetUsernameCreate(
        requestBody: SetUsernameRequest,
    ): CancelablePromise<SetUsername> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/auth/users/set_username/',
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
    public apiTasksAtribuicoesUpdate(
        id: number,
        requestBody: AtribuicaoTarefaRequest,
    ): CancelablePromise<AtribuicaoTarefa> {
        return this.httpRequest.request({
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
    public apiTasksAtribuicoesPartialUpdate(
        id: number,
        requestBody?: PatchedAtribuicaoTarefaRequest,
    ): CancelablePromise<AtribuicaoTarefa> {
        return this.httpRequest.request({
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
    public apiTasksTarefasList(
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
        return this.httpRequest.request({
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
     * Takes a set of user credentials and returns an access and refresh JSON web
     * token pair to prove the authentication of those credentials.
     * @param requestBody
     * @returns any No response body
     * @throws ApiError
     */
    public apiUsersTokenCreate(
        requestBody: CustomTokenObtainPairRequest,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
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
    public apiUsersTokenRefreshCreate(
        requestBody: TokenRefreshRequest,
    ): CancelablePromise<TokenRefresh> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/users/token/refresh/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
}
