<template>
  </template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { storeToRefs } from 'pinia'; // Essencial para manter a reatividade
import { useProjectStore } from '~/stores/projects'; // Importa a nova store
import { useAuth } from '~/stores/auth'; // Mantém a store de autenticação
import { useNotification } from '~lib/composables/useNotification';

const router = useRouter();
const route = useRoute();
const projectStore = useProjectStore(); // Instancia a store
const { user } = useAuth();
const notification = useNotification();

// --- ESTADO LIDO DIRETAMENTE DA STORE ---
// storeToRefs garante que a reatividade seja mantida.
const {
  projects,
  loading,
  error,
  totalPages,
  currentPage,
  totalItems,
  users, // A lista de usuários agora também pode ser gerenciada pela store.
} = storeToRefs(projectStore);

// --- ESTADO LOCAL DO COMPONENTE (Filtros e Modais) ---
const searchQuery = ref('');
const statusFilter = ref('');
const priorityFilter = ref('');
const itemsPerPage = ref(9); // Pode ser movido para a store se for configurável

const showNewProjectModal = ref(false);
const newProject = ref({
  titulo: '',
  descricao: '',
  data_inicio: new Date().toISOString().split('T')[0],
  data_fim: '',
  status: 'PLANEJADO',
  prioridade: 'MEDIA',
  orcamento: 0,
  gerente: null,
});
const formErrors = ref({});
const isSubmitting = ref(false);

const showEditProjectModal = ref(false);
const editingProject = ref(null);

// --- COMPUTED PROPERTIES (Lógica de UI) ---
const userRole = computed(() => user?.role || 'viewer');
// As permissões continuam sendo uma lógica local do componente
const userCanCreate = computed(() => ['admin', 'manager'].includes(userRole.value));
const userCanEdit = computed(() => ['admin', 'manager', 'editor'].includes(userRole.value));
const userCanDelete = computed(() => ['admin', 'manager'].includes(userRole.value));

// Projetos filtrados - podemos manter esta lógica no componente para filtragem local
// ou usar os getters da store para filtragem no backend
const filteredProjects = computed(() => {
  if (!searchQuery.value && !statusFilter.value && !priorityFilter.value) {
    return projects.value;
  }

  return projects.value.filter((project) => {
    const matchesSearch = searchQuery.value
      ? project.titulo?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        project.descricao?.toLowerCase().includes(searchQuery.value.toLowerCase())
      : true;

    const matchesStatus = statusFilter.value
      ? project.status === statusFilter.value
      : true;

    const matchesPriority = priorityFilter.value
      ? project.prioridade === priorityFilter.value
      : true;

    return matchesSearch && matchesStatus && matchesPriority;
  });
});

const paginationRange = computed(() => {
  // Esta lógica é puramente de UI e pode permanecer aqui.
  const range = [];
  const maxVisiblePages = 5;
  if (totalPages.value <= maxVisiblePages) {
    for (let i = 1; i <= totalPages.value; i++) range.push(i);
  } else {
    let start = Math.max(1, currentPage.value - Math.floor(maxVisiblePages / 2));
    let end = Math.min(totalPages.value, start + maxVisiblePages - 1);
    if (end - start + 1 < maxVisiblePages) {
      start = Math.max(1, end - maxVisiblePages + 1);
    }
    for (let i = start; i <= end; i++) range.push(i);
  }
  return range;
});

// --- MÉTODOS QUE CHAMAM AÇÕES DA STORE ---

const fetchProjects = () => {
  // A complexidade agora está na store. O componente só informa os filtros.
  projectStore.fetchProjects({
    page: currentPage.value,
    search: searchQuery.value,
    status: statusFilter.value,
    prioridade: priorityFilter.value,
  });
};

const changePage = (page: number) => {
  if (page < 1 || page > totalPages.value) return;
  // A store gerencia a página atual e busca os dados
  projectStore.changePage(page);
};

const createProject = async () => {
  // Validação básica
  if (!newProject.value.titulo || !newProject.value.data_inicio || !newProject.value.status) {
    notification.error('Preencha todos os campos obrigatórios', {
      title: 'Erro',
      duration: 5000,
    });
    return;
  }

  isSubmitting.value = true;
  formErrors.value = {};
  try {
    // Preparar dados para o formato da API
    const projectData = {
      nome: newProject.value.titulo,
      descricao: newProject.value.descricao,
      data_inicio: newProject.value.data_inicio,
      data_fim: newProject.value.data_fim || null,
      status: newProject.value.status,
      prioridade: newProject.value.prioridade,
      gerente: newProject.value.gerente,
      orcamento: newProject.value.orcamento
    };

    // Usar a store para criar o projeto
    const created = await projectStore.createProject(projectData);
    showNewProjectModal.value = false;
    newProject.value = { /* resetar o form */ }; // Resetar o formulário
    notification.success('Projeto criado com sucesso!');
    router.push(`/projetos/${created.id}`);
  } catch (err) {
    formErrors.value = err.errors || {};
    notification.error('Erro ao criar projeto.');
  } finally {
    isSubmitting.value = false;
  }
};

const updateProject = async () => {
  if (!editingProject.value) return;
  isSubmitting.value = true;
  formErrors.value = {};
  try {
    await projectStore.updateProject(editingProject.value.id, editingProject.value);
    showEditProjectModal.value = false;
    editingProject.value = null;
    notification.success('Projeto atualizado com sucesso!');
  } catch (err) {
    formErrors.value = err.errors || {};
    notification.error('Erro ao atualizar projeto.');
  } finally {
    isSubmitting.value = false;
  }
};

const deleteProject = async (id: string) => {
  if (!confirm('Tem certeza que deseja excluir este projeto?')) return;
  try {
    await projectStore.deleteProject(id);
    notification.success('Projeto excluído com sucesso!');
  } catch (err) {
    notification.error('Erro ao excluir projeto.');
  }
};

// --- MÉTODOS DE UI E HELPERS ---

const openNewProjectModal = () => {
  // A store pode carregar os usuários se necessário
  projectStore.fetchUsersForSelect();
  showNewProjectModal.value = true;
};

const openEditProjectModal = async (project) => {
  // A store busca os detalhes completos do projeto para edição
  const projectDetails = await projectStore.fetchProjectById(project.id);
  if (projectDetails) {
    editingProject.value = { ...projectDetails };
    projectStore.fetchUsersForSelect();
    showEditProjectModal.value = true;
  } else {
    notification.error('Não foi possível carregar os dados do projeto para edição.');
  }
};

const viewProject = (id: string) => {
  router.push(`/projetos/${id}`);
};

const formatDate = (dateString: string) => {
  // Função helper permanece igual
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short' }).format(date);
};

const getStatusLabel = (status: string) => {
  const statusMap = { /* ... */ };
  return statusMap[status] || status;
};

const getPriorityLabel = (priority: string) => {
  const priorityMap = { /* ... */ };
  return priorityMap[priority] || priority;
};

// --- WATCHERS E LIFECYCLE HOOKS ---

// Observa as mudanças nos filtros e chama a ação da store
watch([searchQuery, statusFilter, priorityFilter], () => {
  // Reseta para a primeira página ao aplicar filtros
  currentPage.value = 1;
  fetchProjects();
});

// Ao montar o componente, busca os projetos iniciais
onMounted(() => {
  if (route.query.new === 'true') {
    openNewProjectModal();
  }
  fetchProjects();
});
</script>
