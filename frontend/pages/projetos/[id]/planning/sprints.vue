<template>
  <div class="sprints-container">
    <h1 class="text-2xl font-bold mb-4">Gerenciamento de Sprints</h1>
    <SprintManagement :project-id="projectId" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { SprintManagement } from '@/components/business/project/planning';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/stores/composables/useProjectService';
import { useNotification } from '~/composables/useNotification';

export default defineComponent({
  name: 'SprintsPage',
  components: {
    SprintManagement
  },
  middleware: 'auth',
  layout: 'dashboard',
  setup() {
    const route = useRoute();
    const projectId = String(route.params.id);
    const { getProject } = useProjectService();
    const { showError } = useNotification();

    // Validar que o projeto existe
    getProject(projectId).catch(error => {
      showError('Erro ao carregar projeto', error.message || 'Não foi possível carregar os dados do projeto');
    });

    return {
      projectId
    };
  }
});
</script>

<style scoped>
.sprints-container {
  padding: 1rem;
}
</style>
