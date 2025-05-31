<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold">Dashboard do Líder de Equipe</h1>
      <p class="text-muted-foreground">Visão geral da sua equipe e tarefas</p>
    </div>

    <!-- Resumo da Equipe -->
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Membros da Equipe</CardTitle>
          <Users class="h-5 w-5 text-blue-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ teamMembersCount }}</div>
          <p class="text-xs text-muted-foreground">Membros ativos na equipe</p>
        </CardContent>
        <CardFooter>
          <NuxtLink to="/equipe" class="text-xs text-muted-foreground hover:text-primary">
            Gerenciar equipe →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Tarefas Atribuídas</CardTitle>
          <CheckSquare class="h-5 w-5 text-green-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ assignedTasksCount }}</div>
          <p class="text-xs text-muted-foreground">Tarefas atribuídas à equipe</p>
        </CardContent>
        <CardFooter>
          <NuxtLink to="/tarefas" class="text-xs text-muted-foreground hover:text-primary">
            Ver tarefas →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Tarefas Atrasadas</CardTitle>
          <AlertCircle class="h-5 w-5 text-red-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ overdueTasksCount }}</div>
          <p class="text-xs text-muted-foreground">Tarefas com prazo vencido</p>
        </CardContent>
        <CardFooter>
          <NuxtLink to="/tarefas?status=atrasada" class="text-xs text-muted-foreground hover:text-primary">
            Ver atrasadas →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Produtividade</CardTitle>
          <BarChart class="h-5 w-5 text-purple-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ productivityRate }}%</div>
          <p class="text-xs text-muted-foreground">Taxa de conclusão de tarefas</p>
        </CardContent>
        <CardFooter>
          <NuxtLink to="/relatorios/produtividade" class="text-xs text-muted-foreground hover:text-primary">
            Ver relatório →
          </NuxtLink>
        </CardFooter>
      </Card>
    </div>

    <!-- Desempenho da Equipe -->
    <Card class="mt-8">
      <CardHeader>
        <CardTitle>Desempenho da Equipe</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="space-y-6">
          <div v-for="member in teamMembers" :key="member.id" class="space-y-2">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <Avatar>
                  <AvatarImage v-if="member.avatar" :src="member.avatar" />
                  <AvatarFallback>{{ getInitials(member.name) }}</AvatarFallback>
                </Avatar>
                <div>
                  <h3 class="text-sm font-medium">{{ member.name }}</h3>
                  <p class="text-xs text-muted-foreground">{{ member.role }}</p>
                </div>
              </div>
              <Badge :variant="getPerformanceVariant(member.performance)">
                {{ member.performance }}%
              </Badge>
            </div>
            <div class="h-2 w-full rounded-full bg-muted">
              <div 
                class="h-2 rounded-full" 
                :class="getPerformanceColorClass(member.performance)"
                :style="{ width: `${member.performance}%` }"
              ></div>
            </div>
            <div class="flex items-center justify-between text-xs text-muted-foreground">
              <span>{{ member.completedTasks }} de {{ member.totalTasks }} tarefas</span>
              <span>{{ member.hoursLogged }} horas registradas</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Distribuição de Tarefas e Próximas Reuniões -->
    <div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
      <!-- Distribuição de Tarefas -->
      <Card>
        <CardHeader>
          <CardTitle>Distribuição de Tarefas</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div v-for="status in taskStatusDistribution" :key="status.name" class="flex flex-col items-center justify-center rounded-lg border p-4 text-center">
                <div class="flex h-12 w-12 items-center justify-center rounded-full" :class="status.bgClass">
                  <div class="text-lg font-bold" :class="status.textClass">{{ status.count }}</div>
                </div>
                <h3 class="mt-2 text-sm font-medium">{{ status.name }}</h3>
                <p class="text-xs text-muted-foreground">{{ status.percentage }}% do total</p>
              </div>
            </div>
            
            <div class="mt-6">
              <h3 class="mb-2 text-sm font-medium">Distribuição por Membro</h3>
              <div v-for="member in taskDistributionByMember" :key="member.id" class="mb-4">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-medium">{{ member.name }}</span>
                  <span class="text-xs text-muted-foreground">{{ member.taskCount }} tarefas</span>
                </div>
                <div class="mt-1 h-2 w-full rounded-full bg-muted">
                  <div 
                    class="h-2 rounded-full bg-primary" 
                    :style="{ width: `${(member.taskCount / totalTeamTasks) * 100}%` }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button variant="outline" size="sm">
            <Plus class="mr-2 h-4 w-4" />
            Atribuir Tarefas
          </Button>
        </CardFooter>
      </Card>

      <!-- Próximas Reuniões -->
      <Card>
        <CardHeader>
          <CardTitle>Próximas Reuniões</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div v-for="meeting in upcomingMeetings" :key="meeting.id" class="flex items-start space-x-4">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                <Calendar class="h-5 w-5 text-primary" />
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium">{{ meeting.title }}</p>
                  <Badge variant="outline">{{ formatTime(meeting.startTime) }}</Badge>
                </div>
                <p class="text-xs text-muted-foreground">{{ meeting.description }}</p>
                <div class="mt-2 flex items-center justify-between">
                  <p class="text-xs text-muted-foreground">
                    <span v-if="meeting.attendees">{{ meeting.attendees }} participantes</span>
                  </p>
                  <p class="text-xs text-muted-foreground">{{ formatDate(meeting.date) }}</p>
                </div>
                <div class="mt-2 flex space-x-2">
                  <Button variant="outline" size="sm">
                    <Link class="mr-1 h-3 w-3" />
                    Entrar
                  </Button>
                  <Button variant="outline" size="sm">
                    <Edit class="mr-1 h-3 w-3" />
                    Editar
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button variant="outline" size="sm">
            <Calendar class="mr-2 h-4 w-4" />
            Agendar Reunião
          </Button>
        </CardFooter>
      </Card>
    </div>

    <!-- Problemas e Impedimentos -->
    <Card class="mt-8">
      <CardHeader class="flex items-center justify-between">
        <CardTitle>Problemas e Impedimentos</CardTitle>
        <Button variant="outline" size="sm">
          <Plus class="mr-2 h-4 w-4" />
          Registrar Problema
        </Button>
      </CardHeader>
      <CardContent>
        <div class="space-y-4">
          <div v-for="issue in issues" :key="issue.id" class="rounded-lg border p-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <div class="flex h-8 w-8 items-center justify-center rounded-full" :class="getIssueTypeClass(issue.type)">
                  <IssueIcon :type="issue.type" class="h-4 w-4" :class="getIssueTypeTextClass(issue.type)" />
                </div>
                <h3 class="text-sm font-medium">{{ issue.title }}</h3>
              </div>
              <Badge :variant="getIssuePriorityVariant(issue.priority)">{{ issue.priority }}</Badge>
            </div>
            <p class="mt-2 text-xs text-muted-foreground">{{ issue.description }}</p>
            <div class="mt-4 flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <Avatar class="h-6 w-6">
                  <AvatarImage v-if="issue.reportedBy.avatar" :src="issue.reportedBy.avatar" />
                  <AvatarFallback>{{ getInitials(issue.reportedBy.name) }}</AvatarFallback>
                </Avatar>
                <span class="text-xs text-muted-foreground">Reportado por {{ issue.reportedBy.name }}</span>
              </div>
              <span class="text-xs text-muted-foreground">{{ formatDate(issue.reportedDate) }}</span>
            </div>
            <div class="mt-4 flex space-x-2">
              <Button variant="outline" size="sm">Resolver</Button>
              <Button variant="outline" size="sm">Escalar</Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, h } from 'vue'
import { Users, CheckSquare, AlertCircle, BarChart, Calendar, Link, Edit, Plus, AlertTriangle, Bug, HelpCircle } from 'lucide-vue-next'

// Dados simulados
const teamMembersCount = ref(0)
const assignedTasksCount = ref(0)
const overdueTasksCount = ref(0)
const productivityRate = ref(0)
const teamMembers = ref([])
const taskStatusDistribution = ref([])
const taskDistributionByMember = ref([])
const totalTeamTasks = ref(0)
const upcomingMeetings = ref([])
const issues = ref([])

// Componente para ícone de problema
const IssueIcon = (props) => {
  const iconMap = {
    'bug': Bug,
    'impedimento': AlertTriangle,
    'duvida': HelpCircle
  }
  return h(iconMap[props.type] || HelpCircle)
}

// Formatação de data
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date)
}

// Formatação de hora
const formatTime = (timeString) => {
  const [hours, minutes] = timeString.split(':')
  return `${hours}:${minutes}`
}

// Obter iniciais do nome
const getInitials = (name) => {
  return name
    .split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2)
}

// Classes para desempenho
const getPerformanceColorClass = (performance) => {
  if (performance < 50) return 'bg-red-500'
  if (performance < 75) return 'bg-yellow-500'
  return 'bg-green-500'
}

// Variante para desempenho
const getPerformanceVariant = (performance) => {
  if (performance < 50) return 'destructive'
  if (performance < 75) return 'warning'
  return 'success'
}

// Classes para tipo de problema
const getIssueTypeClass = (type) => {
  switch (type) {
    case 'bug': return 'bg-red-100 dark:bg-red-900/20'
    case 'impedimento': return 'bg-yellow-100 dark:bg-yellow-900/20'
    case 'duvida': return 'bg-blue-100 dark:bg-blue-900/20'
    default: return 'bg-gray-100 dark:bg-gray-800'
  }
}

const getIssueTypeTextClass = (type) => {
  switch (type) {
    case 'bug': return 'text-red-500 dark:text-red-400'
    case 'impedimento': return 'text-yellow-500 dark:text-yellow-400'
    case 'duvida': return 'text-blue-500 dark:text-blue-400'
    default: return 'text-gray-500 dark:text-gray-400'
  }
}

// Variante para prioridade de problema
const getIssuePriorityVariant = (priority) => {
  switch (priority) {
    case 'Alta': return 'destructive'
    case 'Média': return 'warning'
    case 'Baixa': return 'secondary'
    default: return 'outline'
  }
}

onMounted(async () => {
  try {
    // Aqui faríamos chamadas à API para buscar os dados reais
    // Por enquanto, vamos simular com dados estáticos
    teamMembersCount.value = 8
    assignedTasksCount.value = 32
    overdueTasksCount.value = 5
    productivityRate.value = 78
    
    // Membros da equipe simulados
    teamMembers.value = [
      { id: 1, name: 'Ana Silva', role: 'Desenvolvedora Frontend', performance: 85, completedTasks: 17, totalTasks: 20, hoursLogged: 38, avatar: null },
      { id: 2, name: 'Carlos Oliveira', role: 'Desenvolvedor Backend', performance: 92, completedTasks: 23, totalTasks: 25, hoursLogged: 42, avatar: null },
      { id: 3, name: 'Mariana Santos', role: 'Designer UX/UI', performance: 78, completedTasks: 14, totalTasks: 18, hoursLogged: 36, avatar: null },
      { id: 4, name: 'Roberto Almeida', role: 'Desenvolvedor Mobile', performance: 65, completedTasks: 13, totalTasks: 20, hoursLogged: 32, avatar: null },
      { id: 5, name: 'Juliana Costa', role: 'QA Tester', performance: 88, completedTasks: 22, totalTasks: 25, hoursLogged: 40, avatar: null },
      { id: 6, name: 'Fernando Gomes', role: 'DevOps', performance: 75, completedTasks: 15, totalTasks: 20, hoursLogged: 35, avatar: null },
      { id: 7, name: 'Patrícia Lima', role: 'Desenvolvedora Frontend', performance: 45, completedTasks: 9, totalTasks: 20, hoursLogged: 28, avatar: null },
      { id: 8, name: 'Lucas Martins', role: 'Desenvolvedor Backend', performance: 82, completedTasks: 18, totalTasks: 22, hoursLogged: 39, avatar: null }
    ]
    
    // Distribuição de status de tarefas simulada
    taskStatusDistribution.value = [
      { name: 'Concluídas', count: 78, percentage: 61, bgClass: 'bg-green-100 dark:bg-green-900/20', textClass: 'text-green-500 dark:text-green-400' },
      { name: 'Em Andamento', count: 32, percentage: 25, bgClass: 'bg-blue-100 dark:bg-blue-900/20', textClass: 'text-blue-500 dark:text-blue-400' },
      { name: 'Pendentes', count: 12, percentage: 9, bgClass: 'bg-yellow-100 dark:bg-yellow-900/20', textClass: 'text-yellow-500 dark:text-yellow-400' },
      { name: 'Atrasadas', count: 6, percentage: 5, bgClass: 'bg-red-100 dark:bg-red-900/20', textClass: 'text-red-500 dark:text-red-400' }
    ]
    
    // Distribuição de tarefas por membro simulada
    totalTeamTasks.value = 128
    taskDistributionByMember.value = [
      { id: 1, name: 'Ana Silva', taskCount: 20 },
      { id: 2, name: 'Carlos Oliveira', taskCount: 25 },
      { id: 3, name: 'Mariana Santos', taskCount: 18 },
      { id: 4, name: 'Roberto Almeida', taskCount: 20 },
      { id: 5, name: 'Juliana Costa', taskCount: 25 },
      { id: 6, name: 'Fernando Gomes', taskCount: 20 }
    ]
    
    // Reuniões próximas simuladas
    upcomingMeetings.value = [
      { id: 1, title: 'Daily Scrum', description: 'Reunião diária de acompanhamento', date: '2025-05-28', startTime: '09:00', endTime: '09:15', attendees: 8 },
      { id: 2, title: 'Revisão de Sprint', description: 'Apresentação do progresso da sprint atual', date: '2025-05-30', startTime: '14:00', endTime: '15:00', attendees: 12 },
      { id: 3, title: 'Planejamento Técnico', description: 'Discussão sobre arquitetura e tecnologias', date: '2025-06-01', startTime: '10:30', endTime: '12:00', attendees: 6 }
    ]
    
    // Problemas e impedimentos simulados
    issues.value = [
      { id: 1, title: 'Erro na integração com API externa', description: 'A API de pagamentos está retornando erro 500 intermitentemente', type: 'bug', priority: 'Alta', reportedBy: { name: 'Carlos Oliveira', avatar: null }, reportedDate: '2025-05-26' },
      { id: 2, title: 'Acesso ao ambiente de homologação', description: 'Precisamos de acesso ao ambiente de homologação para testar as novas funcionalidades', type: 'impedimento', priority: 'Média', reportedBy: { name: 'Juliana Costa', avatar: null }, reportedDate: '2025-05-25' },
      { id: 3, title: 'Dúvida sobre requisitos do módulo financeiro', description: 'Não está claro como deve funcionar o cálculo de juros no sistema', type: 'duvida', priority: 'Baixa', reportedBy: { name: 'Ana Silva', avatar: null }, reportedDate: '2025-05-24' }
    ]
    
  } catch (error) {
    console.error('Erro ao carregar dados do dashboard de líder de equipe:', error)
  }
})
</script>
