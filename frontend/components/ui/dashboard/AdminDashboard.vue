<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold">Dashboard do Administrador</h1>
      <p class="text-muted-foreground">
        Visão geral do sistema e atividades administrativas
      </p>
    </div>

    <!-- Resumo do Sistema -->
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Usuários</CardTitle>
          <Users class="h-5 w-5 text-blue-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ userCount }}</div>
          <p class="text-xs text-muted-foreground">
            Usuários ativos no sistema
          </p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/usuarios"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Gerenciar usuários →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Projetos</CardTitle>
          <Briefcase class="h-5 w-5 text-green-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ projectCount }}</div>
          <p class="text-xs text-muted-foreground">Projetos ativos</p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/projetos"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver todos →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Logs do Sistema</CardTitle>
          <FileText class="h-5 w-5 text-purple-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ logCount }}</div>
          <p class="text-xs text-muted-foreground">Eventos registrados hoje</p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/logs"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver logs →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Alertas</CardTitle>
          <AlertTriangle class="h-5 w-5 text-yellow-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ alertCount }}</div>
          <p class="text-xs text-muted-foreground">Alertas de segurança</p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/alertas"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver alertas →
          </NuxtLink>
        </CardFooter>
      </Card>
    </div>

    <!-- Atividade Recente e Logs -->
    <div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
      <!-- Atividade Recente -->
      <Card>
        <CardHeader>
          <CardTitle>Atividade Recente</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <template v-if="recentActivity.length > 0">
            <div
              v-for="activity in recentActivity"
              :key="activity.id"
              class="flex items-start space-x-4"
            >
              <div
                class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10"
              >
                <ActivityIcon
                  :type="activity.type"
                  class="h-5 w-5 text-primary"
                />
              </div>
              <div>
                <p class="text-sm font-medium">{{ activity.title }}</p>
                <p class="text-xs text-muted-foreground">
                  {{ activity.description }}
                </p>
                <p class="mt-1 text-xs text-muted-foreground">
                  {{ formatDate(activity.timestamp) }}
                </p>
              </div>
            </div>
          </template>
          <template v-else>
            <div
              class="flex flex-col items-center justify-center py-8 text-center"
            >
              <Activity class="h-12 w-12 text-muted-foreground" />
              <p class="mt-4 text-sm font-semibold">
                Nenhuma atividade recente
              </p>
              <p class="mt-1 text-xs text-muted-foreground">
                Não há atividades registradas recentemente.
              </p>
            </div>
          </template>
        </CardContent>
      </Card>

      <!-- Logs de Segurança -->
      <Card>
        <CardHeader>
          <CardTitle>Logs de Segurança</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <template v-if="securityLogs.length > 0">
            <div
              v-for="log in securityLogs"
              :key="log.id"
              class="flex items-start space-x-4"
            >
              <div
                class="flex h-10 w-10 items-center justify-center rounded-full"
                :class="getSecurityLogClass(log.level)"
              >
                <Shield
                  class="h-5 w-5"
                  :class="getSecurityLogTextClass(log.level)"
                />
              </div>
              <div>
                <p class="text-sm font-medium">{{ log.title }}</p>
                <p class="text-xs text-muted-foreground">{{ log.message }}</p>
                <p class="mt-1 text-xs text-muted-foreground">
                  {{ formatDate(log.timestamp) }}
                </p>
              </div>
            </div>
          </template>
          <template v-else>
            <div
              class="flex flex-col items-center justify-center py-8 text-center"
            >
              <Shield class="h-12 w-12 text-muted-foreground" />
              <p class="mt-4 text-sm font-semibold">Nenhum log de segurança</p>
              <p class="mt-1 text-xs text-muted-foreground">
                Não há logs de segurança registrados recentemente.
              </p>
            </div>
          </template>
        </CardContent>
      </Card>
    </div>

    <!-- Estatísticas do Sistema -->
    <Card class="mt-8">
      <CardHeader>
        <CardTitle>Estatísticas do Sistema</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          <div class="space-y-2">
            <h3 class="text-sm font-medium">Uso de CPU</h3>
            <div class="h-2 w-full rounded-full bg-muted">
              <div
                class="h-2 rounded-full bg-blue-500"
                :style="{ width: `${cpuUsage}%` }"
              ></div>
            </div>
            <p class="text-xs text-muted-foreground">{{ cpuUsage }}% de uso</p>
          </div>

          <div class="space-y-2">
            <h3 class="text-sm font-medium">Uso de Memória</h3>
            <div class="h-2 w-full rounded-full bg-muted">
              <div
                class="h-2 rounded-full bg-green-500"
                :style="{ width: `${memoryUsage}%` }"
              ></div>
            </div>
            <p class="text-xs text-muted-foreground">
              {{ memoryUsage }}% de uso
            </p>
          </div>

          <div class="space-y-2">
            <h3 class="text-sm font-medium">Uso de Disco</h3>
            <div class="h-2 w-full rounded-full bg-muted">
              <div
                class="h-2 rounded-full bg-purple-500"
                :style="{ width: `${diskUsage}%` }"
              ></div>
            </div>
            <p class="text-xs text-muted-foreground">{{ diskUsage }}% de uso</p>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue';
import {
  Users,
  Briefcase,
  FileText,
  AlertTriangle,
  Activity,
  Shield,
} from 'lucide-vue-next';

// Dados simulados
const userCount = ref(0);
const projectCount = ref(0);
const logCount = ref(0);
const alertCount = ref(0);
const recentActivity = ref([]);
const securityLogs = ref([]);
const cpuUsage = ref(0);
const memoryUsage = ref(0);
const diskUsage = ref(0);

// Componente para ícone de atividade
const ActivityIcon = (props) => {
  const iconMap = {
    login: Users,
    project: Briefcase,
    task: Activity,
    document: FileText,
    alert: AlertTriangle,
  };
  return h(iconMap[props.type] || Activity);
};

// Formatação de data
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

// Classes para logs de segurança
const getSecurityLogClass = (level) => {
  switch (level) {
    case 'critical':
      return 'bg-red-100 dark:bg-red-900/20';
    case 'warning':
      return 'bg-yellow-100 dark:bg-yellow-900/20';
    case 'info':
      return 'bg-blue-100 dark:bg-blue-900/20';
    default:
      return 'bg-gray-100 dark:bg-gray-800';
  }
};

const getSecurityLogTextClass = (level) => {
  switch (level) {
    case 'critical':
      return 'text-red-500 dark:text-red-400';
    case 'warning':
      return 'text-yellow-500 dark:text-yellow-400';
    case 'info':
      return 'text-blue-500 dark:text-blue-400';
    default:
      return 'text-gray-500 dark:text-gray-400';
  }
};

onMounted(async () => {
  try {
    // Aqui faríamos chamadas à API para buscar os dados reais
    // Por enquanto, vamos simular com dados estáticos
    userCount.value = 24;
    projectCount.value = 8;
    logCount.value = 156;
    alertCount.value = 3;

    // Atividades recentes simuladas
    recentActivity.value = [
      {
        id: 1,
        type: 'login',
        title: 'Novo login',
        description: 'Usuário João Silva fez login no sistema',
        timestamp: '2025-05-27T10:30:00',
      },
      {
        id: 2,
        type: 'project',
        title: 'Projeto criado',
        description: 'Novo projeto "Sistema ERP" foi criado',
        timestamp: '2025-05-27T09:15:00',
      },
      {
        id: 3,
        type: 'task',
        title: 'Tarefa atualizada',
        description:
          'Status da tarefa "Implementar login" alterado para "Concluído"',
        timestamp: '2025-05-26T16:45:00',
      },
      {
        id: 4,
        type: 'document',
        title: 'Documento aprovado',
        description: 'Documento "Especificação técnica" foi aprovado',
        timestamp: '2025-05-26T14:20:00',
      },
      {
        id: 5,
        type: 'alert',
        title: 'Alerta de segurança',
        description: 'Múltiplas tentativas de login falhas detectadas',
        timestamp: '2025-05-26T11:10:00',
      },
    ];

    // Logs de segurança simulados
    securityLogs.value = [
      {
        id: 1,
        level: 'critical',
        title: 'Tentativa de acesso não autorizado',
        message: 'Múltiplas tentativas de login falhas para o usuário admin',
        timestamp: '2025-05-27T08:45:00',
      },
      {
        id: 2,
        level: 'warning',
        title: 'Permissão alterada',
        message: 'Permissões do usuário Maria Silva foram modificadas',
        timestamp: '2025-05-26T15:30:00',
      },
      {
        id: 3,
        level: 'info',
        title: 'Backup concluído',
        message: 'Backup diário do banco de dados concluído com sucesso',
        timestamp: '2025-05-26T03:00:00',
      },
    ];

    // Estatísticas do sistema simuladas
    cpuUsage.value = 42;
    memoryUsage.value = 68;
    diskUsage.value = 35;
  } catch (error) {
    console.error(
      'Erro ao carregar dados do dashboard de administrador:',
      error
    );
  }
});
</script>
