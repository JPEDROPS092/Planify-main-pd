<template>
  <div class="container mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Minhas Tarefas</h1>
    </div>
    
    <!-- Loading state -->
    <div v-if="isLoading" class="text-center py-8">
      <Icon icon="svg-spinners:180-ring-with-bg" class="w-12 h-12 mx-auto text-primary" />
      <p class="text-gray-600 mt-2">Carregando tarefas...</p>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="text-center py-8">
      <Icon icon="carbon:warning" class="w-12 h-12 mx-auto text-red-500" />
      <p class="text-red-600 mt-2">Erro ao carregar tarefas</p>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!tasks?.results?.length" class="text-center py-8">
      <Icon icon="carbon:task" class="w-12 h-12 mx-auto text-gray-400" />
      <p class="text-gray-600 mt-2">Nenhuma tarefa atribuída a você foi encontrada</p>
    </div>
    
    <!-- Task list -->
    <div v-else class="grid gap-4">
      <div 
        v-for="task in tasks?.results" 
        :key="task.id" 
        class="border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-xl font-semibold text-gray-800">{{ task.titulo }}</h3>
            <p class="text-gray-600 mt-1">Projeto: {{ task.projeto }}</p>
            
            <div class="flex flex-wrap gap-4 mt-3">
              <div v-if="task.data_termino" class="flex items-center gap-1 text-sm text-gray-500">
                <Icon icon="carbon:calendar" class="w-4 h-4" />
                <span>Prazo: {{ formatDate(task.data_termino) }}</span>
              </div>
              
              <div v-if="task.atribuicoes && task.atribuicoes.length > 0" class="flex items-center gap-1 text-sm text-gray-500">
                <Icon icon="carbon:user" class="w-4 h-4" />
                <span>{{ task.atribuicoes.length }} atribuição(ões)</span>
              </div>
              
              <div>
                <span 
                  class="px-2 py-1 rounded-full text-xs font-medium"
                  :class="{
                    'bg-green-100 text-green-800': task.status === 'EM_ANDAMENTO',
                    'bg-blue-100 text-blue-800': task.status === 'A_FAZER',
                    'bg-gray-100 text-gray-800': task.status === 'FEITO'
                  }"
                >
                  {{ getStatusDisplay(task.status) }}
                </span>
              </div>
              
              <div v-if="task.prioridade">
                <span 
                  class="px-2 py-1 rounded-full text-xs font-medium"
                  :class="{
                    'bg-red-100 text-red-800': task.prioridade === 'ALTA',
                    'bg-yellow-100 text-yellow-800': task.prioridade === 'MEDIA',
                    'bg-blue-100 text-blue-800': task.prioridade === 'BAIXA'
                  }"
                >
                  {{ getPriorityDisplay(task.prioridade) }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="flex gap-2">
            <button 
              @click="() => $router.push(`/tasks/${task.id}`)"
              class="text-blue-600 hover:text-blue-800"
            >
              <Icon icon="carbon:view" class="w-5 h-5" />
            </button>
            <button 
              @click="confirmDelete(task.id)"
              class="text-red-600 hover:text-red-800"
            >
              <Icon icon="carbon:trash-can" class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Pagination -->
    <div v-if="tasks?.count" class="mt-8 flex justify-center">
      <div class="flex gap-2">
        <button 
          @click="currentPage--" 
          :disabled="!tasks.previous"
          class="px-4 py-2 border rounded disabled:opacity-50"
          :class="tasks.previous ? 'hover:bg-gray-100' : ''"
        >
          Anterior
        </button>
        <span class="px-4 py-2 border bg-primary text-white rounded">
          {{ currentPage }} de {{ Math.ceil(tasks.count / 10) }}
        </span>
        <button 
          @click="currentPage++" 
          :disabled="!tasks.next"
          class="px-4 py-2 border rounded disabled:opacity-50"
          :class="tasks.next ? 'hover:bg-gray-100' : ''"
        >
          Próxima
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'auth'
})

import { ref } from 'vue';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useTaskService } from '../../services/taskService';
import { Icon } from '@iconify/vue';
import { useToast } from '../../composables/useToast';
import { useAuth } from '../../composables/useAuth';

const taskService = useTaskService();
const queryClient = useQueryClient();
const { toast } = useToast();
const { user } = useAuth();

// Estado para paginação
const currentPage = ref(1);

// Consulta para carregar apenas as tarefas atribuídas ao usuário logado
const { data: tasks, isLoading, error } = useQuery({
  queryKey: ['tasks', 'my-tasks', currentPage],
  queryFn: () => taskService.getTasks({ 
    page: currentPage.value,
    minhas_tarefas: true
  }),
  enabled: !!user.value
});

// Mutação para excluir tarefa
const deleteTaskMutation = useMutation({
  mutationFn: (id) => taskService.deleteTask(id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['tasks', 'my-tasks'] });
    toast({
      title: 'Tarefa excluída',
      description: 'A tarefa foi excluída com sucesso'
    });
  },
  onError: (error) => {
    toast({
      title: 'Erro',
      description: 'Erro ao excluir a tarefa',
      variant: 'destructive'
    });
    console.error('Erro ao excluir tarefa:', error);
  }
});

// Funções auxiliares para display
const getStatusDisplay = (status) => {
  switch (status) {
    case 'A_FAZER': return 'A Fazer';
    case 'EM_ANDAMENTO': return 'Em Andamento';
    case 'FEITO': return 'Feito';
    default: return 'Não definido';
  }
};

const getPriorityDisplay = (priority) => {
  switch (priority) {
    case 'ALTA': return 'Alta';
    case 'MEDIA': return 'Média';
    case 'BAIXA': return 'Baixa';
    default: return 'Não definido';
  }
};

// Formatação de data para exibição
const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('pt-BR');
};

// Confirmar exclusão da tarefa
const confirmDelete = (id) => {
  if (confirm('Tem certeza que deseja excluir esta tarefa?')) {
    deleteTaskMutation.mutate(id);
  }
};
</script>
