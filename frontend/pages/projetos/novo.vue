<template>
  <div class="container mx-auto p-4 md:p-6">
    <div class="space-y-6">
      <!-- Cabeçalho da Página -->
      <div class="flex items-center mb-6">
        <Button variant="ghost" size="sm" @click="navigateBack" class="mr-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
              clip-rule="evenodd"
            />
          </svg>
        </Button>
        <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
          Novo Projeto
        </h1>
      </div>

      <!-- Formulário de Criação -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <form @submit.prevent="createProject" class="space-y-6">
          <!-- Informações Básicas -->
          <div class="space-y-4">
            <h2
              class="text-lg font-medium text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700 pb-2"
            >
              Informações Básicas
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label
                  for="titulo"
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
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
                <label
                  for="status"
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
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
                </select>
              </div>

              <div>
                <label
                  for="data_inicio"
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
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
                <label
                  for="data_fim"
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
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
                <label
                  for="prioridade"
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
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
                <label
                  for="gerente"
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
                >
                  Gerente do Projeto
                </label>
                <select
                  id="gerente"
                  v-model="projectForm.gerente"
                  required
                  class="w-full rounded-md border border-gray-300 dark:border-gray-600 px-3 py-2 text-gray-900 dark:text-gray-100 dark:bg-gray-700 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option v-for="user in users" :key="user.id" :value="user.id">
                    {{
                      user.first_name
                        ? `${user.first_name} ${user.last_name}`
                        : user.username
                    }}
                  </option>
                </select>
              </div>
            </div>

            <div>
              <label
                for="descricao"
                class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
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

          <!-- Botões de Ação -->
          <div
            class="flex justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700"
          >
            <Button variant="outline" type="button" @click="navigateBack">
              Cancelar
            </Button>
            <Button type="submit" :loading="saving">
              {{ saving ? 'Criando...' : 'Criar Projeto' }}
            </Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useProjectService } from '~/services/api/services/projectService';
import { useAuth } from '~/composables/useAuth';
import { useNotification } from '~/composables/useNotification';
import Button from '~/components/ui/Button.vue';

definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'],
});

const router = useRouter();
const projectService = useProjectService();
const { user } = useAuth();
const {
  success: notifySuccess,
  error: notifyError,
  showApiError,
} = useNotification();

// Estado
const saving = ref(false);
const users = ref<any[]>([]);

// Formulário com valores padrão
const projectForm = ref({
  titulo: '',
  descricao: '',
  data_inicio: new Date().toISOString().split('T')[0], // Data atual como padrão
  data_fim: '',
  status: 'PLANEJADO',
  prioridade: 'MEDIA',
  gerente: 0,
});

// Métodos
async function fetchUsers() {
  try {
    const response = await fetch('/api/users/usuarios/');
    users.value = await response.json();

    // Se o usuário atual estiver na lista, defini-lo como gerente padrão
    if (user.value?.id) {
      projectForm.value.gerente = user.value.id;
    } else if (users.value.length > 0) {
      projectForm.value.gerente = users.value[0].id;
    }
  } catch (err: any) {
    showApiError(err, 'Erro ao carregar usuários');
  }
}

async function createProject() {
  saving.value = true;

  try {
    const newProject = await projectService.createProjeto({
      titulo: projectForm.value.titulo,
      descricao: projectForm.value.descricao,
      data_inicio: projectForm.value.data_inicio,
      data_fim: projectForm.value.data_fim || null,
      status: projectForm.value.status,
      prioridade: projectForm.value.prioridade,
      gerente: projectForm.value.gerente,
    });

    notifySuccess('Projeto criado com sucesso!');

    // Redirecionar para a página do novo projeto
    router.push(`/projetos/${newProject.id}`);
  } catch (err: any) {
    showApiError(err);
  } finally {
    saving.value = false;
  }
}

function navigateBack() {
  router.push('/projetos');
}

// Inicialização
onMounted(() => {
  fetchUsers();
});
</script>
