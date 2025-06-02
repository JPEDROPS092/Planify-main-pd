<template>
  <div class="team-permissions-container">
    <h1 class="text-2xl font-bold mb-4">Permissões da Equipe</h1>
    <div class="permissions-content">
      <!-- Implementação de gerenciamento de permissões baseado em papéis -->
      <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4">Gerenciamento de Papéis e Permissões</h2>
        <div v-if="loading" class="flex justify-center">
          <div class="spinner"></div>
        </div>
        <div v-else>
          <!-- Componente de controle de permissões baseado em papéis -->
          <!-- Será implementado com base no permissionService -->
          <div class="roles-list">
            <!-- Lista de papéis e permissões associadas -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '@/stores/composables/useNotification';
import { useTeamService } from '@/composables/useTeamService';

export default defineComponent({
  name: 'TeamPermissionsPage',
  middleware: 'auth',
  layout: 'dashboard',
  setup() {
    const route = useRoute();
    const projectId = String(route.params.id);
    const { getProject } = useProjectService();
    const { getTeamMembers } = useTeamService();
    const { showError } = useNotification();
    const loading = ref(true);

    // Validar que o projeto existe
    getProject(projectId).catch(error => {
      showError('Erro ao carregar projeto', error.message || 'Não foi possível carregar os dados do projeto');
    });

    // Carregar membros da equipe
    getTeamMembers(projectId)
      .then(() => {
        loading.value = false;
      })
      .catch(error => {
        showError('Erro ao carregar equipe', error.message || 'Não foi possível carregar os membros da equipe');
        loading.value = false;
      });

    return {
      projectId,
      loading
    };
  }
});
</script>

<style scoped>
.team-permissions-container {
  padding: 1rem;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #09f;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
