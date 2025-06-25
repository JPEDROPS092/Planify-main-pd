<template>
  <div class="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow duration-200">
    <div class="p-6">
      <!-- Header do projeto -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-3">
          <div class="flex-shrink-0">
            <Icon 
              :icon="getProjectIcon(project.status)" 
              :class="getStatusColor(project.status)"
              class="h-8 w-8"
            />
          </div>
          <div>
            <h3 class="text-lg font-medium text-gray-900 truncate">
              {{ project.titulo }}
            </h3>
            <p class="text-sm text-gray-500">
              {{ project.criador_username }}
            </p>
          </div>
        </div>
        
        <!-- Menu de ações -->
        <div class="relative" ref="menuRef">
          <button
            @click="showMenu = !showMenu"
            class="p-2 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <Icon icon="lucide:more-vertical" class="h-5 w-5 text-gray-400" />
          </button>
          
          <div
            v-if="showMenu"
            class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border border-gray-200"
          >
            <div class="py-1">
              <button
                @click="viewProject"
                class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
              >
                <Icon icon="lucide:eye" class="h-4 w-4 mr-2" />
                Ver Detalhes
              </button>
              <button
                @click="editProject"
                class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
              >
                <Icon icon="lucide:edit" class="h-4 w-4 mr-2" />
                Editar
              </button>
              <button
                @click="archiveProject"
                class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
              >
                <Icon :icon="project.arquivado ? 'lucide:archive-restore' : 'lucide:archive'" class="h-4 w-4 mr-2" />
                {{ project.arquivado ? 'Desarquivar' : 'Arquivar' }}
              </button>
              <button
                @click="deleteProject"
                class="flex items-center px-4 py-2 text-sm text-red-700 hover:bg-red-50 w-full text-left"
              >
                <Icon icon="lucide:trash-2" class="h-4 w-4 mr-2" />
                Excluir
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Descrição -->
      <p class="text-sm text-gray-600 mb-4 line-clamp-2">
        {{ project.descricao || 'Sem descrição' }}
      </p>

      <!-- Status e Prioridade -->
      <div class="flex items-center space-x-4 mb-4">
        <span 
          :class="getStatusBadgeClass(project.status)"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
        >
          {{ project.status_display }}
        </span>
        <span 
          :class="getPriorityBadgeClass(project.prioridade)"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
        >
          {{ project.prioridade_display }}
        </span>
        <span 
          v-if="project.atrasado"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"
        >
          <Icon icon="lucide:clock" class="h-3 w-3 mr-1" />
          Atrasado
        </span>
      </div>

      <!-- Progresso -->
      <div class="mb-4">
        <div class="flex justify-between text-sm text-gray-600 mb-1">
          <span>Progresso</span>
          <span>{{ project.progresso }}%</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div 
            class="bg-primary h-2 rounded-full transition-all duration-300"
            :style="{ width: `${project.progresso}%` }"
          ></div>
        </div>
      </div>

      <!-- Estatísticas -->
      <div class="grid grid-cols-3 gap-4 mb-4">
        <div class="text-center">
          <div class="text-lg font-semibold text-gray-900">{{ project.tasks_count }}</div>
          <div class="text-xs text-gray-500">Tarefas</div>
        </div>
        <div class="text-center">
          <div class="text-lg font-semibold text-gray-900">{{ project.membros_count }}</div>
          <div class="text-xs text-gray-500">Membros</div>
        </div>
        <div class="text-center">
          <div class="text-lg font-semibold text-gray-900">{{ project.dias_restantes || 0 }}</div>
          <div class="text-xs text-gray-500">Dias</div>
        </div>
      </div>

      <!-- Datas -->
      <div class="flex justify-between text-xs text-gray-500">
        <span>Início: {{ formatDate(project.data_inicio) }}</span>
        <span>Fim: {{ formatDate(project.data_fim) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue';
import type { Projeto } from '~/api-types';

interface Props {
  project: Projeto;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  view: [id: number];
  edit: [project: Projeto];
  archive: [id: number];
  delete: [id: number];
}>();

const router = useRouter();
const showMenu = ref(false);
const menuRef = ref<HTMLElement>();

// Fechar menu ao clicar fora
onClickOutside(menuRef, () => {
  showMenu.value = false;
});

const getProjectIcon = (status: string) => {
  const icons = {
    'PLANEJADO': 'lucide:calendar',
    'EM_ANDAMENTO': 'lucide:play-circle',
    'PAUSADO': 'lucide:pause-circle',
    'CONCLUIDO': 'lucide:check-circle',
    'CANCELADO': 'lucide:x-circle'
  };
  return icons[status as keyof typeof icons] || 'lucide:folder';
};

const getStatusColor = (status: string) => {
  const colors = {
    'PLANEJADO': 'text-blue-500',
    'EM_ANDAMENTO': 'text-green-500',
    'PAUSADO': 'text-yellow-500',
    'CONCLUIDO': 'text-green-600',
    'CANCELADO': 'text-red-500'
  };
  return colors[status as keyof typeof colors] || 'text-gray-500';
};

const getStatusBadgeClass = (status: string) => {
  const classes = {
    'PLANEJADO': 'bg-blue-100 text-blue-800',
    'EM_ANDAMENTO': 'bg-green-100 text-green-800',
    'PAUSADO': 'bg-yellow-100 text-yellow-800',
    'CONCLUIDO': 'bg-green-100 text-green-800',
    'CANCELADO': 'bg-red-100 text-red-800'
  };
  return classes[status as keyof typeof classes] || 'bg-gray-100 text-gray-800';
};

const getPriorityBadgeClass = (priority: string) => {
  const classes = {
    'BAIXA': 'bg-gray-100 text-gray-800',
    'MEDIA': 'bg-yellow-100 text-yellow-800',
    'ALTA': 'bg-orange-100 text-orange-800',
    'CRITICA': 'bg-red-100 text-red-800'
  };
  return classes[priority as keyof typeof classes] || 'bg-gray-100 text-gray-800';
};

const formatDate = (date: string) => {
  if (!date) return 'N/A';
  return new Date(date).toLocaleDateString('pt-BR');
};

const viewProject = () => {
  showMenu.value = false;
  router.push(`/projects/${props.project.id}`);
};

const editProject = () => {
  showMenu.value = false;
  emit('edit', props.project);
};

const archiveProject = () => {
  showMenu.value = false;
  emit('archive', props.project.id);
};

const deleteProject = () => {
  showMenu.value = false;
  emit('delete', props.project.id);
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
