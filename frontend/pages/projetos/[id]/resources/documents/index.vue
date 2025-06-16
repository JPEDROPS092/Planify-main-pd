<template>
  <div class="project-documents-container">
    <h1 class="text-2xl font-bold mb-4">Documentos do Projeto</h1>
    <ProjectDocuments :project-id="projectId" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { ProjectDocuments } from '@/components/business/project/resources';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '~/composables/useNotification';

export default defineComponent({
  name: 'ProjectDocumentsPage',
  components: {
    ProjectDocuments
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
.project-documents-container {
  padding: 1rem;
}
</style>
