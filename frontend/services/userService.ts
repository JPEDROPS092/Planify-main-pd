import { useApiClients } from '~/composables/useApiClients';

export const useUserService = () => {
  const { authApi } = useApiClients();

  /**
   * Obtém a lista de usuários
   * @param params Parâmetros de paginação e filtros
   */
  const getUsers = async (params = {}) => {
    const response = await authApi.authUsersList(params);
    return response.data;
  };

  /**
   * Obtém um usuário específico pelo ID
   * @param id ID do usuário
   */
  const getUser = async (id: number) => {
    const response = await authApi.authUsersRetrieve({ id });
    return response.data;
  };

  /**
   * Cria um novo usuário
   * @param data Dados do usuário
   */
  const createUser = async (data: any) => {
    const response = await authApi.authUsersCreate({ userRequest: data });
    return response.data;
  };

  /**
   * Atualiza um usuário existente (completo)
   * @param id ID do usuário
   * @param data Dados do usuário
   */
  const updateUser = async (id: number, data: any) => {
    const response = await authApi.authUsersUpdate({ id, userRequest: data });
    return response.data;
  };

  /**
   * Atualiza um usuário existente (parcial)
   * @param id ID do usuário
   * @param data Dados do usuário
   */
  const patchUser = async (id: number, data: any) => {
    const response = await authApi.authUsersPartialUpdate({ id, patchedUserRequest: data });
    return response.data;
  };

  /**
   * Remove um usuário
   * @param id ID do usuário
   */
  const deleteUser = async (id: number) => {
    await authApi.authUsersDestroy({ id });
  };

  /**
   * Ativa um usuário
   * @param id ID do usuário
   */
  const activateUser = async (id: number) => {
    await authApi.authUsersActivateCreate({ id, userRequest: {} });
  };

  /**
   * Desativa um usuário
   * @param id ID do usuário
   */
  const deactivateUser = async (id: number) => {
    await authApi.authUsersDeactivateCreate({ id, userRequest: {} });
  };

  /**
   * Redefine a senha do usuário
   * @param id ID do usuário
   */
  const resetPassword = async (id: number) => {
    await authApi.authUsersResetPasswordCreate({ id, userRequest: {} });
  };

  /**
   * Desbloqueia um usuário
   * @param id ID do usuário
   */
  const unlockUser = async (id: number) => {
    await authApi.authUsersUnlockCreate({ id, userRequest: {} });
  };

  /**
   * Obtém o perfil do usuário atual
   */
  const getCurrentUserProfile = async () => {
    const response = await authApi.authUsersRetrieve({ id: 'me' });
    return response.data;
  };

  /**
   * Atualiza o perfil do usuário atual
   * @param data Dados do perfil
   */
  const updateCurrentUserProfile = async (data: any) => {
    const response = await authApi.authUsersUpdate({ id: 'me', userRequest: data });
    return response.data;
  };

  /**
   * Obtém a lista de perfis de acesso
   */
  const getAccessProfiles = async () => {
    const response = await authApi.authProfilesList();
    return response.data;
  };

  return {
    getUsers,
    getUser,
    createUser,
    updateUser,
    patchUser,
    deleteUser,
    activateUser,
    deactivateUser,
    resetPassword,
    unlockUser,
    getCurrentUserProfile,
    updateCurrentUserProfile,
    getAccessProfiles
  };
};
