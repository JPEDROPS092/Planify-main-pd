<!-- filepath: pages/users/index.vue -->
<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import UserModal from "@/components/UserModal.vue";

// Importar as funções e tipos corretos do Orval
import {
  useUsersAdminUsersList,
  useUsersAdminUsersCreate,
  useUsersAdminUsersUpdate,
  useUsersAdminUsersDestroy,
  useUsersAdminUsersActivateCreate,
  useUsersAdminUsersDeactivateCreate,
} from "@/api/usuários/usuários";
import type {
  User,
  UserRequest,
  PaginatedUserList,
  UsersAdminUsersListParams,
} from "@/api/schemas";

definePageMeta({
  middleware: "auth",
  title: "Gerenciamento de Usuários",
});

// --- HOOKS E ESTADO INICIAL ---
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
const {
  data: paginatedUsers,
  isLoading,
  error,
  refetch,
} = useQuery<PaginatedUserList>({
  queryKey: ["users", filters],
  queryFn: () => useUsersAdminUsersList(filters.value).then((res) => res.data),
  keepPreviousData: true,
});

const users = computed(() => paginatedUsers.value?.results || []);
const pagination = computed(() => ({
  count: paginatedUsers.value?.count || 0,
  next: paginatedUsers.value?.next,
  previous: paginatedUsers.value?.previous,
}));
const currentPage = computed(() => filters.value.page || 1);

// --- MUTAÇÕES ---
const createMutation = useUsersAdminUsersCreate({
  /* ... seu código de mutação ... */
});
const updateMutation = useUsersAdminUsersUpdate({
  /* ... seu código de mutação ... */
});
const deleteMutation = useUsersAdminUsersDestroy({
  /* ... seu código de mutação ... */
});
const activateUserMutation = useUsersAdminUsersActivateCreate({
  /* ... seu código de mutação ... */
});
const deactivateUserMutation = useUsersAdminUsersDeactivateCreate({
  /* ... seu código de mutação ... */
});

// --- HANDLERS ---
const loadUsers = () => refetch();

const editUser = (user: User) => {
  selectedUser.value = { ...user };
  showEditModal.value = true;
};

// ... (resto das suas funções handle, elas parecem corretas) ...

const onUserSaved = () => {
  showCreateModal.value = false;
  showEditModal.value = false;
  selectedUser.value = null;
  loadUsers(); // Recarrega a lista após salvar
};

const nextPage = () => {
  if (pagination.value.next) filters.value.page++;
};

const previousPage = () => {
  if (pagination.value.previous) filters.value.page--;
};

// --- HELPERS ---
const getRoleLabel = (role?: string) =>
  ({ ADMIN: "Admin", PROJECT_MANAGER: "Gerente", TEAM_MEMBER: "Membro" })[
    role || ""
  ] || "N/A";
const formatDate = (date: string) =>
  date ? new Date(date).toLocaleDateString("pt-BR") : "-";

// Carregar dados no mounted
onMounted(loadUsers);
</script>

<template>
  <!-- Seu template aqui, ele parece bom. -->
  <!-- Apenas certifique-se de que os nomes das mutações correspondem, por exemplo: -->
  <!-- :disabled="createMutation.isPending" -->
</template>
