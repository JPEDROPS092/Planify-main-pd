// Service para gerenciar equipes usando a API Fetch do Nuxt
export const useTeamService = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  // Buscar equipes com filtros
  const getTeams = async (page: number = 1, filters: any = {}) => {
    try {
      return await $fetch(`${apiBase}teams/equipes/`, {
        params: { page, ...filters },
      });
    } catch (error) {
      console.error("Erro ao buscar equipes:", error);
      throw error;
    }
  };

  // Buscar equipe específica
  const getTeamById = async (id: number) => {
    try {
      return await $fetch(`${apiBase}teams/equipes/${id}/`);
    } catch (error) {
      console.error("Erro ao buscar equipe:", error);
      throw error;
    }
  };

  // Criar nova equipe
  const createTeam = async (teamData: any) => {
    try {
      return await $fetch(`${apiBase}teams/equipes/`, {
        method: "POST",
        body: teamData,
      });
    } catch (error) {
      console.error("Erro ao criar equipe:", error);
      throw error;
    }
  };

  // Atualizar equipe
  const updateTeam = async (id: number, teamData: any) => {
    try {
      return await $fetch(`${apiBase}teams/equipes/${id}/`, {
        method: "PUT",
        body: teamData,
      });
    } catch (error) {
      console.error("Erro ao atualizar equipe:", error);
      throw error;
    }
  };

  // Atualizar parcialmente equipe
  const partialUpdateTeam = async (id: number, teamData: any) => {
    try {
      return await $fetch(`${apiBase}teams/equipes/${id}/`, {
        method: "PATCH",
        body: teamData,
      });
    } catch (error) {
      console.error("Erro ao atualizar equipe:", error);
      throw error;
    }
  };

  // Deletar equipe
  const deleteTeam = async (id: number) => {
    try {
      return await $fetch(`${apiBase}teams/equipes/${id}/`, {
        method: "DELETE",
      });
    } catch (error) {
      console.error("Erro ao deletar equipe:", error);
      throw error;
    }
  };

  // Buscar membros da equipe
  const getTeamMembers = async (teamId: number) => {
    try {
      return await $fetch(`${apiBase}teams/equipes/${teamId}/membros/`);
    } catch (error) {
      console.error("Erro ao buscar membros da equipe:", error);
      throw error;
    }
  };

  // Adicionar membro à equipe
  const addTeamMember = async (teamId: number, memberData: any) => {
    try {
      return await $fetch(
        `${apiBase}teams/equipes/${teamId}/adicionar_membro/`,
        {
          method: "POST",
          body: memberData,
        }
      );
    } catch (error) {
      console.error("Erro ao adicionar membro à equipe:", error);
      throw error;
    }
  };

  // Remover membro da equipe
  const removeTeamMember = async (teamId: number, memberData: any) => {
    try {
      return await $fetch(`${apiBase}teams/equipes/${teamId}/remover_membro/`, {
        method: "POST",
        body: memberData,
      });
    } catch (error) {
      console.error("Erro ao remover membro da equipe:", error);
      throw error;
    }
  };

  // Atualizar papel do membro
  const updateMemberRole = async (teamId: number, memberData: any) => {
    try {
      return await $fetch(
        `${apiBase}teams/equipes/${teamId}/atualizar_papel_membro/`,
        {
          method: "POST",
          body: memberData,
        }
      );
    } catch (error) {
      console.error("Erro ao atualizar papel do membro:", error);
      throw error;
    }
  };

  // Buscar usuários disponíveis para adicionar à equipe
  const getAvailableUsers = async () => {
    try {
      return await $fetch(`${apiBase}teams/equipes/usuarios_disponiveis/`);
    } catch (error) {
      console.error("Erro ao buscar usuários disponíveis:", error);
      throw error;
    }
  };

  // Buscar permissões de equipe
  const getTeamPermissions = async () => {
    try {
      return await $fetch(`${apiBase}teams/permissoes/`);
    } catch (error) {
      console.error("Erro ao buscar permissões de equipe:", error);
      throw error;
    }
  };

  return {
    getTeams,
    getTeamById,
    createTeam,
    updateTeam,
    partialUpdateTeam,
    deleteTeam,
    getTeamMembers,
    addTeamMember,
    removeTeamMember,
    updateMemberRole,
    getAvailableUsers,
    getTeamPermissions,
  };
};
