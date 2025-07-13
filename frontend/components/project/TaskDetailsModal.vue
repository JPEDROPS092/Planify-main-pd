<!-- filepath: components/project/TaskDetailsModal.vue -->
<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
  >
    <div
      class="relative top-5 mx-auto p-5 border w-full max-w-4xl shadow-lg rounded-md bg-white"
    >
      <div v-if="task" class="mt-3">
        <!-- Header -->
        <div class="flex justify-between items-start mb-6">
          <div class="flex-1">
            <div class="flex items-center space-x-3 mb-2">
              <h3 class="text-xl font-semibold text-gray-900">
                {{ task.titulo }}
              </h3>
              <span
                class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                :class="getPriorityClasses(task.prioridade)"
              >
                {{ getPriorityLabel(task.prioridade) }}
              </span>
              <span
                class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                :class="getStatusClasses(task.status)"
              >
                {{ getStatusLabel(task.status) }}
              </span>
            </div>
            <div class="flex items-center space-x-4 text-sm text-gray-500">
              <span>Criada em {{ formatDate(task.criado_em) }}</span>
              <span v-if="task.data_fim">
                • Prazo: {{ formatDate(task.data_fim) }}
                <Icon
                  v-if="isOverdue(task.data_fim)"
                  icon="lucide:clock"
                  class="h-4 w-4 text-red-500 ml-1 inline"
                />
              </span>
            </div>
          </div>

          <div class="flex items-center space-x-2">
            <button
              v-if="isAdmin"
              @click="editTask"
              class="text-gray-400 hover:text-gray-600 p-2"
            >
              <Icon icon="lucide:edit" class="h-5 w-5" />
            </button>
            <button
              @click="$emit('close')"
              class="text-gray-400 hover:text-gray-600 p-2"
            >
              <Icon icon="lucide:x" class="h-6 w-6" />
            </button>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-6">
          <!-- Coluna Principal -->
          <div class="col-span-2 space-y-6">
            <!-- Descrição -->
            <div v-if="task.descricao">
              <h4 class="text-sm font-medium text-gray-900 mb-2">Descrição</h4>
              <p class="text-gray-700 whitespace-pre-wrap">
                {{ task.descricao }}
              </p>
            </div>

            <!-- Progresso -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <h4 class="text-sm font-medium text-gray-900">Progresso</h4>
                <span class="text-sm text-gray-500"
                  >{{ task.progresso || 0 }}%</span
                >
              </div>
              <div class="w-full bg-gray-200 rounded-full h-3">
                <div
                  class="bg-blue-600 h-3 rounded-full transition-all duration-300"
                  :style="{ width: `${task.progresso || 0}%` }"
                ></div>
              </div>

              <!-- Controle de progresso para desenvolvedores -->
              <div
                v-if="!isAdmin && task.assignee === currentUser"
                class="mt-3"
              >
                <input
                  v-model.number="localProgress"
                  type="range"
                  min="0"
                  max="100"
                  step="5"
                  @change="updateProgress"
                  class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div class="flex justify-between text-xs text-gray-500 mt-1">
                  <span>0%</span>
                  <span>50%</span>
                  <span>100%</span>
                </div>
              </div>
            </div>

            <!-- Critérios de Aceite -->
            <div v-if="task.criterios_aceite?.length">
              <h4 class="text-sm font-medium text-gray-900 mb-3">
                Critérios de Aceite
              </h4>
              <div class="space-y-2">
                <div
                  v-for="(criterio, index) in task.criterios_aceite"
                  :key="index"
                  class="flex items-center space-x-2"
                >
                  <input
                    type="checkbox"
                    :checked="criterio.completed"
                    @change="toggleCriterio(index)"
                    :disabled="!canEdit"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span
                    :class="
                      criterio.completed
                        ? 'line-through text-gray-500'
                        : 'text-gray-700'
                    "
                  >
                    {{ criterio.text }}
                  </span>
                </div>
              </div>
              <div class="mt-2 text-xs text-gray-500">
                {{ completedCriteria }}/{{
                  task.criterios_aceite.length
                }}
                critérios concluídos
              </div>
            </div>

            <!-- Histórico de Atividades -->
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-3">
                Histórico de Atividades
              </h4>
              <div class="space-y-3 max-h-60 overflow-y-auto">
                <div
                  v-for="activity in taskHistory"
                  :key="activity.id"
                  class="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg"
                >
                  <div
                    class="w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-medium"
                    :class="getActivityIconClass(activity.type)"
                  >
                    <Icon
                      :icon="getActivityIcon(activity.type)"
                      class="h-4 w-4"
                    />
                  </div>
                  <div class="flex-1">
                    <p class="text-sm text-gray-900">
                      {{ activity.description }}
                    </p>
                    <p class="text-xs text-gray-500">
                      {{ activity.user }} •
                      {{ formatDateTime(activity.created_at) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Comentários -->
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-3">
                Comentários
              </h4>

              <!-- Lista de comentários -->
              <div class="space-y-3 mb-4 max-h-40 overflow-y-auto">
                <div
                  v-for="comment in taskComments"
                  :key="comment.id"
                  class="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg"
                >
                  <div
                    class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs font-medium"
                  >
                    {{ comment.user.charAt(0).toUpperCase() }}
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center space-x-2 mb-1">
                      <span class="text-sm font-medium text-gray-900">{{
                        comment.user
                      }}</span>
                      <span class="text-xs text-gray-500">{{
                        formatDateTime(comment.created_at)
                      }}</span>
                    </div>
                    <p class="text-sm text-gray-700">{{ comment.content }}</p>
                  </div>
                </div>
              </div>

              <!-- Adicionar comentário -->
              <div class="flex space-x-3">
                <div
                  class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center text-white text-xs font-medium"
                >
                  {{ currentUser.charAt(0).toUpperCase() }}
                </div>
                <div class="flex-1">
                  <textarea
                    v-model="newComment"
                    rows="2"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Adicionar um comentário..."
                  ></textarea>
                  <div class="flex justify-end mt-2">
                    <button
                      @click="addComment"
                      :disabled="!newComment.trim()"
                      class="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Comentar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- Informações Rápidas -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-sm font-medium text-gray-900 mb-3">
                Informações
              </h4>
              <div class="space-y-3">
                <div>
                  <span class="text-xs text-gray-500 block"
                    >Atribuída para</span
                  >
                  <div class="flex items-center space-x-2 mt-1">
                    <div
                      class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs font-medium"
                    >
                      {{
                        task.assignee
                          ? task.assignee.charAt(0).toUpperCase()
                          : "?"
                      }}
                    </div>
                    <span class="text-sm text-gray-900">{{
                      task.assignee || "Não atribuída"
                    }}</span>
                  </div>
                </div>

                <div v-if="task.estimativa_horas">
                  <span class="text-xs text-gray-500 block">Estimativa</span>
                  <span class="text-sm text-gray-900"
                    >{{ task.estimativa_horas }}h</span
                  >
                </div>

                <div v-if="task.data_inicio">
                  <span class="text-xs text-gray-500 block"
                    >Data de Início</span
                  >
                  <span class="text-sm text-gray-900">{{
                    formatDate(task.data_inicio)
                  }}</span>
                </div>

                <div v-if="task.data_fim">
                  <span class="text-xs text-gray-500 block"
                    >Data de Entrega</span
                  >
                  <span
                    class="text-sm"
                    :class="
                      isOverdue(task.data_fim)
                        ? 'text-red-600'
                        : 'text-gray-900'
                    "
                  >
                    {{ formatDate(task.data_fim) }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Etiquetas -->
            <div v-if="task.etiquetas?.length">
              <h4 class="text-sm font-medium text-gray-900 mb-2">Etiquetas</h4>
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="tag in task.etiquetas"
                  :key="tag"
                  class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {{ tag }}
                </span>
              </div>
            </div>

            <!-- Mudança de Status (para desenvolvedores) -->
            <div v-if="!isAdmin && task.assignee === currentUser">
              <h4 class="text-sm font-medium text-gray-900 mb-2">
                Alterar Status
              </h4>
              <select
                v-model="localStatus"
                @change="updateStatus"
                class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="ABERTA">Aberta</option>
                <option value="EM_ANDAMENTO">Em Andamento</option>
                <option value="EM_REVISAO">Em Revisão</option>
                <option value="CONCLUIDA">Concluída</option>
              </select>
            </div>

            <!-- Métricas -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-sm font-medium text-gray-900 mb-3">Métricas</h4>
              <div class="space-y-2 text-xs">
                <div class="flex justify-between">
                  <span class="text-gray-500">Tempo no status atual:</span>
                  <span class="text-gray-900">{{
                    getTimeInCurrentStatus()
                  }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">Comentários:</span>
                  <span class="text-gray-900">{{ taskComments.length }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">Atividades:</span>
                  <span class="text-gray-900">{{ taskHistory.length }}</span>
                </div>
              </div>
            </div>

            <!-- Ações -->
            <div v-if="isAdmin" class="space-y-2">
              <button
                @click="editTask"
                class="w-full px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                <Icon icon="lucide:edit" class="h-4 w-4 mr-2 inline" />
                Editar Tarefa
              </button>
              <button
                @click="deleteTask"
                class="w-full px-3 py-2 text-sm font-medium text-red-700 bg-white border border-red-300 rounded-md hover:bg-red-50"
              >
                <Icon icon="lucide:trash" class="h-4 w-4 mr-2 inline" />
                Excluir Tarefa
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";

const props = defineProps<{
  show: boolean;
  task?: any;
  projectId: number;
  isAdmin: boolean;
}>();

const emit = defineEmits(["close", "update"]);

const { toast } = useToast();

// Estados locais
const localProgress = ref(0);
const localStatus = ref("");
const newComment = ref("");

// Dados mock
const currentUser = ref("João Silva");
const taskComments = ref([
  {
    id: 1,
    user: "Maria Santos",
    content: "Ótimo progresso! Vamos revisar quando estiver pronto.",
    created_at: "2025-07-08T10:30:00Z",
  },
  {
    id: 2,
    user: "João Silva",
    content:
      "Implementei a funcionalidade principal, agora vou trabalhar nos testes.",
    created_at: "2025-07-08T14:15:00Z",
  },
]);

const taskHistory = ref([
  {
    id: 1,
    type: "created",
    description: "Tarefa criada",
    user: "Admin",
    created_at: "2025-07-01T09:00:00Z",
  },
  {
    id: 2,
    type: "assigned",
    description: "Tarefa atribuída para João Silva",
    user: "Admin",
    created_at: "2025-07-01T09:05:00Z",
  },
  {
    id: 3,
    type: "status_change",
    description: "Status alterado para Em Andamento",
    user: "João Silva",
    created_at: "2025-07-02T08:30:00Z",
  },
  {
    id: 4,
    type: "progress",
    description: "Progresso atualizado para 75%",
    user: "João Silva",
    created_at: "2025-07-07T16:20:00Z",
  },
]);

// Computed
const canEdit = computed(() => {
  return props.isAdmin || props.task?.assignee === currentUser.value;
});

const completedCriteria = computed(() => {
  return props.task?.criterios_aceite?.filter((c) => c.completed).length || 0;
});

// Watchers
watch(
  () => props.task,
  (newTask) => {
    if (newTask) {
      localProgress.value = newTask.progresso || 0;
      localStatus.value = newTask.status || "";
    }
  },
  { immediate: true }
);

// Funções utilitárias
const getPriorityClasses = (priority) => {
  switch (priority) {
    case "ALTA":
      return "bg-red-100 text-red-800";
    case "MEDIA":
      return "bg-yellow-100 text-yellow-800";
    case "BAIXA":
      return "bg-green-100 text-green-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

const getPriorityLabel = (priority) => {
  switch (priority) {
    case "ALTA":
      return "Alta";
    case "MEDIA":
      return "Média";
    case "BAIXA":
      return "Baixa";
    default:
      return "Normal";
  }
};

const getStatusClasses = (status) => {
  switch (status) {
    case "ABERTA":
      return "bg-gray-100 text-gray-800";
    case "EM_ANDAMENTO":
      return "bg-blue-100 text-blue-800";
    case "EM_REVISAO":
      return "bg-yellow-100 text-yellow-800";
    case "CONCLUIDA":
      return "bg-green-100 text-green-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

const getStatusLabel = (status) => {
  switch (status) {
    case "ABERTA":
      return "Aberta";
    case "EM_ANDAMENTO":
      return "Em Andamento";
    case "EM_REVISAO":
      return "Em Revisão";
    case "CONCLUIDA":
      return "Concluída";
    default:
      return "Desconhecido";
  }
};

const getActivityIcon = (type) => {
  switch (type) {
    case "created":
      return "lucide:plus";
    case "assigned":
      return "lucide:user";
    case "status_change":
      return "lucide:arrow-right";
    case "progress":
      return "lucide:trending-up";
    case "comment":
      return "lucide:message-circle";
    default:
      return "lucide:activity";
  }
};

const getActivityIconClass = (type) => {
  switch (type) {
    case "created":
      return "bg-green-500";
    case "assigned":
      return "bg-blue-500";
    case "status_change":
      return "bg-yellow-500";
    case "progress":
      return "bg-purple-500";
    case "comment":
      return "bg-gray-500";
    default:
      return "bg-gray-400";
  }
};

const isOverdue = (deadline) => {
  return new Date(deadline) < new Date();
};

const formatDate = (date) => {
  return new Date(date).toLocaleDateString("pt-BR");
};

const formatDateTime = (date) => {
  return new Date(date).toLocaleString("pt-BR");
};

const getTimeInCurrentStatus = () => {
  // Simular cálculo de tempo no status atual
  return "2 dias";
};

// Ações
const updateProgress = () => {
  const updatedTask = { ...props.task, progresso: localProgress.value };
  emit("update", updatedTask);

  // Adicionar ao histórico
  taskHistory.value.push({
    id: Date.now(),
    type: "progress",
    description: `Progresso atualizado para ${localProgress.value}%`,
    user: currentUser.value,
    created_at: new Date().toISOString(),
  });

  toast({
    title: "Sucesso!",
    description: "Progresso atualizado.",
    type: "success",
  });
};

const updateStatus = () => {
  const updatedTask = { ...props.task, status: localStatus.value };
  emit("update", updatedTask);

  // Adicionar ao histórico
  taskHistory.value.push({
    id: Date.now(),
    type: "status_change",
    description: `Status alterado para ${getStatusLabel(localStatus.value)}`,
    user: currentUser.value,
    created_at: new Date().toISOString(),
  });

  toast({
    title: "Sucesso!",
    description: "Status atualizado.",
    type: "success",
  });
};

const toggleCriterio = (index) => {
  if (!canEdit.value) return;

  const updatedTask = { ...props.task };
  updatedTask.criterios_aceite[index].completed =
    !updatedTask.criterios_aceite[index].completed;
  emit("update", updatedTask);
};

const addComment = () => {
  if (!newComment.value.trim()) return;

  taskComments.value.push({
    id: Date.now(),
    user: currentUser.value,
    content: newComment.value,
    created_at: new Date().toISOString(),
  });

  // Adicionar ao histórico
  taskHistory.value.push({
    id: Date.now(),
    type: "comment",
    description: "Novo comentário adicionado",
    user: currentUser.value,
    created_at: new Date().toISOString(),
  });

  newComment.value = "";

  toast({
    title: "Sucesso!",
    description: "Comentário adicionado.",
    type: "success",
  });
};

const editTask = () => {
  // Emitir evento para abrir modal de edição
  // Esta funcionalidade seria implementada no componente pai
  console.log("Edit task:", props.task);
};

const deleteTask = () => {
  if (confirm("Tem certeza que deseja excluir esta tarefa?")) {
    // Implementar exclusão
    console.log("Delete task:", props.task);
    emit("close");
  }
};
</script>

<style scoped>
.line-through {
  text-decoration: line-through;
}
</style>
