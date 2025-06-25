<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
      <div class="mt-3">
        <!-- Header -->
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-medium text-gray-900">
            {{ isEdit ? 'Editar Usuário' : 'Novo Usuário' }}
          </h3>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <Icon name="heroicons:x-mark" class="w-6 h-6" />
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="saveUser" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Username -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Username *
              </label>
              <input
                v-model="form.username"
                type="text"
                required
                :disabled="isEdit"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                placeholder="Digite o username"
              />
            </div>

            <!-- Email -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Email *
              </label>
              <input
                v-model="form.email"
                type="email"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Digite o email"
              />
            </div>

            <!-- Full Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Nome Completo *
              </label>
              <input
                v-model="form.full_name"
                type="text"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Digite o nome completo"
              />
            </div>

            <!-- Role -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Função *
              </label>
              <select
                v-model="form.role"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Selecione uma função</option>
                <option value="ADMIN">Administrador</option>
                <option value="MANAGER">Gerente</option>
                <option value="USER">Usuário</option>
              </select>
            </div>

            <!-- Password (only for new users) -->
            <div v-if="!isEdit">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Senha *
              </label>
              <input
                v-model="form.password"
                type="password"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Digite a senha"
              />
            </div>

            <!-- Phone -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Telefone
              </label>
              <input
                v-model="form.profile.phone"
                type="tel"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Digite o telefone"
              />
            </div>
          </div>

          <!-- Profile Settings -->
          <div class="border-t pt-6">
            <h4 class="text-md font-medium text-gray-900 mb-4">Configurações do Perfil</h4>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Theme Preference -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Tema Preferido
                </label>
                <select
                  v-model="form.profile.theme_preference"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="LIGHT">Claro</option>
                  <option value="DARK">Escuro</option>
                  <option value="AUTO">Automático</option>
                </select>
              </div>

              <!-- Status (only for edit) -->
              <div v-if="isEdit">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Status
                </label>
                <select
                  v-model="form.is_active"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option :value="true">Ativo</option>
                  <option :value="false">Inativo</option>
                </select>
              </div>
            </div>

            <!-- Notifications -->
            <div class="mt-6">
              <h5 class="text-sm font-medium text-gray-900 mb-3">Notificações</h5>
              <div class="space-y-3">
                <div class="flex items-center">
                  <input
                    v-model="form.profile.email_notifications"
                    type="checkbox"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label class="ml-2 block text-sm text-gray-700">
                    Notificações por email
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    v-model="form.profile.system_notifications"
                    type="checkbox"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label class="ml-2 block text-sm text-gray-700">
                    Notificações do sistema
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end gap-3 pt-6 border-t">
            <button
              type="button"
              @click="$emit('close')"
              class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              <div v-if="loading" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              {{ isEdit ? 'Atualizar' : 'Criar' }} Usuário
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  user?: any
  isEdit?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  user: null,
  isEdit: false
})

const emit = defineEmits(['close', 'saved'])

const { $toast } = useNuxtApp()
const userService = useUserService()

// State
const loading = ref(false)

const form = ref({
  username: '',
  email: '',
  full_name: '',
  role: '',
  password: '',
  is_active: true,
  profile: {
    phone: '',
    profile_picture: '',
    theme_preference: 'LIGHT',
    email_notifications: true,
    system_notifications: true
  }
})

// Methods
const saveUser = async () => {
  try {
    loading.value = true
    
    if (props.isEdit) {
      await userService.updateUser(props.user.id, form.value)
      $toast.success('Usuário atualizado com sucesso')
    } else {
      await userService.createUser(form.value)
      $toast.success('Usuário criado com sucesso')
    }
    
    emit('saved')
  } catch (err: any) {
    const message = props.isEdit ? 'Erro ao atualizar usuário' : 'Erro ao criar usuário'
    $toast.error(message)
    console.error('Error saving user:', err)
  } finally {
    loading.value = false
  }
}

// Initialize form
const initializeForm = () => {
  if (props.isEdit && props.user) {
    form.value = {
      username: props.user.username || '',
      email: props.user.email || '',
      full_name: props.user.full_name || '',
      role: props.user.role || '',
      password: '',
      is_active: props.user.is_active ?? true,
      profile: {
        phone: props.user.profile?.phone || '',
        profile_picture: props.user.profile?.profile_picture || '',
        theme_preference: props.user.profile?.theme_preference || 'LIGHT',
        email_notifications: props.user.profile?.email_notifications ?? true,
        system_notifications: props.user.profile?.system_notifications ?? true
      }
    }
  } else {
    // Reset form for new user
    form.value = {
      username: '',
      email: '',
      full_name: '',
      role: '',
      password: '',
      is_active: true,
      profile: {
        phone: '',
        profile_picture: '',
        theme_preference: 'LIGHT',
        email_notifications: true,
        system_notifications: true
      }
    }
  }
}

// Watch for prop changes
watch(() => props.user, initializeForm, { immediate: true })

onMounted(() => {
  initializeForm()
})
</script>
