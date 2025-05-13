<template>
  <div class="w-full overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700">
    <!-- Cabeçalho da tabela -->
    <div class="flex items-center justify-between bg-gray-50 p-4 dark:bg-gray-800">
      <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ title }}</h3>
      <div class="flex items-center space-x-2">
        <div v-if="searchable" class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Pesquisar..."
            class="rounded-md border border-gray-300 px-3 py-2 text-sm placeholder-gray-500 focus:border-blue-500 focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400"
          />
          <span class="absolute right-3 top-2.5 text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </span>
        </div>
        <slot name="actions"></slot>
      </div>
    </div>

    <!-- Tabela -->
    <div class="overflow-x-auto">
      <table class="w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-800">
          <tr>
            <th
              v-for="column in columns"
              :key="column.key"
              :class="[
                'px-6 py-3 text-left text-xs font-medium uppercase tracking-wider',
                column.sortable ? 'cursor-pointer' : '',
                'text-gray-500 dark:text-gray-400'
              ]"
              @click="column.sortable ? sort(column.key) : null"
            >
              <div class="flex items-center">
                {{ column.label }}
                <span v-if="column.sortable" class="ml-1">
                  <svg
                    v-if="sortKey === column.key"
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      :d="sortOrder === 'asc' ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'"
                    />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 opacity-30" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                  </svg>
                </span>
              </div>
            </th>
            <th v-if="hasActions" class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400">
              Ações
            </th>
          </tr>
        </thead>
        <tbody v-if="loading" class="divide-y divide-gray-200 bg-white dark:divide-gray-700 dark:bg-gray-900">
          <tr v-for="i in 5" :key="i">
            <td v-for="column in columns" :key="column.key" class="whitespace-nowrap px-6 py-4">
              <SkeletonLoader height="1.5rem" />
            </td>
            <td v-if="hasActions" class="whitespace-nowrap px-6 py-4 text-right text-sm font-medium">
              <SkeletonLoader width="80px" height="1.5rem" />
            </td>
          </tr>
        </tbody>
        <tbody v-else-if="filteredData.length === 0" class="divide-y divide-gray-200 bg-white dark:divide-gray-700 dark:bg-gray-900">
          <tr>
            <td :colspan="hasActions ? columns.length + 1 : columns.length" class="px-6 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
              <div class="flex flex-col items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="mb-2 h-10 w-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <p>Nenhum resultado encontrado</p>
                <p v-if="searchQuery" class="mt-1 text-xs">Tente usar termos diferentes na pesquisa</p>
              </div>
            </td>
          </tr>
        </tbody>
        <tbody v-else class="divide-y divide-gray-200 bg-white dark:divide-gray-700 dark:bg-gray-900">
          <tr
            v-for="(item, index) in paginatedData"
            :key="index"
            class="transition-colors hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            <td
              v-for="column in columns"
              :key="column.key"
              :class="[
                'whitespace-nowrap px-6 py-4 text-sm',
                column.align === 'right' ? 'text-right' : column.align === 'center' ? 'text-center' : 'text-left',
                'text-gray-900 dark:text-gray-200'
              ]"
            >
              <slot :name="`cell-${column.key}`" :item="item" :value="getNestedValue(item, column.key)">
                {{ formatValue(getNestedValue(item, column.key), column.format) }}
              </slot>
            </td>
            <td v-if="hasActions" class="whitespace-nowrap px-6 py-4 text-right text-sm font-medium">
              <slot name="row-actions" :item="item"></slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginação -->
    <div v-if="paginated && filteredData.length > 0" class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 dark:border-gray-700 dark:bg-gray-900 sm:px-6">
      <div class="flex flex-1 justify-between sm:hidden">
        <button
          :disabled="currentPage === 1"
          @click="currentPage--"
          class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
        >
          Anterior
        </button>
        <button
          :disabled="currentPage === totalPages"
          @click="currentPage++"
          class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
        >
          Próximo
        </button>
      </div>
      <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
        <div>
          <p class="text-sm text-gray-700 dark:text-gray-300">
            Mostrando <span class="font-medium">{{ startItem }}</span> a
            <span class="font-medium">{{ endItem }}</span> de
            <span class="font-medium">{{ filteredData.length }}</span> resultados
          </p>
        </div>
        <div>
          <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
            <button
              :disabled="currentPage === 1"
              @click="currentPage = 1"
              class="relative inline-flex items-center rounded-l-md border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700"
            >
              <span class="sr-only">Primeira</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fill-rule="evenodd"
                  d="M15.707 15.707a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 010 1.414zm-6 0a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 011.414 1.414L5.414 10l4.293 4.293a1 1 0 010 1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
            <button
              :disabled="currentPage === 1"
              @click="currentPage--"
              class="relative inline-flex items-center border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700"
            >
              <span class="sr-only">Anterior</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fill-rule="evenodd"
                  d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
            <button
              v-for="page in visiblePages"
              :key="page"
              @click="currentPage = page"
              :class="[
                'relative inline-flex items-center border px-4 py-2 text-sm font-medium',
                currentPage === page
                  ? 'z-10 border-blue-500 bg-blue-50 text-blue-600 dark:border-blue-600 dark:bg-blue-900 dark:text-blue-400'
                  : 'border-gray-300 bg-white text-gray-500 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700'
              ]"
            >
              {{ page }}
            </button>
            <button
              :disabled="currentPage === totalPages"
              @click="currentPage++"
              class="relative inline-flex items-center border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700"
            >
              <span class="sr-only">Próximo</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fill-rule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
            <button
              :disabled="currentPage === totalPages"
              @click="currentPage = totalPages"
              class="relative inline-flex items-center rounded-r-md border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700"
            >
              <span class="sr-only">Última</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fill-rule="evenodd"
                  d="M4.293 15.707a1 1 0 001.414 0l5-5a1 1 0 000-1.414l-5-5a1 1 0 00-1.414 1.414L8.586 10 4.293 14.293a1 1 0 000 1.414zm6 0a1 1 0 001.414 0l5-5a1 1 0 000-1.414l-5-5a1 1 0 00-1.414 1.414L15.586 10l-4.293 4.293a1 1 0 000 1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch } from 'vue'
import SkeletonLoader from './SkeletonLoader.vue'

export interface Column {
  key: string
  label: string
  sortable?: boolean
  align?: 'left' | 'center' | 'right'
  format?: 'date' | 'datetime' | 'currency' | 'number' | 'percent' | 'boolean'
}

export default defineComponent({
  name: 'DataTable',
  components: {
    SkeletonLoader
  },
  props: {
    title: {
      type: String,
      default: 'Dados'
    },
    data: {
      type: Array,
      required: true
    },
    columns: {
      type: Array as () => Column[],
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    paginated: {
      type: Boolean,
      default: true
    },
    itemsPerPage: {
      type: Number,
      default: 10
    },
    searchable: {
      type: Boolean,
      default: true
    },
    hasActions: {
      type: Boolean,
      default: true
    },
    initialSortKey: {
      type: String,
      default: ''
    },
    initialSortOrder: {
      type: String,
      default: 'asc'
    }
  },
  setup(props) {
    const currentPage = ref(1)
    const searchQuery = ref('')
    const sortKey = ref(props.initialSortKey)
    const sortOrder = ref(props.initialSortOrder)

    // Reset para a primeira página quando os dados mudam
    watch(() => props.data, () => {
      currentPage.value = 1
    })

    // Reset para a primeira página quando a pesquisa muda
    watch(searchQuery, () => {
      currentPage.value = 1
    })

    // Filtra os dados com base na pesquisa
    const filteredData = computed(() => {
      if (!searchQuery.value) return props.data

      const query = searchQuery.value.toLowerCase()
      return props.data.filter((item: any) => {
        return props.columns.some((column) => {
          const value = getNestedValue(item, column.key)
          if (value === null || value === undefined) return false
          return String(value).toLowerCase().includes(query)
        })
      })
    })

    // Ordena os dados
    const sortedData = computed(() => {
      if (!sortKey.value) return filteredData.value

      return [...filteredData.value].sort((a: any, b: any) => {
        const aValue = getNestedValue(a, sortKey.value)
        const bValue = getNestedValue(b, sortKey.value)

        if (aValue === null || aValue === undefined) return sortOrder.value === 'asc' ? -1 : 1
        if (bValue === null || bValue === undefined) return sortOrder.value === 'asc' ? 1 : -1

        if (typeof aValue === 'string' && typeof bValue === 'string') {
          return sortOrder.value === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue)
        }

        return sortOrder.value === 'asc' ? aValue - bValue : bValue - aValue
      })
    })

    // Calcula o total de páginas
    const totalPages = computed(() => {
      return Math.ceil(filteredData.value.length / props.itemsPerPage)
    })

    // Calcula as páginas visíveis na paginação
    const visiblePages = computed(() => {
      const pages = []
      const maxVisiblePages = 5
      let startPage = Math.max(1, currentPage.value - Math.floor(maxVisiblePages / 2))
      let endPage = Math.min(totalPages.value, startPage + maxVisiblePages - 1)

      if (endPage - startPage + 1 < maxVisiblePages) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1)
      }

      for (let i = startPage; i <= endPage; i++) {
        pages.push(i)
      }

      return pages
    })

    // Pagina os dados
    const paginatedData = computed(() => {
      if (!props.paginated) return sortedData.value

      const start = (currentPage.value - 1) * props.itemsPerPage
      const end = start + props.itemsPerPage
      return sortedData.value.slice(start, end)
    })

    // Calcula o índice do primeiro item na página atual
    const startItem = computed(() => {
      return (currentPage.value - 1) * props.itemsPerPage + 1
    })

    // Calcula o índice do último item na página atual
    const endItem = computed(() => {
      return Math.min(currentPage.value * props.itemsPerPage, filteredData.value.length)
    })

    // Função para ordenar os dados
    const sort = (key: string) => {
      if (sortKey.value === key) {
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortKey.value = key
        sortOrder.value = 'asc'
      }
    }

    // Função para obter valores aninhados (ex: "user.name")
    const getNestedValue = (obj: any, path: string) => {
      return path.split('.').reduce((prev, curr) => {
        return prev ? prev[curr] : null
      }, obj)
    }

    // Função para formatar valores com base no tipo
    const formatValue = (value: any, format?: string) => {
      if (value === null || value === undefined) return '-'

      switch (format) {
        case 'date':
          return new Date(value).toLocaleDateString('pt-BR')
        case 'datetime':
          return new Date(value).toLocaleString('pt-BR')
        case 'currency':
          return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value)
        case 'number':
          return new Intl.NumberFormat('pt-BR').format(value)
        case 'percent':
          return new Intl.NumberFormat('pt-BR', { style: 'percent', minimumFractionDigits: 2 }).format(value / 100)
        case 'boolean':
          return value ? 'Sim' : 'Não'
        default:
          return value
      }
    }

    return {
      currentPage,
      searchQuery,
      sortKey,
      sortOrder,
      filteredData,
      paginatedData,
      totalPages,
      visiblePages,
      startItem,
      endItem,
      sort,
      getNestedValue,
      formatValue
    }
  }
})
</script>
