<template>
  <div class="new-cost-container">
    <h1 class="text-2xl font-bold mb-4">Novo Custo</h1>
    <CostForm :project-id="projectId" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '~/composables/useNotification';
import CostForm from '@/components/forms/CostForm.vue';

export default defineComponent({
  name: 'NewCostPage',
  components: {
    CostForm
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
.new-cost-container {
  padding: 1rem;
}
</style>
