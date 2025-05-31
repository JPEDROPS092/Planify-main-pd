<template>
  <div class="container mx-auto p-4 md:p-6">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <SkeletonLoader type="article" :count="1" />
    </div>
    <div v-else-if="error" class="text-center text-red-500 dark:text-red-400 py-10">
      <h2 class="text-2xl font-semibold mb-2">Erro ao Carregar Projeto</h2>
      <p>{{ error.message || 'Não foi possível carregar os detalhes do projeto.' }}</p>
      <Button class="mt-4" @click="fetchProject">Tentar Novamente</Button>
    </div>
    <div v-else class="space-y-6">
      <!-- Cabeçalho da Página -->
      <div class="flex items-center mb-6">
        <Button variant="ghost" size="sm" @click="navigateBack" class="mr-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
          </svg>
        </Button>
        <h1 class="text-2xl font-bold text-gray-800 dark:text-white">Editar Projeto</h1>
      </div>

      <!-- Formulário de Edição -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <form @submit.prevent="updateProject" class="space-y-6">
          <!-- Informações Básicas -->
          <div class="space-y-4">
            <h2 class="text-lg font-medium text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700 pb-2">
              Informações Básicas
            </h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="titulo" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Título do Projeto
                </label>
                <input
                  id="titulo"
                  v-model="projectForm.titulo"
                  type="text"
                  required
                  class="w-full rounded-md border border-gray-300 dark:border-gray-600 px-3 py-2 text-gray-900 dark:text-gray-100 dark:bg-gray-700 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  placeholder="Digite o título do projeto"
                />
              </div>
              
              <div>
                <label for="status" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Status
                </label>
                <select
                  id="status"
                  v-model="projectForm.status"
                  required
                  class="w-full rounded-md border border-gray-300 dark:border-gray-600 px-3 py-2 text-gray-900 dark:text-gray-100 dark:bg-gray-700 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="PLANEJADO">Planejado</option>
                  <option value="EM_ANDAMENTO">Em Andamento</option>
                  <option value="PAUSADO">Pausado</option>
                  <option value="CONCLUIDO">Concluído</option>
                  <option value="CANCELADO">Cancelado</option>
                </select>
              </div>
              
              <div>
                <label for="data_inicio" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Data de Início
                </label>
                <input
                  id="data_inicio"
                  v-model="projectForm.data_inicio"
                  type="date"
                  required
                  class="w-full rounded-md border border-gray-300 dark:border-gray-600 px-3 py-2 text-gray-900 dark:text-gray-100 dark:bg-gray-700 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label for="data_fim" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Data de Término (Previsão)
                </label>
                <input
                  id="data_fim"
                  v-model="projectForm.data_fim"
                  type="date"
                  class="w-full rounded-md border border-gray-300 dark:border-gray-600 px-3 py-2 text-gray-900 dark:text-gray-100 dark:bg-gray-700 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label for="prioridade" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Prioridade
                </label>
                <select
                  id="prioridade"
                  v-model="projectForm.prioridade"
                  required
                  class="w-full rounded-md border border-gray-300 dark:border-gray-600 px-3 py-2 text-gray-900 dark:text-gray-100 dark:bg-gray-700 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="BAIXA">Baixa</option>
                  <option value="MEDIA">Média</option>
                  <option value="ALTA">Alta</option>
                  <option value="CRITICA">Crítica</option>
                </select>
              </div>
              
              <div>
                <label for="gerente" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Gerente do Projeto
                </label>
                <select
                  id="gerente"
                  v-model="projectForm.gerente"
                  required
                  class="w-full rounded-md border border-gray-300 dark:border-gray-600 px-3 py-2 text-gray-900 dark:text-gray-100 dark:bg-gray-700 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option v-for="user in users" :key="user.id" :value="user.id">
                    {{ user.first_name ? `${user.first_name} ${user.last_name}` : user.username }}
                  </option>
                </select>
              </div>
            </div>
            
            <div>
              <label for="descricao" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Descrição
              </label>
              <textarea
                id="descricao"
                v-model="projectForm.descricao"
                rows="4"
                class="w-full rounded-md border border-gray-300 dark:border-gray-600 px-3 py-2 text-gray-900 dark:text-gray-100 dark:bg-gray-700 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                placeholder="Descreva o projeto..."
              ></textarea>
            </div>
          </div>
          
          <!-- Configurações Adicionais -->
          <div class="space-y-4">
            <h2 class="text-lg font-medium text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700 pb-2">
              Configurações Adicionais
            </h2>
            
            <div class="flex items-center">
              <input
                id="arquivado"
                v-model="projectForm.arquivado"
                type="checkbox"
                class="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
              />
              <label for="arquivado" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                Arquivar projeto
              </label>
            </div>
            
            <p class="text-xs text-gray-500 dark:text-gray-400">
              Projetos arquivados não aparecem na lista principal, mas podem ser acessados através dos filtros.
            </p>
          </div>
          
          <!-- Botões de Ação -->
          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
            <Button variant="outline" type="button" @click="navigateBack">
              Cancelar
            </Button>
            <Button type="submit" :loading="saving">
              {{ saving ? 'Salvando...' : 'Salvar Alterações' }}
            </Button>
          </div>
        </form>
      </div>
      
      <!-- Seção de Perigo -->
      <div class="bg-red-50 dark:bg-red-900/20 rounded-lg p-6 border border-red-200 dark:border-red-800">
        <h2 class="text-lg font-medium text-red-800 dark:text-red-300 mb-3">
          Zona de Perigo
        </h2>
        <p class="text-sm text-red-600 dark:text-red-400 mb-4">
          As ações abaixo não podem ser desfeitas. Tenha certeza antes de prosseguir.
        </p>
        <Button 
          variant="destructive" 
          @click="confirmDeleteProject"
          :loading="deleting"
        >
          {{ deleting ? 'Excluindo...' : 'Excluir Projeto' }}
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectService } from '~/services/api/projects'
import { useNotification } from '~/composables/useNotification'
import Button from '~/components/ui/Button.vue'
import SkeletonLoader from '~/components/SkeletonLoader.vue'

definePageMeta({
  layout: 'dashboard',
  middleware: ['auth']
})

const route = useRoute()
const router = useRouter()
const projectService = useProjectService()
const { success: notifySuccess, error: notifyError, showApiError, confirm } = useNotification()

// Estado
const projectId = computed(() => Number(route.params.id))
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const error = ref<Error | null>(null)
const users = ref<any[]>([])

// Formulário
const projectForm = ref({
  titulo: '',
  descricao: '',
  data_inicio: '',
  data_fim: '',
  status: 'PLANEJADO',
  prioridade: 'MEDIA',
  gerente: 0,
  arquivado: false
})

// Métodos
async function fetchProject() {
  if (!projectId.value) return
  
  loading.value = true
  error.value = null
  
  try {
    // Buscar usuários para o select de gerente
    const usersResponse = await fetch('/api/users/usuarios/')
    users.value = await usersResponse.json()
    
    // Buscar dados do projeto
    const project = await projectService.retrieveProjeto(projectId.value)
    
    // Preencher formulário
    projectForm.value = {
      titulo: project.titulo || '',
      descricao: project.descricao || '',
      data_inicio: project.data_inicio ? new Date(project.data_inicio).toISOString().split('T')[0] : '',
      data_fim: project.data_fim ? new Date(project.data_fim).toISOString().split('T')[0] : '',
      status: project.status || 'PLANEJADO',
      prioridade: project.prioridade || 'MEDIA',
      gerente: project.gerente || 0,
      arquivado: project.arquivado || false
    }
  } catch (err: any) {
    error.value = err
    showApiError(err)
  } finally {
    loading.value = false
  }
}

async function updateProject() {
  saving.value = true
  
  try {
    await projectService.updateProjeto(projectId.value, {
      titulo: projectForm.value.titulo,
      descricao: projectForm.value.descricao,
      data_inicio: projectForm.value.data_inicio,
      data_fim: projectForm.value.data_fim || null,
      status: projectForm.value.status,
      prioridade: projectForm.value.prioridade,
      gerente: projectForm.value.gerente
    })
    
    // Se o projeto foi arquivado/desarquivado, atualizar esse status
    await projectService.archiveProjeto(projectId.value, {
      arquivado: projectForm.value.arquivado
    })
    
    notifySuccess('Projeto atualizado com sucesso!')
    navigateBack()
  } catch (err: any) {
    showApiError(err)
  } finally {
    saving.value = false
  }
}

function navigateBack() {
  router.push(`/projetos/${projectId.value}`)
}

async function confirmDeleteProject() {
  const confirmed = await confirm(
    'Excluir Projeto',
    'Tem certeza que deseja excluir este projeto? Esta ação não pode ser desfeita e todas as tarefas, sprints e dados relacionados serão perdidos.',
    'Excluir',
    'Cancelar'
  )
  
  if (confirmed) {
    deleting.value = true
    
    try {
      await projectService.destroyProjeto(projectId.value)
      notifySuccess('Projeto excluído com sucesso!')
      router.push('/projetos')
    } catch (err: any) {
      showApiError(err)
    } finally {
      deleting.value = false
    }
  }
}

// Inicialização
onMounted(() => {
  fetchProject()
})
</script>
