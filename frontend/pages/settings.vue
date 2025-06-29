<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-6 py-4 border-b border-gray-200">
          <h1 class="text-2xl font-bold text-gray-900">Configurações</h1>
          <p class="text-gray-600 mt-1">Gerencie suas preferências e configurações do sistema</p>
        </div>
      </div>

      <!-- Settings Content -->
      <div class="space-y-6">
        <!-- Account Settings -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Configurações da Conta</h2>
          </div>
          <div class="p-6 space-y-6">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-sm font-medium text-gray-900">Notificações por Email</h3>
                <p class="text-sm text-gray-500">Receba notificações sobre atividades importantes</p>
              </div>
              <button @click="toggleEmailNotifications" 
                      :class="[
                        'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2',
                        emailNotifications ? 'bg-primary' : 'bg-gray-200'
                      ]">
                <span :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  emailNotifications ? 'translate-x-5' : 'translate-x-0'
                ]"></span>
              </button>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-sm font-medium text-gray-900">Notificações Push</h3>
                <p class="text-sm text-gray-500">Receba notificações no navegador</p>
              </div>
              <button @click="togglePushNotifications" 
                      :class="[
                        'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2',
                        pushNotifications ? 'bg-primary' : 'bg-gray-200'
                      ]">
                <span :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  pushNotifications ? 'translate-x-5' : 'translate-x-0'
                ]"></span>
              </button>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-sm font-medium text-gray-900">Modo Escuro</h3>
                <p class="text-sm text-gray-500">Ativar tema escuro da interface</p>
              </div>
              <button @click="toggleDarkMode" 
                      :class="[
                        'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2',
                        darkMode ? 'bg-primary' : 'bg-gray-200'
                      ]">
                <span :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  darkMode ? 'translate-x-5' : 'translate-x-0'
                ]"></span>
              </button>
            </div>
          </div>
        </div>

        <!-- Privacy Settings -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Privacidade</h2>
          </div>
          <div class="p-6 space-y-6">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-sm font-medium text-gray-900">Perfil Público</h3>
                <p class="text-sm text-gray-500">Permitir que outros usuários vejam seu perfil</p>
              </div>
              <button @click="togglePublicProfile" 
                      :class="[
                        'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2',
                        publicProfile ? 'bg-primary' : 'bg-gray-200'
                      ]">
                <span :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  publicProfile ? 'translate-x-5' : 'translate-x-0'
                ]"></span>
              </button>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-sm font-medium text-gray-900">Mostrar Status Online</h3>
                <p class="text-sm text-gray-500">Exibir quando você está online para outros usuários</p>
              </div>
              <button @click="toggleOnlineStatus" 
                      :class="[
                        'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2',
                        onlineStatus ? 'bg-primary' : 'bg-gray-200'
                      ]">
                <span :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  onlineStatus ? 'translate-x-5' : 'translate-x-0'
                ]"></span>
              </button>
            </div>
          </div>
        </div>

        <!-- Security Settings -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Segurança</h2>
          </div>
          <div class="p-6 space-y-6">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-sm font-medium text-gray-900">Alterar Senha</h3>
                <p class="text-sm text-gray-500">Atualize sua senha regularmente para maior segurança</p>
              </div>
              <button @click="showPasswordModal = true" 
                      class="bg-primary text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors">
                Alterar
              </button>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-sm font-medium text-gray-900">Autenticação de Dois Fatores</h3>
                <p class="text-sm text-gray-500">Adicione uma camada extra de segurança à sua conta</p>
              </div>
              <button @click="toggle2FA" 
                      :class="[
                        'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2',
                        twoFactorAuth ? 'bg-primary' : 'bg-gray-200'
                      ]">
                <span :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  twoFactorAuth ? 'translate-x-5' : 'translate-x-0'
                ]"></span>
              </button>
            </div>
          </div>
        </div>

        <!-- Save Button -->
        <div class="flex justify-end">
          <button @click="saveSettings" :disabled="saving"
                  class="bg-primary text-white px-6 py-2 rounded-md hover:bg-primary-700 transition-colors disabled:opacity-50">
            <span v-if="saving" class="inline-block mr-2">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            </span>
            Salvar Configurações
          </button>
        </div>
      </div>
    </div>

    <!-- Password Change Modal -->
    <div v-if="showPasswordModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Alterar Senha</h3>
          <form @submit.prevent="changePassword" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Senha Atual</label>
              <input v-model="passwordForm.currentPassword" type="password" required
                     class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Nova Senha</label>
              <input v-model="passwordForm.newPassword" type="password" required
                     class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Confirmar Nova Senha</label>
              <input v-model="passwordForm.confirmPassword" type="password" required
                     class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary focus:border-primary">
            </div>
            <div class="flex justify-end space-x-3 pt-4">
              <button @click="showPasswordModal = false" type="button" 
                      class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md">
                Cancelar
              </button>
              <button type="submit" :disabled="changingPassword"
                      class="px-4 py-2 text-sm font-medium text-white bg-primary hover:bg-primary-700 rounded-md disabled:opacity-50">
                <span v-if="changingPassword" class="inline-block mr-2">
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                </span>
                Alterar Senha
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

// Settings state
const emailNotifications = ref(true)
const pushNotifications = ref(false)
const darkMode = ref(false)
const publicProfile = ref(true)
const onlineStatus = ref(true)
const twoFactorAuth = ref(false)
const saving = ref(false)

// Password modal
const showPasswordModal = ref(false)
const changingPassword = ref(false)
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// Toggle functions
const toggleEmailNotifications = () => {
  emailNotifications.value = !emailNotifications.value
}

const togglePushNotifications = () => {
  pushNotifications.value = !pushNotifications.value
}

const toggleDarkMode = () => {
  darkMode.value = !darkMode.value
}

const togglePublicProfile = () => {
  publicProfile.value = !publicProfile.value
}

const toggleOnlineStatus = () => {
  onlineStatus.value = !onlineStatus.value
}

const toggle2FA = () => {
  twoFactorAuth.value = !twoFactorAuth.value
}

const saveSettings = async () => {
  try {
    saving.value = true
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('Configurações salvas:', {
      emailNotifications: emailNotifications.value,
      pushNotifications: pushNotifications.value,
      darkMode: darkMode.value,
      publicProfile: publicProfile.value,
      onlineStatus: onlineStatus.value,
      twoFactorAuth: twoFactorAuth.value
    })
  } catch (error) {
    console.error('Erro ao salvar configurações:', error)
  } finally {
    saving.value = false
  }
}

const changePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    alert('As senhas não coincidem')
    return
  }

  try {
    changingPassword.value = true
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('Senha alterada com sucesso')
    showPasswordModal.value = false
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (error) {
    console.error('Erro ao alterar senha:', error)
  } finally {
    changingPassword.value = false
  }
}
</script>
