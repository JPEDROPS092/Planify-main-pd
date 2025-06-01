<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold">Dashboard do Membro da Equipe</h1>
      <p class="text-muted-foreground">
        Visão geral das suas tarefas e projetos
      </p>
    </div>

    <!-- Resumo das Tarefas -->
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Minhas Tarefas</CardTitle>
          <CheckSquare class="h-5 w-5 text-blue-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ totalTasks }}</div>
          <p class="text-xs text-muted-foreground">
            Total de tarefas atribuídas
          </p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/minhas-tarefas"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver todas →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Para Hoje</CardTitle>
          <Clock class="h-5 w-5 text-yellow-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ todayTasks }}</div>
          <p class="text-xs text-muted-foreground">
            Tarefas com prazo para hoje
          </p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/minhas-tarefas?prazo=hoje"
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
          <CardTitle class="text-sm font-medium">Concluídas</CardTitle>
          <CheckCircle2 class="h-5 w-5 text-green-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ completedTasks }}</div>
          <p class="text-xs text-muted-foreground">
            Tarefas concluídas esta semana
          </p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/minhas-tarefas?status=concluida"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver histórico →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Atrasadas</CardTitle>
          <AlertCircle class="h-5 w-5 text-red-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ lateTasks }}</div>
          <p class="text-xs text-muted-foreground">Tarefas com prazo vencido</p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/minhas-tarefas?status=atrasada"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver atrasadas →
          </NuxtLink>
        </CardFooter>
      </Card>
    </div>

    <!-- Tarefas Pendentes -->
    <Card class="mt-8">
      <CardHeader class="flex items-center justify-between">
        <CardTitle>Tarefas Pendentes</CardTitle>
        <Button variant="outline" size="sm">
          <Plus class="mr-2 h-4 w-4" />
          Adicionar Tarefa
        </Button>
      </CardHeader>
      <CardContent>
        <div class="space-y-4">
          <div
            v-for="task in pendingTasks"
            :key="task.id"
            class="flex items-start space-x-4"
          >
            <div
              class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10"
            >
              <TaskPriorityIcon :priority="task.priority" class="h-5 w-5" />
            </div>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <p class="text-sm font-medium">{{ task.title }}</p>
                <Badge :variant="getTaskPriorityVariant(task.priority)">{{
                  task.priority
                }}</Badge>
              </div>
              <p class="text-xs text-muted-foreground">
                {{ task.description }}
              </p>
              <div class="mt-2 flex items-center justify-between">
                <p class="text-xs text-muted-foreground">
                  Projeto: {{ task.project }}
                </p>
                <p class="text-xs text-muted-foreground">
                  Prazo: {{ formatDate(task.dueDate) }}
                </p>
              </div>
              <div class="mt-2 flex space-x-2">
                <Button variant="outline" size="sm">
                  <CheckCircle2 class="mr-1 h-3 w-3" />
                  Concluir
                </Button>
                <Button variant="outline" size="sm">
                  <Clock class="mr-1 h-3 w-3" />
                  Iniciar
                </Button>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Meus Projetos e Próximas Reuniões -->
    <div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
      <!-- Meus Projetos -->
      <Card>
        <CardHeader>
          <CardTitle>Meus Projetos</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div
              v-for="project in myProjects"
              :key="project.id"
              class="space-y-2"
            >
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-medium">{{ project.name }}</h3>
                <Badge>{{ project.role }}</Badge>
              </div>
              <div class="flex items-center space-x-4">
                <div class="flex-1">
                  <div class="h-2 w-full rounded-full bg-muted">
                    <div
                      class="h-2 rounded-full"
                      :class="getProgressColorClass(project.progress)"
                      :style="{ width: `${project.progress}%` }"
                    ></div>
                  </div>
                </div>
                <span class="text-xs font-medium">{{ project.progress }}%</span>
              </div>
              <div
                class="flex items-center justify-between text-xs text-muted-foreground"
              >
                <span
                  >{{ project.tasksCompleted }} de
                  {{ project.totalTasks }} tarefas</span
                >
                <span>Prazo: {{ formatDate(project.endDate) }}</span>
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/meus-projetos"
            class="text-sm text-muted-foreground hover:text-primary"
          >
            Ver todos os projetos →
          </NuxtLink>
        </CardFooter>
      </Card>

      <!-- Próximas Reuniões -->
      <Card>
        <CardHeader>
          <CardTitle>Próximas Reuniões</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div
              v-for="meeting in upcomingMeetings"
              :key="meeting.id"
              class="flex items-start space-x-4"
            >
              <div
                class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10"
              >
                <Calendar class="h-5 w-5 text-primary" />
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium">{{ meeting.title }}</p>
                  <Badge variant="outline">{{
                    formatTime(meeting.startTime)
                  }}</Badge>
                </div>
                <p class="text-xs text-muted-foreground">
                  {{ meeting.description }}
                </p>
                <div class="mt-2 flex items-center justify-between">
                  <p class="text-xs text-muted-foreground">
                    Projeto: {{ meeting.project }}
                  </p>
                  <p class="text-xs text-muted-foreground">
                    {{ formatDate(meeting.date) }}
                  </p>
                </div>
                <div class="mt-2">
                  <Button variant="outline" size="sm">
                    <Link class="mr-1 h-3 w-3" />
                    Entrar na Reunião
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/reunioes"
            class="text-sm text-muted-foreground hover:text-primary"
          >
            Ver agenda completa →
          </NuxtLink>
        </CardFooter>
      </Card>
    </div>

    <!-- Meu Tempo de Trabalho -->
    <Card class="mt-8">
      <CardHeader>
        <CardTitle>Meu Tempo de Trabalho (Esta Semana)</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-medium">Horas Registradas</h3>
              <span class="text-sm font-medium"
                >{{ workHours.logged }} de {{ workHours.expected }} horas</span
              >
            </div>
            <div class="h-2 w-full rounded-full bg-muted">
              <div
                class="h-2 rounded-full bg-blue-500"
                :style="{
                  width: `${(workHours.logged / workHours.expected) * 100}%`,
                }"
              ></div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div class="rounded-lg border p-3">
                <div class="text-sm font-medium">Média Diária</div>
                <div class="text-2xl font-bold">
                  {{ workHours.dailyAverage }}h
                </div>
              </div>
              <div class="rounded-lg border p-3">
                <div class="text-sm font-medium">Produtividade</div>
                <div class="text-2xl font-bold">
                  {{ workHours.productivity }}%
                </div>
              </div>
            </div>
          </div>

          <div class="space-y-4">
            <h3 class="text-sm font-medium">Distribuição por Projeto</h3>
            <div
              v-for="project in workHours.byProject"
              :key="project.id"
              class="space-y-2"
            >
              <div class="flex items-center justify-between">
                <span class="text-xs">{{ project.name }}</span>
                <span class="text-xs font-medium">{{ project.hours }}h</span>
              </div>
              <div class="h-2 w-full rounded-full bg-muted">
                <div
                  class="h-2 rounded-full"
                  :style="{
                    width: `${(project.hours / workHours.logged) * 100}%`,
                    backgroundColor: project.color,
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
      <CardFooter>
        <Button variant="outline">
          <Clock class="mr-2 h-4 w-4" />
          Registrar Horas
        </Button>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue';
import {
  CheckSquare,
  Clock,
  CheckCircle2,
  AlertCircle,
  Plus,
  Calendar,
  Link,
  ArrowUp,
  ArrowRight,
  ArrowDown,
} from 'lucide-vue-next';

// Dados simulados
const totalTasks = ref(0);
const todayTasks = ref(0);
const completedTasks = ref(0);
const lateTasks = ref(0);
const pendingTasks = ref([]);
const myProjects = ref([]);
const upcomingMeetings = ref([]);
const workHours = ref({
  logged: 0,
  expected: 40,
  dailyAverage: 0,
  productivity: 0,
  byProject: [],
});

// Componente para ícone de prioridade de tarefa
const TaskPriorityIcon = (props) => {
  const iconMap = {
    Alta: ArrowUp,
    Média: ArrowRight,
    Baixa: ArrowDown,
  };
  return h(iconMap[props.priority] || ArrowRight, {
    class: getTaskPriorityIconClass(props.priority),
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

// Formatação de hora
const formatTime = (timeString) => {
  const [hours, minutes] = timeString.split(':');
  return `${hours}:${minutes}`;
};

// Classes para progresso
const getProgressColorClass = (progress) => {
  if (progress < 30) return 'bg-red-500';
  if (progress < 70) return 'bg-yellow-500';
  return 'bg-green-500';
};

// Variante para prioridade de tarefa
const getTaskPriorityVariant = (priority) => {
  switch (priority) {
    case 'Alta':
      return 'destructive';
    case 'Média':
      return 'warning';
    case 'Baixa':
      return 'secondary';
    default:
      return 'outline';
  }
};

// Classe para ícone de prioridade de tarefa
const getTaskPriorityIconClass = (priority) => {
  switch (priority) {
    case 'Alta':
      return 'text-red-500';
    case 'Média':
      return 'text-yellow-500';
    case 'Baixa':
      return 'text-blue-500';
    default:
      return 'text-gray-500';
  }
};

onMounted(async () => {
  try {
    // Aqui faríamos chamadas à API para buscar os dados reais
    // Por enquanto, vamos simular com dados estáticos
    totalTasks.value = 18;
    todayTasks.value = 5;
    completedTasks.value = 12;
    lateTasks.value = 2;

    // Tarefas pendentes simuladas
    pendingTasks.value = [
      {
        id: 1,
        title: 'Implementar validação de formulários',
        description: 'Adicionar validação nos formulários de cadastro',
        priority: 'Alta',
        project: 'Sistema ERP',
        dueDate: '2025-05-30',
      },
      {
        id: 2,
        title: 'Corrigir bug na exibição de gráficos',
        description: 'Resolver problema com gráficos em telas pequenas',
        priority: 'Média',
        project: 'Dashboard Analytics',
        dueDate: '2025-06-02',
      },
      {
        id: 3,
        title: 'Atualizar documentação da API',
        description: 'Documentar novos endpoints e parâmetros',
        priority: 'Baixa',
        project: 'API Gateway',
        dueDate: '2025-06-10',
      },
      {
        id: 4,
        title: 'Revisar código de colegas',
        description: 'Fazer code review das últimas alterações',
        priority: 'Média',
        project: 'Sistema ERP',
        dueDate: '2025-05-29',
      },
    ];

    // Projetos simulados
    myProjects.value = [
      {
        id: 1,
        name: 'Sistema ERP',
        role: 'Desenvolvedor',
        progress: 75,
        tasksCompleted: 15,
        totalTasks: 20,
        endDate: '2025-06-30',
      },
      {
        id: 2,
        name: 'Dashboard Analytics',
        role: 'Líder Técnico',
        progress: 45,
        tasksCompleted: 9,
        totalTasks: 20,
        endDate: '2025-07-15',
      },
      {
        id: 3,
        name: 'API Gateway',
        role: 'Desenvolvedor',
        progress: 30,
        tasksCompleted: 6,
        totalTasks: 20,
        endDate: '2025-08-20',
      },
    ];

    // Reuniões próximas simuladas
    upcomingMeetings.value = [
      {
        id: 1,
        title: 'Daily Scrum',
        description: 'Reunião diária de acompanhamento',
        project: 'Sistema ERP',
        date: '2025-05-28',
        startTime: '09:00',
        endTime: '09:15',
      },
      {
        id: 2,
        title: 'Revisão de Sprint',
        description: 'Apresentação do progresso da sprint atual',
        project: 'Dashboard Analytics',
        date: '2025-05-30',
        startTime: '14:00',
        endTime: '15:00',
      },
      {
        id: 3,
        title: 'Planejamento Técnico',
        description: 'Discussão sobre arquitetura e tecnologias',
        project: 'API Gateway',
        date: '2025-06-01',
        startTime: '10:30',
        endTime: '12:00',
      },
    ];

    // Horas de trabalho simuladas
    workHours.value = {
      logged: 32,
      expected: 40,
      dailyAverage: 6.4,
      productivity: 85,
      byProject: [
        { id: 1, name: 'Sistema ERP', hours: 18, color: '#3b82f6' },
        { id: 2, name: 'Dashboard Analytics', hours: 10, color: '#10b981' },
        { id: 3, name: 'API Gateway', hours: 4, color: '#8b5cf6' },
      ],
    };
  } catch (error) {
    console.error(
      'Erro ao carregar dados do dashboard de membro da equipe:',
      error
    );
  }
});
</script>
