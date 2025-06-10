// frontend/stores/projects.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ProjetosService, type Projeto } from '~/lib/api-client';

export const useProjectStore = defineStore('projects', {
  state: () => ({
    projects: [] as Projeto[], // Usa o tipo 'Projeto' gerado!
    loading: false,
  }),
  actions: {
    async fetchProjects() {
      this.loading = true;
      try {
        // Usa a função do serviço gerado. Sem URL, sem axios manual.
        const response = await ProjetosService.projetosControllerFindAll(); // O nome pode variar
        this.projects = response;
      } finally {
        this.loading = false;
      }
    },
  },
});
