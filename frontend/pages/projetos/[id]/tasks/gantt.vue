<template>
  <div class="gantt-container">
    <h1 class="text-2xl font-bold mb-4">Gráfico de Gantt</h1>
    <GanttChart :project-id="projectId" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { GanttChart } from '@/components/business/project/planning';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '@/stores/composables/useNotification';

export default defineComponent({
  name: 'ProjectGanttPage',
  components: {
    GanttChart
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
.gantt-container {
  padding: 1rem;
}
</style>
