<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold">Dashboard</h1>
      <p class="text-muted-foreground">
        Bem-vindo ao seu painel de controle, {{ userName }}
      </p>
    </div>

    <!-- Usar o componente RoleBasedDashboard para exibir o dashboard apropriado com base no papel do usuário -->
    <RoleBasedDashboard />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, shallowRef } from 'vue';
import { useRouter } from 'vue-router'; // or 'nuxt/app' for Nuxt 3
import { useNuxtApp } from '#app';
import RoleBasedDashboard from '~/components/dashboard/RoleBasedDashboard.vue';

// Shadcn-vue components (auto-imported by Nuxt if in components/ui directory)
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

// Lucide Icons
import {
  Briefcase,
  ListChecks,
  Users,
  AlertTriangle,
  FolderKanban,
  ClipboardCheck,
  MessageSquare, // For MENSAGEM
  ShieldAlert, // For ALERTA
  Cog, // For SISTEMA
  BellOff,
} from 'lucide-vue-next';

const router = useRouter();
const { $api } = useNuxtApp();

const userName = ref('Usuário');
const projetosCount = ref(0);
const tarefasCount = ref(0);
const equipesCount = ref(0);
const riscosCount = ref(0);
const projetos = ref([]);
const todasTarefas = ref([]); // Store all tasks
const notificacoes = ref([]);

// Computed property for pending tasks
const tarefasPendentes = computed(() => {
  // Assuming tasks have a 'status' property, e.g., 'PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA'
  // Adjust this filter based on your actual task status values
  return todasTarefas.value.filter(
    (tarefa) =>
      tarefa.status?.toUpperCase() !== 'CONCLUÍDA' &&
      tarefa.status?.toUpperCase() !== 'FINALIZADA'
  );
});

// Computed property for unread notifications
const notificacoesNaoLidas = computed(() => {
  return notificacoes.value.filter((n) => !n.lida);
});

// Formatar data
const formatDate = (dateString) => {
  if (!dateString) return 'Sem data';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(date);
};

// Obter variant para Badge de prioridade
const getPrioridadeVariant = (prioridade) => {
  switch (prioridade?.toUpperCase()) {
    case 'ALTA':
      return 'destructive';
    case 'MÉDIA': // Shadcn 'warning' variant might be yellow-ish, or use 'default' with custom CSS if needed
      return 'warning'; // Or 'default' and style it if 'warning' is not suitable
    case 'BAIXA':
      return 'outline'; // Or 'secondary' or 'success' (if green is desired)
    default:
      return 'secondary';
  }
};

// Get Lucide icon component for notification type
const getNotificacaoIcon = (tipo) => {
  switch (tipo?.toUpperCase()) {
    case 'MENSAGEM':
      return shallowRef(MessageSquare);
    case 'ALERTA':
      return shallowRef(ShieldAlert);
    case 'SISTEMA':
      return shallowRef(Cog);
    default:
      return shallowRef(MessageSquare); // Default icon
  }
};
// Get Avatar background class (optional, for visual distinction)
const getNotificacaoAvatarClass = (tipo) => {
  switch (tipo?.toUpperCase()) {
    case 'MENSAGEM':
      return 'bg-blue-100 dark:bg-blue-800 text-blue-600 dark:text-blue-300';
    case 'ALERTA':
      return 'bg-yellow-100 dark:bg-yellow-800 text-yellow-600 dark:text-yellow-300';
    case 'SISTEMA':
      return 'bg-purple-100 dark:bg-purple-800 text-purple-600 dark:text-purple-300';
    default:
      return 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300';
  }
};

// Marcar notificação como lida
const marcarComoLida = async (id) => {
  try {
    await $api.patch(`/api/communications/${id}/`, {
      status: 'LIDA', // Or whatever your API expects for 'read'
    });
    // Re-fetch or update local state
    const index = notificacoes.value.findIndex((n) => n.id === id);
    if (index !== -1) {
      notificacoes.value[index].lida = true;
      notificacoes.value[index].status = 'LIDA'; // Also update status if your filter relies on it
    }
  } catch (error) {
    console.error('Erro ao marcar notificação como lida:', error);
  }
};

const openNewProjectModal = () => {
  router.push('/projetos?new=true');
};

const openNewTaskModal = () => {
  router.push('/tarefas?new=true');
};

onMounted(async () => {
  try {
    const userResponse = await $api.get('/api/auth/users/me/');
    userName.value = userResponse.data.full_name || userResponse.data.username;

    // --- Projetos ---
    const projetosResponse = await $api.get('/api/projects/');
    if (projetosResponse.data.results) {
      // Paginated
      projetosCount.value = projetosResponse.data.count;
      projetos.value = projetosResponse.data.results;
    } else {
      // Not paginated
      projetosCount.value = projetosResponse.data.length;
      projetos.value = projetosResponse.data;
    }

    // --- Tarefas ---
    // Fetch all tasks and then filter for pending ones using the computed property
    const tarefasResponse = await $api.get('/api/tasks/'); // Endpoint for ALL tasks
    if (tarefasResponse.data.results) {
      tarefasCount.value = tarefasResponse.data.count; // This might be total tasks, not just pending
      todasTarefas.value = tarefasResponse.data.results;
    } else {
      tarefasCount.value = tarefasResponse.data.length;
      todasTarefas.value = tarefasResponse.data;
    }
    // You might want a separate count for pending tasks displayed on the summary card
    // For simplicity, I'm using the total count here. Or you could fetch /api/tasks/?status=PENDENTE for the count.

    // --- Equipes ---
    const equipesResponse = await $api.get('/api/teams/');
    equipesCount.value =
      equipesResponse.data.count ?? equipesResponse.data.length;

    // --- Riscos ---
    const riscosResponse = await $api.get('/api/risks/');
    riscosCount.value = riscosResponse.data.count ?? riscosResponse.data.length;

    // --- Notificações ---
    // Fetch all notifications and filter in computed, or fetch only unread
    // const notificacoesResponse = await $api.get('/api/communications/?status=NAO_LIDA') // Example: fetch only unread
    const notificacoesResponse = await $api.get('/api/communications/'); // Fetch all
    if (notificacoesResponse.data.results) {
      notificacoes.value = notificacoesResponse.data.results.map((n) => ({
        ...n,
        lida: n.status === 'LIDA',
      }));
    } else {
      notificacoes.value = notificacoesResponse.data.map((n) => ({
        ...n,
        lida: n.status === 'LIDA',
      }));
    }
  } catch (error) {
    console.error('Erro ao carregar dados do dashboard:', error);
    // Fallback data for demonstration
    userName.value = 'Usuário Exemplo';
    projetosCount.value = 2;
    projetos.value = [
      { id: 1, nome: 'Sistema de Gestão Exemplo', status: 'Em andamento' },
      { id: 2, nome: 'App Mobile Exemplo', status: 'Planejamento' },
    ];
    tarefasCount.value = 3; // Total tasks
    todasTarefas.value = [
      {
        id: 1,
        titulo: 'API REST Exemplo',
        prazo: '2025-07-15',
        prioridade: 'ALTA',
        status: 'PENDENTE',
      },
      {
        id: 2,
        titulo: 'UI Design Exemplo',
        prazo: '2025-07-20',
        prioridade: 'MÉDIA',
        status: 'PENDENTE',
      },
      {
        id: 3,
        titulo: 'Documentação Exemplo',
        prazo: '2025-06-30',
        prioridade: 'BAIXA',
        status: 'CONCLUÍDA',
      },
    ];
    equipesCount.value = 1;
    riscosCount.value = 0;
    notificacoes.value = [
      {
        id: 1,
        tipo: 'MENSAGEM',
        titulo: 'Nova Mensagem Exemplo',
        mensagem: 'Confira os detalhes.',
        data: '2025-07-01',
        lida: false,
        status: 'NAO_LIDA',
      },
      {
        id: 2,
        tipo: 'ALERTA',
        titulo: 'Alerta de Prazo Exemplo',
        mensagem: 'Tarefa X está próxima do prazo.',
        data: '2025-06-28',
        lida: true,
        status: 'LIDA',
      },
    ];
  }
});
</script>

<style scoped>
/* You can add minimal scoped styles here if absolutely necessary,
   but prefer Tailwind and shadcn-vue defaults. */
</style>
