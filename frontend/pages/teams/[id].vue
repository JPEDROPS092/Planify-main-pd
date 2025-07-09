<script lang="ts" setup>
import { ref, computed, type ComputedRef, type Ref } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import type { Equipe, EquipeRequest, MembroEquipe } from "@/api/schemas";
import { watchEffect } from "vue";
import { useAuthStore } from "@/stores/auth";

// Importar os componentes de cada aba
import TeamOverview from "@/components/teams/TeamOverview.vue";
import TeamMembers from "@/components/teams/TeamMembers.vue";
import TeamModal from "@/components/teams/TeamModal.vue";

// Importar funções do Orval
import {
  useTeamsEquipesAdicionarMembroCreate,
  useTeamsEquipesRetrieve,
  useTeamsEquipesUpdate,
  useTeamsEquipesDestroy,
  useTeamsEquipesAtualizarPapelMembroCreate,
  useTeamsEquipesRemoverMembroCreate
} from "@/api/equipes/equipes";

definePageMeta({
  middleware: "auth",
});

const route = useRoute();
const router = useRouter();
const queryClient = useQueryClient();
const { toast } = useToast();
const membersData: Ref<MembroEquipe[]> = ref([]);
const currentUserData: Ref<MembroEquipe | null> = ref(null);

const teamId = computed(() => parseInt(route.params.id as string, 10));
const activeTab = ref("overview");
const showEditModal = ref(false);
const showMembersModal = ref(false);

// Usados para trocar o papel de um membro.
const memberModalEditMode = ref(false); 
const memberModalEditId = ref(0); 

const authStore = useAuthStore();
const user = computed(() => authStore.user);

// Query principal para buscar os dados do projeto.
// Esta query é a ÚNICA que carrega os dados do PROJETO.
// const {
//   data: team,
//   isLoading: teamLoading,
//   error: teamError,
// } = useQuery<Equipe>({
//   queryKey: ["equipe", teamId],
//   queryFn: () =>
//     useTeamsEquipesRetrieve(teamId.value).then((res) => {
//       console.log(res);
//       return res.data;
//     }),
//   enabled: computed(() => !!teamId.value && !isNaN(teamId.value)),
// });

const {
  data: teamData,
  isLoading: teamLoading,
  error: teamError,
} = useTeamsEquipesRetrieve(teamId.value, {
  query: {
    enabled: computed(() => !!teamId.value && !isNaN(teamId.value)),
    queryKey: ["equipe", teamId.value],
  },  
});

let teamCreationDate: Date;

const team: ComputedRef<Equipe | undefined> = computed(
  () => {
    teamCreationDate = new Date(teamData.value?.data?.criado_em || "");

    membersData.value = [...(teamData.value?.data?.membros || [])];

    return teamData.value?.data
  } 
);

// Mutação para atualizar a equipe (usada pelo modal)
const updateMutation = useTeamsEquipesUpdate({
  mutation: {
    onSuccess: (updatedTeam) => {
      toast({ title: "Sucesso!", description: "Equipe atualizada." });
      // Atualiza o cache da query com os novos dados para evitar um refetch
      queryClient.invalidateQueries({ queryKey: ['equipe'] });
      showEditModal.value = false;
    },
    onError: (err: any) =>
      toast({
        title: "Erro",
        description: "Falha ao atualizar o projeto.",
        variant: "destructive",
      }),
  },
});

// Mutação para atualizar papel de membro de equipe
const atualizarPapelMembroMutation = useTeamsEquipesAtualizarPapelMembroCreate({
  mutation: {
    onSuccess: (updatedTeam) => {
      toast({
        title: "Papel atualizado",
        description: "O papel do membro foi atualizado com sucesso.",
      });
      console.log('updated team', updatedTeam.data);

      queryClient.invalidateQueries({ queryKey: ['equipe'] });
      showMembersModal.value = false;
    },
    onError: (err: any) => {
      console.error(err);
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail || "Não foi possível trocar o papel do membro de equipe.",
        variant: "destructive",
      });
    },
  },
});

// Mutação para adicionar membro na equipe
const adicionarMembroMutation = useTeamsEquipesAdicionarMembroCreate({
  mutation: {
    onSuccess: (updatedTeam) => {
      toast({
        title: "Membro Adicionado",
        description: "O novo membro de equipe foi adicionado com sucesso.",
      });

      queryClient.invalidateQueries({ queryKey: ['equipe'] });
      queryClient.invalidateQueries({ queryKey: ['membros-disponiveis'] });
      console.log('updated team', updatedTeam.data);
      showMembersModal.value = false;
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail || "Não foi possível adicionar o membro de equipe.",
        variant: "destructive",
      });
    },
  },
});

// Mutação para remover membro de equipe
const removeMembroMutation = useTeamsEquipesRemoverMembroCreate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Membro Removido",
        description: "O novo membro de equipe foi adicionado com sucesso.",
      });

      queryClient.invalidateQueries({ queryKey: ['equipe'] });
      queryClient.invalidateQueries({ queryKey: ['membros-disponiveis'] });
      showMembersModal.value = false;
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail || "Não foi possível adicionar o membro de equipe.",
        variant: "destructive",
      });
    },
  },
});

// Mutação para excluir a equipe
const deleteMutation = useTeamsEquipesDestroy({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso!", description: "Equipe excluída." });
      queryClient.invalidateQueries({ queryKey: ['teams-equipes-list'] });
      router.push("/teams");
    },
    onError: (err: any) =>
      toast({
        title: "Erro",
        description: "Falha ao excluir o projeto.",
        variant: "destructive",
      }),
  },
});

const handleDelete = () => {
  if (
    window.confirm(
      "Tem certeza que deseja excluir esta equipe? Todos os membros e permissões associados serão removidos."
    )
  ) {
    deleteMutation.mutate({ id: teamId.value });
  }
}

const handleRemoveMember = (data: {usuario: number}) => {
  if (
    window.confirm(
      "Tem certeza que deseja excluir esta equipe? Todos os membros e permissões associados serão removidos."
    )
  ) {
    removeMembroMutation.mutate({ id: teamId.value, data: data });
  }
}

const handleAddMember = () => {

}

</script>

<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <div v-if="teamLoading" class="text-center py-8">
        Carregando equipe...
      </div>
      <div v-else-if="teamError" class="text-center py-8 text-red-500">
        Erro ao carregar o equipe.
        <pre>{{ teamError }}</pre>
      </div>
      <div v-else-if="team">
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg mb-6 p-6">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {{ team.nome }}
              </h1>
              <div class="mt-1 flex justify-between items-center space-x-4 text-gray-800 dark:text-gray-200">
                <span><b>Criado por:</b> {{ team.criado_por_nome }}</span>
                <span><b>Data de criação:</b> {{ String(teamCreationDate.getDate()+1).padStart(2, '0') }}/{{ String(teamCreationDate.getMonth()+1).padStart(2, '0') }}/{{ teamCreationDate.getFullYear() }}</span>
              </div>
              <div class="mt-1 flex items-center space-x-4 text-gray-800 dark:text-gray-200">
                {{ team.descricao }}
              </div>
            </div>

            <div class="flex items-center space-x-2">
              <button
                @click="showEditModal = true"
                class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                <Icon icon="lucide:edit" class="h-4 w-4 mr-2" />
                Editar
              </button>
              <button
                @click="handleDelete"
                class="inline-flex items-center px-3 py-2 border border-red-300 shadow-sm text-sm leading-4 font-medium rounded-md text-red-700 bg-white hover:bg-red-50"
              >
                <Icon icon="lucide:trash" class="h-4 w-4 mr-2" />
                Excluir
              </button>
            </div>
          </div>

          <!-- Progresso -->
          <div class="mt-4">
          </div>

          <TeamModal
            :show="showEditModal"
            :equipe="team"
            :loading="updateMutation.isPending.value"
            @close="showEditModal = false"
            @submit="(data) => updateMutation.mutate({ id: teamId, data })"
          />

          <TeamMembers
            :show="showMembersModal"
            :defining-role="memberModalEditMode"
            :member-id="memberModalEditId"
            :team-id="teamId"
            @close="showMembersModal = false"
            @add="(data) => adicionarMembroMutation.mutate({ id: teamId, data })"
            @change-role="(data) => atualizarPapelMembroMutation.mutate({ id: teamId, data })"
          />
        </div>

        <div class="bg-white dark:bg-gray-800 dark:text-gray-100 shadow rounded-lg mb-6 p-6">
          <h2 class="text-1xl mb-4 font-bold text-gray-900 dark:text-gray-100">
            Membros da Equipe
          </h2>
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50 font-bold dark:text-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-4 py-2 text-left text-xs uppercase">Nome</th>
                <th class="px-4 py-2 text-left text-xs uppercase">Email</th>
                <th class="px-4 py-2 text-left text-xs uppercase">Papel</th>
                <th class="px-4 py-2 text-left text-xs uppercase">Ações</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200 dark:text-gray-50 dark:bg-gray-800">
              <tr v-for="membro in membersData" :key="membro.id">
                <td class="px-4 py-2">{{ membro.usuario_nome }}</td>
                <td class="px-4 py-2">{{ membro.usuario_email }}</td>
                <td class="px-4 py-2">{{ membro.papel_display }}</td>
                <td class="flex justify-around px-4 py-2">
                    <button
                      v-if="membro.usuario !== user.id"
                      @click="() => handleRemoveMember({usuario: membro.usuario})"
                      class="inline-flex items-center px-3 py-2 m-0 border border-red-300 shadow-sm text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50"
                    >
                      <Icon icon="lucide:trash" class="h-4 w-4" />
                      Remover
                    </button>
                    <button
                      @click="() => {showMembersModal = true; memberModalEditMode = true; memberModalEditId = membro.usuario}"
                      class="inline-flex items-center px-3 py-2 border border-cyan-300 shadow-sm text-sm font-medium rounded-md text-cyan-700 bg-white hover:bg-cyan-50"
                    >
                      <Icon icon="lucide:file-badge" class="h-4 w-4" />
                      Papel
                    </button>
                </td>
              </tr>
              <tr v-if="!membersData || membersData.length === 0">
                <td colspan="4" class="px-4 py-2 text-center text-gray-400">Nenhum membro encontrado.</td>
              </tr>
              <tr>
                <td colspan="4" class="px-4 py-2 text-center text-gray-400">
                  <button
                    @click="() => {showMembersModal = true; memberModalEditMode = false; memberModalEditId = 0}"
                    class="flex w-full justify-center items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-50">
                    <Icon icon="lucide:plus"/>
                  </button>
                </td> 
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style>

</style>