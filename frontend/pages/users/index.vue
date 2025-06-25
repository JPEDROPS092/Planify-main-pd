<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center">
          <h1 class="text-3xl font-bold text-gray-900">Gerenciamento de Usuários</h1>
          <button
            @click="showCreateModal = true"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
          >
            <Icon name="heroicons:plus" class="w-5 h-5" />
            Novo Usuário
          </button>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <!-- Filters -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Buscar</label>
            <input
              v-model="filters.search"
              type="text"
              placeholder="Nome, email ou username..."
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Função</label>
            <select
              v-model="filters.role"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Todas</option>
              <option value="ADMIN">Administrador</option>
              <option value="MANAGER">Gerente</option>
              <option value="USER">Usuário</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select
              v-model="filters.status"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Todos</option>
              <option value="active">Ativo</option>
              <option value="inactive">Inativo</option>
            </select>
          </div>
          <div class="flex items-end">
            <button
              @click="loadUsers"
              class="w-full bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Filtrar
            </button>
          </div>
        </div>
      </div>

      <!-- Users Table -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div v-if="loading" class="p-8 text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">Carregando usuários...</p>
        </div>

        <div v-else-if="error" class="p-8 text-center">
          <Icon name="heroicons:exclamation-triangle" class="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p class="text-red-600 mb-4">{{ error }}</p>
          <button @click="loadUsers" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
            Tentar Novamente
          </button>
        </div>

        <div v-else>
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Usuário
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Email
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Função
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Data de Cadastro
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                      <img
                        v-if="user.profile?.profile_picture"
                        :src="user.profile.profile_picture"
                        :alt="user.full_name"
                        class="h-10 w-10 rounded-full object-cover"
                      />
                      <div
                        v-else
                        class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center"
                      >
                        <Icon name="heroicons:user" class="w-6 h-6 text-gray-600" />
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ user.full_name || user.username }}</div>
                      <div class="text-sm text-gray-500">@{{ user.username }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ user.email }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="{
                      'bg-red-100 text-red-800': user.role === 'ADMIN',
                      'bg-yellow-100 text-yellow-800': user.role === 'MANAGER',
                      'bg-green-100 text-green-800': user.role === 'USER'
                    }"
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  >
                    {{ getRoleLabel(user.role) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="{
                      'bg-green-100 text-green-800': user.is_active,
                      'bg-red-100 text-red-800': !user.is_active
                    }"
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  >
                    {{ user.is_active ? 'Ativo' : 'Inativo' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(user.date_joined) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex justify-end gap-2">
                    <button
                      @click="editUser(user)"
                      class="text-blue-600 hover:text-blue-900 transition-colors"
                      title="Editar"
                    >
                      <Icon name="heroicons:pencil" class="w-4 h-4" />
                    </button>
                    <button
                      v-if="user.is_active"
                      @click="deactivateUser(user)"
                      class="text-yellow-600 hover:text-yellow-900 transition-colors"
                      title="Desativar"
                    >
                      <Icon name="heroicons:pause" class="w-4 h-4" />
                    </button>
                    <button
                      v-else
                      @click="activateUser(user)"
                      class="text-green-600 hover:text-green-900 transition-colors"
                      title="Ativar"
                    >
                      <Icon name="heroicons:play" class="w-4 h-4" />
                    </button>
                    <button
                      @click="resetUserPassword(user)"
                      class="text-purple-600 hover:text-purple-900 transition-colors"
                      title="Redefinir Senha"
                    >
                      <Icon name="heroicons:key" class="w-4 h-4" />
                    </button>
                    <button
                      @click="deleteUser(user)"
                      class="text-red-600 hover:text-red-900 transition-colors"
                      title="Excluir"
                    >
                      <Icon name="heroicons:trash" class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div v-if="pagination.count > 0" class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
            <div class="flex-1 flex justify-between sm:hidden">
              <button
                @click="previousPage"
                :disabled="!pagination.previous"
                class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Anterior
              </button>
              <button
                @click="nextPage"
                :disabled="!pagination.next"
                class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Próximo
              </button>
            </div>
            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p class="text-sm text-gray-700">
                  Mostrando
                  <span class="font-medium">{{ (currentPage - 1) * 20 + 1 }}</span>
                  até
                  <span class="font-medium">{{ Math.min(currentPage * 20, pagination.count) }}</span>
                  de
                  <span class="font-medium">{{ pagination.count }}</span>
                  resultados
                </p>
              </div>
              <div>
                <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                  <button
                    @click="previousPage"
                    :disabled="!pagination.previous"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                  >
                    <Icon name="heroicons:chevron-left" class="w-5 h-5" />
                  </button>
                  <button
                    @click="nextPage"
                    :disabled="!pagination.next"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                  >
                    <Icon name="heroicons:chevron-right" class="w-5 h-5" />
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit User Modal -->
    <UserModal
      v-if="showCreateModal || showEditModal"
      :user="selectedUser"
      :is-edit="showEditModal"
      @close="closeModal"
      @saved="onUserSaved"
    />
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

const { $toast } = useNuxtApp()
const userService = useUserService()

// State
const loading = ref(false)
const error = ref('')
const users = ref([])
const pagination = ref({
  count: 0,
  next: null,
  previous: null
})
const currentPage = ref(1)

const showCreateModal = ref(false)
const showEditModal = ref(false)
const selectedUser = ref(null)

const filters = ref({
  search: '',
  role: '',
  status: ''
})

// Methods
const loadUsers = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const params: any = {
      page: currentPage.value
    }
    
    if (filters.value.search) {
      params.search = filters.value.search
    }
    if (filters.value.role) {
      params.role = filters.value.role
    }
    if (filters.value.status) {
      params.is_active = filters.value.status === 'active'
    }
    
    const response = await userService.getUsers(params)
    users.value = response.results
    pagination.value = {
      count: response.count,
      next: response.next,
      previous: response.previous
    }
  } catch (err: any) {
    error.value = err.message || 'Erro ao carregar usuários'
    $toast.error('Erro ao carregar usuários')
  } finally {
    loading.value = false
  }
}

const editUser = (user: any) => {
  selectedUser.value = { ...user }
  showEditModal.value = true
}

const activateUser = async (user: any) => {
  try {
    await userService.activateUser(user.id)
    $toast.success('Usuário ativado com sucesso')
    await loadUsers()
  } catch (err: any) {
    $toast.error('Erro ao ativar usuário')
  }
}

const deactivateUser = async (user: any) => {
  if (confirm('Tem certeza que deseja desativar este usuário?')) {
    try {
      await userService.deactivateUser(user.id)
      $toast.success('Usuário desativado com sucesso')
      await loadUsers()
    } catch (err: any) {
      $toast.error('Erro ao desativar usuário')
    }
  }
}

const resetUserPassword = async (user: any) => {
  if (confirm('Tem certeza que deseja redefinir a senha deste usuário?')) {
    try {
      await userService.resetPassword(user.id)
      $toast.success('Senha redefinida com sucesso')
    } catch (err: any) {
      $toast.error('Erro ao redefinir senha')
    }
  }
}

const deleteUser = async (user: any) => {
  if (confirm('Tem certeza que deseja excluir este usuário? Esta ação não pode ser desfeita.')) {
    try {
      await userService.deleteUser(user.id)
      $toast.success('Usuário excluído com sucesso')
      await loadUsers()
    } catch (err: any) {
      $toast.error('Erro ao excluir usuário')
    }
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  selectedUser.value = null
}

const onUserSaved = () => {
  closeModal()
  loadUsers()
}

const nextPage = () => {
  if (pagination.value.next) {
    currentPage.value++
    loadUsers()
  }
}

const previousPage = () => {
  if (pagination.value.previous) {
    currentPage.value--
    loadUsers()
  }
}

const getRoleLabel = (role: string) => {
  const labels = {
    ADMIN: 'Administrador',
    MANAGER: 'Gerente',
    USER: 'Usuário'
  }
  return labels[role] || role
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('pt-BR')
}

// Watchers
watch(filters, () => {
  currentPage.value = 1
  loadUsers()
}, { deep: true })

// Load data on mount
onMounted(() => {
  loadUsers()
})
</script>
