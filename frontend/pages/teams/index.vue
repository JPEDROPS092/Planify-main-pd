<!-- filepath: pages/teams/index.vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";

// 1. Importar as funções e tipos corretos do Orval
import {
  useTeamsEquipesList,
  useTeamsEquipesCreate,
  useTeamsEquipesDestroy,
} from "@/api/equipes/equipes";
import type {
  Equipe,
  EquipeRequest,
  EquipeList,
  PaginatedEquipeListList,
} from "@/api/schemas";

definePageMeta({
  middleware: "auth",
});

// --- HOOKS E ESTADO INICIAL ---
const router = useRouter();
const queryClient = useQueryClient();
const { toast } = useToast();

const currentPage = ref(1);
const pageSize = 9; // 9 para um grid 3x3
const showModal = ref(false);

const getInitialFormState = (): EquipeRequest => ({
  nome: "",
  descricao: "",
});

const newTeam = ref<EquipeRequest>(getInitialFormState());

// --- QUERIES ---
const {
  data: paginatedTeams,
  isLoading,
  error,
  refetch,
} = useQuery<PaginatedEquipeListList>({
  queryKey: ["teams", currentPage],
  queryFn: () =>
    useTeamsEquipesList({ page: currentPage.value, page_size: pageSize }).then(
      (res) => res.data
    ),
});

const teams = computed(() => paginatedTeams.value?.results || []);
const totalPages = computed(() =>
  paginatedTeams.value?.count
    ? Math.ceil(paginatedTeams.value.count / pageSize)
    : 1
);

// --- MUTAÇÕES ---
const createTeamMutation = useTeamsEquipesCreate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Equipe Criada",
        description: "A nova equipe foi criada com sucesso.",
      });
      queryClient.invalidateQueries({ queryKey: ["teams"] });
      closeModal();
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail || "Não foi possível criar a equipe.",
        variant: "destructive",
      });
    },
  },
});

const deleteTeamMutation = useTeamsEquipesDestroy({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Equipe Excluída",
        description: "A equipe foi removida com sucesso.",
      });
      queryClient.invalidateQueries({ queryKey: ["teams"] });
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail || "Não foi possível excluir a equipe.",
        variant: "destructive",
      });
    },
  },
});

// --- FUNÇÕES DE MANIPULAÇÃO ---
const openModal = () => {
  newTeam.value = getInitialFormState();
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const handleCreateTeam = () => {
  if (!newTeam.value.nome) {
    toast({
      title: "Campo Obrigatório",
      description: "O nome da equipe é obrigatório.",
      variant: "destructive",
    });
    return;
  }
  createTeamMutation.mutate({ data: newTeam.value });
};

const confirmDelete = (id: number) => {
  if (
    window.confirm(
      "Tem certeza que deseja excluir esta equipe? Todos os membros e permissões associados serão removidos."
    )
  ) {
    deleteTeamMutation.mutate({ id });
  }
};

const getInitials = (name: string) => {
  if (!name) return "U";
  return name
    .split(" ")
    .map((n) => n[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();
};
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div
      class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4"
    >
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
          Gerenciamento de Equipes
        </h1>
        <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
          Crie e organize suas equipes de projeto.
        </p>
      </div>
      <button
        @click="openModal"
        class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
      >
        <Icon icon="lucide:plus" class="mr-2 h-5 w-5" />
        Nova Equipe
      </button>
    </div>

    <!-- Estados da UI -->
    <div v-if="isLoading" class="text-center py-20">
      <Icon
        icon="svg-spinners:180-ring-with-bg"
        class="w-16 h-16 mx-auto text-primary-600"
      />
    </div>
    <div
      v-else-if="error"
      class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md"
      role="alert"
    >
      Erro ao carregar equipes.
    </div>
    <div
      v-else-if="teams.length === 0"
      class="text-center py-20 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg"
    >
      <Icon
        icon="lucide:users"
        class="w-20 h-20 mx-auto text-gray-400 dark:text-gray-500"
      />
      <h3 class="mt-4 text-xl font-medium text-gray-800 dark:text-gray-200">
        Nenhuma equipe encontrada
      </h3>
      <p class="mt-1 text-gray-500 dark:text-gray-400">
        Crie uma equipe para começar a colaborar.
      </p>
    </div>

    <!-- Grid de Equipes -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="team in teams"
        :key="team.id"
        class="bg-white dark:bg-gray-800/50 border dark:border-gray-700 rounded-lg overflow-hidden shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200"
      >
        <div class="p-5">
          <div class="flex justify-between items-start">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {{ team.nome }}
            </h3>
            <div class="flex space-x-2">
              <button
                @click="router.push(`/teams/${team.id}`)"
                class="text-gray-400 hover:text-primary-600 dark:hover:text-primary-400"
                title="Editar Equipe"
              >
                <Icon icon="lucide:edit" class="w-5 h-5" />
              </button>
              <button
                @click="confirmDelete(team.id)"
                class="text-gray-400 hover:text-red-600 dark:hover:text-red-500"
                title="Excluir Equipe"
              >
                <Icon icon="lucide:trash-2" class="w-5 h-5" />
              </button>
            </div>
          </div>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-2 min-h-[40px]">
            {{ team.descricao || "Sem descrição" }}
          </p>
          <div class="mt-4">
            <h4
              class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase mb-2"
            >
              Membros ({{ team.total_membros || 0 }})
            </h4>
            <div
              v-if="(team as any).membros?.length"
              class="flex -space-x-2 overflow-hidden"
            >
              <div
                v-for="membro in (team as any).membros.slice(0, 5)"
                :key="membro.id"
                class="inline-block h-8 w-8 rounded-full ring-2 ring-white dark:ring-gray-800"
                :title="membro.usuario_nome"
              >
                <div
                  class="h-full w-full bg-primary-100 flex items-center justify-center text-primary-700 text-xs font-bold"
                >
                  {{ getInitials(membro.usuario_nome) }}
                </div>
              </div>
              <div
                v-if="(team as any).membros.length > 5"
                class="h-8 w-8 rounded-full ring-2 ring-white dark:ring-gray-800 bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-600 dark:text-gray-300 text-xs font-medium"
              >
                +{{ (team as any).membros.length - 5 }}
              </div>
            </div>
            <p v-else class="text-xs text-gray-400">
              Nenhum membro adicionado.
            </p>
          </div>
          <div class="mt-5 pt-4 border-t border-gray-200 dark:border-gray-700">
            <button
              @click="router.push(`/teams/${team.id}`)"
              class="text-sm font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300 flex items-center"
            >
              Gerenciar equipe
              <Icon icon="lucide:arrow-right" class="ml-1.5 h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Paginação -->
    <div v-if="totalPages > 1" class="mt-8 flex justify-center">
      <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
        <button
          @click="currentPage--"
          :disabled="!paginatedTeams?.previous"
          class="relative inline-flex items-center px-3 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Anterior
        </button>
        <span
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-200"
          >Página {{ currentPage }} de {{ totalPages }}</span
        >
        <button
          @click="currentPage++"
          :disabled="!paginatedTeams?.next"
          class="relative inline-flex items-center px-3 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Próximo
        </button>
      </nav>
    </div>

    <!-- Modal de Criação de Equipe -->
    <div v-if="showModal" class="fixed z-50 inset-0 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen">
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75"
          @click="closeModal"
        ></div>
        <div
          class="bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full"
        >
          <form @submit.prevent="handleCreateTeam">
            <div class="px-4 pt-5 pb-4 sm:p-6">
              <h3
                class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100"
              >
                Criar Nova Equipe
              </h3>
              <div class="mt-4 space-y-4">
                <div>
                  <label
                    for="nome"
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                    >Nome da Equipe *</label
                  >
                  <input
                    type="text"
                    v-model="newTeam.nome"
                    id="nome"
                    class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700"
                    required
                  />
                </div>
                <div>
                  <label
                    for="descricao"
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                    >Descrição</label
                  >
                  <textarea
                    v-model="newTeam.descricao"
                    id="descricao"
                    rows="3"
                    class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700"
                  ></textarea>
                </div>
              </div>
            </div>
            <div
              class="bg-gray-50 dark:bg-gray-900 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse"
            >
              <button
                type="submit"
                :disabled="createTeamMutation.isPending.value"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
              >
                <Icon
                  v-if="createTeamMutation.isPending.value"
                  icon="svg-spinners:180-ring-with-bg"
                  class="mr-2 h-5 w-5"
                />
                Criar Equipe
              </button>
              <button
                type="button"
                @click="closeModal"
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 shadow-sm px-4 py-2 bg-white dark:bg-gray-700 text-base font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-600 sm:mt-0 sm:w-auto sm:text-sm"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
