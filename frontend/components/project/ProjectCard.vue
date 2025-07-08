<template>
  <div
    class="bg-white overflow-hidden shadow-sm rounded-xl hover:shadow-lg transition-all duration-300 border border-gray-100 hover:border-gray-200 group cursor-pointer min-h-[380px] flex flex-col"
  >
    <!-- Header do Card -->
    <div class="p-6 pb-4">
      <div class="flex items-start justify-between gap-4">
        <!-- Título e Status -->
        <div class="flex-1 min-w-0">
          <div class="flex items-start gap-3 mb-3">
            <div class="flex-shrink-0 mt-1">
              <div
                :class="[
                  'w-10 h-10 rounded-lg flex items-center justify-center',
                  getStatusIconBg(project.status),
                ]"
              >
                <Icon
                  :icon="getProjectIcon(project.status)"
                  class="h-5 w-5 text-white"
                />
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <h3
                class="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors leading-tight mb-2"
                :title="project.titulo"
              >
                {{ project.titulo }}
              </h3>
              <div class="flex items-center gap-2 flex-wrap">
                <Badge :variant="getStatusVariant(project.status)" size="sm">
                  {{ getStatusLabel(project.status) }}
                </Badge>
                <Badge
                  :variant="getPriorityVariant(project.prioridade)"
                  size="sm"
                >
                  {{ getPriorityLabel(project.prioridade) }}
                </Badge>
              </div>
            </div>
          </div>
        </div>

        <!-- Menu de Ações -->
        <div class="flex-shrink-0 relative" ref="menuRef">
          <Dropdown>
            <template #trigger>
              <button
                class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <Icon icon="lucide:more-horizontal" class="h-4 w-4" />
              </button>
            </template>

            <DropdownItem
              icon="lucide:eye"
              label="Ver Detalhes"
              @click="viewProject"
            />
            <DropdownItem
              icon="lucide:edit"
              label="Editar"
              @click="editProject"
            />
            <DropdownItem
              :icon="
                project.arquivado ? 'lucide:archive-restore' : 'lucide:archive'
              "
              :label="project.arquivado ? 'Desarquivar' : 'Arquivar'"
              @click="archiveProject"
            />
            <DropdownItem
              icon="lucide:trash-2"
              label="Excluir"
              danger
              @click="deleteProject"
              divider
            />
          </Dropdown>
        </div>
      </div>

      <!-- Descrição -->
      <div v-if="project.descricao" class="mt-3">
        <p class="text-gray-600 text-sm line-clamp-3 leading-relaxed">
          {{ project.descricao }}
        </p>
      </div>
    </div>

    <!-- Progresso -->
    <div class="px-6 pb-4 mt-auto">
      <div class="flex items-center justify-between text-sm text-gray-500 mb-2">
        <span>Progresso</span>
        <span class="font-medium">{{ progressPercentage }}%</span>
      </div>
      <Progress
        :value="progressPercentage"
        size="sm"
        :variant="getProgressVariant()"
        animated
      />
    </div>

    <!-- Estatísticas -->
    <div class="px-6 pb-4 grid grid-cols-3 gap-5 border-t border-gray-100">
      <div class="text-center">
        <div class="text-lg font-semibold text-gray-900">
          {{ project.total_tarefas || 0 }}
        </div>
        <div class="text-xs text-gray-500">Tarefas</div>
      </div>
      <div class="text-center">
        <div class="text-lg font-semibold text-green-600">
          {{ project.tarefas_concluidas || 0 }}
        </div>
        <div class="text-xs text-gray-500">Concluídas</div>
      </div>
      <div class="text-center">
        <div class="text-lg font-semibold text-blue-600">
          {{ project.total_membros || 0 }}
        </div>
        <div class="text-xs text-gray-500">Membros</div>
      </div>
    </div>

    <!-- Datas e Membros -->
    <div class="px-6 pb-6">
      <!-- Datas -->
      <div class="flex items-center gap-4 text-sm text-gray-500 mb-3">
        <div class="flex items-center gap-1">
          <Icon icon="lucide:calendar" class="h-4 w-4" />
          <span>{{ formatDate(project.data_inicio) }}</span>
        </div>
        <div class="flex items-center gap-1">
          <Icon icon="lucide:flag" class="h-4 w-4" />
          <span>{{ formatDate(project.data_fim) }}</span>
        </div>
      </div>

      <!-- Membros -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="flex -space-x-2">
            <Avatar
              v-for="(member, index) in project.membros?.slice(0, 3)"
              :key="index"
              :name="member.nome || `Membro ${index + 1}`"
              :src="member.avatar"
              size="sm"
              class="border-2 border-white"
            />
            <div
              v-if="(project.membros?.length || 0) > 3"
              class="w-8 h-8 rounded-full bg-gray-200 border-2 border-white flex items-center justify-center text-xs font-medium text-gray-600"
            >
              +{{ (project.membros?.length || 0) - 3 }}
            </div>
          </div>
        </div>

        <!-- Indicador de atraso -->
        <div
          v-if="isOverdue"
          class="flex items-center gap-1 text-red-500 text-sm"
        >
          <Icon icon="lucide:alert-triangle" class="h-4 w-4" />
          <span>Atrasado</span>
        </div>
      </div>
    </div>

    <!-- Footer com ações rápidas -->
    <div class="px-6 py-3 bg-gray-50 border-t border-gray-100">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <Tooltip content="Última atualização">
            <template #trigger>
              <div class="flex items-center gap-1 text-xs text-gray-500">
                <Icon icon="lucide:clock" class="h-3 w-3" />
                <span>{{ formatRelativeTime(project.atualizado_em) }}</span>
              </div>
            </template>
          </Tooltip>
        </div>

        <div class="flex items-center gap-2">
          <button
            @click="viewProject"
            class="text-primary-600 hover:text-primary-700 text-sm font-medium transition-colors"
          >
            Ver Detalhes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";
import type { Projeto } from "~/api/schemas";
import Badge from "@/components/ui/Badge.vue";
import Avatar from "@/components/ui/Avatar.vue";
import Progress from "@/components/ui/Progress.vue";
import Tooltip from "@/components/ui/Tooltip.vue";
import Dropdown from "@/components/ui/Dropdown.vue";
import DropdownItem from "@/components/ui/DropdownItem.vue";

interface Props {
  project: Projeto;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  view: [id: number];
  edit: [project: Projeto];
  archive: [id: number];
  delete: [id: number];
}>();

const router = useRouter();
const menuRef = ref<HTMLElement>();

// Computed properties
const progressPercentage = computed(() => {
  const total = props.project.total_tarefas || 0;
  const completed = props.project.tarefas_concluidas || 0;
  return total > 0 ? Math.round((completed / total) * 100) : 0;
});

const isOverdue = computed(() => {
  if (!props.project.data_fim) return false;
  const today = new Date();
  const endDate = new Date(props.project.data_fim);
  return endDate < today && props.project.status !== "CONCLUIDO";
});

// Ícones e cores para status
const getProjectIcon = (status: string) => {
  const icons = {
    PLANEJADO: "lucide:calendar",
    EM_ANDAMENTO: "lucide:play-circle",
    PAUSADO: "lucide:pause-circle",
    CONCLUIDO: "lucide:check-circle",
    CANCELADO: "lucide:x-circle",
  };
  return icons[status as keyof typeof icons] || "lucide:folder";
};

const getStatusIconBg = (status: string) => {
  const colors = {
    PLANEJADO: "bg-blue-500",
    EM_ANDAMENTO: "bg-green-500",
    PAUSADO: "bg-yellow-500",
    CONCLUIDO: "bg-emerald-500",
    CANCELADO: "bg-red-500",
  };
  return colors[status as keyof typeof colors] || "bg-gray-500";
};

const getStatusVariant = (status: string) => {
  const variants = {
    PLANEJADO: "status-planejado" as const,
    EM_ANDAMENTO: "status-andamento" as const,
    PAUSADO: "status-pausado" as const,
    CONCLUIDO: "status-concluido" as const,
    CANCELADO: "status-cancelado" as const,
  };
  return variants[status as keyof typeof variants] || ("default" as const);
};

const getStatusLabel = (status: string) => {
  const labels = {
    PLANEJADO: "Planejado",
    EM_ANDAMENTO: "Em Andamento",
    PAUSADO: "Pausado",
    CONCLUIDO: "Concluído",
    CANCELADO: "Cancelado",
  };
  return labels[status as keyof typeof labels] || status;
};

const getPriorityVariant = (priority: string) => {
  const variants = {
    BAIXA: "priority-baixa" as const,
    MEDIA: "priority-media" as const,
    ALTA: "priority-alta" as const,
    CRITICA: "priority-critica" as const,
  };
  return variants[priority as keyof typeof variants] || ("default" as const);
};

const getPriorityLabel = (priority: string) => {
  const labels = {
    BAIXA: "Baixa",
    MEDIA: "Média",
    ALTA: "Alta",
    CRITICA: "Crítica",
  };
  return labels[priority as keyof typeof labels] || priority;
};

const getProgressVariant = () => {
  if (progressPercentage.value >= 80) return "success" as const;
  if (progressPercentage.value >= 60) return "info" as const;
  if (progressPercentage.value >= 40) return "warning" as const;
  return "danger" as const;
};

// Formatação de datas
const formatDate = (date: string) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "2-digit",
  });
};

const formatRelativeTime = (date: string) => {
  if (!date) return "N/A";

  const now = new Date();
  const past = new Date(date);
  const diffInHours = Math.floor(
    (now.getTime() - past.getTime()) / (1000 * 60 * 60)
  );

  if (diffInHours < 1) return "Agora mesmo";
  if (diffInHours < 24) return `${diffInHours}h atrás`;
  if (diffInHours < 48) return "Ontem";

  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 7) return `${diffInDays}d atrás`;
  if (diffInDays < 30) return `${Math.floor(diffInDays / 7)}sem atrás`;

  return formatDate(date);
};

// Handlers
const viewProject = () => {
  router.push(`/projects/${props.project.id}`);
};

const editProject = () => {
  emit("edit", props.project);
};

const archiveProject = () => {
  emit("archive", props.project.id);
};

const deleteProject = () => {
  emit("delete", props.project.id);
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
