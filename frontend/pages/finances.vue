<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Finanças</h1>
              <p class="text-gray-600 mt-1">Gerencie orçamentos, custos e relatórios financeiros</p>
            </div>
            <button @click="showCreateModal = true" 
                    class="bg-primary text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors">
              <Icon icon="lucide:plus" class="h-4 w-4 inline mr-2" />
              Nova Transação
            </button>
          </div>
        </div>
      </div>

      <!-- Financial Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Icon icon="lucide:trending-up" class="h-6 w-6 text-green-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Receitas</dt>
                  <dd class="text-lg font-medium text-gray-900">R$ 125.430,00</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Icon icon="lucide:trending-down" class="h-6 w-6 text-red-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Despesas</dt>
                  <dd class="text-lg font-medium text-gray-900">R$ 89.250,00</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Icon icon="lucide:dollar-sign" class="h-6 w-6 text-blue-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Lucro</dt>
                  <dd class="text-lg font-medium text-gray-900">R$ 36.180,00</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Icon icon="lucide:target" class="h-6 w-6 text-purple-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Orçamento</dt>
                  <dd class="text-lg font-medium text-gray-900">R$ 150.000,00</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Período</label>
              <select v-model="filters.period" 
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
                <option value="all">Todos</option>
                <option value="month">Este mês</option>
                <option value="quarter">Este trimestre</option>
                <option value="year">Este ano</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Tipo</label>
              <select v-model="filters.type" 
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
                <option value="all">Todos</option>
                <option value="receita">Receita</option>
                <option value="despesa">Despesa</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Categoria</label>
              <select v-model="filters.category" 
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
                <option value="all">Todas</option>
                <option value="projeto">Projeto</option>
                <option value="operacional">Operacional</option>
                <option value="marketing">Marketing</option>
                <option value="rh">Recursos Humanos</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Buscar</label>
              <input v-model="filters.search" type="text" placeholder="Buscar transações..."
                     class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
            </div>
          </div>
        </div>
      </div>

      <!-- Transactions Table -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">Transações Recentes</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Data
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Descrição
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Categoria
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tipo
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Valor
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="transaction in mockTransactions" :key="transaction.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(transaction.date) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">{{ transaction.description }}</div>
                  <div class="text-sm text-gray-500">{{ transaction.project }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ transaction.category }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    transaction.type === 'receita' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  ]">
                    {{ transaction.type === 'receita' ? 'Receita' : 'Despesa' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium"
                    :class="transaction.type === 'receita' ? 'text-green-600' : 'text-red-600'">
                  {{ transaction.type === 'receita' ? '+' : '-' }}R$ {{ transaction.amount.toLocaleString('pt-BR') }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button class="text-primary hover:text-primary-700 mr-3">Editar</button>
                  <button class="text-red-600 hover:text-red-700">Excluir</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Create Transaction Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Nova Transação</h3>
          <form @submit.prevent="createTransaction" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Descrição</label>
              <input v-model="transactionForm.description" type="text" required
                     class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Tipo</label>
              <select v-model="transactionForm.type" required
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
                <option value="">Selecione</option>
                <option value="receita">Receita</option>
                <option value="despesa">Despesa</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Categoria</label>
              <select v-model="transactionForm.category" required
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
                <option value="">Selecione</option>
                <option value="projeto">Projeto</option>
                <option value="operacional">Operacional</option>
                <option value="marketing">Marketing</option>
                <option value="rh">Recursos Humanos</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Valor</label>
              <input v-model="transactionForm.amount" type="number" step="0.01" required
                     class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Data</label>
              <input v-model="transactionForm.date" type="date" required
                     class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
            </div>
            <div class="flex justify-end space-x-3 pt-4">
              <button @click="showCreateModal = false" type="button" 
                      class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md">
                Cancelar
              </button>
              <button type="submit" :disabled="creating"
                      class="px-4 py-2 text-sm font-medium text-white bg-primary hover:bg-primary-700 rounded-md disabled:opacity-50">
                <span v-if="creating" class="inline-block mr-2">
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                </span>
                Criar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

definePageMeta({
  middleware: 'auth'
})

const showCreateModal = ref(false)
const creating = ref(false)

const filters = ref({
  period: 'all',
  type: 'all',
  category: 'all',
  search: ''
})

const transactionForm = ref({
  description: '',
  type: '',
  category: '',
  amount: 0,
  date: new Date().toISOString().split('T')[0]
})

// Mock data
const mockTransactions = ref([
  {
    id: 1,
    date: '2024-01-15',
    description: 'Pagamento do cliente ABC',
    project: 'Projeto Website',
    category: 'projeto',
    type: 'receita',
    amount: 15000
  },
  {
    id: 2,
    date: '2024-01-14',
    description: 'Compra de equipamentos',
    project: 'Infraestrutura',
    category: 'operacional',
    type: 'despesa',
    amount: 5000
  },
  {
    id: 3,
    date: '2024-01-13',
    description: 'Campanha Google Ads',
    project: 'Marketing Digital',
    category: 'marketing',
    type: 'despesa',
    amount: 2500
  },
  {
    id: 4,
    date: '2024-01-12',
    description: 'Salários da equipe',
    project: 'Folha de pagamento',
    category: 'rh',
    type: 'despesa',
    amount: 25000
  }
])

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pt-BR')
}

const createTransaction = async () => {
  try {
    creating.value = true
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const newTransaction = {
      id: mockTransactions.value.length + 1,
      ...transactionForm.value,
      project: 'Novo Projeto'
    }
    
    mockTransactions.value.unshift(newTransaction)
    showCreateModal.value = false
    
    // Reset form
    transactionForm.value = {
      description: '',
      type: '',
      category: '',
      amount: 0,
      date: new Date().toISOString().split('T')[0]
    }
  } catch (error) {
    console.error('Erro ao criar transação:', error)
  } finally {
    creating.value = false
  }
}
</script>
