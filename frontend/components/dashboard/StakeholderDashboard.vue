<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold">Dashboard do Stakeholder</h1>
      <p class="text-muted-foreground">Visão geral dos projetos e seu progresso</p>
    </div>

    <!-- Resumo dos Projetos -->
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Projetos Ativos</CardTitle>
          <Briefcase class="h-5 w-5 text-blue-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ activeProjects }}</div>
          <p class="text-xs text-muted-foreground">Projetos em andamento</p>
        </CardContent>
        <CardFooter>
          <NuxtLink to="/projetos" class="text-xs text-muted-foreground hover:text-primary">
            Ver projetos →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Marcos Concluídos</CardTitle>
          <Flag class="h-5 w-5 text-green-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ completedMilestones }}</div>
          <p class="text-xs text-muted-foreground">De {{ totalMilestones }} marcos planejados</p>
        </CardContent>
        <CardFooter>
          <NuxtLink to="/marcos" class="text-xs text-muted-foreground hover:text-primary">
            Ver marcos →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Aprovações Pendentes</CardTitle>
          <ClipboardCheck class="h-5 w-5 text-yellow-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ pendingApprovals }}</div>
          <p class="text-xs text-muted-foreground">Itens aguardando aprovação</p>
        </CardContent>
        <CardFooter>
          <NuxtLink to="/aprovacoes" class="text-xs text-muted-foreground hover:text-primary">
            Ver aprovações →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle class="text-sm font-medium">Riscos Identificados</CardTitle>
          <AlertTriangle class="h-5 w-5 text-red-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ identifiedRisks }}</div>
          <p class="text-xs text-muted-foreground">Riscos que precisam de atenção</p>
        </CardContent>
        <CardFooter>
          <NuxtLink to="/riscos" class="text-xs text-muted-foreground hover:text-primary">
            Ver riscos →
          </NuxtLink>
        </CardFooter>
      </Card>
    </div>

    <!-- Status dos Projetos -->
    <Card class="mt-8">
      <CardHeader>
        <CardTitle>Status dos Projetos</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="space-y-6">
          <div v-for="project in projects" :key="project.id" class="space-y-2">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-medium">{{ project.name }}</h3>
              <Badge :variant="getProjectStatusVariant(project.status)">{{ project.status }}</Badge>
            </div>
            <div class="space-y-1">
              <div class="flex items-center justify-between text-xs">
                <span>Progresso</span>
                <span>{{ project.progress }}%</span>
              </div>
              <div class="h-2 w-full rounded-full bg-muted">
                <div 
                  class="h-2 rounded-full" 
                  :class="getProgressColorClass(project.progress)"
                  :style="{ width: `${project.progress}%` }"
                ></div>
              </div>
            </div>
            <div class="space-y-1">
              <div class="flex items-center justify-between text-xs">
                <span>Orçamento</span>
                <span>{{ formatCurrency(project.budget.spent) }} de {{ formatCurrency(project.budget.total) }}</span>
              </div>
              <div class="h-2 w-full rounded-full bg-muted">
                <div 
                  class="h-2 rounded-full" 
                  :class="getBudgetColorClass(project.budget.spent, project.budget.total)"
                  :style="{ width: `${(project.budget.spent / project.budget.total) * 100}%` }"
                ></div>
              </div>
            </div>
            <div class="flex items-center justify-between text-xs text-muted-foreground">
              <span>Início: {{ formatDate(project.startDate) }}</span>
              <span>Prazo: {{ formatDate(project.endDate) }}</span>
            </div>
            <div class="mt-2">
              <NuxtLink :to="`/projetos/${project.id}`">
                <Button variant="outline" size="sm">Ver detalhes</Button>
              </NuxtLink>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Aprovações Pendentes e Próximos Marcos -->
    <div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
      <!-- Aprovações Pendentes -->
      <Card>
        <CardHeader>
          <CardTitle>Aprovações Pendentes</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div v-for="approval in pendingApprovalItems" :key="approval.id" class="flex items-start space-x-4">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                <ApprovalTypeIcon :type="approval.type" class="h-5 w-5 text-primary" />
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium">{{ approval.title }}</p>
                  <Badge variant="outline">{{ approval.project }}</Badge>
                </div>
                <p class="text-xs text-muted-foreground">{{ approval.description }}</p>
                <p class="mt-1 text-xs text-muted-foreground">Solicitado em: {{ formatDate(approval.requestDate) }}</p>
                <div class="mt-2 flex space-x-2">
                  <Button variant="default" size="sm">Aprovar</Button>
                  <Button variant="outline" size="sm">Rejeitar</Button>
                  <Button variant="ghost" size="sm">Ver detalhes</Button>
                </div>
              </div>
            </div>
            <div v-if="pendingApprovalItems.length === 0" class="flex flex-col items-center justify-center py-8 text-center">
              <ClipboardCheck class="h-12 w-12 text-muted-foreground" />
              <p class="mt-4 text-sm font-semibold">Nenhuma aprovação pendente</p>
              <p class="mt-1 text-xs text-muted-foreground">Não há itens aguardando sua aprovação no momento.</p>
            </div>
          </div>
        </CardContent>
        <CardFooter v-if="pendingApprovalItems.length > 0">
          <NuxtLink to="/aprovacoes" class="text-sm text-muted-foreground hover:text-primary">
            Ver todas as aprovações →
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
            <div v-for="milestone in upcomingMilestones" :key="milestone.id" class="flex items-start space-x-4">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                <Flag class="h-5 w-5 text-primary" />
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium">{{ milestone.title }}</p>
                  <Badge :variant="getMilestoneVariant(milestone.daysLeft)">
                    {{ milestone.daysLeft }} dias
                  </Badge>
                </div>
                <p class="text-xs text-muted-foreground">{{ milestone.description }}</p>
                <div class="mt-2 flex items-center justify-between">
                  <p class="text-xs text-muted-foreground">Projeto: {{ milestone.project }}</p>
                  <p class="text-xs text-muted-foreground">{{ formatDate(milestone.date) }}</p>
                </div>
              </div>
            </div>
            <div v-if="upcomingMilestones.length === 0" class="flex flex-col items-center justify-center py-8 text-center">
              <Flag class="h-12 w-12 text-muted-foreground" />
              <p class="mt-4 text-sm font-semibold">Nenhum marco próximo</p>
              <p class="mt-1 text-xs text-muted-foreground">Não há marcos programados para o futuro próximo.</p>
            </div>
          </div>
        </CardContent>
        <CardFooter v-if="upcomingMilestones.length > 0">
          <NuxtLink to="/marcos" class="text-sm text-muted-foreground hover:text-primary">
            Ver todos os marcos →
          </NuxtLink>
        </CardFooter>
      </Card>
    </div>

    <!-- Relatório Financeiro -->
    <Card class="mt-8">
      <CardHeader>
        <CardTitle>Relatório Financeiro</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
          <div class="rounded-lg border p-4">
            <h3 class="text-sm font-medium">Orçamento Total</h3>
            <div class="mt-2 text-2xl font-bold">{{ formatCurrency(financialSummary.totalBudget) }}</div>
            <p class="text-xs text-muted-foreground">Orçamento aprovado para todos os projetos</p>
          </div>
          
          <div class="rounded-lg border p-4">
            <h3 class="text-sm font-medium">Gasto Atual</h3>
            <div class="mt-2 text-2xl font-bold">{{ formatCurrency(financialSummary.totalSpent) }}</div>
            <p class="text-xs text-muted-foreground">{{ financialSummary.spentPercentage }}% do orçamento total</p>
          </div>
          
          <div class="rounded-lg border p-4">
            <h3 class="text-sm font-medium">Economia Estimada</h3>
            <div class="mt-2 text-2xl font-bold">{{ formatCurrency(financialSummary.projectedSavings) }}</div>
            <p class="text-xs text-muted-foreground">Baseado no progresso atual</p>
          </div>
        </div>
        
        <div class="mt-6">
          <h3 class="mb-4 text-sm font-medium">Distribuição de Gastos por Categoria</h3>
          <div class="space-y-4">
            <div v-for="category in financialSummary.spendingByCategory" :key="category.name" class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-medium">{{ category.name }}</span>
                <span class="text-xs">{{ formatCurrency(category.amount) }} ({{ category.percentage }}%)</span>
              </div>
              <div class="h-2 w-full rounded-full bg-muted">
                <div 
                  class="h-2 rounded-full" 
                  :style="{ width: `${category.percentage}%`, backgroundColor: category.color }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
      <CardFooter>
        <NuxtLink to="/relatorios/financeiro" class="text-sm text-muted-foreground hover:text-primary">
          Ver relatório financeiro completo →
        </NuxtLink>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue'
import { Briefcase, Flag, ClipboardCheck, AlertTriangle, FileText, DollarSign, Clock } from 'lucide-vue-next'

// Dados simulados
const activeProjects = ref(0)
const completedMilestones = ref(0)
const totalMilestones = ref(0)
const pendingApprovals = ref(0)
const identifiedRisks = ref(0)
const projects = ref([])
const pendingApprovalItems = ref([])
const upcomingMilestones = ref([])
const financialSummary = ref({
  totalBudget: 0,
  totalSpent: 0,
  spentPercentage: 0,
  projectedSavings: 0,
  spendingByCategory: []
})

// Componente para ícone de tipo de aprovação
const ApprovalTypeIcon = (props) => {
  const iconMap = {
    'documento': FileText,
    'orcamento': DollarSign,
    'prazo': Clock
  }
  return h(iconMap[props.type] || FileText)
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

// Formatação de moeda
const formatCurrency = (value) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

// Classes para progresso
const getProgressColorClass = (progress) => {
  if (progress < 30) return 'bg-red-500'
  if (progress < 70) return 'bg-yellow-500'
  return 'bg-green-500'
}

// Classes para orçamento
const getBudgetColorClass = (spent, total) => {
  const percentage = (spent / total) * 100
  if (percentage > 90) return 'bg-red-500'
  if (percentage > 75) return 'bg-yellow-500'
  return 'bg-green-500'
}

// Variante para status de projeto
const getProjectStatusVariant = (status) => {
  switch (status) {
    case 'Em Dia': return 'success'
    case 'Atenção': return 'warning'
    case 'Atrasado': return 'destructive'
    case 'Em Planejamento': return 'secondary'
    case 'Concluído': return 'default'
    default: return 'outline'
  }
}

// Variante para marcos
const getMilestoneVariant = (daysLeft) => {
  if (daysLeft <= 7) return 'destructive'
  if (daysLeft <= 14) return 'warning'
  return 'outline'
}

onMounted(async () => {
  try {
    // Aqui faríamos chamadas à API para buscar os dados reais
    // Por enquanto, vamos simular com dados estáticos
    activeProjects.value = 4
    completedMilestones.value = 12
    totalMilestones.value = 20
    pendingApprovals.value = 3
    identifiedRisks.value = 5
    
    // Projetos simulados
    projects.value = [
      { 
        id: 1, 
        name: 'Sistema ERP', 
        status: 'Em Dia', 
        progress: 75, 
        startDate: '2025-01-15', 
        endDate: '2025-06-30',
        budget: { total: 250000, spent: 175000 }
      },
      { 
        id: 2, 
        name: 'Aplicativo Mobile', 
        status: 'Atenção', 
        progress: 45, 
        startDate: '2025-02-10', 
        endDate: '2025-07-15',
        budget: { total: 120000, spent: 65000 }
      },
      { 
        id: 3, 
        name: 'Portal do Cliente', 
        status: 'Em Dia', 
        progress: 90, 
        startDate: '2025-03-01', 
        endDate: '2025-05-30',
        budget: { total: 80000, spent: 72000 }
      },
      { 
        id: 4, 
        name: 'Integração de APIs', 
        status: 'Atrasado', 
        progress: 30, 
        startDate: '2025-04-05', 
        endDate: '2025-08-20',
        budget: { total: 60000, spent: 25000 }
      }
    ]
    
    // Aprovações pendentes simuladas
    pendingApprovalItems.value = [
      { id: 1, title: 'Especificação Técnica', description: 'Documento de especificação técnica para o módulo financeiro', type: 'documento', project: 'Sistema ERP', requestDate: '2025-05-25' },
      { id: 2, title: 'Aumento de Orçamento', description: 'Solicitação de aumento de orçamento para desenvolvimento mobile', type: 'orcamento', project: 'Aplicativo Mobile', requestDate: '2025-05-24' },
      { id: 3, title: 'Extensão de Prazo', description: 'Solicitação de extensão de prazo para entrega da integração', type: 'prazo', project: 'Integração de APIs', requestDate: '2025-05-23' }
    ]
    
    // Marcos próximos simulados
    upcomingMilestones.value = [
      { id: 1, title: 'Entrega do Módulo Financeiro', description: 'Finalização do módulo de gestão financeira', project: 'Sistema ERP', date: '2025-06-15', daysLeft: 20 },
      { id: 2, title: 'Lançamento Beta', description: 'Versão beta para testes com usuários selecionados', project: 'Aplicativo Mobile', date: '2025-06-01', daysLeft: 5 },
      { id: 3, title: 'Apresentação para Stakeholders', description: 'Demonstração do progresso para os stakeholders', project: 'Portal do Cliente', date: '2025-05-30', daysLeft: 3 },
      { id: 4, title: 'Finalização da Documentação', description: 'Entrega da documentação técnica completa', project: 'Integração de APIs', date: '2025-07-10', daysLeft: 45 }
    ]
    
    // Resumo financeiro simulado
    financialSummary.value = {
      totalBudget: 510000,
      totalSpent: 337000,
      spentPercentage: 66,
      projectedSavings: 35000,
      spendingByCategory: [
        { name: 'Desenvolvimento', amount: 185000, percentage: 55, color: '#3b82f6' },
        { name: 'Design', amount: 68000, percentage: 20, color: '#10b981' },
        { name: 'Infraestrutura', amount: 50000, percentage: 15, color: '#8b5cf6' },
        { name: 'Testes e QA', amount: 34000, percentage: 10, color: '#f59e0b' }
      ]
    }
    
  } catch (error) {
    console.error('Erro ao carregar dados do dashboard de stakeholder:', error)
  }
})
</script>
