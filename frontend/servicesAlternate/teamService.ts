import { useApiClient } from '~/composables/useApiClient';

export const useTeamService = () => {
  const apiClient = useApiClient();

  /**
   * Obtém a lista de equipes
   * @param params Parâmetros de paginação e filtros
   */
  const getTeams = async (params = {}) => {
    const response = await apiClient.get('teams/equipes/', { params });
    return response.data;
  };

  /**
   * Obtém uma equipe específica pelo ID
   * @param id ID da equipe
   */
  const getTeam = async (id: number) => {
    const response = await apiClient.get(`teams/equipes/${id}/`);
    return response.data;
  };

  /**
   * Cria uma nova equipe
   * @param data Dados da equipe
   */
  const createTeam = async (data: any) => {
    const response = await apiClient.post('teams/equipes/', data);
    return response.data;
  };

  /**
   * Atualiza uma equipe existente
   * @param id ID da equipe
   * @param data Dados da equipe
   */
  const updateTeam = async (id: number, data: any) => {
    const response = await apiClient.patch(`teams/equipes/${id}/`, data);
    return response.data;
  };

  /**
   * Exclui uma equipe
   * @param id ID da equipe
   */
  const deleteTeam = async (id: number) => {
    const response = await apiClient.delete(`teams/equipes/${id}/`);
    return response.data;
  };

  /**
   * Obtém a lista de membros de uma equipe
   * @param teamId ID da equipe
   * @param params Parâmetros de paginação e filtros
   */
  const getTeamMembers = async (teamId: number, params = {}) => {
    const response = await apiClient.get(`teams/equipes/${teamId}/membros/`, { params });
    return response.data;
  };

  /**
   * Adiciona um membro a uma equipe
   * @param teamId ID da equipe
   * @param data Dados do membro
   */
  const addTeamMember = async (teamId: number, data: any) => {
    const response = await apiClient.post(`teams/equipes/${teamId}/membros/`, data);
    return response.data;
  };

  /**
   * Remove um membro de uma equipe
   * @param teamId ID da equipe
   * @param memberId ID do membro
   */
  const removeTeamMember = async (teamId: number, memberId: number) => {
    const response = await apiClient.delete(`teams/equipes/${teamId}/membros/${memberId}/`);
    return response.data;
  };

  return {
    getTeams,
    getTeam,
    createTeam,
    updateTeam,
    deleteTeam,
    getTeamMembers,
    addTeamMember,
    removeTeamMember
  };
};
