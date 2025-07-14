<!-- filepath: pages/users/index.vue -->
<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import UserModal from "@/components/UserModal.vue";

// Import Orval functions and types
import {
  useUsersAdminUsersList,
  useUsersAdminUsersCreate,
  useUsersAdminUsersUpdate,
  useUsersAdminUsersDestroy,
  useUsersAdminUsersActivateCreate,
  useUsersAdminUsersDeactivateCreate,
} from "@/api/usuarios/usuarios";
import type {
  User,
  UserRequest,
  UsersAdminUsersListParams,
} from "@/api/schemas";

definePageMeta({
  middleware: "auth",
  title: "Gerenciamento de Usuários",
});

// --- HOOKS AND INITIAL STATE ---
const queryClient = useQueryClient();
const { toast } = useToast();

const showCreateModal = ref(false);
const showEditModal = ref(false);
const selectedUser = ref<User | null>(null);

// Filtros apenas com paginação
const filters = ref<UsersAdminUsersListParams>({
  page: 1,
});

// --- QUERIES ---
// Use the Orval hook directly
const {
  data: usersResponse,
  isLoading,
  error,
} = useUsersAdminUsersList(filters, {
  query: {
    keepPreviousData: true,
  },
});

// Computed properties
const users = computed<User[]>(() => usersResponse.value?.data.results || []);
const pagination = computed(() => ({
  count: usersResponse.value?.data.count || 0,
  next: usersResponse.value?.data.next,
  previous: usersResponse.value?.data.previous,
}));
const currentPage = computed(() => filters.value.page || 1);

// --- MUTATIONS ---
const createUserMutation = useUsersAdminUsersCreate({
  mutation: {
    onSuccess: (response) => {
      toast({
        title: "Sucesso",
        description: "Usuário criado com sucesso.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["users-admin-users-list"] });
      showCreateModal.value = false;
    },
    onError: (error: any) => {
      toast({
        title: "Erro",
        description: error.response?.data?.detail || "Erro ao criar usuário",
        type: "error",
      });
    },
  },
});

const updateUserMutation = useUsersAdminUsersUpdate({
  mutation: {
    onSuccess: (response) => {
      toast({
        title: "Sucesso",
        description: "Usuário atualizado com sucesso.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["users-admin-users-list"] });
      showEditModal.value = false;
      selectedUser.value = null;
    },
    onError: (error: any) => {
      toast({
        title: "Erro",
        description:
          error.response?.data?.detail || "Erro ao atualizar usuário",
        type: "error",
      });
    },
  },
});

const deleteUserMutation = useUsersAdminUsersDestroy({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso",
        description: "Usuário excluído com sucesso.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["users-admin-users-list"] });
    },
    onError: (error: any) => {
      toast({
        title: "Erro",
        description: error.response?.data?.detail || "Erro ao excluir usuário",
        type: "error",
      });
    },
  },
});

const activateUserMutation = useUsersAdminUsersActivateCreate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso",
        description: "Usuário ativado com sucesso.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["users-admin-users-list"] });
    },
    onError: (error: any) => {
      toast({
        title: "Erro",
        description: error.response?.data?.detail || "Erro ao ativar usuário",
        type: "error",
      });
    },
  },
});

const deactivateUserMutation = useUsersAdminUsersDeactivateCreate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso",
        description: "Usuário desativado com sucesso.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["users-admin-users-list"] });
    },
    onError: (error: any) => {
      toast({
        title: "Erro",
        description:
          error.response?.data?.detail || "Erro ao desativar usuário",
        type: "error",
      });
    },
  },
});

// --- HANDLERS ---
const editUser = (user: User) => {
  selectedUser.value = { ...user };
  showEditModal.value = true;
};

const deleteUser = (userId: number) => {
  if (confirm("Tem certeza que deseja excluir este usuário?")) {
    deleteUserMutation.mutate({ id: userId });
  }
};

// Corrigir toggleUserStatus para enviar dados obrigatórios
const toggleUserStatus = (user: User) => {
  const userData = {
    username: user.username,
    email: user.email,
    full_name: user.full_name,
  };
  if (user.is_active) {
    deactivateUserMutation.mutate({ id: user.id, data: userData });
  } else {
    activateUserMutation.mutate({ id: user.id, data: userData });
  }
};

watch(
  () => filters.value,
  (newFilters) => {
    // The Orval hook will automatically refetch when params change
  },
  { deep: true }
);

// Corrigir paginação para evitar undefined
const nextPage = () => {
  if (pagination.value.next) {
    filters.value.page = (filters.value.page ?? 1) + 1;
  }
};
const previousPage = () => {
  if (pagination.value.previous && (filters.value.page ?? 1) > 1) {
    filters.value.page = (filters.value.page ?? 2) - 1;
  }
};
</script>

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Usuários
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mt-1">
            Gerencie os usuários do sistema.
          </p>
        </div>
        <button
          @click="showCreateModal = true"
          class="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors"
        >
          <Icon icon="lucide:plus" class="mr-2 h-5 w-5" /> Novo Usuário
        </button>
      </div>

      <!-- Tabela de Usuários -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase"
              >
                Nome
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase"
              >
                Email
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase"
              >
                Username
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase"
              >
                Papel
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase"
              >
                Status
              </th>
              <th
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase"
              >
                Ações
              </th>
            </tr>
          </thead>
          <tbody
            class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700"
          >
            <tr
              v-for="user in users"
              :key="user.id"
              class="hover:bg-gray-50 dark:hover:bg-gray-700/50"
            >
              <td
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100"
              >
                {{ user.full_name }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100"
              >
                {{ user.email }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100"
              >
                {{ user.username }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100"
              >
                {{ user.role }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="
                    user.is_active
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  "
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                >
                  {{ user.is_active ? "Ativo" : "Inativo" }}
                </span>
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
              >
                <button
                  @click="editUser(user)"
                  class="text-primary-600 hover:text-primary-900 mr-2"
                  title="Editar"
                >
                  <Icon icon="lucide:edit" class="w-5 h-5" />
                </button>
                <button
                  @click="toggleUserStatus(user)"
                  :title="user.is_active ? 'Desativar' : 'Ativar'"
                  class="text-yellow-600 hover:text-yellow-900 mr-2"
                >
                  <Icon
                    :icon="
                      user.is_active ? 'lucide:user-x' : 'lucide:user-check'
                    "
                    class="w-5 h-5"
                  />
                </button>
                <button
                  @click="deleteUser(user.id)"
                  class="text-red-600 hover:text-red-900"
                  title="Excluir"
                >
                  <Icon icon="lucide:trash" class="w-5 h-5" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="isLoading" class="text-center py-8">
          <Icon
            icon="svg-spinners:ring-resize"
            class="w-12 h-12 text-primary-600 mx-auto"
          />
        </div>
        <div v-if="error" class="text-center py-8 text-red-600">
          <p>Erro ao carregar usuários.</p>
        </div>
        <div
          v-if="users.length === 0 && !isLoading"
          class="text-center py-8 text-gray-500"
        >
          <p>Nenhum usuário encontrado.</p>
        </div>
      </div>

      <!-- Paginação -->
      <div class="flex justify-between items-center mt-6">
        <button
          @click="previousPage"
          :disabled="!pagination.previous || currentPage === 1"
          class="px-4 py-2 rounded-md border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50"
        >
          Anterior
        </button>
        <span class="text-sm text-gray-600 dark:text-gray-400"
          >Página {{ currentPage }}</span
        >
        <button
          @click="nextPage"
          :disabled="!pagination.next"
          class="px-4 py-2 rounded-md border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50"
        >
          Próxima
        </button>
      </div>

      <!-- Modais -->
      <UserModal
        v-if="showCreateModal"
        :mode="'create'"
        :is-open="showCreateModal"
        @close="showCreateModal = false"
        @submit="createUserMutation.mutate"
        :is-pending="createUserMutation.isPending"
      />
      <UserModal
        v-if="showEditModal && selectedUser"
        :mode="'edit'"
        :is-open="showEditModal"
        :user="selectedUser"
        @close="showEditModal = false"
        @submit="
          (payload: UserRequest) =>
            updateUserMutation.mutate({ id: selectedUser!.id, data: payload })
        "
        :is-pending="updateUserMutation.isPending"
      />
    </div>
  </div>
</template>
