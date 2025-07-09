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

const filters = ref<UsersAdminUsersListParams>({
  page: 1,
  search: "",
  role: undefined,
  is_active: undefined,
});

// --- QUERIES ---
// Use the Orval hook directly
const {
  data: usersResponse,
  isLoading,
  error,
} = useUsersAdminUsersList(filters.value, {
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
      toast({ title: "Sucesso", description: "Usuário criado com sucesso." });
      queryClient.invalidateQueries({ queryKey: ["users-admin-users-list"] });
      showCreateModal.value = false;
    },
    onError: (error: any) => {
      toast({
        title: "Erro",
        description: error.response?.data?.detail || "Erro ao criar usuário",
        variant: "destructive",
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
        variant: "destructive",
      });
    },
  },
});

const deleteUserMutation = useUsersAdminUsersDestroy({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso", description: "Usuário excluído com sucesso." });
      queryClient.invalidateQueries({ queryKey: ["users-admin-users-list"] });
    },
    onError: (error: any) => {
      toast({
        title: "Erro",
        description: error.response?.data?.detail || "Erro ao excluir usuário",
        variant: "destructive",
      });
    },
  },
});

const activateUserMutation = useUsersAdminUsersActivateCreate({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso", description: "Usuário ativado com sucesso." });
      queryClient.invalidateQueries({ queryKey: ["users-admin-users-list"] });
    },
    onError: (error: any) => {
      toast({
        title: "Erro",
        description: error.response?.data?.detail || "Erro ao ativar usuário",
        variant: "destructive",
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
      });
      queryClient.invalidateQueries({ queryKey: ["users-admin-users-list"] });
    },
    onError: (error: any) => {
      toast({
        title: "Erro",
        description:
          error.response?.data?.detail || "Erro ao desativar usuário",
        variant: "destructive",
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

const toggleUserStatus = (user: User) => {
  if (user.is_active) {
    deactivateUserMutation.mutate({ id: user.id });
  } else {
    activateUserMutation.mutate({ id: user.id });
  }
};

watch(
  () => filters.value,
  (newFilters) => {
    // The Orval hook will automatically refetch when params change
  },
  { deep: true }
);

const nextPage = () => {
  if (pagination.value.next) {
    filters.value.page = (filters.value.page || 1) + 1;
  }
};

const previousPage = () => {
  if (pagination.value.previous && filters.value.page > 1) {
    filters.value.page = (filters.value.page || 2) - 1;
  }
};

const handleSearch = (searchTerm: string) => {
  filters.value = {
    ...filters.value,
    search: searchTerm,
    page: 1,
  };
};

const handleFilterChange = (newFilters: Partial<UsersAdminUsersListParams>) => {
  filters.value = {
    ...filters.value,
    ...newFilters,
    page: 1,
  };
};
</script>

<template>
  <!-- Seu template aqui, ele parece bom. -->
  <!-- Apenas certifique-se de que os nomes das mutações correspondem, por exemplo: -->
  <!-- :disabled="createMutation.isPending" -->
</template>
