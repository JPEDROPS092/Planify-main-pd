<template>
  <!-- ... -->
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

import { ref, computed } from 'vue';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useRiskService } from '~/services/riskService';
import { useProjectService } from '~/services/projectService';
import { Icon } from '@iconify/vue';
import { useToast } from '~/composables/useToast';
import type { Risco, RiscoRequest, PaginatedRiscoList, PaginatedProjetoList } from '~/api-types';

const queryClient = useQueryClient();
const riskService = useRiskService();
const projectService = useProjectService();
const { toast } = useToast();

const currentPage = ref(1);
const showModal = ref(false);
const editingRisk = ref<Risco | null>(null);

const form = ref<RiscoRequest>({
  descricao: '',
  projeto: null,
  probabilidade: 'BAIXA',
  impacto: 'BAIXO',
  status: 'IDENTIFICADO'
});

// Fetch risks
const { data: risks, isLoading, error, refetch } = useQuery<PaginatedRiscoList>({
  queryKey: ['risks', currentPage],
  queryFn: () => riskService.getRisks({ page: currentPage.value }),
});

// Fetch projects for select
const { data: projectsList } = useQuery<PaginatedProjetoList>({
    queryKey: ['projectsList'],
    queryFn: () => projectService.getProjects(1, 100)
});

const riskMutation = useMutation({
  mutationFn: (data: { id?: number; risk: RiscoRequest }) => 
    data.id ? riskService.updateRisk(data.id, data.risk) : riskService.createRisk(data.risk),
  onSuccess: () => {
    const action = editingRisk.value ? 'atualizado' : 'criado';
    toast({ title: 'Sucesso', description: `Risco ${action} com sucesso!` });
    queryClient.invalidateQueries({ queryKey: ['risks'] });
    closeModal();
  },
  onError: (err: any) => {
    const action = editingRisk.value ? 'atualizar' : 'criar';
    toast({ title: 'Erro', description: `Falha ao ${action} o risco.`, variant: 'destructive' });
  },
});

const deleteMutation = useMutation({
  mutationFn: (id: number) => riskService.deleteRisk(id),
  onSuccess: () => {
    toast({ title: 'Sucesso', description: 'Risco excluído com sucesso!' });
    queryClient.invalidateQueries({ queryKey: ['risks'] });
  },
  onError: (err: any) => {
    toast({ title: 'Erro', description: 'Falha ao excluir o risco.', variant: 'destructive' });
  },
});

const openModal = (risk: Risco | null = null) => {
  editingRisk.value = risk;
  if (risk) {
    editingRisk.value = risk;
    form.value = {
      descricao: risk.descricao,
      projeto: risk.projeto,
      probabilidade: risk.probabilidade,
      impacto: risk.impacto,
      status: risk.status,
    };
  } else {
    editingRisk.value = null;
    form.value = {
      descricao: '',
      projeto: null,
      probabilidade: 'BAIXA',
      impacto: 'BAIXO',
      status: 'IDENTIFICADO'
    };
  }
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingRisk.value = null;
};

const handleSubmit = () => {
  riskMutation.mutate({ id: editingRisk.value?.id, risk: form.value });
};

const confirmDelete = (id: number) => {
  if (window.confirm('Tem certeza?')) {
    deleteMutation.mutate(id);
  }
};

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    'IDENTIFICADO': 'bg-blue-100 text-blue-800',
    'EM_ANALISE': 'bg-yellow-100 text-yellow-800',
    'MITIGADO': 'bg-green-100 text-green-800',
    'FECHADO': 'bg-gray-100 text-gray-800',
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
};

</script>
