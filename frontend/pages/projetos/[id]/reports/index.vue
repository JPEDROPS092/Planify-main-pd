<template>
  <div class="project-reports-container">
    <h1 class="text-2xl font-bold mb-4">Relatórios do Projeto</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Card de Relatório de Tarefas -->
      <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Relatório de Tarefas</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <p class="text-gray-600 dark:text-gray-300 mb-4">Visualize o progresso das tarefas, distribuição por status e responsáveis.</p>
        <router-link :to="`/projetos/${projectId}/reports/tasks`" class="text-blue-600 hover:text-blue-800 font-medium">
          Ver relatório →
        </router-link>
      </div>
      
      <!-- Card de Relatório de Custos -->
      <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Relatório de Custos</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p class="text-gray-600 dark:text-gray-300 mb-4">Analise os custos do projeto, distribuição por categorias e tendências.</p>
        <router-link :to="`/projetos/${projectId}/reports/costs`" class="text-blue-600 hover:text-blue-800 font-medium">
          Ver relatório →
        </router-link>
      </div>
      
      <!-- Card de Relatório de Riscos -->
      <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Relatório de Riscos</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <p class="text-gray-600 dark:text-gray-300 mb-4">Identifique os principais riscos, impacto potencial e medidas de mitigação.</p>
        <router-link :to="`/projetos/${projectId}/reports/risks`" class="text-blue-600 hover:text-blue-800 font-medium">
          Ver relatório →
        </router-link>
      </div>
      
      <!-- Card de Relatório de Desempenho -->
      <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Desempenho do Projeto</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <p class="text-gray-600 dark:text-gray-300 mb-4">Acompanhe métricas de desempenho, produtividade e progresso geral.</p>
        <router-link :to="`/projetos/${projectId}/reports/performance`" class="text-blue-600 hover:text-blue-800 font-medium">
          Ver relatório →
        </router-link>
      </div>
      
      <!-- Card de Relatório de Equipe -->
      <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Relatório de Equipe</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <p class="text-gray-600 dark:text-gray-300 mb-4">Analise a distribuição de trabalho, desempenho e contribuições da equipe.</p>
        <router-link :to="`/projetos/${projectId}/reports/team`" class="text-blue-600 hover:text-blue-800 font-medium">
          Ver relatório →
        </router-link>
      </div>
      
      <!-- Card de Exportação de Relatórios -->
      <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6 hover:shadow-lg transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Exportar Relatórios</h2>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
        </div>
        <p class="text-gray-600 dark:text-gray-300 mb-4">Exporte relatórios em diferentes formatos para compartilhamento e apresentações.</p>
        <router-link :to="`/projetos/${projectId}/reports/export`" class="text-blue-600 hover:text-blue-800 font-medium">
          Exportar →
        </router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '@/stores/composables/useNotification';

export default defineComponent({
  name: 'ProjectReportsPage',
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
.project-reports-container {
  padding: 1rem;
}
</style>
