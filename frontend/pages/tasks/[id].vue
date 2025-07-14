<!-- filepath: pages/tasks/[id].vue -->
<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useRouter, useRoute } from "vue-router";
import { useToast } from "@/composables/useToast";
import type {
  NovoStatusBbcEnum,
  TasksAddCommentRequest,
  TasksUpdateStatusRequest,
  TasksAssignUserRequest,
} from "@/api/schemas";
import { useApiErrorHandler } from "@/composables/useApiErrorHandler";
import { useAuthStore } from "@/stores/auth";
import { format } from "date-fns";

import AssociatedDocuments from "@/components/documents/AssociatedDocuments.vue";

import {
  useTasksTarefasRetrieve,
  useTasksTarefasAddCommentCreate,
  useTasksTarefasUpdateStatusCreate,
  useTasksTarefasUnassignUserCreate,
} from "@/api/tasks/tasks";
import { useProjectsProjectsRetrieve } from "@/api/projetos/projetos";

// Habilita middleware de autenticação seguindo o padrão do index.vue
// definePageMeta({
//   middleware: "auth",
// });

// Estado do componente
const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const taskId = computed(() => Number(route.params.id));

const queryClient = useQueryClient();
const { toast } = useToast();
const { handleApiError } = useApiErrorHandler();

const newComment = ref("");

// Query para buscar os detalhes da tarefa
const {
  data: taskResponse,
  isLoading,
  error,
} = useTasksTarefasRetrieve(taskId, {
  query: {
    enabled: computed(() => !!taskId.value),
    retry: (failureCount, error: any) => {
      // Não tenta novamente para erros 403/404
      if (error?.response?.status === 403 || error?.response?.status === 404) {
        return false;
      }
      return failureCount < 3;
    },
  },
});

// Query para buscar os membros do projeto da tarefa
const projectId = computed(() => taskResponse.value?.data?.projeto ?? null);
const {
  data: projectResponse,
  isLoading: isLoadingProject,
  error: errorProject,
} = useProjectsProjectsRetrieve(projectId, {
  query: { enabled: computed(() => !!projectId.value) },
});
const project = computed(() => projectResponse.value?.data);

// Tratamento de erros seguindo o padrão do index.vue
watch(error, (newError: any) => {
  if (newError) {
    console.error("Erro ao buscar tarefa:", newError);

    if (newError?.response?.status === 403) {
      toast({
        title: "Acesso Negado",
        description:
          "Você não tem permissão para acessar esta tarefa. Redirecionando para a lista de tarefas.",
        type: "error",
      });
      router.push("/tasks");
    } else if (newError?.response?.status === 404) {
      toast({
        title: "Tarefa Não Encontrada",
        description:
          "A tarefa solicitada não foi encontrada. Redirecionando para a lista de tarefas.",
        type: "error",
      });
      router.push("/tasks");
    } else if (newError?.response?.status === 401) {
      toast({
        title: "Não Autorizado",
        description: "Sua sessão expirou. Faça login novamente.",
        type: "error",
      });
      authStore.logout();
      router.push("/login");
    } else {
      handleApiError(newError);
    }
  }
});

const task = computed(() => taskResponse.value?.data);

// Verificação adicional de permissão baseada no usuário logado
const canAccessTask = computed(() => {
  if (!task.value || !authStore.user) return false;

  // Verifica se o usuário é o responsável pela tarefa ou tem permissão de admin
  const isAssigned = task.value.atribuicoes?.some(
    (atribuicao: any) => atribuicao.usuario.id === authStore.user?.id
  );
  const isCreator = task.value.criado_por?.id === authStore.user?.id;
  const isAdmin = authStore.user?.is_staff || authStore.user?.is_superuser;
  // Novo: verifica se é membro do projeto
  const isProjectMember = project.value?.membros?.some(
    (m: any) => m.usuario_id === authStore.user?.id
  );
  return isAssigned || isCreator || isAdmin || isProjectMember;
});

// Watch para verificar permissões quando a tarefa é carregada
watch(
  [task, () => authStore.user],
  ([newTask, newUser]) => {
    if (newTask && newUser && !canAccessTask.value) {
      toast({
        title: "Acesso Restrito",
        description: "Você não tem permissão para visualizar esta tarefa.",
        type: "warning",
      });
      router.push("/tasks");
    }
  },
  { immediate: true }
);

// --- MUTAÇÕES ---

// 3. Enhanced mutação para adicionar comentário
const addCommentMutation = useTasksTarefasAddCommentCreate({
  mutation: {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["task", taskId.value] });
      newComment.value = "";
      toast({ title: "Comentário adicionado!", type: "success" });
    },
    onError: (err: any) => {
      console.error("Add Comment Error Details:", {
        status: err.response?.status,
        statusText: err.response?.statusText,
        data: err.response?.data,
        headers: err.response?.headers,
      });

      handleApiError(err, "Não foi possível adicionar o comentário.");
    },
  },
});

// 4. Enhanced mutação para atualizar o status
const updateStatusMutation = useTasksTarefasUpdateStatusCreate({
  mutation: {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["task", taskId.value] });
      toast({ title: "Status Atualizado", type: "success" });
    },
    onError: (err: any) => {
      console.error("Update Status Error Details:", {
        status: err.response?.status,
        statusText: err.response?.statusText,
        data: err.response?.data,
        headers: err.response?.headers,
        config: err.config,
      });

      handleApiError(err, "Não foi possível atualizar o status.");
    },
  },
});

// 5. Enhanced mutação para remover responsável
const removeAssignmentMutation = useTasksTarefasUnassignUserCreate({
  mutation: {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["task", taskId.value] });
      toast({ title: "Responsável Removido", type: "success" });
    },
    onError: (err: any) => {
      console.error("Remove Assignment Error Details:", {
        status: err.response?.status,
        statusText: err.response?.statusText,
        data: err.response?.data,
        headers: err.response?.headers,
      });

      handleApiError(err, "Não foi possível remover o responsável.");
    },
  },
});

// --- HANDLERS ---
const handleAddComment = () => {
  if (!newComment.value.trim()) return;

  console.log(`Attempting to add comment to task ${taskId.value}`);

  const payload: TasksAddCommentRequest = { texto: newComment.value };
  addCommentMutation.mutate({ id: taskId.value, data: payload });
};

const handleUpdateStatus = (newStatus: NovoStatusBbcEnum) => {
  console.log(
    `Attempting to update status of task ${taskId.value} to ${newStatus}`
  );

  const payload: TasksUpdateStatusRequest = { status: newStatus };
  updateStatusMutation.mutate({ id: taskId.value, data: payload });
};

const handleRemoveAssignment = (userId: number) => {
  if (
    window.confirm("Tem certeza que deseja remover o responsável desta tarefa?")
  ) {
    const payload: TasksAssignUserRequest = { usuario_id: userId };
    removeAssignmentMutation.mutate({ id: taskId.value, data: payload });
  }
};

// --- HELPERS ---
const formatDate = (date: string) =>
  date ? format(new Date(`${date}T12:00:00`), "dd/MM/yyyy") : "Não definida";

const statusDisplayMap = {
  A_FAZER: { label: "A Fazer", class: "bg-yellow-100 text-yellow-800" },
  EM_ANDAMENTO: { label: "Em Andamento", class: "bg-blue-100 text-blue-800" },
  FEITO: { label: "Feito", class: "bg-green-100 text-green-800" },
} as const;

const priorityDisplayMap = {
  ALTA: { label: "Alta", class: "text-red-600" },
  MEDIA: { label: "Média", class: "text-orange-500" },
  BAIXA: { label: "Baixa", class: "text-green-600" },
} as const;
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div v-if="isLoading" class="text-center py-20">
      <Icon
        icon="svg-spinners:180-ring-with-bg"
        class="w-16 h-16 mx-auto text-primary-600"
      />
      <p class="mt-4 text-gray-600 dark:text-gray-400">Carregando tarefa...</p>
    </div>
    <div v-else-if="error" class="text-center py-20">
      <Icon
        icon="lucide:alert-circle"
        class="w-16 h-16 mx-auto text-red-500 mb-4"
      />
      <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
        Erro ao carregar a tarefa
      </h2>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        Você pode não ter permissão para acessar esta tarefa ou ela pode não
        existir.
      </p>
      <button
        @click="router.push('/tasks')"
        class="bg-primary-600 hover:bg-primary-700 text-white px-6 py-2 rounded-lg transition-colors"
      >
        Voltar para Tarefas
      </button>
    </div>
    <div
      v-else-if="task"
      class="bg-white dark:bg-gray-800 rounded-lg shadow-sm"
    >
      <div class="border-b dark:border-gray-700 p-4 sm:p-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button
              @click="router.back()"
              class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
            >
              <Icon icon="lucide:arrow-left" class="w-6 h-6" />
            </button>
            <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">
              {{ task?.titulo }}
            </h1>
          </div>
        </div>
      </div>

      <div class="p-4 sm:p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="md:col-span-2 space-y-6">
          <div>
            <h2
              class="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-200"
            >
              Descrição
            </h2>
            <p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
              {{ task?.descricao || "Sem descrição detalhada." }}
            </p>
          </div>

          <div>
            <h2
              class="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-200"
            >
              Adicionar Comentário
            </h2>
            <form @submit.prevent="handleAddComment">
              <textarea
                v-model="newComment"
                rows="3"
                placeholder="Escreva seu comentário..."
                class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-primary-500 focus:outline-none bg-white dark:bg-gray-700"
              ></textarea>
              <button
                type="submit"
                :disabled="
                  !newComment.trim() || addCommentMutation.isPending.value
                "
                class="mt-2 px-4 py-2 bg-gray-800 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 dark:border dark:border-white"
              >
                Enviar
              </button>
            </form>
          </div>

          <AssociatedDocuments 
            :tarefa-id="taskId"
          />
        </div>

        <div class="space-y-6">
          <div class="border dark:border-gray-700 rounded-lg p-4">
            <h2
              class="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-200"
            >
              Detalhes
            </h2>
            <dl class="space-y-4">
              <div>
                <dt
                  class="text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Status
                </dt>
                <dd class="mt-1">
                  <span
                    class="px-2 py-1 rounded-full text-xs font-medium"
                    :class="
                      task?.status ? statusDisplayMap[task.status]?.class : ''
                    "
                    >{{
                      task?.status
                        ? statusDisplayMap[task.status]?.label
                        : "N/A"
                    }}</span
                  >
                </dd>
              </div>
              <div>
                <dt
                  class="text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Prioridade
                </dt>
                <dd class="mt-1">
                  <span
                    class="font-medium"
                    :class="
                      task?.prioridade
                        ? priorityDisplayMap[task.prioridade]?.class
                        : ''
                    "
                    >{{
                      task?.prioridade
                        ? priorityDisplayMap[task.prioridade]?.label
                        : "N/A"
                    }}</span
                  >
                </dd>
              </div>
              <div>
                <dt
                  class="text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Projeto ID
                </dt>
                <dd class="mt-1 font-medium text-gray-900 dark:text-gray-100">
                  {{ task?.projeto }}
                </dd>
              </div>
              <div>
                <dt
                  class="text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Responsáveis
                </dt>
                <dd
                  v-if="task?.atribuicoes?.length"
                  class="mt-1 font-medium text-gray-900 dark:text-gray-100"
                >
                  <span
                    v-for="(atribuicao, i) in task.atribuicoes"
                    :key="atribuicao.id"
                    >{{ atribuicao.usuario.full_name
                    }}{{ i < task.atribuicoes.length - 1 ? ", " : "" }}</span
                  >
                </dd>
                <dd
                  v-else
                  class="mt-1 text-sm text-gray-500 dark:text-gray-400"
                >
                  Não atribuído
                </dd>
              </div>
              <div>
                <dt
                  class="text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Prazo
                </dt>
                <dd class="mt-1 font-medium text-gray-900 dark:text-gray-100">
                  {{ formatDate(task?.data_termino || "") }}
                </dd>
              </div>
            </dl>
            <div class="mt-6 border-t dark:border-gray-700 pt-4 space-y-2">
              <button
                @click="handleUpdateStatus('FEITO')"
                class="w-full flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
                :disabled="task?.status === 'FEITO'"
              >
                Marcar como Concluída
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Debug Panel for development -->
  <DebugAuthPanel :task-id="taskId" />
</template>
