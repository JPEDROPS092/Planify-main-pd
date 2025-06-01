<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold">Dashboard do Auditor</h1>
      <p class="text-muted-foreground">
        Visão geral de auditorias, conformidade e riscos
      </p>
    </div>

    <!-- Resumo de Auditoria -->
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Projetos Auditados</CardTitle>
          <ClipboardCheck class="h-5 w-5 text-blue-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ auditedProjects }}</div>
          <p class="text-xs text-muted-foreground">
            De {{ totalProjects }} projetos ativos
          </p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/auditorias/projetos"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver detalhes →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium">Não Conformidades</CardTitle>
          <AlertTriangle class="h-5 w-5 text-red-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ nonCompliance }}</div>
          <p class="text-xs text-muted-foreground">Problemas identificados</p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/auditorias/nao-conformidades"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver lista →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium"
            >Auditorias Pendentes</CardTitle
          >
          <Calendar class="h-5 w-5 text-yellow-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ pendingAudits }}</div>
          <p class="text-xs text-muted-foreground">Auditorias programadas</p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/auditorias/agenda"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver agenda →
          </NuxtLink>
        </CardFooter>
      </Card>

      <Card>
        <CardHeader
          class="flex flex-row items-center justify-between space-y-0 pb-2"
        >
          <CardTitle class="text-sm font-medium"
            >Taxa de Conformidade</CardTitle
          >
          <BarChart class="h-5 w-5 text-green-500" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ complianceRate }}%</div>
          <p class="text-xs text-muted-foreground">
            Média de todos os projetos
          </p>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/auditorias/relatorios"
            class="text-xs text-muted-foreground hover:text-primary"
          >
            Ver relatórios →
          </NuxtLink>
        </CardFooter>
      </Card>
    </div>

    <!-- Conformidade por Projeto -->
    <Card class="mt-8">
      <CardHeader>
        <CardTitle>Conformidade por Projeto</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="space-y-6">
          <div
            v-for="project in projectCompliance"
            :key="project.id"
            class="space-y-2"
          >
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-medium">{{ project.name }}</h3>
              <Badge :variant="getComplianceVariant(project.complianceRate)">
                {{ project.complianceRate }}%
              </Badge>
            </div>
            <div class="h-2 w-full rounded-full bg-muted">
              <div
                class="h-2 rounded-full"
                :class="getComplianceColorClass(project.complianceRate)"
                :style="{ width: `${project.complianceRate}%` }"
              ></div>
            </div>
            <div
              class="flex items-center justify-between text-xs text-muted-foreground"
            >
              <span
                >{{ project.compliantItems }} de {{ project.totalItems }} itens
                em conformidade</span
              >
              <span
                >Última auditoria: {{ formatDate(project.lastAuditDate) }}</span
              >
            </div>
            <div class="mt-2">
              <NuxtLink :to="`/auditorias/projetos/${project.id}`">
                <Button variant="outline" size="sm">Ver detalhes</Button>
              </NuxtLink>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Não Conformidades e Próximas Auditorias -->
    <div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
      <!-- Não Conformidades Recentes -->
      <Card>
        <CardHeader>
          <CardTitle>Não Conformidades Recentes</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div
              v-for="issue in recentNonCompliance"
              :key="issue.id"
              class="flex items-start space-x-4"
            >
              <div
                class="flex h-10 w-10 items-center justify-center rounded-full"
                :class="getSeverityBgClass(issue.severity)"
              >
                <SeverityIcon
                  :severity="issue.severity"
                  class="h-5 w-5"
                  :class="getSeverityTextClass(issue.severity)"
                />
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium">{{ issue.title }}</p>
                  <Badge :variant="getSeverityVariant(issue.severity)">{{
                    issue.severity
                  }}</Badge>
                </div>
                <p class="text-xs text-muted-foreground">
                  {{ issue.description }}
                </p>
                <div class="mt-2 flex items-center justify-between">
                  <p class="text-xs text-muted-foreground">
                    Projeto: {{ issue.project }}
                  </p>
                  <p class="text-xs text-muted-foreground">
                    Identificado em: {{ formatDate(issue.identifiedDate) }}
                  </p>
                </div>
                <div class="mt-2 flex space-x-2">
                  <Button variant="outline" size="sm"
                    >Verificar Resolução</Button
                  >
                  <Button variant="outline" size="sm">Atualizar Status</Button>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/auditorias/nao-conformidades"
            class="text-sm text-muted-foreground hover:text-primary"
          >
            Ver todas as não conformidades →
          </NuxtLink>
        </CardFooter>
      </Card>

      <!-- Próximas Auditorias -->
      <Card>
        <CardHeader>
          <CardTitle>Próximas Auditorias</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div
              v-for="audit in upcomingAudits"
              :key="audit.id"
              class="flex items-start space-x-4"
            >
              <div
                class="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10"
              >
                <Calendar class="h-5 w-5 text-primary" />
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium">{{ audit.title }}</p>
                  <Badge :variant="getAuditTypeVariant(audit.type)">{{
                    audit.type
                  }}</Badge>
                </div>
                <p class="text-xs text-muted-foreground">
                  {{ audit.description }}
                </p>
                <div class="mt-2 flex items-center justify-between">
                  <p class="text-xs text-muted-foreground">
                    Projeto: {{ audit.project }}
                  </p>
                  <p class="text-xs text-muted-foreground">
                    Data: {{ formatDate(audit.date) }}
                  </p>
                </div>
                <div class="mt-2 flex space-x-2">
                  <Button variant="outline" size="sm"
                    >Preparar Checklist</Button
                  >
                  <Button variant="outline" size="sm">Reagendar</Button>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <NuxtLink
            to="/auditorias/agenda"
            class="text-sm text-muted-foreground hover:text-primary"
          >
            Ver agenda completa →
          </NuxtLink>
        </CardFooter>
      </Card>
    </div>

    <!-- Relatório de Riscos -->
    <Card class="mt-8">
      <CardHeader>
        <CardTitle>Relatório de Riscos</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
          <!-- Distribuição de Riscos por Categoria -->
          <div>
            <h3 class="mb-4 text-sm font-medium">
              Distribuição de Riscos por Categoria
            </h3>
            <div class="space-y-4">
              <div
                v-for="category in risksByCategory"
                :key="category.name"
                class="space-y-2"
              >
                <div class="flex items-center justify-between">
                  <span class="text-xs font-medium">{{ category.name }}</span>
                  <span class="text-xs"
                    >{{ category.count }} riscos ({{
                      category.percentage
                    }}%)</span
                  >
                </div>
                <div class="h-2 w-full rounded-full bg-muted">
                  <div
                    class="h-2 rounded-full"
                    :style="{
                      width: `${category.percentage}%`,
                      backgroundColor: category.color,
                    }"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Distribuição de Riscos por Severidade -->
          <div>
            <h3 class="mb-4 text-sm font-medium">
              Distribuição de Riscos por Severidade
            </h3>
            <div class="grid grid-cols-3 gap-4">
              <div
                v-for="severity in risksBySeverity"
                :key="severity.level"
                class="flex flex-col items-center justify-center rounded-lg border p-4 text-center"
              >
                <div
                  class="flex h-12 w-12 items-center justify-center rounded-full"
                  :class="getSeverityBgClass(severity.level)"
                >
                  <div
                    class="text-lg font-bold"
                    :class="getSeverityTextClass(severity.level)"
                  >
                    {{ severity.count }}
                  </div>
                </div>
                <h3 class="mt-2 text-sm font-medium">{{ severity.level }}</h3>
                <p class="text-xs text-muted-foreground">
                  {{ severity.percentage }}% do total
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Riscos de Alta Severidade -->
        <div class="mt-6">
          <h3 class="mb-4 text-sm font-medium">Riscos de Alta Severidade</h3>
          <div class="space-y-4">
            <div
              v-for="risk in highSeverityRisks"
              :key="risk.id"
              class="rounded-lg border p-4"
            >
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-medium">{{ risk.title }}</h3>
                <Badge variant="destructive">Alta</Badge>
              </div>
              <p class="mt-2 text-xs text-muted-foreground">
                {{ risk.description }}
              </p>
              <div class="mt-4 flex items-center justify-between">
                <div>
                  <p class="text-xs text-muted-foreground">
                    Projeto: {{ risk.project }}
                  </p>
                  <p class="text-xs text-muted-foreground">
                    Categoria: {{ risk.category }}
                  </p>
                </div>
                <Button variant="outline" size="sm"
                  >Ver Plano de Mitigação</Button
                >
              </div>
            </div>
          </div>
        </div>
      </CardContent>
      <CardFooter>
        <NuxtLink
          to="/auditorias/riscos"
          class="text-sm text-muted-foreground hover:text-primary"
        >
          Ver relatório de riscos completo →
        </NuxtLink>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue';
import {
  ClipboardCheck,
  AlertTriangle,
  Calendar,
  BarChart,
  AlertCircle,
  AlertOctagon,
  HelpCircle,
} from 'lucide-vue-next';

// Dados simulados
const auditedProjects = ref(0);
const totalProjects = ref(0);
const nonCompliance = ref(0);
const pendingAudits = ref(0);
const complianceRate = ref(0);
const projectCompliance = ref([]);
const recentNonCompliance = ref([]);
const upcomingAudits = ref([]);
const risksByCategory = ref([]);
const risksBySeverity = ref([]);
const highSeverityRisks = ref([]);

// Componente para ícone de severidade
const SeverityIcon = (props) => {
  const iconMap = {
    Alta: AlertOctagon,
    Média: AlertTriangle,
    Baixa: AlertCircle,
  };
  return h(iconMap[props.severity] || HelpCircle);
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

// Classes para conformidade
const getComplianceColorClass = (rate) => {
  if (rate < 70) return 'bg-red-500';
  if (rate < 90) return 'bg-yellow-500';
  return 'bg-green-500';
};

// Variante para conformidade
const getComplianceVariant = (rate) => {
  if (rate < 70) return 'destructive';
  if (rate < 90) return 'warning';
  return 'success';
};

// Classes para severidade
const getSeverityBgClass = (severity) => {
  switch (severity) {
    case 'Alta':
      return 'bg-red-100 dark:bg-red-900/20';
    case 'Média':
      return 'bg-yellow-100 dark:bg-yellow-900/20';
    case 'Baixa':
      return 'bg-blue-100 dark:bg-blue-900/20';
    default:
      return 'bg-gray-100 dark:bg-gray-800';
  }
};

const getSeverityTextClass = (severity) => {
  switch (severity) {
    case 'Alta':
      return 'text-red-500 dark:text-red-400';
    case 'Média':
      return 'text-yellow-500 dark:text-yellow-400';
    case 'Baixa':
      return 'text-blue-500 dark:text-blue-400';
    default:
      return 'text-gray-500 dark:text-gray-400';
  }
};

// Variante para severidade
const getSeverityVariant = (severity) => {
  switch (severity) {
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

// Variante para tipo de auditoria
const getAuditTypeVariant = (type) => {
  switch (type) {
    case 'Completa':
      return 'default';
    case 'Parcial':
      return 'secondary';
    case 'Seguimento':
      return 'outline';
    default:
      return 'outline';
  }
};

onMounted(async () => {
  try {
    // Aqui faríamos chamadas à API para buscar os dados reais
    // Por enquanto, vamos simular com dados estáticos
    auditedProjects.value = 6;
    totalProjects.value = 8;
    nonCompliance.value = 14;
    pendingAudits.value = 5;
    complianceRate.value = 85;

    // Conformidade por projeto simulada
    projectCompliance.value = [
      {
        id: 1,
        name: 'Sistema ERP',
        complianceRate: 92,
        compliantItems: 46,
        totalItems: 50,
        lastAuditDate: '2025-05-15',
      },
      {
        id: 2,
        name: 'Aplicativo Mobile',
        complianceRate: 78,
        compliantItems: 39,
        totalItems: 50,
        lastAuditDate: '2025-05-10',
      },
      {
        id: 3,
        name: 'Portal do Cliente',
        complianceRate: 96,
        compliantItems: 48,
        totalItems: 50,
        lastAuditDate: '2025-05-05',
      },
      {
        id: 4,
        name: 'Integração de APIs',
        complianceRate: 64,
        compliantItems: 32,
        totalItems: 50,
        lastAuditDate: '2025-04-28',
      },
      {
        id: 5,
        name: 'Migração de Dados',
        complianceRate: 88,
        compliantItems: 44,
        totalItems: 50,
        lastAuditDate: '2025-04-20',
      },
      {
        id: 6,
        name: 'Sistema de BI',
        complianceRate: 94,
        compliantItems: 47,
        totalItems: 50,
        lastAuditDate: '2025-04-15',
      },
    ];

    // Não conformidades recentes simuladas
    recentNonCompliance.value = [
      {
        id: 1,
        title: 'Documentação incompleta',
        description:
          'A documentação técnica não inclui todos os requisitos de segurança',
        severity: 'Média',
        project: 'Aplicativo Mobile',
        identifiedDate: '2025-05-20',
      },
      {
        id: 2,
        title: 'Testes insuficientes',
        description:
          'Não há evidência de testes de carga e estresse no sistema',
        severity: 'Alta',
        project: 'Integração de APIs',
        identifiedDate: '2025-05-18',
      },
      {
        id: 3,
        title: 'Falta de logs de auditoria',
        description:
          'O sistema não registra logs de auditoria para operações críticas',
        severity: 'Alta',
        project: 'Sistema ERP',
        identifiedDate: '2025-05-15',
      },
      {
        id: 4,
        title: 'Controle de versão inadequado',
        description:
          'Não há um processo claro para controle de versão do código',
        severity: 'Baixa',
        project: 'Portal do Cliente',
        identifiedDate: '2025-05-12',
      },
    ];

    // Próximas auditorias simuladas
    upcomingAudits.value = [
      {
        id: 1,
        title: 'Auditoria de Segurança',
        description: 'Verificação de conformidade com políticas de segurança',
        type: 'Completa',
        project: 'Sistema ERP',
        date: '2025-06-10',
      },
      {
        id: 2,
        title: 'Revisão de Código',
        description: 'Análise de qualidade e segurança do código',
        type: 'Parcial',
        project: 'Aplicativo Mobile',
        date: '2025-06-05',
      },
      {
        id: 3,
        title: 'Verificação de Correções',
        description:
          'Verificar se as não conformidades anteriores foram corrigidas',
        type: 'Seguimento',
        project: 'Integração de APIs',
        date: '2025-05-30',
      },
      {
        id: 4,
        title: 'Auditoria de Processos',
        description: 'Verificação de aderência aos processos definidos',
        type: 'Completa',
        project: 'Migração de Dados',
        date: '2025-06-15',
      },
    ];

    // Riscos por categoria simulados
    risksByCategory.value = [
      { name: 'Segurança', count: 8, percentage: 32, color: '#ef4444' },
      { name: 'Técnico', count: 7, percentage: 28, color: '#3b82f6' },
      { name: 'Operacional', count: 5, percentage: 20, color: '#10b981' },
      { name: 'Compliance', count: 3, percentage: 12, color: '#8b5cf6' },
      { name: 'Financeiro', count: 2, percentage: 8, color: '#f59e0b' },
    ];

    // Riscos por severidade simulados
    risksBySeverity.value = [
      {
        level: 'Alta',
        count: 6,
        percentage: 24,
        bgClass: 'bg-red-100',
        textClass: 'text-red-500',
      },
      {
        level: 'Média',
        count: 12,
        percentage: 48,
        bgClass: 'bg-yellow-100',
        textClass: 'text-yellow-500',
      },
      {
        level: 'Baixa',
        count: 7,
        percentage: 28,
        bgClass: 'bg-blue-100',
        textClass: 'text-blue-500',
      },
    ];

    // Riscos de alta severidade simulados
    highSeverityRisks.value = [
      {
        id: 1,
        title: 'Vulnerabilidade de segurança crítica',
        description:
          'Identificada vulnerabilidade que pode permitir acesso não autorizado a dados sensíveis',
        project: 'Sistema ERP',
        category: 'Segurança',
      },
      {
        id: 2,
        title: 'Dependência de biblioteca obsoleta',
        description:
          'O sistema utiliza biblioteca sem suporte e com vulnerabilidades conhecidas',
        project: 'Aplicativo Mobile',
        category: 'Técnico',
      },
      {
        id: 3,
        title: 'Não conformidade com LGPD',
        description:
          'O sistema não atende a todos os requisitos da Lei Geral de Proteção de Dados',
        project: 'Portal do Cliente',
        category: 'Compliance',
      },
    ];
  } catch (error) {
    console.error('Erro ao carregar dados do dashboard de auditor:', error);
  }
});
</script>
