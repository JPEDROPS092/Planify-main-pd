<!-- filepath: pages/profile.vue -->
<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import { useAuthStore } from "@/stores/auth";

// Import Orval types and functions
import { useAuthUsersMePartialUpdate } from "@/api/auth/auth";
import type { User, PatchedUserRequest } from "@/api/schemas";

definePageMeta({
  middleware: "auth",
  title: "Meu Perfil",
});

// --- HOOKS E ESTADO INICIAL ---
const queryClient = useQueryClient();
const { toast } = useToast();
const authStore = useAuthStore();

const showEditModal = ref(false);
const editForm = ref<PatchedUserRequest>({});

// User from store with proper typing
const user = computed<User | null>(() => authStore.user);
const isLoadingProfile = ref(!authStore.user);

onMounted(() => {
  if (authStore.user) isLoadingProfile.value = false;
});

watch(
  () => authStore.user,
  (newUser) => {
    if (newUser) isLoadingProfile.value = false;
  }
);

// --- MUTAÇÃO ---
const updateProfileMutation = useAuthUsersMePartialUpdate({
  mutation: {
    onSuccess: (updatedUserData) => {
      authStore.setUser(updatedUserData.data);
      toast({ title: "Sucesso!", description: "Seu perfil foi atualizado." });
      showEditModal.value = false;
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail ||
          "Não foi possível atualizar seu perfil.",
        variant: "destructive",
      });
    },
  },
});

// --- FUNÇÕES DE MANIPULAÇÃO ---
const openEditModal = () => {
  if (!user.value) return;
  editForm.value = {
    full_name: user.value.full_name,
    email: user.value.email,
  };
  showEditModal.value = true;
};

const handleSubmit = () => {
  updateProfileMutation.mutate({ data: editForm.value });
};
</script>

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg mb-6">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Meu Perfil
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mt-1">
            Gerencie suas informações pessoais e preferências.
          </p>
        </div>
      </div>

      <!-- Conteúdo do Perfil -->
      <div v-if="isLoadingProfile" class="text-center py-20">
        <Icon
          icon="svg-spinners:ring-resize"
          class="w-12 h-12 text-primary-600 mx-auto"
        />
      </div>
      <div v-else-if="user" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Coluna de Informações -->
        <div class="lg:col-span-2">
          <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
            <div
              class="px-6 py-4 border-b border-gray-200 dark:border-gray-700"
            >
              <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100">
                Informações Pessoais
              </h2>
            </div>
            <div class="p-6 space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label
                    class="block text-sm font-medium text-gray-500 dark:text-gray-400"
                    >Nome Completo</label
                  >
                  <p class="mt-1 text-sm text-gray-900 dark:text-gray-200">
                    {{ user.full_name }}
                  </p>
                </div>
                <div>
                  <label
                    class="block text-sm font-medium text-gray-500 dark:text-gray-400"
                    >Email</label
                  >
                  <p class="mt-1 text-sm text-gray-900 dark:text-gray-200">
                    {{ user.email }}
                  </p>
                </div>
                <div>
                  <label
                    class="block text-sm font-medium text-gray-500 dark:text-gray-400"
                    >Username</label
                  >
                  <p class="mt-1 text-sm text-gray-900 dark:text-gray-200">
                    {{ user.username }}
                  </p>
                </div>
                <div>
                  <label
                    class="block text-sm font-medium text-gray-500 dark:text-gray-400"
                    >Status</label
                  >
                  <p class="mt-1">
                    <span
                      :class="
                        user.is_active
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      "
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    >
                      {{ user.is_active ? "Ativo" : "Inativo" }}
                    </span>
                  </p>
                </div>
              </div>
              <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
                <button
                  @click="openEditModal"
                  class="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors"
                >
                  Editar Perfil
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Coluna da Foto e Ações -->
        <div class="space-y-6">
          <div
            class="bg-white dark:bg-gray-800 shadow rounded-lg p-6 text-center"
          >
            <div
              class="mx-auto h-24 w-24 rounded-full bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center text-primary-700 dark:text-primary-300"
            >
              <span class="text-3xl font-bold">{{
                user.full_name?.charAt(0)?.toUpperCase() || "U"
              }}</span>
            </div>
            <h3
              class="mt-4 text-lg font-medium text-gray-900 dark:text-gray-100"
            >
              {{ user.full_name }}
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              {{ user.role }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Edição -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div
        class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4"
      >
        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">
          Editar Perfil
        </h3>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
            >
              Nome Completo
            </label>
            <input
              v-model="editForm.full_name"
              type="text"
              class="w-full rounded-md border border-gray-300 dark:border-gray-700 px-3 py-2 focus:ring-primary-500 focus:border-primary-500"
              required
            />
          </div>

          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
            >
              Email
            </label>
            <input
              v-model="editForm.email"
              type="email"
              class="w-full rounded-md border border-gray-300 dark:border-gray-700 px-3 py-2 focus:ring-primary-500 focus:border-primary-500"
              required
            />
          </div>

          <div class="flex justify-end gap-3 mt-6">
            <button
              type="button"
              @click="showEditModal = false"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
              :disabled="updateProfileMutation.isPending"
            >
              {{ updateProfileMutation.isPending ? "Salvando..." : "Salvar" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
