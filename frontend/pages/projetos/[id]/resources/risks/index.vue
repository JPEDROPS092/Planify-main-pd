<template>
  <div class="project-risks-container">
    <h1 class="text-2xl font-bold mb-4">Riscos do Projeto</h1>
    <ProjectRisks :project-id="projectId" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { ProjectRisks } from '@/components/business/project/resources';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '@/stores/composables/useNotification';

export default defineComponent({
  name: 'ProjectRisksPage',
  components: {
    ProjectRisks
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
.project-risks-container {
  padding: 1rem;
}
</style>
