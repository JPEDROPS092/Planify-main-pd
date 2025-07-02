<!-- filepath: pages/alerts/index.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: "auth",
});

import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import { formatDistanceToNow } from "date-fns";
import { ptBR } from "date-fns/locale";

// 1. Importar as funções e tipos corretos gerados pelo Orval para alertas
import {
  useCostsAlertasList,
  costsAlertasResolverCreate,
} from "@/api/custo/custo";
import type { PaginatedAlertaList, Alerta } from "@/api/schemas";

const queryClient = useQueryClient();
const { toast } = useToast();

const currentPage = ref(1);
const pageSize = 10; // Defina um tamanho de página para calcular o total

// 2. Usar o hook correto do Orval para buscar os alertas
const {
  data: paginatedAlerts,
  isLoading,
  error,
  refetch,
} = useQuery<PaginatedAlertaList>({
  queryKey: ["alerts", currentPage],
  queryFn: () => costsAlertasList({ page: currentPage.value }),
  placeholderData: (previousData) => previousData, // Mantém os dados antigos enquanto busca novos
});

// Calcula o total de páginas a partir do 'count' da API
const totalPages = computed(() => {
  if (!paginatedAlerts.value?.count) return 1;
  return Math.ceil(paginatedAlerts.value.count / pageSize);
});

// Extrai a lista de resultados para facilitar o uso no template
const alerts = computed(() => paginatedAlerts.value?.results || []);

// 3. Usar a função correta do Orval para a mutação de resolver o alerta
const resolveAlertMutation = useMutation({
  mutationFn: (alertId: number) => {
    // A função do Orval não precisa de um corpo, apenas o ID
    return costsAlertasResolverCreate(alertId);
  },
  onSuccess: () => {
    toast({ title: "Sucesso", description: "Alerta marcado como resolvido." });
    // Invalida a query para forçar o refetch dos dados atualizados
    queryClient.invalidateQueries({ queryKey: ["alerts"] });
  },
  onError: (err: any) => {
    toast({
      title: "Erro",
      description: err.response?.data?.detail || "Falha ao resolver o alerta.",
      variant: "destructive",
    });
  },
});

const timeAgo = (dateString: string) => {
  if (!dateString) return "";
  return formatDistanceToNow(new Date(dateString), {
    addSuffix: true,
    locale: ptBR,
  });
};

// 4. Mapear o 'status' do alerta para classes e ícones
const getAlertClass = (status?: Alerta["status"]) => {
  const classes: Record<string, string> = {
    ATIVO:
      "bg-yellow-50 border-yellow-200 text-yellow-800 dark:bg-yellow-900/30 dark:border-yellow-700/50 dark:text-yellow-300",
    RESOLVIDO:
      "bg-green-50 border-green-200 text-green-800 dark:bg-green-900/30 dark:border-green-700/50 dark:text-green-300",
    IGNORADO:
      "bg-gray-100 border-gray-200 text-gray-600 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400",
  };
  return classes[status || ""] || "bg-gray-50 border-gray-200 text-gray-800";
};

const getAlertIcon = (status?: Alerta["status"]) => {
  const icons: Record<string, string> = {
    ATIVO: "lucide:alert-triangle",
    RESOLVIDO: "lucide:check-circle-2",
    IGNORADO: "lucide:circle-slash",
  };
  return icons[status || ""] || "lucide:bell";
};
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
        Alertas do Sistema
      </h1>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-20">
      <Icon
        icon="svg-spinners:180-ring-with-bg"
        class="w-16 h-16 mx-auto text-primary-600"
      />
      <p class="mt-4 text-lg text-gray-600 dark:text-gray-400">
        Carregando alertas...
      </p>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md"
      role="alert"
    >
      <p class="font-bold">Ocorreu um erro</p>
      <p>{{ (error as any).message }}</p>
      <button
        @click="refetch()"
        class="mt-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
      >
        Tentar Novamente
      </button>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="alerts.length === 0"
      class="text-center py-20 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg"
    >
      <Icon
        icon="lucide:shield-check"
        class="w-20 h-20 mx-auto text-gray-400 dark:text-gray-500"
      />
      <h3 class="mt-4 text-xl font-medium text-gray-800 dark:text-gray-200">
        Tudo certo por aqui!
      </h3>
      <p class="mt-1 text-gray-500 dark:text-gray-400">
        Nenhum alerta do sistema para exibir no momento.
      </p>
    </div>

    <!-- Alerts List -->
    <div v-else class="space-y-4">
      <div
        v-for="alert in alerts"
        :key="alert.id"
        class="p-4 rounded-lg border-l-4"
        :class="getAlertClass(alert.status)"
      >
        <div class="flex items-start justify-between">
          <div class="flex items-start">
            <Icon
              :icon="getAlertIcon(alert.status)"
              class="h-6 w-6 mr-4 flex-shrink-0 mt-0.5"
            />
            <div>
              <p class="font-semibold">{{ alert.mensagem }}</p>
              <p class="text-sm opacity-80">
                Associado ao {{ alert.tipo_display }}:
                <strong>{{
                  alert.tarefa ? alert.tarefa_titulo : alert.projeto_nome
                }}</strong>
              </p>
              <p class="text-xs opacity-70 mt-1">
                Criado {{ timeAgo(alert.data_criacao) }}
              </p>
            </div>
          </div>
          <button
            v-if="alert.status === 'ATIVO'"
            @click="resolveAlertMutation.mutate(alert.id)"
            :disabled="
              resolveAlertMutation.isPending.value &&
              resolveAlertMutation.variables.value === alert.id
            "
            class="ml-4 flex-shrink-0 px-3 py-1 text-xs font-medium rounded-full bg-white text-gray-700 hover:bg-gray-100 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 disabled:opacity-50"
            title="Marcar como resolvido"
          >
            Resolver
          </button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="mt-8 flex justify-center">
      <nav
        class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
        aria-label="Pagination"
      >
        <button
          @click="currentPage--"
          :disabled="!paginatedAlerts?.previous"
          class="relative inline-flex items-center px-3 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Anterior
        </button>
        <span
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-200"
        >
          Página {{ currentPage }} de {{ totalPages }}
        </span>
        <button
          @click="currentPage++"
          :disabled="!paginatedAlerts?.next"
          class="relative inline-flex items-center px-3 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Próximo
        </button>
      </nav>
    </div>
  </div>
</template>
