<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold">Dashboard do Gerente de Projetos</h1>
      <p class="text-muted-foreground">
        Visão geral dos projetos e tarefas sob sua responsabilidade
      </p>
    </div>

    <!-- Resumo dos Projetos -->
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Projetos Ativos</CardTitle>
          <Briefcase class="h-5 w-5 text-blue-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ activeProjects }}</div>
          <p class="text-xs text-muted-foreground">Projetos em andamento</p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/projetos"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver projetos →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Tarefas Pendentes</CardTitle>
          <CheckSquare class="h-5 w-5 text-yellow-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ pendingTasks }}</div>
          <p class="text-xs text-muted-foreground">Tarefas aguardando ação</p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/tarefas"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver tarefas →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Membros da Equipe</CardTitle>
          <Users class="h-5 w-5 text-green-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ teamMembers }}</div>
          <p class="text-xs text-muted-foreground">
            Membros ativos nas equipes
          </p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/equipes"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Gerenciar equipes →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium"
            >Riscos Identificados</CardTitle
          >
          <AlertTriangle class="h-5 w-5 text-red-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ risks }}</div>
          <p class="text-xs text-muted-foreground">
            Riscos que precisam de atenção
          </p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/riscos"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Gerenciar riscos →
          </NuxtLink>
        </CardFooter>
      </Card>
    </div>

    <!-- Progresso dos Projetos -->
    <Card class="mt-8">
      <CardHeader>
        <CardTitle>Progresso dos Projetos</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="space-y-6">
          <div v-for="project in projects" :key="project.id" class="space-y-2">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-medium">{{ project.name }}</h3>
              <span class="text-xs text-muted-foreground"
                >{{ project.progress }}%</span
              >
            </div>
            <div class="h-2 w-full rounded-full bg-muted">
              <div
                class="h-2 rounded-full"
                :class="getProgressColorClass(project.progress)"
                :style="{ width: `${project.progress}%` }"
              ></div>
            </div>
            <div
              class="flex items-center justify-between text-xs text-muted-foreground"
            >
              <span>Início: {{ formatDate(project.startDate) }}</span>
              <span>Prazo: {{ formatDate(project.endDate) }}</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Tarefas Recentes e Próximos Marcos -->
    <div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
      <!-- Tarefas Recentes -->
      <Card>
        <CardHeader>
          <CardTitle>Tarefas Recentes</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div
              v-for="task in recentTasks"
              :key="task.id"
              class="flex items-start space-x-4"
            >
              <div
                class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10"
              >
                <TaskIcon :status="task.status" class="h-5 w-5" />
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium">{{ task.title }}</p>
                  <Badge :variant="getTaskStatusVariant(task.status)">{{
                    task.status
                  }}</Badge>
                </div>
                <p class="text-xs text-muted-foreground">
                  {{ task.description }}
                </p>
                <div class="mt-2 flex items-center justify-between">
                  <p class="text-xs text-muted-foreground">
                    Responsável: {{ task.assignee }}
                  </p>
                  <p class="text-xs text-muted-foreground">
                    {{ formatDate(task.dueDate) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/tarefas"
            class="text-sm text-muted-foreground hover:text-primary"
          >
            Ver todas as tarefas →
          </NuxtLink>
        </CardFooter>
      </Card>

      <!-- Próximos Marcos -->
      <Card>
        <CardHeader>
          <CardTitle>Próximos Marcos</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div
              v-for="milestone in upcomingMilestones"
              :key="milestone.id"
              class="flex items-start space-x-4"
            >
              <div
                class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10"
              >
                <Flag class="h-5 w-5 text-primary" />
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium">{{ milestone.title }}</p>
                  <Badge :variant="getMilestoneVariant(milestone.daysLeft)">
                    {{ milestone.daysLeft }} dias
                  </Badge>
                </div>
                <p class="text-xs text-muted-foreground">
                  {{ milestone.description }}
                </p>
                <div class="mt-2 flex items-center justify-between">
                  <p class="text-xs text-muted-foreground">
                    Projeto: {{ milestone.project }}
                  </p>
                  <p class="text-xs text-muted-foreground">
                    {{ formatDate(milestone.date) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/marcos"
            class="text-sm text-muted-foreground hover:text-primary"
          >
            Ver todos os marcos →
          </NuxtLink>
        </CardFooter>
      </Card>
    </div>

    <!-- Gráfico de Distribuição de Tarefas -->
    <Card class="mt-8">
      <CardHeader>
        <CardTitle>Distribuição de Tarefas por Status</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 gap-4 md:grid-cols-4">
          <div
            v-for="status in taskStatusDistribution"
            :key="status.name"
            class="flex flex-col items-center justify-center p-4 text-center"
          >
            <div
              class="flex h-16 w-16 items-center justify-center rounded-full"
              :class="status.bgClass"
            >
              <div class="text-lg font-bold" :class="status.textClass">
                {{ status.count }}
              </div>
            </div>
            <h3 class="mt-2 text-sm font-medium">{{ status.name }}</h3>
            <p class="text-xs text-muted-foreground">
              {{ status.percentage }}% do total
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue';
import {
  Briefcase,
  CheckSquare,
  Users,
  AlertTriangle,
  Flag,
  CheckCircle2,
  Clock,
  XCircle,
  CircleDashed,
} from 'lucide-vue-next';

// Dados simulados
const activeProjects = ref(0);
const pendingTasks = ref(0);
const teamMembers = ref(0);
const risks = ref(0);
const projects = ref([]);
const recentTasks = ref([]);
const upcomingMilestones = ref([]);
const taskStatusDistribution = ref([]);

// Componente para ícone de tarefa
const TaskIcon = (props) => {
  const iconMap = {
    Concluída: CheckCircle2,
    'Em Andamento': Clock,
    Pendente: CircleDashed,
    Atrasada: XCircle,
  };
  return h(iconMap[props.status] || CircleDashed, {
    class: getTaskStatusIconClass(props.status),
  });
};

// Formatação de data
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(date);
};

// Classes para progresso
const getProgressColorClass = (progress) => {
  if (progress < 30) return 'bg-red-500';
  if (progress < 70) return 'bg-yellow-500';
  return 'bg-green-500';
};

// Variante para status de tarefa
const getTaskStatusVariant = (status) => {
  switch (status) {
    case 'Concluída':
      return 'success';
    case 'Em Andamento':
      return 'default';
    case 'Pendente':
      return 'secondary';
    case 'Atrasada':
      return 'destructive';
    default:
      return 'outline';
  }
};

// Classe para ícone de status de tarefa
const getTaskStatusIconClass = (status) => {
  switch (status) {
    case 'Concluída':
      return 'text-green-500';
    case 'Em Andamento':
      return 'text-blue-500';
    case 'Pendente':
      return 'text-yellow-500';
    case 'Atrasada':
      return 'text-red-500';
    default:
      return 'text-gray-500';
  }
};

// Variante para marcos
const getMilestoneVariant = (daysLeft) => {
  if (daysLeft <= 7) return 'destructive';
  if (daysLeft <= 14) return 'warning';
  return 'outline';
};

onMounted(async () => {
  try {
    // Aqui faríamos chamadas à API para buscar os dados reais
    // Por enquanto, vamos simular com dados estáticos
    activeProjects.value = 5;
    pendingTasks.value = 23;
    teamMembers.value = 12;
    risks.value = 8;

    // Projetos simulados
    projects.value = [
      {
        id: 1,
        name: 'Sistema ERP',
        progress: 75,
        startDate: '2025-01-15',
        endDate: '2025-06-30',
      },
      {
        id: 2,
        name: 'Aplicativo Mobile',
        progress: 45,
        startDate: '2025-02-10',
        endDate: '2025-07-15',
      },
      {
        id: 3,
        name: 'Portal do Cliente',
        progress: 90,
        startDate: '2025-03-01',
        endDate: '2025-05-30',
      },
      {
        id: 4,
        name: 'Integração de APIs',
        progress: 30,
        startDate: '2025-04-05',
        endDate: '2025-08-20',
      },
      {
        id: 5,
        name: 'Migração de Dados',
        progress: 10,
        startDate: '2025-05-01',
        endDate: '2025-09-15',
      },
    ];

    // Tarefas recentes simuladas
    recentTasks.value = [
      {
        id: 1,
        title: 'Implementar autenticação',
        description: 'Adicionar sistema de login com múltiplos fatores',
        status: 'Concluída',
        assignee: 'João Silva',
        dueDate: '2025-05-20',
      },
      {
        id: 2,
        title: 'Criar telas de dashboard',
        description: 'Desenvolver interfaces para diferentes perfis de usuário',
        status: 'Em Andamento',
        assignee: 'Maria Santos',
        dueDate: '2025-05-30',
      },
      {
        id: 3,
        title: 'Testes de integração',
        description: 'Realizar testes entre módulos do sistema',
        status: 'Pendente',
        assignee: 'Pedro Oliveira',
        dueDate: '2025-06-05',
      },
      {
        id: 4,
        title: 'Correção de bugs',
        description: 'Resolver problemas reportados pelos usuários',
        status: 'Atrasada',
        assignee: 'Ana Costa',
        dueDate: '2025-05-15',
      },
    ];

    // Marcos próximos simulados
    upcomingMilestones.value = [
      {
        id: 1,
        title: 'Entrega do Módulo Financeiro',
        description: 'Finalização do módulo de gestão financeira',
        project: 'Sistema ERP',
        date: '2025-06-15',
        daysLeft: 20,
      },
      {
        id: 2,
        title: 'Lançamento Beta',
        description: 'Versão beta para testes com usuários selecionados',
        project: 'Aplicativo Mobile',
        date: '2025-06-01',
        daysLeft: 5,
      },
      {
        id: 3,
        title: 'Apresentação para Stakeholders',
        description: 'Demonstração do progresso para os stakeholders',
        project: 'Portal do Cliente',
        date: '2025-05-30',
        daysLeft: 3,
      },
      {
        id: 4,
        title: 'Finalização da Documentação',
        description: 'Entrega da documentação técnica completa',
        project: 'Integração de APIs',
        date: '2025-07-10',
        daysLeft: 45,
      },
    ];

    // Distribuição de status de tarefas simulada
    taskStatusDistribution.value = [
      {
        name: 'Concluídas',
        count: 42,
        percentage: 35,
        bgClass: 'bg-green-100 dark:bg-green-900/20',
        textClass: 'text-green-500 dark:text-green-400',
      },
      {
        name: 'Em Andamento',
        count: 38,
        percentage: 32,
        bgClass: 'bg-blue-100 dark:bg-blue-900/20',
        textClass: 'text-blue-500 dark:text-blue-400',
      },
      {
        name: 'Pendentes',
        count: 27,
        percentage: 23,
        bgClass: 'bg-yellow-100 dark:bg-yellow-900/20',
        textClass: 'text-yellow-500 dark:text-yellow-400',
      },
      {
        name: 'Atrasadas',
        count: 12,
        percentage: 10,
        bgClass: 'bg-red-100 dark:bg-red-900/20',
        textClass: 'text-red-500 dark:text-red-400',
      },
    ];
  } catch (error) {
    console.error(
      'Erro ao carregar dados do dashboard de gerente de projetos:',
      error
    );
  }
});
</script>
