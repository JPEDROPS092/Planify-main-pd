<script setup>
definePageMeta({
  middleware: 'auth'
})

import { useQuery, useQueryClient } from '@tanstack/vue-query';
import { Icon } from '@iconify/vue';
import { computed } from 'vue';

// Usar o composable de autenticação para dados do usuário
const { user, isAuthenticated, isLoadingUser } = useAuth();

// Simulação de dados enquanto os serviços não estão implementados
const { data: projects, isLoading: projectsLoading } = useQuery({
  queryKey: ['my-projects'],
  queryFn: async () => {
    // Simular dados de projetos
    return {
      results: [
        { id: 1, nome: 'Projeto Alpha', status: 'ATIVO', descricao: 'Desenvolvimento de app mobile' },
        { id: 2, nome: 'Projeto Beta', status: 'CONCLUIDO', descricao: 'Sistema de gestão' }
      ]
    }
  },
  enabled: isAuthenticated
});

const { data: tasks, isLoading: tasksLoading } = useQuery({
  queryKey: ['my-tasks'],
  queryFn: async () => {
    // Simular dados de tarefas
    return {
      results: [
        { id: 1, titulo: 'Revisar documentação', status: 'PENDENTE', projeto: 'Projeto Alpha' },
        { id: 2, titulo: 'Implementar login', status: 'CONCLUIDA', projeto: 'Projeto Beta' }
      ]
    }
  },
  enabled: isAuthenticated
});

// Computed properties para estatísticas
const projectStats = computed(() => {
  if (!projects?.results) return { active: 0, completed: 0, total: 0 };
  const results = projects.results;
  return {
    active: results.filter(p => p.status === 'ATIVO').length,
    completed: results.filter(p => p.status === 'CONCLUIDO').length,
    total: results.length
  };
});

const taskStats = computed(() => {
  if (!tasks?.results) return { completed: 0, pending: 0, total: 0 };
  const results = tasks.results;
  return {
    completed: results.filter(t => t.status === 'CONCLUIDA').length,
    pending: results.filter(t => t.status === 'PENDENTE').length,
    total: results.length
  };
});
</script>

<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <h1 class="text-2xl font-semibold text-gray-900">Dashboard</h1>
      <p class="mt-2 text-gray-600">
        Bem-vindo de volta, {{ user?.first_name || user?.username || 'Usuário' }}!
      </p>
    </div>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <!-- Resumo em cards -->
      <div class="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Icon icon="lucide:briefcase" class="h-8 w-8 text-blue-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    Projetos Ativos
                  </dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ projectStats.active }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Icon icon="lucide:check-square" class="h-8 w-8 text-green-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    Tarefas Concluídas
                  </dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ taskStats.completed }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Icon icon="lucide:clock" class="h-8 w-8 text-yellow-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    Tarefas Pendentes
                  </dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ taskStats.pending }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Icon icon="lucide:users" class="h-8 w-8 text-purple-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    Total de Projetos
                  </dt>
                  <dd class="text-lg font-medium text-gray-900">
                    {{ projectStats.total }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Projetos recentes -->
      <div class="mt-8">
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 border-b border-gray-200 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Projetos Recentes
            </h3>
          </div>
          
          <div v-if="projectsLoading" class="p-4 flex justify-center">
            <div class="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
          </div>
          
          <div v-else-if="projects?.results?.length === 0" class="p-8 text-center text-gray-500">
            <Icon icon="lucide:folder" class="h-12 w-12 mx-auto text-gray-400" />
            <p class="mt-2">Você não tem projetos. Comece criando um novo projeto!</p>
          </div>
          
          <ul v-else class="divide-y divide-gray-200">
            <li v-for="project in projects?.results" :key="project.id" class="px-4 py-4 sm:px-6">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <Icon icon="lucide:folder" class="h-6 w-6 text-gray-400" />
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">
                      {{ project.nome }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ project.descricao }}
                    </div>
                  </div>
                </div>
                <div class="flex items-center">
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    project.status === 'ATIVO' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  ]">
                    {{ project.status }}
                  </span>
                </div>
              </div>
            </li>
          </ul>
          
          <div class="border-t border-gray-200 px-4 py-4 sm:px-6">
            <NuxtLink to="/projects" class="text-sm font-medium text-primary hover:text-primary-600">
              Ver todos os projetos →
            </NuxtLink>
          </div>
        </div>
      </div>
      
      <!-- Tarefas recentes -->
      <div class="mt-8">
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 border-b border-gray-200 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Tarefas Recentes
            </h3>
          </div>
          
          <div v-if="tasksLoading" class="p-4 flex justify-center">
            <div class="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
          </div>
          
          <div v-else-if="tasks?.results?.length === 0" class="p-8 text-center text-gray-500">
            <Icon icon="lucide:check-square" class="h-12 w-12 mx-auto text-gray-400" />
            <p class="mt-2">Você não tem tarefas. Que tal criar uma?</p>
          </div>
          
          <ul v-else class="divide-y divide-gray-200">
            <li v-for="task in tasks?.results" :key="task.id" class="px-4 py-4 sm:px-6">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <Icon :icon="task.status === 'CONCLUIDA' ? 'lucide:check-circle' : 'lucide:clock'" 
                          :class="task.status === 'CONCLUIDA' ? 'text-green-500' : 'text-yellow-500'" 
                          class="h-5 w-5" />
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">
                      {{ task.titulo }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ task.projeto }}
                    </div>
                  </div>
                </div>
                <div class="flex items-center">
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    task.status === 'CONCLUIDA' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  ]">
                    {{ task.status }}
                  </span>
                </div>
              </div>
            </li>
          </ul>
          
          <div class="border-t border-gray-200 px-4 py-4 sm:px-6">
            <NuxtLink to="/tasks" class="text-sm font-medium text-primary hover:text-primary-600">
              Ver todas as tarefas →
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
