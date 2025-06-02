<template>
  <div class="project-overview-container">
    <ProjectOverview :project-id="projectId" />
    <ProjectStatistics :project-id="projectId" class="mt-6" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { ProjectOverview, ProjectStatistics } from '@/components/business/project/management';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '@/stores/composables/useNotification';

export default defineComponent({
  name: 'ProjectOverviewPage',
  components: {
    ProjectOverview,
    ProjectStatistics
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
.project-overview-container {
  padding: 1rem;
}
</style>
