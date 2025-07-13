<!-- components/TaskModal.vue -->
<template>
  <div
    class="fixed inset-0 bg-black/60 z-40 flex items-center justify-center"
    @click.self="close"
  >
    <div
      class="bg-white dark:bg-gray-800 rounded-lg shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col"
    >
      <div
        class="p-4 border-b dark:border-gray-700 flex justify-between items-center"
      >
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
          {{ isNewTask ? "Criar Nova Tarefa" : "Editar Tarefa" }}
        </h2>
        <button
          @click="close"
          class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        >
          <Icon icon="lucide:x" class="w-6 h-6" />
        </button>
      </div>

      <form @submit.prevent="saveTask" class="p-6 space-y-4 overflow-y-auto">
        <!-- Título -->
        <div>
          <label
            for="titulo"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >Título *</label
          >
          <input
            type="text"
            v-model="form.titulo"
            id="titulo"
            required
            class="form-input"
          />
        </div>

        <!-- Descrição -->
        <div>
          <label
            for="descricao"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >Descrição</label
          >
          <textarea
            v-model="form.descricao"
            id="descricao"
            rows="4"
            class="form-input"
          ></textarea>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Status -->
          <div>
            <label
              for="status"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300"
              >Status</label
            >
            <select v-model="form.status" id="status" class="form-input">
              <option
                v-for="status in statusOptions"
                :key="status.value"
                :value="status.value"
              >
                {{ status.label }}
              </option>
            </select>
          </div>

          <!-- Prioridade -->
          <div>
            <label
              for="prioridade"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300"
              >Prioridade</label
            >
            <select
              v-model="form.prioridade"
              id="prioridade"
              class="form-input"
            >
              <option
                v-for="prio in priorityOptions"
                :key="prio.value"
                :value="prio.value"
              >
                {{ prio.label }}
              </option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Data de Início -->
          <div>
            <label
              for="data_inicio"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300"
              >Data de Início</label
            >
            <input
              type="date"
              v-model="form.data_inicio"
              id="data_inicio"
              class="form-input"
            />
          </div>

          <!-- Data de Término -->
          <div>
            <label
              for="data_termino"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300"
              >Data de Término</label
            >
            <input
              type="date"
              v-model="form.data_termino"
              id="data_termino"
              class="form-input"
            />
          </div>
        </div>
      </form>

      <!-- Footer com Ações -->
      <div
        class="p-4 border-t dark:border-gray-700 flex justify-between items-center bg-gray-50 dark:bg-gray-800/50 rounded-b-lg"
      >
        <div>
          <button
            v-if="!isNewTask"
            @click="deleteTask"
            type="button"
            class="px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-100 dark:hover:bg-red-900/50 rounded-md transition-colors"
          >
            Excluir Tarefa
          </button>
        </div>
        <div class="space-x-3">
          <button
            @click="close"
            type="button"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="saveTask"
            type="submit"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors"
          >
            {{ isNewTask ? "Criar Tarefa" : "Salvar Alterações" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { Icon } from "@iconify/vue";
import {
  useTasksTarefasCreate,
  useTasksTarefasUpdate,
  useTasksTarefasDestroy,
} from "../../api/tasks/tasks";
import type {
  TarefaRequest,
  TarefaList,
  NovoStatusBbcEnum,
  PrioridadeEnum,
} from "../../api/schemas";
import { useToast } from "../../composables/useToast";

// --- PROPS E EMITS ---
const props = defineProps<{
  taskData: TarefaList | null;
  projectId: number;
}>();

const emit = defineEmits(["close", "task-saved", "task-deleted"]);

// --- TOAST ---
const { toast } = useToast();

// --- API MUTATIONS ---
const createTaskMutation = useTasksTarefasCreate();
const updateTaskMutation = useTasksTarefasUpdate();
const deleteTaskMutation = useTasksTarefasDestroy();

// --- ESTADO DO FORMULÁRIO ---
const form = ref<any>({});
const isNewTask = computed(() => !props.taskData?.id);

// --- OPÇÕES DOS SELECTS ---
const statusOptions = ref([
  { value: "A_FAZER", label: "A Fazer" },
  { value: "EM_ANDAMENTO", label: "Em Andamento" },
  { value: "FEITO", label: "Feito" },
]);

const priorityOptions = ref([
  { value: "BAIXA", label: "Baixa" },
  { value: "MEDIA", label: "Média" },
  { value: "ALTA", label: "Alta" },
]);

// --- MÉTODOS ---
const close = () => emit("close");

const saveTask = async () => {
  if (!form.value.titulo) {
    toast({
      title: "Erro de validação",
      description: "O título é obrigatório.",
      type: "error",
    });
    return;
  }

  const payload: TarefaRequest = {
    titulo: form.value.titulo,
    descricao: form.value.descricao || "",
    projeto: props.projectId,
    sprint: form.value.sprint || null,
    data_inicio:
      form.value.data_inicio || new Date().toISOString().split("T")[0],
    data_termino: form.value.data_termino || "",
    prioridade: form.value.prioridade || "BAIXA",
    status: form.value.status || "A_FAZER",
  };

  try {
    let savedTask;
    if (isNewTask.value) {
      const result = await createTaskMutation.mutateAsync({ data: payload });
      savedTask = result.data;
      toast({
        title: "Tarefa criada",
        description: "A tarefa foi criada com sucesso.",
        type: "success",
      });
    } else {
      const result = await updateTaskMutation.mutateAsync({
        id: props.taskData!.id,
        data: payload,
      });
      savedTask = result.data;
      toast({
        title: "Tarefa atualizada",
        description: "A tarefa foi atualizada com sucesso.",
        type: "success",
      });
    }
    emit("task-saved", savedTask);
  } catch (error) {
    console.error("Erro ao salvar tarefa:", error);
    toast({
      title: "Erro ao salvar",
      description: "Não foi possível salvar a tarefa.",
      type: "error",
    });
  }
};

const deleteTask = async () => {
  if (isNewTask.value) return;
  if (confirm("Tem certeza que deseja excluir esta tarefa?")) {
    try {
      await deleteTaskMutation.mutateAsync({ id: props.taskData!.id });
      toast({
        title: "Tarefa excluída",
        description: "A tarefa foi excluída com sucesso.",
        type: "success",
      });
      emit("task-deleted", props.taskData!.id);
    } catch (error) {
      console.error("Erro ao excluir tarefa:", error);
      toast({
        title: "Erro ao excluir",
        description: "Não foi possível excluir a tarefa.",
        type: "error",
      });
    }
  }
};

onMounted(() => {
  // Inicializa o formulário com os dados da tarefa passada
  if (props.taskData) {
    form.value = { ...props.taskData };
    // Para tarefas existentes, adicionar campos padrão se não existirem
    if (!form.value.data_inicio) {
      form.value.data_inicio = new Date().toISOString().split("T")[0];
    }
    // Formata a data de término para o input type="date"
    if (props.taskData.data_termino) {
      form.value.data_termino = new Date(props.taskData.data_termino)
        .toISOString()
        .split("T")[0];
    }
    // Se não tiver descrição, inicializar como string vazia
    if (!form.value.descricao) {
      form.value.descricao = "";
    }
  }
});
</script>

<style scoped>
.form-input {
  margin-top: 0.25rem;
  display: block;
  width: 100%;
  border-radius: 0.375rem;
  border-color: rgb(209 213 219);
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.form-input:focus {
  border-color: rgb(59 130 246);
  box-shadow: 0 0 0 1px rgb(59 130 246);
  outline: none;
}

.dark .form-input {
  background-color: rgb(55 65 81);
  border-color: rgb(75 85 99);
  color: white;
}

.dark .form-input:focus {
  border-color: rgb(59 130 246);
  box-shadow: 0 0 0 1px rgb(59 130 246);
}
</style>
