<template>
  <div class="new-task-container">
    <h1 class="text-2xl font-bold mb-4">Nova Tarefa</h1>
    <TaskForm :project-id="projectId" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { TaskForm } from '@/components/business/project/tasks';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '~/composables/useNotification';

export default defineComponent({
  name: 'NewTaskPage',
  components: {
    TaskForm
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
.new-task-container {
  padding: 1rem;
}
</style>
