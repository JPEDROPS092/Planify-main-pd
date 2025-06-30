<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useProjectService } from '~/services/projectService';
import { Icon } from '@iconify/vue';
import { useToast } from '~/composables/useToast';
import type { Projeto, ProjetoRequest, Membro, Sprint, Tarefa } from '~/api-types';
import ProjectModal from '~/components/ProjectModal.vue';

const route = useRoute();
const router = useRouter();
const projectService = useProjectService();

const projectId = computed(() => parseInt(route.params.id as string));

// Queries
const { data: project, isLoading: projectLoading, error: projectError } = useQuery({
  queryKey: ['project', projectId],
  queryFn: () => projectService.getProject(projectId.   value),
  enabled: computed(() => !!projectId.value)
});

</script>

<template>
    <div class="py-6">
      <div v-if="projectLoading" class="flex justify-center items-center py-12">
          <Icon icon="lucide:loader-2" class="h-8 w-8 animate-spin text-primary" />
      </div>
      <!-- Error -->
      <div v-else-if="projectError" class="bg-red-50 border border-red-200 rounded-md p-4">
        <div class="flex">
          <Icon icon="lucide:alert-circle" class="h-5 w-5 text-red-400" />
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">
              Erro ao carregar projeto
            </h3>
            <div class="mt-2 text-sm text-red-700">
              <p>Projeto não encontrado ou você não tem permissão para visualizá-lo.</p>
            </div>
            <div class="mt-4">
              <button
                @click="router.push('/projects')"
                class="bg-red-100 px-3 py-2 rounded-md text-sm font-medium text-red-800 hover:bg-red-200"
              >
                Voltar aos Projetos
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Project Content -->
      <div v-else-if="project">
        <!-- Header -->
        <div class="bg-white shadow rounded-lg mb-6">
          <div class="px-6 py-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <p>AAA</p>
                <h1>{{ project?.nome }}</h1>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>