<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-6 py-4 border-b border-gray-200">
          <h1 class="text-2xl font-bold text-gray-900">Meu Perfil</h1>
          <p class="text-gray-600 mt-1">Gerencie suas informações pessoais e preferências</p>
        </div>
      </div>

      <!-- Profile Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Profile Info -->
        <div class="lg:col-span-2">
          <div class="bg-white shadow rounded-lg">
            <div class="px-6 py-4 border-b border-gray-200">
              <h2 class="text-lg font-medium text-gray-900">Informações Pessoais</h2>
            </div>
            <div class="p-6">
              <div v-if="loading" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
              <div v-else-if="user" class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Nome</label>
                    <p class="mt-1 text-sm text-gray-900">{{ user.first_name }} {{ user.last_name }}</p>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Email</label>
                    <p class="mt-1 text-sm text-gray-900">{{ user.email }}</p>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Usuário</label>
                    <p class="mt-1 text-sm text-gray-900">{{ user.username }}</p>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Status</label>
                    <span class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                          :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                      {{ user.is_active ? 'Ativo' : 'Inativo' }}
                    </span>
                  </div>
                </div>
                <div class="pt-4">
                  <button @click="showEditModal = true" 
                          class="bg-primary text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors">
                    Editar Perfil
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Profile Picture & Quick Stats -->
        <div class="space-y-6">
          <div class="bg-white shadow rounded-lg p-6">
            <div class="text-center">
              <div class="mx-auto h-24 w-24 rounded-full bg-gray-300 flex items-center justify-center">
                <Icon icon="lucide:user" class="h-12 w-12 text-gray-600" />
              </div>
              <h3 class="mt-4 text-lg font-medium text-gray-900">
                {{ user?.first_name }} {{ user?.last_name }}
              </h3>
              <p class="text-gray-600">{{ user?.email }}</p>
            </div>
          </div>

          <div class="bg-white shadow rounded-lg p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Estatísticas</h3>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600">Projetos</span>
                <span class="font-medium">-</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Tarefas</span>
                <span class="font-medium">-</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Equipes</span>
                <span class="font-medium">-</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Editar Perfil</h3>
          <form @submit.prevent="updateProfile" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Nome</label>
              <input v-model="editForm.first_name" type="text" 
                     class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Sobrenome</label>
              <input v-model="editForm.last_name" type="text" 
                     class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input v-model="editForm.email" type="email" 
                     class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
            </div>
            <div class="flex justify-end space-x-3 pt-4">
              <button @click="showEditModal = false" type="button" 
                      class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md">
                Cancelar
              </button>
              <button type="submit" :disabled="updateLoading"
                      class="px-4 py-2 text-sm font-medium text-white bg-primary hover:bg-primary-700 rounded-md disabled:opacity-50">
                <span v-if="updateLoading" class="inline-block mr-2">
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                </span>
                Salvar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { userService } from '~/services/userService'

definePageMeta({
  middleware: 'auth'
})

const { user: authUser } = useAuth()
const user = ref(null)
const loading = ref(true)
const showEditModal = ref(false)
const updateLoading = ref(false)

const editForm = ref({
  first_name: '',
  last_name: '',
  email: ''
})

const loadProfile = async () => {
  try {
    loading.value = true
    if (authUser.value?.id) {
      const response = await userService.getUser(authUser.value.id)
      user.value = response
      editForm.value = {
        first_name: response.first_name || '',
        last_name: response.last_name || '',
        email: response.email || ''
      }
    }
  } catch (error) {
    console.error('Erro ao carregar perfil:', error)
  } finally {
    loading.value = false
  }
}

const updateProfile = async () => {
  try {
    updateLoading.value = true
    if (authUser.value?.id) {
      await userService.patchUser(authUser.value.id, editForm.value)
      await loadProfile()
      showEditModal.value = false
    }
  } catch (error) {
    console.error('Erro ao atualizar perfil:', error)
  } finally {
    updateLoading.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>
