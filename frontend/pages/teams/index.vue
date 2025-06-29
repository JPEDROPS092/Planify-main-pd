<template>
  <div class="container mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Equipes</h1>
      <button 
        @click="showModal = true"
        class="bg-primary hover:bg-primary-700 text-white px-4 py-2 rounded-md flex items-center"
      >
        <Icon icon="lucide:plus" class="mr-2 h-4 w-4" />
        Nova Equipe
      </button>
    </div>
    
    <!-- Loading state -->
    <div v-if="isLoading" class="text-center py-8">
      <Icon icon="svg-spinners:180-ring-with-bg" class="w-12 h-12 mx-auto text-primary" />
      <p class="mt-2">Carregando equipes...</p>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 text-center">
      <Icon icon="lucide:alert-circle" class="w-8 h-8 mx-auto text-red-500" />
      <p class="mt-2 text-red-600">Erro ao carregar equipes</p>
      <button 
        @click="() => queryClient.invalidateQueries({ queryKey: ['teams'] })"
        class="mt-2 text-red-600 underline"
      >
        Tentar novamente
      </button>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!teams?.results?.length" class="text-center py-8 border rounded-lg">
      <Icon icon="lucide:users" class="w-16 h-16 mx-auto text-gray-300" />
      <h3 class="mt-2 text-xl font-medium text-gray-700">Nenhuma equipe encontrada</h3>
      <p class="mt-1 text-gray-500">Crie uma equipe para começar a colaborar</p>
      <button 
        @click="showModal = true"
        class="mt-4 bg-primary hover:bg-primary-700 text-white px-4 py-2 rounded-md"
      >
        <Icon icon="lucide:plus" class="mr-2 h-4 w-4 inline-block" />
        Nova Equipe
      </button>
    </div>
    
    <!-- Teams grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="team in teams.results" 
        :key="team.id" 
        class="bg-white border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="p-5">
          <div class="flex justify-between items-start">
            <h3 class="text-xl font-semibold text-gray-800">{{ team.nome }}</h3>
            <div class="flex space-x-2">
              <button 
                @click="() => router.push(`/teams/${team.id}`)"
                class="text-blue-600 hover:text-blue-800"
              >
                <Icon icon="lucide:edit" class="w-5 h-5" />
              </button>
              <button 
                @click="confirmDelete(team.id)"
                class="text-red-600 hover:text-red-800"
              >
                <Icon icon="lucide:trash-2" class="w-5 h-5" />
              </button>
            </div>
          </div>
          
          <p class="text-gray-600 mt-2">{{ team.descricao || "Sem descrição" }}</p>
          
          <div class="mt-4">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Membros ({{ team.membros?.length || 0 }})</h4>
            <div class="flex -space-x-2 overflow-hidden">
              <div v-for="(membro, index) in team.membros?.slice(0, 5)" :key="index" 
                   class="inline-block h-8 w-8 rounded-full ring-2 ring-white">
                <div class="h-full w-full bg-primary-100 flex items-center justify-center text-primary text-xs font-medium">
                  {{ membro.usuario_nome?.charAt(0) || 'U' }}
                </div>
              </div>
              <div v-if="team.membros?.length > 5" 
                   class="h-8 w-8 rounded-full ring-2 ring-white bg-gray-200 flex items-center justify-center text-gray-600 text-xs">
                +{{ team.membros.length - 5 }}
              </div>
            </div>
          </div>
          
          <div class="mt-4 pt-4 border-t border-gray-100">
            <button 
              @click="() => router.push(`/teams/${team.id}`)"
              class="text-primary hover:text-primary-700 text-sm font-medium flex items-center"
            >
              Ver detalhes
              <Icon icon="lucide:chevron-right" class="ml-1 h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Pagination -->
    <div v-if="teams?.count" class="mt-8 flex justify-center">
      <div class="flex gap-2">
        <button 
          @click="currentPage--" 
          :disabled="currentPage === 1"
          class="px-4 py-2 border rounded disabled:opacity-50"
          :class="currentPage !== 1 ? 'hover:bg-gray-100' : ''"
        >
          <Icon icon="lucide:chevron-left" class="h-4 w-4" />
        </button>
        <span class="px-4 py-2 border bg-primary text-white rounded">
          {{ currentPage }} de {{ Math.ceil(teams.count / 10) }}
        </span>
        <button 
          @click="currentPage++" 
          :disabled="currentPage >= Math.ceil(teams.count / 10)"
          class="px-4 py-2 border rounded disabled:opacity-50"
          :class="currentPage < Math.ceil(teams.count / 10) ? 'hover:bg-gray-100' : ''"
        >
          <Icon icon="lucide:chevron-right" class="h-4 w-4" />
        </button>
      </div>
    </div>
    
    <!-- Create team modal -->
    <div v-if="showModal" class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showModal = false"></div>

        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
          <div class="absolute top-0 right-0 pt-4 pr-4">
            <button
              type="button"
              @click="showModal = false"
              class="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <span class="sr-only">Fechar</span>
              <Icon icon="lucide:x" class="h-6 w-6" />
            </button>
          </div>
          
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                Nova Equipe
              </h3>
              <div class="mt-4">
                <form @submit.prevent="handleCreateTeam" class="space-y-4">
                  <div>
                    <label for="nome" class="block text-sm font-medium text-gray-700">
                      Nome *
                    </label>
                    <input
                      type="text"
                      id="nome"
                      v-model="newTeam.nome"
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      placeholder="Nome da equipe"
                      required
                    />
                  </div>
                  
                  <div>
                    <label for="descricao" class="block text-sm font-medium text-gray-700">
                      Descrição
                    </label>
                    <textarea
                      id="descricao"
                      v-model="newTeam.descricao"
                      rows="3"
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      placeholder="Descrição da equipe"
                    ></textarea>
                  </div>
                  
                  <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                    <button
                      type="submit"
                      class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-start-2 sm:text-sm"
                      :disabled="createTeamMutation.isLoading"
                    >
                      <span v-if="createTeamMutation.isLoading" class="inline-block mr-2">
                        <Icon icon="lucide:loader-2" class="h-4 w-4 animate-spin" />
                      </span>
                      Criar
                    </button>
                    <button
                      type="button"
                      @click="showModal = false"
                      class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:col-start-1 sm:text-sm"
                    >
                      Cancelar
                    </button>
                  </div>
                </form>
              </div>
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

import { ref } from 'vue';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useTeamService } from '../../services/teamService';
import { Icon } from '@iconify/vue';
import { useToast } from '../../composables/useToast';
import { Equipe, EquipeRequest, PaginatedEquipeList } from '../../api-types';

const router = useRouter();
const teamService = useTeamService();
const queryClient = useQueryClient();
const { toast } = useToast();

// Estado para paginação
const currentPage = ref(1);

// Estado para modal
const showModal = ref(false);

// Estado para nova equipe
const newTeam = ref<EquipeRequest>({
  nome: '',
  descricao: ''
} as EquipeRequest);

// Consulta para carregar equipes
const { data: teams, isLoading, error } = useQuery<PaginatedEquipeList>({
  queryKey: ['teams', currentPage],
  queryFn: () => teamService.getTeams(currentPage.value)
});

// Mutação para criar equipe
const createTeamMutation = useMutation({
  mutationFn: (team: EquipeRequest) => teamService.createTeam(team),
  onSuccess: () => {
    // Invalidar a consulta para recarregar a lista de equipes
    queryClient.invalidateQueries({ queryKey: ['teams'] });
    // Limpar formulário
    newTeam.value = {
      nome: '',
      descricao: ''
    } as EquipeRequest;
    // Fechar modal
    showModal.value = false;
    
    toast({
      title: 'Equipe criada',
      description: 'A equipe foi criada com sucesso'
    });
  },
  onError: (error: any) => {
    toast({
      title: 'Erro',
      description: 'Erro ao criar a equipe',
      variant: 'destructive'
    });
    console.error('Erro ao criar equipe:', error);
  }
});

// Mutação para excluir equipe
const deleteTeamMutation = useMutation({
  mutationFn: (id: number) => teamService.deleteTeam(id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['teams'] });
    toast({
      title: 'Equipe excluída',
      description: 'A equipe foi excluída com sucesso'
    });
  },
  onError: (error: any) => {
    toast({
      title: 'Erro',
      description: 'Erro ao excluir a equipe',
      variant: 'destructive'
    });
    console.error('Erro ao excluir equipe:', error);
  }
});

// Confirmar exclusão da equipe
const confirmDelete = (id: number) => {
  if (confirm('Tem certeza que deseja excluir esta equipe?')) {
    deleteTeamMutation.mutate(id);
  }
};

// Criar nova equipe
const handleCreateTeam = () => {
  if (!newTeam.value.nome) {
    toast({
      title: 'Erro',
      description: 'O nome da equipe é obrigatório',
      variant: 'destructive'
    });
    return;
  }
  
  createTeamMutation.mutate(newTeam.value);
};
</script>
