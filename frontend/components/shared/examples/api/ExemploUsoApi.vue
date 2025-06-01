<!-- Exemplo de uso dos serviços da API gerados -->
<template>
  <div class="exemplo-uso-api">
    <h2 class="text-xl font-bold mb-4">Exemplo de Uso da API</h2>

    <!-- Exemplo de autenticação -->
    <div v-if="!isAuthenticated" class="mb-6 p-4 border rounded-lg">
      <h3 class="text-lg font-semibold mb-2">Login</h3>
      <form @submit.prevent="handleLogin" class="space-y-3">
        <div>
          <label class="block text-sm mb-1">Usuário</label>
          <input
            v-model="loginForm.username"
            type="text"
            class="w-full px-3 py-2 border rounded"
            placeholder="Nome de usuário"
            required
          />
        </div>
        <div>
          <label class="block text-sm mb-1">Senha</label>
          <input
            v-model="loginForm.password"
            type="password"
            class="w-full px-3 py-2 border rounded"
            placeholder="Senha"
            required
          />
        </div>
        <div>
          <button
            type="submit"
            class="px-4 py-2 bg-blue-600 text-white rounded"
            :disabled="isLoading"
          >
            <span v-if="isLoading">Carregando...</span>
            <span v-else>Entrar</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Exemplo de listagem de projetos -->
    <div v-if="isAuthenticated" class="mb-6 p-4 border rounded-lg">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Projetos</h3>
        <button
          @click="loadProjetos"
          class="px-3 py-1 bg-gray-200 rounded text-sm"
          :disabled="isLoadingProjetos"
        >
          <span v-if="isLoadingProjetos">Carregando...</span>
          <span v-else>Atualizar</span>
        </button>
      </div>

      <div v-if="isLoadingProjetos" class="py-4 text-center text-gray-500">
        Carregando projetos...
      </div>

      <div
        v-else-if="projetos.length === 0"
        class="py-4 text-center text-gray-500"
      >
        Nenhum projeto encontrado.
      </div>

      <ul v-else class="space-y-2">
        <li
          v-for="projeto in projetos"
          :key="projeto.id"
          class="p-3 border rounded hover:bg-gray-50"
        >
          <div class="flex justify-between">
            <div>
              <h4 class="font-medium">{{ projeto.nome }}</h4>
              <p class="text-sm text-gray-600">
                {{ projeto.descricao || 'Sem descrição' }}
              </p>
              <div class="mt-1 flex items-center text-xs text-gray-500">
                <span class="mr-2">Status: {{ projeto.status_display }}</span>
                <span>Progresso: {{ projeto.progresso }}%</span>
              </div>
            </div>
            <div class="flex space-x-2">
              <button
                @click="viewProjeto(projeto.id)"
                class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs"
              >
                Detalhes
              </button>
              <button
                @click="deleteProjeto(projeto.id)"
                class="px-2 py-1 bg-red-100 text-red-700 rounded text-xs"
              >
                Excluir
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Exemplo de criação de projeto -->
    <div v-if="isAuthenticated" class="mb-6 p-4 border rounded-lg">
      <h3 class="text-lg font-semibold mb-2">Novo Projeto</h3>
      <form @submit.prevent="createNewProjeto" class="space-y-3">
        <div>
          <label class="block text-sm mb-1">Nome</label>
          <input
            v-model="newProjeto.nome"
            type="text"
            class="w-full px-3 py-2 border rounded"
            placeholder="Nome do projeto"
            required
          />
        </div>
        <div>
          <label class="block text-sm mb-1">Descrição</label>
          <textarea
            v-model="newProjeto.descricao"
            class="w-full px-3 py-2 border rounded"
            placeholder="Descrição do projeto"
            rows="3"
          ></textarea>
        </div>
        <div>
          <label class="block text-sm mb-1">Data de Início</label>
          <input
            v-model="newProjeto.data_inicio"
            type="date"
            class="w-full px-3 py-2 border rounded"
            required
          />
        </div>
        <div>
          <label class="block text-sm mb-1">Status</label>
          <select
            v-model="newProjeto.status"
            class="w-full px-3 py-2 border rounded"
            required
          >
            <option value="PENDENTE">Pendente</option>
            <option value="EM_ANDAMENTO">Em Andamento</option>
            <option value="CONCLUIDO">Concluído</option>
            <option value="BLOQUEADO">Bloqueado</option>
            <option value="CANCELADO">Cancelado</option>
          </select>
        </div>
        <div>
          <button
            type="submit"
            class="px-4 py-2 bg-green-600 text-white rounded"
            :disabled="isCreatingProjeto"
          >
            <span v-if="isCreatingProjeto">Criando...</span>
            <span v-else>Criar Projeto</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Exemplo de perfil do usuário -->
    <div v-if="isAuthenticated && currentUser" class="p-4 border rounded-lg">
      <h3 class="text-lg font-semibold mb-2">Perfil do Usuário</h3>
      <div class="space-y-2">
        <p><strong>Nome:</strong> {{ currentUser.full_name }}</p>
        <p><strong>Email:</strong> {{ currentUser.email }}</p>
        <p><strong>Função:</strong> {{ currentUser.role }}</p>
        <p>
          <strong>Último login:</strong> {{ currentUser.last_login || 'N/A' }}
        </p>
      </div>
      <div class="mt-4">
        <button @click="logout" class="px-4 py-2 bg-red-600 text-white rounded">
          Sair
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import {
  useAuth,
  createProjeto,
  listProjetos,
  retrieveProjeto,
  destroyProjeto,
} from '~/services/api';
import { useApiService } from '~/composables/useApiService';
import type { ProjetoList, ProjetoRequest } from '~/services/api/types';

export default defineComponent({
  name: 'ExemploUsoApi',

  setup() {
    const auth = useAuth();
    const apiService = useApiService();

    // Estado de autenticação
    const isAuthenticated = computed(() => auth.isAuthenticated.value);
    const currentUser = computed(() => auth.user.value);
    const isLoading = ref(false);
    const loginForm = reactive({
      username: '',
      password: '',
    });

    // Estado de projetos
    const projetos = ref<ProjetoList[]>([]);
    const isLoadingProjetos = ref(false);
    const selectedProjetoId = ref<number | null>(null);
    const selectedProjeto = ref(null);

    // Estado de criação de projeto
    const isCreatingProjeto = ref(false);
    const newProjeto = reactive<Partial<ProjetoRequest>>({
      nome: '',
      descricao: '',
      data_inicio: new Date().toISOString().split('T')[0],
      status: 'PENDENTE',
      gerente: 0, // Será preenchido com o ID do usuário atual
    });

    // Função para fazer login
    const handleLogin = async () => {
      isLoading.value = true;
      try {
        await auth.login({
          username: loginForm.username,
          password: loginForm.password,
        });

        // Após login bem-sucedido, carregar projetos
        if (auth.isAuthenticated.value) {
          loadProjetos();
          // Atualizar o gerente do novo projeto com o ID do usuário atual
          if (auth.user.value) {
            newProjeto.gerente = auth.user.value.id;
          }
        }
      } catch (error) {
        console.error('Erro ao fazer login:', error);
      } finally {
        isLoading.value = false;
      }
    };

    // Função para fazer logout
    const logout = () => {
      auth.logout();
      projetos.value = [];
    };

    // Função para carregar projetos
    const loadProjetos = async () => {
      await apiService.withLoading(
        async () => {
          isLoadingProjetos.value = true;
          try {
            const response = await listProjetos({
              page: 1,
              ordering: '-data_criacao',
            });
            projetos.value = response.results;
          } finally {
            isLoadingProjetos.value = false;
          }
        },
        {
          loadingMessage: 'Carregando projetos...',
          successMessage: 'Projetos carregados com sucesso!',
          errorMessage: 'Erro ao carregar projetos.',
        }
      );
    };

    // Função para visualizar detalhes de um projeto
    const viewProjeto = async (id: number) => {
      selectedProjetoId.value = id;

      await apiService.withLoading(
        async () => {
          const projeto = await retrieveProjeto(id);
          selectedProjeto.value = projeto;
          alert(`Detalhes do projeto "${projeto.nome}" carregados!`);
        },
        {
          loadingMessage: 'Carregando detalhes do projeto...',
          successMessage: 'Detalhes do projeto carregados!',
          errorMessage: 'Erro ao carregar detalhes do projeto.',
        }
      );
    };

    // Função para excluir um projeto
    const deleteProjeto = async (id: number) => {
      if (!confirm('Tem certeza que deseja excluir este projeto?')) {
        return;
      }

      await apiService.withLoading(
        async () => {
          await destroyProjeto(id);
          // Remover o projeto da lista
          projetos.value = projetos.value.filter((p) => p.id !== id);
        },
        {
          loadingMessage: 'Excluindo projeto...',
          successMessage: 'Projeto excluído com sucesso!',
          errorMessage: 'Erro ao excluir projeto.',
        }
      );
    };

    // Função para criar um novo projeto
    const createNewProjeto = async () => {
      // Garantir que o gerente está definido
      if (!newProjeto.gerente && auth.user.value) {
        newProjeto.gerente = auth.user.value.id;
      }

      await apiService.withLoading(
        async () => {
          isCreatingProjeto.value = true;
          try {
            const projeto = await createProjeto(newProjeto as ProjetoRequest);
            // Adicionar o novo projeto à lista
            projetos.value = [projeto, ...projetos.value];
            // Limpar o formulário
            newProjeto.nome = '';
            newProjeto.descricao = '';
            newProjeto.data_inicio = new Date().toISOString().split('T')[0];
            newProjeto.status = 'PENDENTE';
          } finally {
            isCreatingProjeto.value = false;
          }
        },
        {
          loadingMessage: 'Criando projeto...',
          successMessage: 'Projeto criado com sucesso!',
          errorMessage: 'Erro ao criar projeto.',
        }
      );
    };

    // Carregar projetos se o usuário já estiver autenticado
    onMounted(() => {
      if (auth.isAuthenticated.value) {
        loadProjetos();
        // Atualizar o gerente do novo projeto com o ID do usuário atual
        if (auth.user.value) {
          newProjeto.gerente = auth.user.value.id;
        }
      }
    });

    return {
      // Estado de autenticação
      isAuthenticated,
      currentUser,
      isLoading,
      loginForm,
      handleLogin,
      logout,

      // Estado de projetos
      projetos,
      isLoadingProjetos,
      loadProjetos,
      viewProjeto,
      deleteProjeto,

      // Estado de criação de projeto
      isCreatingProjeto,
      newProjeto,
      createNewProjeto,
    };
  },
});
</script>
