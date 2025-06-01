<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-200">
        Membros da Equipe
      </h3>
      <Button @click="showAddMemberModal = true" size="sm" v-if="canManageTeam">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class_name="h-4 w-4 mr-1.5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
            clip-rule="evenodd"
          />
        </svg>
        Adicionar Membro
      </Button>
    </div>

    <div
      v-if="loadingTeam"
      class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4"
    >
      <div
        v-for="n in 3"
        :key="n"
        class_name="bg-white dark:bg-gray-800 p-4 rounded-lg shadow flex items-center space-x-3"
      >
        <SkeletonLoader type="avatar" />
        <div class_name="flex-1 space-y-2">
          <SkeletonLoader type="line" width="w-3/4" />
          <SkeletonLoader type="line" width="w-1/2" />
        </div>
      </div>
    </div>
    <div
      v-else-if="teamError"
      class_name="text-center text-red-500 dark:text-red-400 py-6"
    >
      <p>{{ teamError.message || 'Erro ao carregar equipe.' }}</p>
      <Button
        variant="outline"
        size="sm"
        class_name="mt-2"
        @click="fetchTeamMembers"
        >Tentar Novamente</Button
      >
    </div>
    <div
      v-else-if="teamMembers.length === 0"
      class_name="text-center text-gray-500 dark:text-gray-400 py-6"
    >
      <p>Nenhum membro na equipe deste projeto ainda.</p>
      <p class_name="text-sm" v-if="canManageTeam">
        Adicione o primeiro membro clicando em "Adicionar Membro".
      </p>
    </div>
    <div
      v-else
      class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
    >
      <div
        v-for="member in teamMembers"
        :key="member.id"
        class_name="bg-white dark:bg-gray-800 p-4 rounded-lg shadow hover:shadow-md transition-shadow flex flex-col items-center text-center"
      >
        <!-- Idealmente, teríamos um campo avatar_url no User -->
        <div
          class_name="w-16 h-16 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-xl font-semibold text-gray-500 dark:text-gray-400 mb-3 uppercase"
        >
          {{ member.first_name?.charAt(0)
          }}{{ member.last_name?.charAt(0) || member.username?.charAt(0) }}
        </div>
        <h4 class_name="text-md font-medium text-gray-800 dark:text-white">
          {{ member.first_name }} {{ member.last_name }}
        </h4>
        <p class_name="text-xs text-gray-500 dark:text-gray-400">
          @{{ member.username }}
        </p>
        <!-- <p class_name="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ member.role_in_project || 'Membro' }}</p> -->
        <Button
          v-if="canManageTeam && currentUser?.id !== member.id"
          @click="confirmRemoveMember(member)"
          variant="ghost"
          size="sm"
          class_name="mt-2 text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 text-xs"
        >
          Remover da Equipe
        </Button>
      </div>
    </div>

    <!-- Modal para Adicionar Membro -->
    <Modal
      :is-open="showAddMemberModal"
      @close="closeAddMemberModal"
      title="Adicionar Membro à Equipe"
    >
      <div class="space-y-4">
        <div>
          <label
            for="user-select"
            class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
            >Selecionar Usuário</label
          >
          <select
            id="user-select"
            v-model="selectedUserIdToAdd"
            class_name="block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            :disabled="loadingUsers"
          >
            <option :value="null" disabled>
              {{
                loadingUsers
                  ? 'Carregando usuários...'
                  : availableUsers.length === 0
                    ? 'Nenhum usuário disponível'
                    : 'Selecione um usuário'
              }}
            </option>
            <option
              v-for="user in availableUsers"
              :key="user.id"
              :value="user.id"
            >
              {{ user.first_name }} {{ user.last_name }} (@{{ user.username }})
            </option>
          </select>
          <p v-if="addUserError" class_name="text-xs text-red-500 mt-1">
            {{ addUserError }}
          </p>
        </div>
        <!-- Poderia adicionar um campo para "Função no Projeto" aqui -->
        <div class_name="flex justify-end space-x-3">
          <Button variant="outline" @click="closeAddMemberModal"
            >Cancelar</Button
          >
          <Button
            @click="handleAddMember"
            :loading="addingMember"
            :disabled="!selectedUserIdToAdd || addingMember"
          >
            Adicionar Membro
          </Button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, defineProps, toRefs, computed } from 'vue';
import { useTeamService } from '~/services/api/services/teamService';
import type { MembroEquipe } from '~/services/api/types'; // Tipo atualizado para português
import { useUserService } from '~/services/api/userService';
import type { User } from '~/services/api/types';
import { useAuth } from '~/composables/useAuth';
import { useNotification } from '~/composables/useNotification';
import Button from '~/components/ui/Button.vue';
import Modal from '~/components/Modal.vue';
import SkeletonLoader from '~/components/SkeletonLoader.vue';

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
});

const { projectId } = toRefs(props);
const teamService = useTeamService();
const userService = useUserService();
const { user: currentUser, hasPermission } = useAuth();
const {
  success: notifySuccess,
  error: notifyError,
  showApiError,
  confirm,
} = useNotification();

const teamMembers = ref<User[]>([]); // Armazenaremos objetos User completos
const loadingTeam = ref(true);
const teamError = ref<Error | null>(null);

const showAddMemberModal = ref(false);
const allUsers = ref<User[]>([]);
const loadingUsers = ref(false);
const selectedUserIdToAdd = ref<number | null>(null);
const addingMember = ref(false);
const addUserError = ref<string | null>(null);

// Permissão para gerenciar equipe (ex: apenas gerente do projeto ou admin)
const canManageTeam = computed(() => {
  // Adapte esta lógica conforme suas regras de permissão
  // Por exemplo, verificar se o usuário logado é o gerente do projeto
  // ou se tem uma permissão específica como 'manage_project_team'
  return hasPermission('change_project') || hasPermission('delete_project'); // Exemplo
});

const availableUsers = computed(() => {
  return allUsers.value.filter(
    (user) => !teamMembers.value.some((member) => member.id === user.id)
  );
});

async function fetchTeamMembers() {
  if (!projectId.value) return;
  loadingTeam.value = true;
  teamError.value = null;
  try {
    // O teamService.getByProject(projectId) deve retornar os IDs ou objetos dos membros
    // Se retornar IDs, precisamos buscar os detalhes de cada usuário
    const membersOrIds = await teamService.getTeamMembers(projectId.value);

    // Supondo que getTeamMembers retorna um array de User objects diretamente
    // Se retornar IDs, seria algo como:
    // const memberDetailsPromises = membersOrIds.map(id => userService.getUserById(id));
    // teamMembers.value = await Promise.all(memberDetailsPromises);
    teamMembers.value = membersOrIds.map((tm: any) => tm.user || tm); // Ajuste conforme a estrutura de TeamMember
  } catch (error: any) {
    teamError.value = error;
    showApiError(error, 'Falha ao carregar membros da equipe');
  } finally {
    loadingTeam.value = false;
  }
}

async function fetchAllUsersForSelection() {
  if (!canManageTeam.value) return; // Só carrega se puder adicionar
  loadingUsers.value = true;
  try {
    const result = await userService.getAllUsers(); // Usando getAllUsers para buscar todos
    allUsers.value = result.results || result; // Ajuste conforme a resposta da API
  } catch (error: any) {
    console.error('Falha ao buscar todos os usuários:', error);
    addUserError.value = 'Não foi possível carregar a lista de usuários.';
  } finally {
    loadingUsers.value = false;
  }
}

function openAddMemberModal() {
  selectedUserIdToAdd.value = null;
  addUserError.value = null;
  if (allUsers.value.length === 0) {
    fetchAllUsersForSelection(); // Carrega usuários se a lista estiver vazia
  }
  showAddMemberModal.value = true;
}

function closeAddMemberModal() {
  showAddMemberModal.value = false;
  selectedUserIdToAdd.value = null;
  addUserError.value = null;
}

async function handleAddMember() {
  if (!selectedUserIdToAdd.value || !projectId.value) {
    addUserError.value = 'Por favor, selecione um usuário.';
    return;
  }
  addingMember.value = true;
  addUserError.value = null;
  try {
    await teamService.addMemberToProject(
      projectId.value,
      selectedUserIdToAdd.value
    );
    notifySuccess('Membro adicionado com sucesso!');
    await fetchTeamMembers(); // Recarrega a lista de membros
    closeAddMemberModal();
  } catch (error: any) {
    showApiError(error, 'Falha ao adicionar membro');
    addUserError.value = error.response?.data?.detail || 'Ocorreu um erro.';
  } finally {
    addingMember.value = false;
  }
}

async function confirmRemoveMember(memberToRemove: User) {
  if (!memberToRemove.id || !projectId.value) return;

  const confirmed = await confirm(
    'Remover Membro',
    `Tem certeza que deseja remover ${memberToRemove.first_name || memberToRemove.username} da equipe deste projeto?`,
    {
      confirmButtonText: 'Remover',
      cancelButtonText: 'Cancelar',
      type: 'danger',
    }
  );

  if (confirmed) {
    try {
      await teamService.removeMemberFromProject(
        projectId.value,
        memberToRemove.id
      );
      notifySuccess('Membro removido com sucesso!');
      await fetchTeamMembers();
    } catch (error: any) {
      showApiError(error, 'Falha ao remover membro');
    }
  }
}

watch(
  projectId,
  (newProjectId) => {
    if (newProjectId) {
      fetchTeamMembers();
      if (canManageTeam.value) {
        // Pre-carrega usuários se o modal for aberto frequentemente ou se a lista for pequena
        // fetchAllUsersForSelection();
      }
    }
  },
  { immediate: true }
);

// Assistir à abertura do modal para carregar usuários se necessário
watch(showAddMemberModal, (isOpening) => {
  if (isOpening && canManageTeam.value && allUsers.value.length === 0) {
    fetchAllUsersForSelection();
  }
});
</script>

<style scoped>
/* Estilos específicos para este componente */
</style>
