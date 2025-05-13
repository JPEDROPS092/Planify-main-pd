<template>
  <form @submit.prevent="submitForm" class_name="space-y-6">
    <div>
      <label for="risk-name" class_name="block text-sm font-medium text-gray-700 dark:text-gray-300">Nome do Risco</label>
      <input type="text" id="risk-name" v-model="form.name" required
             class_name="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white" />
      <span v-if="errors.name" class_name="text-xs text-red-500">{{ errors.name }}</span>
    </div>

    <div>
      <label for="risk-description" class_name="block text-sm font-medium text-gray-700 dark:text-gray-300">Descrição</label>
      <textarea id="risk-description" v-model="form.description" rows="3" required
                class_name="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"></textarea>
      <span v-if="errors.description" class_name="text-xs text-red-500">{{ errors.description }}</span>
    </div>

    <div class_name="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label for="risk-impact" class_name="block text-sm font-medium text-gray-700 dark:text-gray-300">Impacto</label>
        <select id="risk-impact" v-model="form.impact" required
                class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
          <option value="BAIXO">Baixo</option>
          <option value="MEDIO">Médio</option>
          <option value="ALTO">Alto</option>
        </select>
        <span v-if="errors.impact" class_name="text-xs text-red-500">{{ errors.impact }}</span>
      </div>
      <div>
        <label for="risk-probability" class_name="block text-sm font-medium text-gray-700 dark:text-gray-300">Probabilidade</label>
        <select id="risk-probability" v-model="form.probability" required
                class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
          <option value="BAIXA">Baixa</option>
          <option value="MEDIA">Média</option>
          <option value="ALTA">Alta</option>
        </select>
        <span v-if="errors.probability" class_name="text-xs text-red-500">{{ errors.probability }}</span>
      </div>
    </div>
    
    <div>
      <label for="risk-status" class_name="block text-sm font-medium text-gray-700 dark:text-gray-300">Status</label>
      <select id="risk-status" v-model="form.status" required
              class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
        <option value="IDENTIFICADO">Identificado</option>
        <option value="EM_ANDAMENTO">Em Andamento</option>
        <option value="MITIGADO">Mitigado</option>
        <option value="FECHADO">Fechado</option>
      </select>
      <span v-if="errors.status" class_name="text-xs text-red-500">{{ errors.status }}</span>
    </div>

    <div>
      <label for="risk-mitigation_plan" class_name="block text-sm font-medium text-gray-700 dark:text-gray-300">Plano de Mitigação</label>
      <textarea id="risk-mitigation_plan" v-model="form.mitigation_plan" rows="3"
                class_name="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"></textarea>
      <span v-if="errors.mitigation_plan" class_name="text-xs text-red-500">{{ errors.mitigation_plan }}</span>
    </div>

    <div>
      <label for="risk-assignee" class_name="block text-sm font-medium text-gray-700 dark:text-gray-300">Responsável (Opcional)</label>
      <select id="risk-assignee" v-model="form.assignee"
              class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
        <option :value="null">Ninguém atribuído</option>
        <option v-for="user in projectTeamMembers" :key="user.id" :value="user.id">
          {{ user.first_name }} {{ user.last_name }} (@{{ user.username }})
        </option>
      </select>
      <span v-if="errors.assignee" class_name="text-xs text-red-500">{{ errors.assignee }}</span>
    </div>

    <div class_name="flex justify-end space-x-3 pt-4">
      <Button type="button" variant="outline" @click="cancelForm">Cancelar</Button>
      <LoadingButton type="submit" :loading="isSubmitting" :disabled="!isFormValid || isSubmitting">
        {{ risk && risk.id ? 'Salvar Alterações' : 'Registrar Risco' }}
      </LoadingButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits, onMounted, computed } from 'vue'
import type { Risk, RiskCreate, RiskUpdate } from '~/services/riskService'
import { useUserService } from '~/services/userService' // Para buscar membros da equipe do projeto
import { useTeamService } from '~/services/teamService'
import type { User } from '~/services/userService'
import Button from '~/components/ui/Button.vue'
import LoadingButton from '~/components/LoadingButton.vue'

const props = defineProps({
  projectId: {
    type: Number,
    required: true
  },
  risk: {
    type: Object as () => Risk | null,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const userService = useUserService()
const teamService = useTeamService()

const initialFormState: RiskCreate | RiskUpdate = {
  name: '',
  description: '',
  impact: 'MEDIO',
  probability: 'MEDIA',
  status: 'IDENTIFICADO',
  mitigation_plan: '',
  assignee: null,
  project: props.projectId
}

const form = ref({ ...initialFormState })
const errors = ref<Partial<Record<keyof (RiskCreate | RiskUpdate), string>>>({})
const isSubmitting = ref(false)
const projectTeamMembers = ref<User[]>([])

const isFormValid = computed(() => {
  return form.value.name && form.value.description && form.value.impact && form.value.probability && form.value.status;
});

async function fetchProjectTeam() {
  if (!props.projectId) return;
  try {
    const members = await teamService.getTeamMembers(props.projectId);
    projectTeamMembers.value = members.map((tm: any) => tm.user || tm); // Ajustar conforme a estrutura de TeamMember
  } catch (error) {
    console.error("Erro ao buscar membros da equipe do projeto:", error);
    // Tratar erro opcionalmente (ex: notificação)
  }
}

watch(() => props.risk, (newRisk) => {
  if (newRisk) {
    form.value = {
      name: newRisk.name,
      description: newRisk.description,
      impact: newRisk.impact,
      probability: newRisk.probability,
      status: newRisk.status,
      mitigation_plan: newRisk.mitigation_plan || '',
      assignee: newRisk.assignee || null,
      project: newRisk.project || props.projectId
    }
    if (newRisk.id) {
      (form.value as RiskUpdate).id = newRisk.id;
    }
  } else {
    form.value = { ...initialFormState, project: props.projectId }
  }
  errors.value = {}
}, { immediate: true, deep: true })

function validateForm(): boolean {
  errors.value = {}
  let isValid = true
  if (!form.value.name.trim()) {
    errors.value.name = 'O nome do risco é obrigatório.'
    isValid = false
  }
  if (!form.value.description.trim()) {
    errors.value.description = 'A descrição é obrigatória.'
    isValid = false
  }
  // Adicione mais validações conforme necessário
  return isValid
}

async function submitForm() {
  if (!validateForm()) {
    return
  }
  isSubmitting.value = true
  try {
    emit('submit', { ...form.value })
    // O componente pai (ProjectRisks) lidará com a chamada de API e notificação
  } catch (error) {
    // Erros de submissão podem ser tratados aqui se necessário, mas geralmente são no pai
    console.error("Erro ao submeter formulário de risco:", error)
  } finally {
    isSubmitting.value = false
    // Não resetar o form aqui, o pai decide se fecha o modal e reseta
  }
}

function cancelForm() {
  emit('cancel')
}

onMounted(() => {
  fetchProjectTeam();
  if (!props.risk) { // Se não estiver editando, garanta que o ID do projeto está no form
     form.value.project = props.projectId;
  }
})

</script>
