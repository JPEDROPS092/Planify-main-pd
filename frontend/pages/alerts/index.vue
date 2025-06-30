<template>
  <div class="container mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Alertas do Sistema</h1>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-10">
      <Icon icon="svg-spinners:180-ring-with-bg" class="w-12 h-12 mx-auto text-primary" />
      <p class="mt-2 text-gray-600">Carregando alertas...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 text-center">
      <Icon icon="lucide:alert-triangle" class="w-10 h-10 mx-auto text-red-500" />
      <p class="mt-2 font-semibold text-red-700">Erro ao carregar alertas</p>
      <p class="text-sm text-red-600">{{ error.message }}</p>
      <button @click="refetch()" class="mt-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700">Tentar Novamente</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="!alerts || alerts.results.length === 0" class="text-center py-10 border-2 border-dashed rounded-lg">
      <Icon icon="lucide:shield-check" class="w-16 h-16 mx-auto text-gray-400" />
      <h3 class="mt-2 text-xl font-medium text-gray-800">Nenhum alerta ativo</h3>
      <p class="mt-1 text-gray-500">O sistema está operando normalmente.</p>
    </div>

    <!-- Alerts List -->
    <div v-else class="space-y-4">
      <div v-for="alert in alerts.results" :key="alert.id" 
           class="p-4 rounded-md border"
           :class="getAlertClass(alert.nivel)">
        <div class="flex items-start justify-between">
          <div class="flex items-start">
            <Icon :icon="getAlertIcon(alert.nivel)" class="h-6 w-6 mr-3" />
            <div>
              <p class="font-semibold">{{ alert.titulo }}</p>
              <p class="text-sm">{{ alert.descricao }}</p>
              <p class="text-xs opacity-75 mt-1">{{ timeAgo(alert.criado_em) }}</p>
            </div>
          </div>
          <button v-if="!alert.resolvido" @click="resolveAlertMutation.mutate(alert.id)" class="text-sm font-medium hover:underline" title="Marcar como resolvido">
            Resolver
          </button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="alerts && alerts.total_pages > 1" class="mt-6 flex justify-center">
       <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
        <button @click="currentPage--" :disabled="currentPage === 1" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
          Anterior
        </button>
        <span class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
          Página {{ currentPage }} de {{ alerts.total_pages }}
        </span>
        <button @click="currentPage++" :disabled="currentPage === alerts.total_pages" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
          Próximo
        </button>
      </nav>
    </div>

  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

import { ref } from 'vue';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useAlertService } from '~/services/alertService';
import { Icon } from '@iconify/vue';
import { useToast } from '~/composables/useToast';
import type { PaginatedAlertaList } from '~/api-types';
import { formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';

const queryClient = useQueryClient();
const alertService = useAlertService();
const { toast } = useToast();

const currentPage = ref(1);

// Fetch alerts
const { data: alerts, isLoading, error, refetch } = useQuery<PaginatedAlertaList>({
  queryKey: ['alerts', currentPage],
  queryFn: () => alertService.getAlerts({ page: currentPage.value }),
});

// Resolve alert mutation
const resolveAlertMutation = useMutation({
  mutationFn: (id: number) => alertService.resolveAlert(id),
  onSuccess: () => {
    toast({ title: 'Sucesso', description: 'Alerta marcado como resolvido.' });
    queryClient.invalidateQueries({ queryKey: ['alerts'] });
  },
  onError: (err: any) => {
    toast({ title: 'Erro', description: 'Falha ao resolver o alerta.', variant: 'destructive' });
  },
});

const timeAgo = (dateString: string) => {
  return formatDistanceToNow(new Date(dateString), { addSuffix: true, locale: ptBR });
};

const getAlertClass = (level: string) => {
  const classes: Record<string, string> = {
    INFO: 'bg-blue-50 border-blue-200 text-blue-800',
    AVISO: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    CRITICO: 'bg-red-50 border-red-200 text-red-800',
  };
  return classes[level] || 'bg-gray-50 border-gray-200 text-gray-800';
};

const getAlertIcon = (level: string) => {
  const icons: Record<string, string> = {
    INFO: 'lucide:info',
    AVISO: 'lucide:alert-triangle',
    CRITICO: 'lucide:alert-octagon',
  };
  return icons[level] || 'lucide:bell';
};
</script>
