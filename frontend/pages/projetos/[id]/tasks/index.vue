<template>
  <div class="project-tasks-container">
    <h1 class="text-2xl font-bold mb-4">Tarefas do Projeto</h1>
    <ProjectTasks :project-id="projectId" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { ProjectTasks } from '@/components/business/project/tasks';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '~/composables/useNotification';

export default defineComponent({
  name: 'ProjectTasksPage',
  components: {
    ProjectTasks
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
.project-tasks-container {
  padding: 1rem;
}
</style>
