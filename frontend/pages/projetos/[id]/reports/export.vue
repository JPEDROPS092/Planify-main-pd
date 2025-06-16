<template>
  <div class="project-export-container">
    <h1 class="text-2xl font-bold mb-4">Exportar Relatórios</h1>
    <ProjectExport :project-id="projectId" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { ProjectExport } from '@/components/business/project/management';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '~/composables/useNotification';

export default defineComponent({
  name: 'ProjectExportPage',
  components: {
    ProjectExport
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
.project-export-container {
  padding: 1rem;
}
</style>
