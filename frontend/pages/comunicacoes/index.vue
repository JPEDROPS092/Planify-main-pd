<template>
  <NuxtLayout name="dashboard">
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h1
          class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white"
        >
          Comunicações
        </h1>
        <button
          @click="openNewMessageModal"
          class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4 mr-2"
          >
            <path d="M5 12h14"></path>
            <path d="M12 5v14"></path>
          </svg>
          Nova Mensagem
        </button>
      </div>

      <!-- Filtros -->
      <div class="flex flex-wrap gap-4">
        <div class="relative w-64">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar mensagens..."
            class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
          />
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="absolute right-3 top-2.5 h-4 w-4 text-gray-400 dark:text-gray-500"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.3-4.3"></path>
          </svg>
        </div>
        <select
          v-model="typeFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
        >
          <option value="">Todos os tipos</option>
          <option value="MENSAGEM">Mensagem</option>
          <option value="NOTIFICACAO">Notificação</option>
          <option value="ALERTA">Alerta</option>
        </select>
        <select
          v-model="statusFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
        >
          <option value="">Todos os status</option>
          <option value="NAO_LIDA">Não lida</option>
          <option value="LIDA">Lida</option>
        </select>
        <select
          v-model="projectFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
        >
          <option value="">Todos os projetos</option>
          <option
            v-for="project in projects"
            :key="project.id"
            :value="project.id"
          >
            {{ project.titulo }}
          </option>
        </select>
      </div>

      <!-- Loading e estados vazios -->
      <div
        v-if="loading"
        class="flex flex-col items-center justify-center py-12"
      >
        <div
          class="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"
        ></div>
        <p class="mt-4 text-sm text-gray-500 dark:text-gray-400">
          Carregando mensagens...
        </p>
      </div>

      <EmptyState
        v-else-if="filteredMessages.length === 0"
        title="Nenhuma mensagem encontrada"
        description="Não encontramos nenhuma mensagem com os filtros atuais. Tente ajustar os filtros ou envie uma nova mensagem."
        icon="message-square"
      >
        <template #action>
          <button
            @click="openNewMessageModal"
            class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="h-4 w-4 mr-2"
            >
              <path d="M5 12h14"></path>
              <path d="M12 5v14"></path>
            </svg>
            Enviar nova mensagem
          </button>
        </template>
      </EmptyState>

      <!-- Messages list -->
      <div v-else class="space-y-4">
        <div
          v-for="message in filteredMessages"
          :key="message.id"
          class="flex rounded-lg border bg-white p-4 shadow-sm transition-all hover:shadow-md dark:border-gray-700 dark:bg-gray-800"
        >
          <div class="mr-4 flex-shrink-0">
            <div
              class="flex h-10 w-10 items-center justify-center rounded-full text-white"
              :class="{
                'bg-blue-500': message.tipo === 'MENSAGEM',
                'bg-yellow-500': message.tipo === 'NOTIFICACAO',
                'bg-red-500': message.tipo === 'ALERTA',
              }"
            >
              <svg
                v-if="message.tipo === 'MENSAGEM'"
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="h-5 w-5"
              >
                <path
                  d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                ></path>
              </svg>
              <svg
                v-else-if="message.tipo === 'NOTIFICACAO'"
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="h-5 w-5"
              >
                <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path>
                <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"></path>
              </svg>
              <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="h-5 w-5"
              >
                <path
                  d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                ></path>
                <line x1="12" x2="12" y1="9" y2="13"></line>
                <line x1="12" x2="12.01" y1="17" y2="17"></line>
              </svg>
            </div>
          </div>
          <div class="flex-1">
            <div class="flex items-center justify-between">
              <h3 class="font-medium text-gray-900 dark:text-white">
                {{ message.titulo }}
              </h3>
              <div class="flex items-center gap-2">
                <span class="text-xs text-gray-500 dark:text-gray-400">{{
                  formatDate(message.data_envio)
                }}</span>
                <button
                  v-if="message.status === 'NAO_LIDA'"
                  @click="markAsRead(message.id)"
                  class="rounded-full p-1 text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
                  title="Marcar como lida"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="h-4 w-4"
                  >
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                  </svg>
                </button>
              </div>
            </div>
            <p class="mt-1 text-sm text-gray-700 dark:text-gray-400">
              {{ message.conteudo }}
            </p>
            <div class="mt-2 flex items-center text-xs">
              <span
                :class="{
                  'bg-blue-100 text-blue-800': message.tipo === 'MENSAGEM',
                  'bg-yellow-100 text-yellow-800':
                    message.tipo === 'NOTIFICACAO',
                  'bg-red-100 text-red-800': message.tipo === 'ALERTA',
                }"
                class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
              >
                {{ getTypeLabel(message.tipo) }}
              </span>
              <span class="mx-2 text-gray-500 dark:text-gray-400">•</span>
              <span class="text-gray-500 dark:text-gray-400"
                >De: {{ message.remetente }}</span
              >
              <span
                v-if="message.projeto"
                class="mx-2 text-gray-500 dark:text-gray-400"
                >•</span
              >
              <span
                v-if="message.projeto"
                class="text-gray-500 dark:text-gray-400"
                >Projeto: {{ getProjectName(message.projeto) }}</span
              >
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div
        v-if="totalPages > 1"
        class="flex items-center justify-center space-x-2 pt-4"
      >
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50 dark:border-gray-700 dark:text-gray-400"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4"
          >
            <path d="m15 18-6-6 6-6"></path>
          </svg>
        </button>
        <div
          v-for="page in paginationRange"
          :key="page"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md text-sm font-medium"
          :class="
            page === currentPage
              ? 'bg-blue-600 text-white'
              : 'border border-gray-300 text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700'
          "
          @click="changePage(page)"
        >
          {{ page }}
        </div>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50 dark:border-gray-700 dark:text-gray-400"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4"
          >
            <path d="m9 18 6-6-6-6"></path>
          </svg>
        </button>
      </div>

      <!-- Modal para nova mensagem -->
      <div
        v-if="showMessageModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
      >
        <div
          class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl dark:bg-gray-900"
        >
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">
              Nova Mensagem
            </h3>
            <button
              @click="showMessageModal = false"
              class="rounded-full p-1 hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="h-5 w-5"
              >
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
              </svg>
            </button>
          </div>
          <form @submit.prevent="sendMessage" class="mt-4 space-y-4">
            <div>
              <label
                for="titulo"
                class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                >Título</label
              >
              <input
                id="titulo"
                v-model="messageForm.titulo"
                type="text"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              />
            </div>
            <div>
              <label
                for="conteudo"
                class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                >Conteúdo</label
              >
              <textarea
                id="conteudo"
                v-model="messageForm.conteudo"
                rows="4"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              ></textarea>
            </div>
            <div>
              <label
                for="tipo"
                class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                >Tipo</label
              >
              <select
                id="tipo"
                v-model="messageForm.tipo"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              >
                <option value="MENSAGEM">Mensagem</option>
                <option value="NOTIFICACAO">Notificação</option>
                <option value="ALERTA">Alerta</option>
              </select>
            </div>
            <div>
              <label
                for="destinatarios"
                class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                >Destinatários</label
              >
              <select
                id="destinatarios"
                v-model="messageForm.destinatarios"
                multiple
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              >
                <option v-for="user in users" :key="user.id" :value="user.id">
                  {{ user.username }}
                </option>
              </select>
              <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                Segure Ctrl (ou Cmd) para selecionar múltiplos destinatários
              </p>
            </div>
            <div>
              <label
                for="projeto"
                class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                >Projeto (opcional)</label
              >
              <select
                id="projeto"
                v-model="messageForm.projeto"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              >
                <option value="">Nenhum</option>
                <option
                  v-for="project in projects"
                  :key="project.id"
                  :value="project.id"
                >
                  {{ project.titulo }}
                </option>
              </select>
            </div>
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="showMessageModal = false"
                class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-gray-700"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="sending"
                class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-70 dark:bg-blue-700 dark:hover:bg-blue-600"
              >
                <span
                  v-if="sending"
                  class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
                ></span>
                {{ sending ? 'Enviando...' : 'Enviar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeMount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useMessageService, useNotificationService } from '~/services/api'; // Updated import from central API
import { useProjectService } from '~/services/api'; // Updated import from central API
import { useUserService } from '~/services/api'; // Updated import from central API
import { useAuth } from '~/composables/useAuth';
import EmptyState from '~/components/EmptyState.vue';

definePageMeta({
  middleware: ['auth'],
});

const router = useRouter();
const route = useRoute();

// Get services from the new API structure
const { messages: messagesRef, isLoading, error: serviceError, fetchMessages, sendMessage: sendNewMessage, markAsRead: markMessageAsRead } = useMessageService();
const { fetchProjects } = useProjectService();
const { fetchUsers } = useUserService();
const { user } = useAuth();

// Estado
const messages = ref([]);
const projects = ref([]);
const users = ref([]);
const loading = ref(true);
const error = ref(null);
const currentPage = ref(1);
const totalPages = ref(1);
const totalItems = ref(0);
const itemsPerPage = ref(10);
const searchQuery = ref('');
const typeFilter = ref('');
const statusFilter = ref('');
const projectFilter = ref('');
const showMessageModal = ref(false);
const sending = ref(false);

// Formulário de mensagem
const messageForm = ref({
  titulo: '',
  conteudo: '',
  tipo: 'MENSAGEM',
  destinatarios: [],
  projeto: '',
});

// Filtrar mensagens
const filteredMessages = computed(() => {
  return messages.value.filter((message) => {
    const matchesSearch =
      searchQuery.value === '' ||
      message.titulo.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      message.conteudo.toLowerCase().includes(searchQuery.value.toLowerCase());

    const matchesType =
      typeFilter.value === '' || message.tipo === typeFilter.value;
    const matchesStatus =
      statusFilter.value === '' || message.status === statusFilter.value;
    const matchesProject =
      projectFilter.value === '' ||
      message.projeto === parseInt(projectFilter.value);

    return matchesSearch && matchesType && matchesStatus && matchesProject;
  });
});

// Paginação
const paginationRange = computed(() => {
  const range = [];
  const maxVisiblePages = 5;

  if (totalPages.value <= maxVisiblePages) {
    for (let i = 1; i <= totalPages.value; i++) {
      range.push(i);
    }
  } else {
    let start = Math.max(
      1,
      currentPage.value - Math.floor(maxVisiblePages / 2)
    );
    let end = Math.min(totalPages.value, start + maxVisiblePages - 1);

    if (end - start + 1 < maxVisiblePages) {
      start = Math.max(1, end - maxVisiblePages + 1);
    }

    for (let i = start; i <= end; i++) {
      range.push(i);
    }
  }

  return range;
});

// Verificar se há um parâmetro na URL para abrir o modal
onBeforeMount(() => {
  if (route.query.new === 'true') {
    showMessageModal.value = true;
  }
});

// Escutar evento global para abrir o modal
onMounted(() => {
  // Buscar dados iniciais
  loadInitialData();
});

// Função para carregar dados iniciais
const loadInitialData = async () => {
  try {
    await Promise.all([
      loadProjects(),
      loadUsers(),
      loadMessages()
    ]);
  } catch (err) {
    console.error('Erro ao carregar dados iniciais:', err);
    error.value = 'Ocorreu um erro ao carregar os dados. Por favor, recarregue a página.';
  }
};

// Buscar mensagens usando o serviço de API
const loadMessages = async () => {
  loading.value = true;
  error.value = null;

  try {
    const params = {
      page: currentPage.value,
      ordering: '-created_at',
    };

    if (typeFilter.value) {
      params.message_type = typeFilter.value;
    }

    if (statusFilter.value) {
      params.is_read = statusFilter.value === 'LIDA';
    }

    if (projectFilter.value) {
      params.project_id = projectFilter.value;
    }

    if (searchQuery.value) {
      params.search = searchQuery.value;
    }

    // Usar o serviço de API para mensagens
    const response = await fetchMessages(params);

    messages.value = response.results.map((message) => ({
      id: message.id,
      titulo: message.title || message.content.substring(0, 30),
      conteudo: message.content,
      tipo: message.is_global ? 'MENSAGEM' : 'NOTIFICACAO',
      tipo_display: message.is_global ? 'Mensagem' : 'Notificação',
      status: message.is_read ? 'LIDA' : 'NAO_LIDA',
      status_display: message.is_read ? 'Lida' : 'Não lida',
      remetente: message.sender_id,
      remetente_nome: message.sender_name,
      destinatario: message.recipient_id,
      destinatario_nome: message.recipient_name,
      projeto: message.project_id,
      projeto_nome: message.project_name,
      data_envio: message.created_at,
      data_leitura: message.read_at,
    }));

    totalItems.value = response.count;
    totalPages.value = Math.ceil(response.count / itemsPerPage.value);
  } catch (err) {
    console.error('Erro ao buscar mensagens:', err);
    error.value =
      'Não foi possível carregar as mensagens. Por favor, tente novamente.';
  } finally {
    loading.value = false;
  }
};

// Buscar projetos usando o serviço de API
const loadProjects = async () => {
  try {
    const response = await fetchProjects();
    projects.value = response.results.map((project) => ({
      id: project.id,
      titulo: project.name || project.title,
    }));
  } catch (err) {
    console.error('Erro ao buscar projetos:', err);
  }
};

// Buscar usuários usando o serviço de API
const loadUsers = async () => {
  try {
    const response = await fetchUsers();
    users.value = response.results.map((user) => ({
      id: user.id,
      nome: user.full_name || `${user.first_name} ${user.last_name}`,
      email: user.email,
      username: user.username,
    }));
  } catch (err) {
    console.error('Erro ao buscar usuários:', err);
  }
};

// Mudar página
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
};

// Formatar data
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

// Obter label do tipo
const getTypeLabel = (type) => {
  const typeMap = {
    MENSAGEM: 'Mensagem',
    NOTIFICACAO: 'Notificação',
    ALERTA: 'Alerta',
  };
  return typeMap[type] || type;
};

// Obter nome do projeto
const getProjectName = (projectId) => {
  const project = projects.value.find((p) => p.id === projectId);
  return project ? project.titulo : 'Projeto não encontrado';
};

// Abrir modal de nova mensagem
const openNewMessageModal = () => {
  messageForm.value = {
    titulo: '',
    conteudo: '',
    tipo: 'MENSAGEM',
    destinatarios: [],
    projeto: '',
  };
  showMessageModal.value = true;
};

// Enviar mensagem usando o serviço de API
const sendMessage = async () => {
  if (
    !messageForm.value.titulo ||
    !messageForm.value.conteudo ||
    messageForm.value.destinatarios.length === 0
  ) {
    alert('Preencha os campos obrigatórios');
    return;
  }

  sending.value = true;

  try {
    // Preparar dados da mensagem usando a nova estrutura
    const isGlobal = messageForm.value.tipo === 'MENSAGEM';
    
    // Para mensagens globais, enviaremos uma para cada destinatário
    const sendPromises = messageForm.value.destinatarios.map(userId => {
      return sendNewMessage({
        content: messageForm.value.conteudo,
        title: messageForm.value.titulo,
        project_id: messageForm.value.projeto || null,
        recipient_id: userId,
        is_global: isGlobal,
        sender_id: user.value?.id
      });
    });
    
    await Promise.all(sendPromises);

    showMessageModal.value = false;
    await loadMessages();
  } catch (err) {
    console.error('Erro ao enviar mensagem:', err);
    alert('Não foi possível enviar a mensagem. Por favor, tente novamente.');
  } finally {
    sending.value = false;
  }
};

// Marcar mensagem como lida usando o serviço de API
const markAsRead = async (id) => {
  try {
    // Marcar como lida usando o serviço
    await markMessageAsRead(id);

    // Atualizar status na lista local
    const message = messages.value.find((m) => m.id === id);
    if (message) {
      message.status = 'LIDA';
      message.status_display = 'Lida';
      message.data_leitura = new Date().toISOString();
    }
  } catch (err) {
    console.error('Erro ao marcar mensagem como lida:', err);
    alert(
      'Não foi possível marcar a mensagem como lida. Por favor, tente novamente.'
    );
  }
};

// Observar mudanças nos filtros e página
watch(
  [currentPage, searchQuery, typeFilter, statusFilter, projectFilter],
  () => {
    loadMessages();
  }
);
</script>
