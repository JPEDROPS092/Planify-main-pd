// frontend/stores/teams.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';
// Ex: import type { Equipe, MembroEquipe } from '~/services/utils/types';

export const useTeamsStore = defineStore('teams', () => {
  // State
  const teams = ref<any[]>([]); // Substituir 'any' pelo tipo Equipe[]
  const currentTeam = ref<any | null>(null); // Substituir 'any' pelo tipo Equipe | null
  const teamMembers = ref<any[]>([]); // Substituir 'any' pelo tipo MembroEquipe[]
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Actions
  async function fetchTeamsForProject(projectId: number | string) {
    isLoading.value = true;
    error.value = null;
    try {
      // TODO: Chamar API para buscar equipes de um projeto
      console.warn(`fetchTeamsForProject(${projectId}): Mock implementation.`);
      // teams.value = [{ id: 1, nome: 'Equipe Mock 1', projeto: projectId }];
    } catch (e:any) {
      error.value = e.message || `Falha ao buscar equipes para o projeto ${projectId}.`;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchTeamMembers(teamId: number | string) {
    isLoading.value = true;
    error.value = null;
    try {
      // TODO: Chamar API para buscar membros de uma equipe
      console.warn(`fetchTeamMembers(${teamId}): Mock implementation.`);
      // teamMembers.value = [{ id: 1, nomeUsuario: 'Membro Mock 1', equipeId: teamId }];
    } catch (e:any) {
      error.value = e.message || `Falha ao buscar membros da equipe ${teamId}.`;
    } finally {
      isLoading.value = false;
    }
  }
  
  // TODO: Adicionar actions para CRUD de equipes e gerenciamento de membros

  return {
    teams,
    currentTeam,
    teamMembers,
    isLoading,
    error,
    fetchTeamsForProject,
    fetchTeamMembers,
  };
});
