<script setup>
definePageMeta({
  middleware: 'auth'
})

import { useQuery, useQueryClient } from '@tanstack/vue-query';
import { useProjectService } from '~/services/projectService';
import { useTaskService } from '~/servicesMock/taskService';
import { useNotificationService } from '~/servicesMock/notificationService';
import { useAlertService } from '~/servicesMock/alertService';
import { Icon } from '@iconify/vue';
import { computed } from 'vue';

const projectService = useProjectService();
const taskService = useTaskService();
const notificationService = useNotificationService();
const alertService = useAlertService();

// Consultas para carregar dados do dashboard
const { data: projects, isLoading: projectsLoading } = useQuery({
  queryKey: ['my-projects'],
  queryFn: () => projectService.getMyProjects()
});

const { data: tasks, isLoading: tasksLoading } = useQuery({
  queryKey: ['my-tasks'],
  queryFn: () => taskService.getMyTasks({ page: 1 })
});

const { data: notifications, isLoading: notificationsLoading } = useQuery({
  queryKey: ['recent-notifications'],
  queryFn: () => notificationService.getNotifications({ page: 1, page_size: 5 })
});

const { data: alerts, isLoading: alertsLoading } = useQuery({
  queryKey: ['recent-alerts'],
  queryFn: () => alertService.getAlerts({ page: 1, page_size: 3 })
});

// Função para formatar data
const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('pt-BR');
};

// Função para formatar tempo relativo
const timeAgo = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  const now = new Date();
  const diffInMinutes = Math.floor((now - date) / (1000 * 60));
  
  if (diffInMinutes < 1) return 'agora';
  if (diffInMinutes < 60) return `${diffInMinutes}m atrás`;
  if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h atrás`;
  return `${Math.floor(diffInMinutes / 1440)}d atrás`;
};

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

const unreadNotifications = computed(() => {
  if (!notifications?.results) return 0;
  return notifications.results.filter(n => !n.lida).length;
});

const criticalAlerts = computed(() => {
  if (!alerts?.results) return 0;
  return alerts.results.filter(a => a.nivel === 'CRITICO' && !a.resolvido).length;
});
</script>

<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <h1 class="text-2xl font-semibold text-gray-900">Dashboard</h1>
    </div>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <!-- Resumo em cards -->
      <div class="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-primary-100 rounded-md p-3">
                <Icon icon="lucide:briefcase" class="h-6 w-6 text-primary" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Projetos Ativos</dt>
                  <dd>
                    <div class="text-lg font-medium text-gray-900">
                      {{ projectStats.active }}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-green-100 rounded-md p-3">
                <Icon icon="lucide:check-circle" class="h-6 w-6 text-green-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Tarefas Concluídas</dt>
                  <dd>
                    <div class="text-lg font-medium text-gray-900">
                      {{ taskStats.completed }}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-yellow-100 rounded-md p-3">
                <Icon icon="lucide:clock" class="h-6 w-6 text-yellow-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Notificações Não Lidas</dt>
                  <dd>
                    <div class="text-lg font-medium text-gray-900">
                      {{ unreadNotifications }}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-red-100 rounded-md p-3">
                <Icon icon="lucide:alert-circle" class="h-6 w-6 text-red-600" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">Alertas Críticos</dt>
                  <dd>
                    <div class="text-lg font-medium text-gray-900">
                      {{ criticalAlerts }}
                    </div>
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
              Meus Projetos
            </h3>
          </div>
          
          <div v-if="projectsLoading" class="p-4 flex justify-center">
            <div class="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
          </div>
          
          <div v-else-if="projects?.results?.length === 0" class="p-8 text-center text-gray-500">
            <Icon icon="lucide:folder" class="h-12 w-12 mx-auto text-gray-400" />
            <p class="mt-2">Você não tem projetos. Comece criando um novo projeto!</p>
            <button class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
              <Icon icon="lucide:plus" class="mr-2 h-4 w-4" />
              Novo Projeto
            </button>
          </div>
          
          <ul v-else class="divide-y divide-gray-200">
            
            <li v-for="project in projects.results" :key="project.id" class="px-4 py-4 sm:px-6 hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <Icon icon="lucide:folder" class="h-5 w-5 text-gray-400" />
                  </div>
                  <div class="ml-3">
                    <NuxtLink :to="`/projects/${project.id}`" class="text-sm font-medium text-primary hover:text-primary-600">
                      {{ project.titulo }}
                    </NuxtLink>
                    <p class="text-sm text-gray-500">
                      {{ formatDate(project.data_inicio) }} - {{ formatDate(project.data_fim_previsto) }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" 
                        :class="{
                          'bg-green-100 text-green-800': project.status === 'CONCLUIDO',
                          'bg-blue-100 text-blue-800': project.status === 'ATIVO',
                          'bg-yellow-100 text-yellow-800': project.status === 'PAUSADO',
                          'bg-red-100 text-red-800': project.status === 'CANCELADO',
                          'bg-gray-100 text-gray-800': !['CONCLUIDO', 'ATIVO', 'PAUSADO', 'CANCELADO'].includes(project.status)
                        }">
                    {{ project.status_display }}
                  </span>
                  <div class="ml-2 flex-shrink-0 flex">
                    <NuxtLink :to="`/projects/${project.id}/kanban`" class="ml-2 text-gray-400 hover:text-gray-500">
                      <Icon icon="lucide:layout-kanban" class="h-5 w-5" />
                    </NuxtLink>
                    <NuxtLink :to="`/projects/${project.id}/gantt`" class="ml-2 text-gray-400 hover:text-gray-500">
                      <Icon icon="lucide:gantt-chart" class="h-5 w-5" />
                    </NuxtLink>
                  </div>
                </div>
              </div>
            </li>
          </ul>
          
          <div class="border-t border-gray-200 px-4 py-4 sm:px-6">
            <NuxtLink to="/projects" class="text-sm font-medium text-primary hover:text-primary-600">
              Ver todos os projetos
            </NuxtLink>
          </div>
        </div>
      </div>
      
      <!-- Tarefas recentes -->
      <div class="mt-8">
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 border-b border-gray-200 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Minhas Tarefas
            </h3>
          </div>
          
          <div v-if="tasksLoading" class="p-4 flex justify-center">
            <div class="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
          </div>
          
          <div v-else-if="tasks?.results?.length === 0" class="p-8 text-center text-gray-500">
            <Icon icon="lucide:task" class="h-12 w-12 mx-auto text-gray-400" />
            <p class="mt-2">Você não tem tarefas. Comece criando uma nova tarefa!</p>
            <button class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
              <Icon icon="lucide:plus" class="mr-2 h-4 w-4" />
              Nova Tarefa
            </button>
          </div>
          
          <ul v-else class="divide-y divide-gray-200">
            <li v-for="task in tasks.results" :key="task.id" class="px-4 py-4 sm:px-6 hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <Icon icon="lucide:task" class="h-5 w-5 text-gray-400" />
                  </div>
                  <div class="ml-3">
                    <NuxtLink :to="`/tasks/${task.id}`" class="text-sm font-medium text-primary hover:text-primary-600">
                      {{ task.titulo }}
                    </NuxtLink>
                    <p class="text-sm text-gray-500">
                      {{ formatDate(task.data_inicio) }} - {{ formatDate(task.data_fim_previsto) }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" 
                        :class="{
                          'bg-green-100 text-green-800': task.status === 'CONCLUIDA',
                          'bg-blue-100 text-blue-800': task.status === 'PENDENTE',
                          'bg-yellow-100 text-yellow-800': task.status === 'PAUSADA',
                          'bg-red-100 text-red-800': task.status === 'CANCELADA',
                          'bg-gray-100 text-gray-800': !['CONCLUIDA', 'PENDENTE', 'PAUSADA', 'CANCELADA'].includes(task.status)
                        }">
                    {{ task.status_display }}
                  </span>
                  <div class="ml-2 flex-shrink-0 flex">
                    <NuxtLink :to="`/tasks/${task.id}/edit`" class="ml-2 text-gray-400 hover:text-gray-500">
                      <Icon icon="lucide:edit" class="h-5 w-5" />
                    </NuxtLink>
                  </div>
                </div>
              </div>
            </li>
          </ul>
          
          <div class="border-t border-gray-200 px-4 py-4 sm:px-6">
            <NuxtLink to="/tasks" class="text-sm font-medium text-primary hover:text-primary-600">
              Ver todas as tarefas
            </NuxtLink>
          </div>
        </div>
      </div>
      
      <!-- Notificações recentes -->
      <div class="mt-8">
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 border-b border-gray-200 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Notificações
            </h3>
          </div>
          
          <div v-if="notificationsLoading" class="p-4 flex justify-center">
            <div class="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
          </div>
          
          <div v-else-if="notifications?.results?.length === 0" class="p-8 text-center text-gray-500">
            <Icon icon="lucide:bell" class="h-12 w-12 mx-auto text-gray-400" />
            <p class="mt-2">Você não tem notificações.</p>
          </div>
          
          <ul v-else class="divide-y divide-gray-200">
            <li v-for="notification in notifications.results" :key="notification.id" class="px-4 py-4 sm:px-6 hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <Icon icon="lucide:bell" class="h-5 w-5 text-gray-400" />
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium text-gray-900">
                      {{ notification.titulo }}
                    </p>
                    <p class="text-sm text-gray-500">
                      {{ timeAgo(notification.data_criacao) }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center">
                  <button @click="notification.lida = true" class="ml-2 text-gray-400 hover:text-gray-500">
                    <Icon icon="lucide:check" class="h-5 w-5" />
                  </button>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
      
      <!-- Alertas recentes -->
      <div class="mt-8">
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 border-b border-gray-200 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Alertas
            </h3>
          </div>
          
          <div v-if="alertsLoading" class="p-4 flex justify-center">
            <div class="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
          </div>
          
          <div v-else-if="alerts?.results?.length === 0" class="p-8 text-center text-gray-500">
            <Icon icon="lucide:alert-circle" class="h-12 w-12 mx-auto text-gray-400" />
            <p class="mt-2">Você não tem alertas.</p>
          </div>
          
          <ul v-else class="divide-y divide-gray-200">
            <li v-for="alert in alerts.results" :key="alert.id" class="px-4 py-4 sm:px-6 hover:bg-gray-50">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <Icon icon="lucide:alert-circle" class="h-5 w-5 text-gray-400" />
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium text-gray-900">
                      {{ alert.titulo }}
                    </p>
                    <p class="text-sm text-gray-500">
                      {{ timeAgo(alert.data_criacao) }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center">
                  <button @click="alert.resolvido = true" class="ml-2 text-gray-400 hover:text-gray-500">
                    <Icon icon="lucide:check" class="h-5 w-5" />
                  </button>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
