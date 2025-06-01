<!--
  Pagination.vue
  
  Componente para navegação em listas e tabelas com muitos itens.
  Suporta navegação por página, controle de itens por página e exibição de informações de paginação.
  
  Props:
  - currentPage: Página atual
  - totalPages: Total de páginas
  - totalItems: Total de itens
  - itemsPerPage: Itens por página
  - showItemsPerPage: Exibir controle de itens por página
  - itemsPerPageOptions: Opções de itens por página
  - siblingCount: Número de páginas vizinhas a serem exibidas
  - class: Classes CSS adicionais
  
  Eventos:
  - update:currentPage: Emitido quando a página atual é alterada
  - update:itemsPerPage: Emitido quando o número de itens por página é alterado
-->

<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '@/lib/utils';
import {
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
} from 'lucide-vue-next';
import { Button } from '@/components/ui/button';

// Props do componente
const props = withDefaults(
  defineProps<{
    currentPage: number;
    totalPages: number;
    totalItems?: number;
    itemsPerPage?: number;
    showItemsPerPage?: boolean;
    itemsPerPageOptions?: number[];
    siblingCount?: number;
    class?: string;
  }>(),
  {
    totalItems: 0,
    itemsPerPage: 10,
    showItemsPerPage: false,
    itemsPerPageOptions: () => [5, 10, 25, 50, 100],
    siblingCount: 1,
  }
);

const emit = defineEmits<{
  'update:currentPage': [page: number];
  'update:itemsPerPage': [itemsPerPage: number];
}>();

// Calcular intervalo de páginas a serem exibidas
const pageRange = computed(() => {
  const { currentPage, totalPages, siblingCount } = props;

  // Garantir que a página atual esteja dentro dos limites
  const safePage = Math.max(1, Math.min(currentPage, totalPages));

  // Calcular o intervalo de páginas a serem exibidas
  let startPage = Math.max(1, safePage - siblingCount);
  let endPage = Math.min(totalPages, safePage + siblingCount);

  // Ajustar o intervalo para exibir sempre o mesmo número de páginas
  const displayedPageCount = siblingCount * 2 + 1;
  if (endPage - startPage + 1 < displayedPageCount) {
    if (startPage === 1) {
      endPage = Math.min(totalPages, startPage + displayedPageCount - 1);
    } else if (endPage === totalPages) {
      startPage = Math.max(1, endPage - displayedPageCount + 1);
    }
  }

  // Gerar o array de páginas
  const pages = [];
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return {
    startPage,
    endPage,
    pages,
  };
});

// Verificar se deve exibir os controles de primeira/última página
const showFirstLastControls = computed(() => {
  return props.totalPages > props.siblingCount * 2 + 1;
});

// Verificar se deve exibir os ellipsis (...)
const showStartEllipsis = computed(() => {
  return pageRange.value.startPage > 1;
});

const showEndEllipsis = computed(() => {
  return pageRange.value.endPage < props.totalPages;
});

// Informações sobre os itens exibidos
const itemsInfo = computed(() => {
  if (!props.totalItems) return '';

  const start = (props.currentPage - 1) * props.itemsPerPage + 1;
  const end = Math.min(start + props.itemsPerPage - 1, props.totalItems);

  return `${start}-${end} de ${props.totalItems} itens`;
});

// Navegar para uma página específica
const goToPage = (page: number) => {
  if (page >= 1 && page <= props.totalPages && page !== props.currentPage) {
    emit('update:currentPage', page);
  }
};

// Alterar o número de itens por página
const changeItemsPerPage = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  const value = parseInt(target.value, 10);

  if (value !== props.itemsPerPage) {
    emit('update:itemsPerPage', value);
    // Voltar para a primeira página ao alterar o número de itens por página
    emit('update:currentPage', 1);
  }
};
</script>

<template>
  <div
    :class="
      cn(
        'flex flex-col sm:flex-row items-center justify-between gap-4',
        props.class
      )
    "
  >
    <!-- Informações de paginação -->
    <div v-if="totalItems" class="text-sm text-muted-foreground">
      {{ itemsInfo }}
    </div>

    <!-- Controle de itens por página -->
    <div v-if="showItemsPerPage" class="flex items-center gap-2">
      <label for="items-per-page" class="text-sm text-muted-foreground">
        Itens por página:
      </label>
      <select
        id="items-per-page"
        :value="itemsPerPage"
        @change="changeItemsPerPage"
        class="h-8 w-20 rounded-md border border-input bg-background px-2 text-sm focus:outline-none focus:ring-1 focus:ring-ring"
      >
        <option
          v-for="option in itemsPerPageOptions"
          :key="option"
          :value="option"
        >
          {{ option }}
        </option>
      </select>
    </div>

    <!-- Controles de navegação -->
    <nav class="flex items-center gap-1" aria-label="Paginação">
      <!-- Primeira página -->
      <Button
        v-if="showFirstLastControls"
        variant="outline"
        size="icon"
        :disabled="currentPage === 1"
        @click="goToPage(1)"
        aria-label="Primeira página"
      >
        <ChevronsLeft class="h-4 w-4" />
      </Button>

      <!-- Página anterior -->
      <Button
        variant="outline"
        size="icon"
        :disabled="currentPage === 1"
        @click="goToPage(currentPage - 1)"
        aria-label="Página anterior"
      >
        <ChevronLeft class="h-4 w-4" />
      </Button>

      <!-- Ellipsis inicial -->
      <div
        v-if="showStartEllipsis"
        class="flex items-center justify-center h-8 w-8 text-sm text-muted-foreground"
      >
        ...
      </div>

      <!-- Páginas numeradas -->
      <Button
        v-for="page in pageRange.pages"
        :key="page"
        variant="outline"
        size="icon"
        :class="{
          'bg-primary text-primary-foreground hover:bg-primary/90 hover:text-primary-foreground':
            page === currentPage,
        }"
        @click="goToPage(page)"
        :aria-label="`Página ${page}`"
        :aria-current="page === currentPage ? 'page' : undefined"
      >
        {{ page }}
      </Button>

      <!-- Ellipsis final -->
      <div
        v-if="showEndEllipsis"
        class="flex items-center justify-center h-8 w-8 text-sm text-muted-foreground"
      >
        ...
      </div>

      <!-- Próxima página -->
      <Button
        variant="outline"
        size="icon"
        :disabled="currentPage === totalPages || totalPages === 0"
        @click="goToPage(currentPage + 1)"
        aria-label="Próxima página"
      >
        <ChevronRight class="h-4 w-4" />
      </Button>

      <!-- Última página -->
      <Button
        v-if="showFirstLastControls"
        variant="outline"
        size="icon"
        :disabled="currentPage === totalPages || totalPages === 0"
        @click="goToPage(totalPages)"
        aria-label="Última página"
      >
        <ChevronsRight class="h-4 w-4" />
      </Button>
    </nav>
  </div>
</template>

<style scoped>
/* Estilos específicos para o componente, se necessário */
</style>
