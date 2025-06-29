<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'

const emit = defineEmits(['close', 'success', 'switch-to-login'])

// Usar o composable de autenticação
const { register, isRegistering } = useAuth()

// State
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const form = ref({
  username: '',
  email: '',
  firstName: '',
  lastName: '',
  password: '',
  confirmPassword: '',
  role: 'USER',
  acceptTerms: false,
  profile: {
    cargo: '',
    departamento: '',
    telefone: '',
    preferencias: {
      notificacoes_email: true,
      notificacoes_push: true,
      tema_escuro: false
    }
  }
})

// Computed
const isFormValid = computed(() => {
  return form.value.username &&
         form.value.email &&
         form.value.firstName &&
         form.value.lastName &&
         form.value.password &&
         form.value.password === form.value.confirmPassword &&
         form.value.acceptTerms
})

// Methods
const handleRegister = async () => {
  if (!isFormValid.value) return
  
  const registerData = {
    username: form.value.username,
    email: form.value.email,
    first_name: form.value.firstName,
    last_name: form.value.lastName,
    password: form.value.password,
    role: form.value.role
  }

  try {
    await register(registerData)
    emit('success')
  } catch (error) {
    // Erro já tratado no composable useAuth
    console.error('Registration failed:', error)
  }
}

const switchToLogin = () => {
  emit('close')
  nextTick(() => {
    emit('switch-to-login')
  })
}
</script>