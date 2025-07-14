<!-- filepath: pages/communications/index.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: "auth",
});

import { ref, computed, watch, onMounted, onUnmounted, nextTick } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import { useApiErrorHandler } from "@/composables/useApiErrorHandler";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { useAuthStore } from "@/stores/auth";

// Importa endpoints de chat/mensagens
import {
  useCommunicationsMensagensList,
  useCommunicationsMensagensCreate,
  useCommunicationsMensagensUpdate,
  useCommunicationsMensagensDestroy,
} from "@/api/comunicação/comunicação";
import type {
  ChatMensagem,
  ChatMensagemRequest,
  CommunicationsMensagensListParams,
} from "@/api/schemas";
import { useProjectsProjectsList } from "@/api/projetos/projetos";
import type { ProjetoList } from "@/api/schemas";

const queryClient = useQueryClient();
const { toast } = useToast();
const { handleApiError } = useApiErrorHandler();
const authStore = useAuthStore();

// Filtros e estado
const currentPage = ref(1);
const pageSize = 30;
const searchTerm = ref("");
const selectedProjeto = ref<number | "">("");
const dataInicio = ref("");
const dataFim = ref("");

// Estado do chat
const chatInput = ref("");
const chatContainer = ref<HTMLElement | null>(null);

// Modal de edição
const showEditModal = ref(false);
const editingMessage = ref<ChatMensagem | null>(null);
const editInput = ref("");

// Query para buscar mensagens
const {
  data: paginatedMessages,
  isLoading,
  error,
  refetch,
} = useCommunicationsMensagensList(
  computed(() => ({
    page: currentPage.value,
    search: searchTerm.value || undefined,
    projeto: selectedProjeto.value || undefined,
    data_inicio: dataInicio.value || undefined,
    data_fim: dataFim.value || undefined,
    ordering: "enviado_em", // ordem cronológica
    page_size: pageSize,
  })),
  {
    query: {
      enabled: computed(() => !!selectedProjeto.value),
      placeholderData: (previousData) => previousData,
      refetchInterval: 5000, // polling 5s
    },
  }
);

const messages = computed(() => paginatedMessages.value?.data?.results || []);
const totalPages = computed(() => {
  if (!paginatedMessages.value?.data?.count) return 1;
  return Math.ceil(paginatedMessages.value.data.count / pageSize);
});

// Mutations para enviar, editar, deletar mensagem
const sendMutation = useCommunicationsMensagensCreate({
  mutation: {
    onSuccess: () => {
      chatInput.value = "";
      queryClient.invalidateQueries({
        queryKey: ["api", "communications", "mensagens"],
      });
      nextTick(() => scrollToBottom());
    },
    onError: (error) => handleApiError(error, "Erro ao enviar mensagem"),
  },
});

const updateMutation = useCommunicationsMensagensUpdate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Editado!",
        description: "Mensagem editada com sucesso.",
        type: "success",
      });
      showEditModal.value = false;
      queryClient.invalidateQueries({
        queryKey: ["api", "communications", "mensagens"],
      });
    },
    onError: (error) => handleApiError(error, "Erro ao editar mensagem"),
  },
});

const deleteMutation = useCommunicationsMensagensDestroy({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Removida!",
        description: "Mensagem removida com sucesso.",
        type: "success",
      });
      queryClient.invalidateQueries({
        queryKey: ["api", "communications", "mensagens"],
      });
    },
    onError: (error) => handleApiError(error, "Erro ao remover mensagem"),
  },
});

const isSending = computed(() => sendMutation.isPending.value);

// Funções de chat
const sendMessage = () => {
  if (isSending.value || !chatInput.value.trim() || !selectedProjeto.value)
    return;
  sendMutation.mutate({
    data: { projeto: selectedProjeto.value as number, texto: chatInput.value },
  });
};

const openEditModal = (msg: ChatMensagem) => {
  editingMessage.value = msg;
  editInput.value = msg.texto;
  showEditModal.value = true;
};

const handleEdit = () => {
  if (!editingMessage.value || updateMutation.isPending.value) return;
  updateMutation.mutate({
    id: editingMessage.value.id,
    data: { projeto: editingMessage.value.projeto, texto: editInput.value },
  });
};

const handleDelete = (id: number) => {
  if (confirm("Tem certeza que deseja remover esta mensagem?")) {
    deleteMutation.mutate({ id });
  }
};

const formatDate = (dateString: string) => {
  if (!dateString) return "";
  return format(new Date(dateString), "dd/MM/yy 'às' HH:mm", {
    locale: ptBR,
  });
};

// Scroll automático para o fim do chat
const scrollToBottom = (behavior: "smooth" | "auto" = "auto") => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTo({
        top: chatContainer.value.scrollHeight,
        behavior,
      });
    }
  });
};

watch(messages, (newMessages, oldMessages) => {
  if (newMessages.length > oldMessages.length) {
    scrollToBottom("smooth");
  } else {
    scrollToBottom("auto");
  }
});

onMounted(() => scrollToBottom());
onUnmounted(() => {});

// Filtros e helpers
const clearFilters = () => {
  searchTerm.value = "";
  // Não limpar o projeto selecionado para não interromper o chat
  // selectedProjeto.value = "";
  dataInicio.value = "";
  dataFim.value = "";
  currentPage.value = 1;
};

watch([searchTerm, dataInicio, dataFim], () => {
  currentPage.value = 1;
});

// Projetos disponíveis para chat
const {
  data: projectsData,
  isLoading: isLoadingProjects,
  error: errorProjects,
} = useProjectsProjectsList();
const projects = computed<ProjetoList[]>(
  () => projectsData.value?.data?.results || []
);
</script>

<template>
  <div class="bg-slate-50 dark:bg-slate-900 min-h-screen">
    <div class="container mx-auto p-4 sm:p-6 lg:p-8">
      <!-- Header -->
      <div
        class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-8 gap-4"
      >
        <div>
          <h1 class="text-3xl font-bold text-slate-900 dark:text-slate-100">
            Comunicações
          </h1>
          <p class="mt-1 text-slate-600 dark:text-slate-400">
            Canal de chat para projetos.
          </p>
        </div>
        <div class="flex items-center gap-2">
          <select
            v-model="selectedProjeto"
            class="w-full sm:w-72 px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
          >
            <option value="" disabled>Selecione um projeto</option>
            <option v-for="proj in projects" :key="proj.id" :value="proj.id">
              {{ proj.titulo }}
            </option>
          </select>
        </div>
      </div>

      <div v-if="isLoadingProjects" class="text-center py-20 text-slate-500">
        <Icon icon="svg-spinners:180-ring-with-bg" class="w-12 h-12 mx-auto" />
        <div class="mt-2 text-lg">Carregando projetos...</div>
      </div>
      <div v-else-if="errorProjects" class="text-center text-red-500 py-20">
        <Icon icon="lucide:alert-triangle" class="w-16 h-16 mx-auto mb-4" />
        <h3 class="text-xl font-semibold">Erro ao carregar projetos</h3>
        <p>Por favor, tente recarregar a página.</p>
      </div>
      <div
        v-else-if="!selectedProjeto"
        class="text-center py-20 text-slate-500 dark:text-slate-400 bg-white dark:bg-slate-800/50 rounded-2xl shadow-sm"
      >
        <Icon
          icon="lucide:message-square-dashed"
          class="w-20 h-20 mx-auto mb-4 opacity-50"
        />
        <h3 class="text-xl font-semibold text-slate-700 dark:text-slate-300">
          Bem-vindo!
        </h3>
        <p>Selecione um projeto acima para iniciar a conversa.</p>
      </div>
      <div v-else>
        <!-- Chat UI -->
        <div
          class="bg-white dark:bg-slate-800 rounded-2xl shadow-lg flex flex-col h-[75vh] max-h-[75vh]"
        >
          <div
            ref="chatContainer"
            class="flex-1 overflow-y-auto px-6 py-8 space-y-6 fancy-scrollbar"
          >
            <template v-if="isLoading">
              <div class="text-center text-slate-400 py-10">
                <Icon
                  icon="svg-spinners:180-ring-with-bg"
                  class="w-10 h-10 mx-auto"
                />
                <div class="mt-2">Carregando mensagens...</div>
              </div>
            </template>
            <template v-else-if="error">
              <div class="text-center text-red-500 py-10">
                <Icon icon="lucide:wifi-off" class="w-12 h-12 mx-auto mb-2" />
                <p>Erro ao carregar mensagens</p>
                <button
                  @click="refetch()"
                  class="mt-2 font-semibold text-blue-500 hover:underline"
                >
                  Tentar novamente
                </button>
              </div>
            </template>
            <template v-else-if="messages.length === 0">
              <div class="text-center text-slate-400 py-10">
                <Icon
                  icon="lucide:messages-square"
                  class="w-16 h-16 mx-auto mb-4 opacity-50"
                />
                <p class="text-lg">Nenhuma mensagem por aqui.</p>
                <p>Seja o primeiro a enviar uma!</p>
              </div>
            </template>
            <template v-else>
              <div
                v-for="msg in messages"
                :key="msg.id"
                class="flex items-start gap-4 group"
                :class="
                  msg.autor_username === authStore.user?.username
                    ? 'justify-end'
                    : 'justify-start'
                "
              >
                <div
                  class="flex items-end max-w-[80%] sm:max-w-[70%]"
                  :class="
                    msg.autor_username === authStore.user?.username
                      ? 'flex-row-reverse'
                      : 'flex-row'
                  "
                >
                  <div
                    class="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center text-white font-bold shadow-md"
                    :class="
                      msg.autor_username === authStore.user?.username
                        ? 'bg-blue-500'
                        : 'bg-slate-400 dark:bg-slate-500'
                    "
                  >
                    {{ msg.autor_nome?.charAt(0)?.toUpperCase() || "?" }}
                  </div>
                  <div class="relative mx-3">
                    <div
                      :class="[
                        'rounded-2xl px-4 py-3 shadow-md transition-all text-base',
                        msg.autor_username === authStore.user?.username
                          ? 'bg-blue-600 text-white rounded-br-lg'
                          : 'bg-slate-100 dark:bg-slate-700 text-slate-800 dark:text-slate-200 rounded-bl-lg',
                      ]"
                    >
                      <div
                        class="font-bold text-sm mb-1"
                        :class="{
                          'text-blue-200':
                            msg.autor_username === authStore.user?.username,
                          'text-slate-600 dark:text-slate-300':
                            msg.autor_username !== authStore.user?.username,
                        }"
                      >
                        {{ msg.autor_nome }}
                      </div>
                      <div class="whitespace-pre-wrap break-words">
                        {{ msg.texto }}
                      </div>
                    </div>
                    <div
                      class="text-xs text-slate-400 dark:text-slate-500 mt-1.5 px-2"
                      :class="{
                        'text-right':
                          msg.autor_username === authStore.user?.username,
                      }"
                    >
                      <span>{{ formatDate(msg.enviado_em) }}</span>
                      <span v-if="msg.editado" class="italic opacity-80">
                        (editada)</span
                      >
                    </div>
                    <div
                      v-if="msg.autor_username === authStore.user?.username"
                      class="absolute -top-4 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-0.5 p-0.5 bg-white dark:bg-slate-900 rounded-full shadow-lg border border-slate-200 dark:border-slate-700"
                    >
                      <button
                        @click="openEditModal(msg)"
                        class="p-1.5 text-slate-500 hover:text-blue-500 dark:hover:text-blue-400 rounded-full hover:bg-slate-100 dark:hover:bg-slate-700 transition"
                      >
                        <Icon icon="lucide:pencil" class="w-4 h-4" />
                      </button>
                      <button
                        @click="handleDelete(msg.id)"
                        class="p-1.5 text-slate-500 hover:text-red-500 dark:hover:text-red-400 rounded-full hover:bg-slate-100 dark:hover:bg-slate-700 transition"
                      >
                        <Icon icon="lucide:trash-2" class="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </div>
          <!-- Input de mensagem -->
          <form
            @submit.prevent="sendMessage"
            class="flex items-center gap-4 p-4 border-t border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50"
          >
            <input
              v-model="chatInput"
              :disabled="isSending"
              type="text"
              placeholder="Digite sua mensagem..."
              class="flex-1 px-5 py-3 bg-white dark:bg-slate-700 border border-transparent rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-slate-800 dark:text-slate-200"
            />
            <button
              type="submit"
              :disabled="isSending || !chatInput.trim() || !selectedProjeto"
              class="flex-shrink-0 w-12 h-12 bg-blue-600 hover:bg-blue-700 text-white rounded-full font-semibold shadow-md disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center"
            >
              <Icon
                v-if="isSending"
                icon="svg-spinners:180-ring-with-bg"
                class="w-6 h-6"
              />
              <Icon v-else icon="lucide:send-horizontal" class="w-6 h-6" />
            </button>
          </form>
        </div>

        <!-- Paginação -->
        <div
          v-if="totalPages > 1"
          class="mt-6 flex justify-center items-center gap-4"
        >
          <button
            @click="currentPage--"
            :disabled="!paginatedMessages?.data?.previous"
            class="inline-flex items-center justify-center px-4 h-10 text-sm font-medium text-slate-600 bg-white border border-slate-300 rounded-lg hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-slate-800 dark:border-slate-700 dark:text-slate-400 dark:hover:bg-slate-700 dark:hover:text-white transition"
          >
            <Icon icon="lucide:arrow-left" class="w-4 h-4 mr-2" />
            Anterior
          </button>
          <span class="text-sm text-slate-700 dark:text-slate-400">
            Página
            <span class="font-semibold text-slate-900 dark:text-white">{{
              currentPage
            }}</span>
            de
            <span class="font-semibold text-slate-900 dark:text-white">{{
              totalPages
            }}</span>
          </span>
          <button
            @click="currentPage++"
            :disabled="!paginatedMessages?.data?.next"
            class="inline-flex items-center justify-center px-4 h-10 text-sm font-medium text-slate-600 bg-white border border-slate-300 rounded-lg hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-slate-800 dark:border-slate-700 dark:text-slate-400 dark:hover:bg-slate-700 dark:hover:text-white transition"
          >
            Próximo
            <Icon icon="lucide:arrow-right" class="w-4 h-4 ml-2" />
          </button>
        </div>
      </div>

      <!-- Modal de edição -->
      <div
        v-if="showEditModal"
        @click.self="showEditModal = false"
        class="fixed inset-0 bg-slate-900 bg-opacity-60 flex items-center justify-center z-50 p-4 transition-opacity"
      >
        <div
          class="bg-white dark:bg-slate-800 rounded-xl shadow-2xl p-6 w-full max-w-md relative transform transition-all"
        >
          <button
            @click="showEditModal = false"
            class="absolute top-3 right-3 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
          >
            <Icon icon="lucide:x" class="w-6 h-6" />
          </button>
          <h3 class="text-xl font-bold mb-5 text-slate-800 dark:text-slate-100">
            Editar Mensagem
          </h3>
          <textarea
            v-model="editInput"
            rows="4"
            class="w-full px-4 py-3 bg-slate-100 dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-lg mb-6 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition text-slate-800 dark:text-slate-200"
          ></textarea>
          <div class="flex justify-end gap-3">
            <button
              @click="showEditModal = false"
              class="px-5 py-2.5 text-sm font-medium text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-700 border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-600 transition-colors"
            >
              Cancelar
            </button>
            <button
              @click="handleEdit"
              :disabled="updateMutation.isPending.value"
              class="px-5 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 transition-colors disabled:opacity-50 flex items-center justify-center min-w-[120px]"
            >
              <Icon
                v-if="updateMutation.isPending.value"
                icon="svg-spinners:ring-resize"
                class="w-5 h-5"
              />
              <span v-else>Salvar</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fancy-scrollbar::-webkit-scrollbar {
  width: 8px;
}
.fancy-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.fancy-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e1; /* slate-300 */
  border-radius: 20px;
  border: 3px solid transparent;
  background-clip: content-box;
}
.fancy-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: #94a3b8; /* slate-400 */
}
.dark .fancy-scrollbar::-webkit-scrollbar-thumb {
  background-color: #475569; /* slate-600 */
}
.dark .fancy-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: #64748b; /* slate-500 */
}
.whitespace-pre-wrap {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
