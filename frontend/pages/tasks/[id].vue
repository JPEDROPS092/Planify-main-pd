<template>
  <div class="container mx-auto p-6">
    <!-- Loading state -->
    <div v-if="isLoading" class="text-center py-8">
      <Icon icon="svg-spinners:180-ring-with-bg" class="w-12 h-12 mx-auto text-primary" />
      <p class="mt-2">Carregando tarefa...</p>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 text-center">
      <Icon icon="carbon:warning" class="w-8 h-8 mx-auto text-red-500" />
      <p class="mt-2 text-red-600">Erro ao carregar tarefa</p>
      <button 
        @click="() => router.back()"
        class="mt-2 text-red-600 underline"
      >
        Voltar
      </button>
    </div>
    
    <!-- Task details -->
    <div v-else-if="task" class="bg-white rounded-lg shadow-sm">
      <div class="border-b p-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button 
              @click="router.back()" 
              class="text-gray-500 hover:text-gray-700"
            >
              <Icon icon="carbon:arrow-left" class="w-6 h-6" />
            </button>
            <h1 class="text-2xl font-bold">{{ task.titulo }}</h1>
          </div>
          
          <div class="flex gap-2">
            <button 
              @click="showEditModal = true"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center gap-2"
            >
              <Icon icon="carbon:edit" class="w-4 h-4" />
              Editar
            </button>
          </div>
        </div>
      </div>
      
      <div class="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="md:col-span-2 space-y-6">
          <div>
            <h2 class="text-xl font-semibold mb-2">Descrição</h2>
            <p class="text-gray-700 whitespace-pre-line">{{ task.descricao || "Sem descrição detalhada" }}</p>
          </div>
          
          <div v-if="task.comentarios && task.comentarios.length">
            <h2 class="text-xl font-semibold mb-2">Comentários</h2>
            <div class="space-y-4">
              <div 
                v-for="comentario in task.comentarios" 
                :key="comentario.id"
                class="border rounded-lg p-4"
              >
                <div class="flex justify-between items-center mb-2">
                  <div class="font-medium">{{ comentario.autor_nome }}</div>
                  <div class="text-sm text-gray-500">{{ formatDate(comentario.data_criacao) }}</div>
                </div>
                <p class="text-gray-700">{{ comentario.texto }}</p>
              </div>
            </div>
          </div>
          
          <!-- Add comment form -->
          <div>
            <h2 class="text-xl font-semibold mb-2">Adicionar Comentário</h2>
            <form @submit.prevent="addComment">
              <textarea 
                v-model="newComment" 
                class="w-full p-2 border rounded-md focus:ring-2 focus:ring-primary focus:outline-none"
                rows="3"
                placeholder="Escreva seu comentário aqui..."
              ></textarea>
              <button 
                type="submit" 
                class="mt-2 px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark disabled:opacity-50"
                :disabled="!newComment.trim() || addCommentMutation.isPending"
              >
                <span v-if="addCommentMutation.isPending">Enviando...</span>
                <span v-else>Enviar Comentário</span>
              </button>
            </form>
          </div>
        </div>
        
        <div class="space-y-6">
          <div class="border rounded-lg p-4">
            <h2 class="text-lg font-semibold mb-3">Detalhes</h2>
            
            <div class="space-y-3">
              <div>
                <div class="text-sm text-gray-500">Status</div>
                <div class="flex items-center mt-1">
                  <span 
                    class="px-2 py-1 rounded-full text-xs font-medium"
                    :class="{
                      'bg-green-100 text-green-800': task.status === 'EM_ANDAMENTO',
                      'bg-blue-100 text-blue-800': task.status === 'NAO_INICIADA',
                      'bg-gray-100 text-gray-800': task.status === 'CONCLUIDA',
                      'bg-red-100 text-red-800': task.status === 'ATRASADA',
                      'bg-yellow-100 text-yellow-800': task.status === 'BLOQUEADA'
                    }"
                  >
                    {{ task.status_display }}
                  </span>
                </div>
              </div>
              
              <div>
                <div class="text-sm text-gray-500">Prioridade</div>
                <div class="flex items-center mt-1">
                  <span 
                    class="px-2 py-1 rounded-full text-xs font-medium"
                    :class="{
                      'bg-red-100 text-red-800': task.prioridade === 'ALTA',
                      'bg-yellow-100 text-yellow-800': task.prioridade === 'MEDIA',
                      'bg-blue-100 text-blue-800': task.prioridade === 'BAIXA'
                    }"
                  >
                    {{ task.prioridade_display }}
                  </span>
                </div>
              </div>
              
              <div>
                <div class="text-sm text-gray-500">Projeto</div>
                <div class="font-medium">{{ task.projeto_nome }}</div>
              </div>
              
              <div>
                <div class="text-sm text-gray-500">Responsável</div>
                <div class="font-medium">{{ task.responsavel_nome || "Não atribuído" }}</div>
              </div>
              
              <div>
                <div class="text-sm text-gray-500">Data de Criação</div>
                <div class="font-medium">{{ formatDate(task.data_criacao) }}</div>
              </div>
              
              <div>
                <div class="text-sm text-gray-500">Prazo</div>
                <div class="font-medium">{{ formatDate(task.data_vencimento) }}</div>
              </div>
            </div>
            
            <div class="mt-4 space-y-2">
              <button 
                @click="updateStatus('CONCLUIDA')"
                class="w-full px-3 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 flex items-center justify-center gap-2"
                :disabled="task.status === 'CONCLUIDA'"
              >
                <Icon icon="carbon:checkmark" class="w-4 h-4" />
                Marcar como Concluída
              </button>
              
              <button 
                v-if="task.responsavel"
                @click="removeAssignment"
                class="w-full px-3 py-2 bg-yellow-600 text-white rounded-md hover:bg-yellow-700 flex items-center justify-center gap-2"
              >
                <Icon icon="carbon:user-remove" class="w-4 h-4" />
                Remover Responsável
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useTaskService } from '../../services/taskService';
import { Icon } from '@iconify/vue';
import { useToast } from '../../composables/useToast';
import { Tarefa } from '../../api-types';

const router = useRouter();
const route = useRoute();
const taskId = computed(() => Number(route.params.id));

const taskService = useTaskService();
const queryClient = useQueryClient();
const { toast } = useToast();

// Estado para o formulário de comentários
const newComment = ref('');
const showEditModal = ref(false);

// Consulta para carregar a tarefa
const { data: task, isLoading, error } = useQuery<Tarefa>({
  queryKey: ['task', taskId],
  queryFn: () => taskService.getTask(taskId.value)
});

// Mutação para adicionar comentário
const addCommentMutation = useMutation({
  mutationFn: () => taskService.addComment(taskId.value, { texto: newComment.value }),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['task', taskId] });
    newComment.value = '';
    toast({
      title: 'Comentário adicionado',
      description: 'Seu comentário foi adicionado com sucesso'
    });
  },
  onError: (error: any) => {
    toast({
      title: 'Erro',
      description: 'Erro ao adicionar comentário',
      variant: 'destructive'
    });
    console.error('Erro ao adicionar comentário:', error);
  }
});

// Mutação para atualizar status
const updateStatusMutation = useMutation({
  mutationFn: (status: string) => taskService.updateTaskStatus(taskId.value, { status }),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['task', taskId] });
    toast({
      title: 'Status atualizado',
      description: 'O status da tarefa foi atualizado com sucesso'
    });
  },
  onError: (error: any) => {
    toast({
      title: 'Erro',
      description: 'Erro ao atualizar status',
      variant: 'destructive'
    });
    console.error('Erro ao atualizar status:', error);
  }
});

// Mutação para remover responsável
const removeAssignmentMutation = useMutation({
  mutationFn: () => taskService.removeAssignment(taskId.value),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['task', taskId] });
    toast({
      title: 'Responsável removido',
      description: 'O responsável foi removido com sucesso'
    });
  },
  onError: (error: any) => {
    toast({
      title: 'Erro',
      description: 'Erro ao remover responsável',
      variant: 'destructive'
    });
    console.error('Erro ao remover responsável:', error);
  }
});

// Formatação de data para exibição
const formatDate = (date: string): string => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('pt-BR');
};

// Adicionar comentário
const addComment = () => {
  if (!newComment.value.trim()) return;
  addCommentMutation.mutate();
};

// Atualizar status
const updateStatus = (status: string) => {
  updateStatusMutation.mutate(status);
};

// Remover responsável
const removeAssignment = () => {
  if (confirm('Tem certeza que deseja remover o responsável desta tarefa?')) {
    removeAssignmentMutation.mutate();
  }
};
</script>
