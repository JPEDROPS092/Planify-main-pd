<!--
  ActivityFeed.vue
  
  Componente para exibição de atividades e atualizações recentes.
  Útil para feeds de notificações, histórico de atividades e atualizações de projetos.
  
  Props:
  - activities: Array de atividades
  - loading: Estado de carregamento
  - emptyMessage: Mensagem a ser exibida quando não há atividades
  - maxItems: Número máximo de itens a serem exibidos
  - class: Classes CSS adicionais
  
  Slots:
  - activity-item: Slot para personalizar a renderização de cada atividade
  - empty: Slot para personalizar a mensagem de vazio
  - loading: Slot para personalizar o estado de carregamento
-->

<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '@/lib/utils';
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar';
import {
  MessageSquare,
  FileText,
  CheckSquare,
  Users,
  AlertTriangle,
  DollarSign,
  Calendar,
  Clock,
} from 'lucide-vue-next';

// Definir tipos para as atividades
export interface Activity {
  id: string | number;
  user: {
    id: string | number;
    name: string;
    avatar?: string;
    initials?: string;
  };
  action: string;
  target: {
    type:
      | 'task'
      | 'document'
      | 'project'
      | 'team'
      | 'risk'
      | 'cost'
      | 'comment'
      | 'other';
    id: string | number;
    name: string;
  };
  timestamp: string | Date;
  metadata?: Record<string, any>;
}

// Props do componente
const props = withDefaults(
  defineProps<{
    activities: Activity[];
    loading?: boolean;
    emptyMessage?: string;
    maxItems?: number;
    class?: string;
  }>(),
  {
    loading: false,
    emptyMessage: 'Nenhuma atividade recente',
    maxItems: 10,
  }
);

// Limitar o número de atividades exibidas
const visibleActivities = computed(() => {
  return props.activities.slice(0, props.maxItems);
});

// Formatação de data relativa
const formatRelativeTime = (date: string | Date): string => {
  if (!date) return '';

  const dateObj = typeof date === 'string' ? new Date(date) : date;
  const now = new Date();
  const diffMs = now.getTime() - dateObj.getTime();
  const diffSec = Math.round(diffMs / 1000);
  const diffMin = Math.round(diffSec / 60);
  const diffHour = Math.round(diffMin / 60);
  const diffDay = Math.round(diffHour / 24);

  if (diffSec < 60) {
    return 'agora mesmo';
  } else if (diffMin < 60) {
    return `${diffMin} ${diffMin === 1 ? 'minuto' : 'minutos'} atrás`;
  } else if (diffHour < 24) {
    return `${diffHour} ${diffHour === 1 ? 'hora' : 'horas'} atrás`;
  } else if (diffDay < 30) {
    return `${diffDay} ${diffDay === 1 ? 'dia' : 'dias'} atrás`;
  } else {
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    }).format(dateObj);
  }
};

// Obter ícone com base no tipo de alvo
const getTargetIcon = (targetType: string) => {
  switch (targetType) {
    case 'task':
      return CheckSquare;
    case 'document':
      return FileText;
    case 'project':
      return Calendar;
    case 'team':
      return Users;
    case 'risk':
      return AlertTriangle;
    case 'cost':
      return DollarSign;
    case 'comment':
      return MessageSquare;
    default:
      return Clock;
  }
};

// Obter classe de cor com base no tipo de alvo
const getTargetClass = (targetType: string) => {
  switch (targetType) {
    case 'task':
      return 'text-blue-500';
    case 'document':
      return 'text-purple-500';
    case 'project':
      return 'text-green-500';
    case 'team':
      return 'text-orange-500';
    case 'risk':
      return 'text-red-500';
    case 'cost':
      return 'text-emerald-500';
    case 'comment':
      return 'text-sky-500';
    default:
      return 'text-gray-500';
  }
};
</script>

<template>
  <div :class="cn('activity-feed space-y-4', props.class)">
    <!-- Estado de carregamento -->
    <div v-if="loading" class="py-4">
      <slot name="loading">
        <div class="flex flex-col items-center justify-center space-y-2">
          <div
            class="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent"
          ></div>
          <p class="text-sm text-muted-foreground">Carregando atividades...</p>
        </div>
      </slot>
    </div>

    <!-- Lista de atividades -->
    <template v-else-if="activities.length > 0">
      <div
        v-for="activity in visibleActivities"
        :key="activity.id"
        class="activity-item flex gap-3 pb-4 last:pb-0"
      >
        <!-- Slot para personalizar cada item -->
        <slot name="activity-item" :activity="activity">
          <!-- Avatar do usuário -->
          <Avatar size="sm">
            <AvatarImage
              v-if="activity.user.avatar"
              :src="activity.user.avatar"
              :alt="activity.user.name"
            />
            <AvatarFallback>
              {{ activity.user.initials || activity.user.name.substring(0, 2) }}
            </AvatarFallback>
          </Avatar>

          <div class="flex-1 space-y-1">
            <!-- Descrição da atividade -->
            <p class="text-sm leading-tight">
              <span class="font-medium">{{ activity.user.name }}</span>
              <span class="text-muted-foreground"> {{ activity.action }} </span>
              <span class="font-medium">
                <component
                  :is="getTargetIcon(activity.target.type)"
                  class="inline-block h-3.5 w-3.5 mr-0.5"
                  :class="getTargetClass(activity.target.type)"
                />
                {{ activity.target.name }}
              </span>
            </p>

            <!-- Timestamp -->
            <p class="text-xs text-muted-foreground">
              {{ formatRelativeTime(activity.timestamp) }}
            </p>
          </div>
        </slot>
      </div>

      <!-- Indicador de mais itens -->
      <div
        v-if="activities.length > maxItems"
        class="pt-2 text-center text-sm text-muted-foreground"
      >
        + {{ activities.length - maxItems }} mais atividades
      </div>
    </template>

    <!-- Estado vazio -->
    <div v-else class="py-6">
      <slot name="empty">
        <div class="flex flex-col items-center justify-center text-center">
          <Clock class="h-10 w-10 text-muted-foreground mb-2 opacity-50" />
          <p class="text-sm text-muted-foreground">{{ emptyMessage }}</p>
        </div>
      </slot>
    </div>
  </div>
</template>

<style scoped>
/* Estilos específicos para o componente, se necessário */
</style>
