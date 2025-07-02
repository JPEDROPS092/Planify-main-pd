<!-- filepath: layouts/default.vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { Icon } from "@iconify/vue";
import { useAuthStore } from "~/stores/auth";

// O layout agora é "burro". Ele não faz chamadas de API nem verifica tokens.
// Ele apenas lê o estado que já foi preparado pela store (Pinia) e pelos plugins.

const route = useRoute();
const authStore = useAuthStore();

// Os dados do usuário e o estado de login vêm diretamente da store.
const user = computed(() => authStore.user);

// Estado local da UI para controlar a sidebar.
const isSidebarOpen = ref(false);

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: "lucide:home" },
  { name: "Projetos", href: "/projects", icon: "lucide:briefcase" },
  { name: "Tarefas", href: "/tasks", icon: "lucide:check-square" },
  { name: "Equipes", href: "/teams", icon: "lucide:users" },
  { name: "Usuários", href: "/users", icon: "lucide:user-cog" },
  { name: "Documentos", href: "/documents", icon: "lucide:file-text" },
  { name: "Custos", href: "/costs", icon: "lucide:dollar-sign" },
  { name: "Riscos", href: "/risks", icon: "lucide:alert-triangle" },
  { name: "Notificações", href: "/notifications", icon: "lucide:bell" },
  { name: "Alertas", href: "/alerts", icon: "lucide:shield-alert" },
];

const isActive = (path: string) => {
  return route.path === path || (path !== "/" && route.path.startsWith(path));
};

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const handleLogout = async () => {
  authStore.logout();
  await navigateTo("/login");
};
</script>

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <div class="flex">
      <!-- Sidebar para Desktop (fixa) -->
      <div class="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
        <div
          class="flex-1 flex flex-col min-h-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700"
        >
          <div class="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
            <div class="flex items-center flex-shrink-0 px-4 mb-5">
              <NuxtLink to="/dashboard" class="flex items-center gap-2">
                <Icon
                  icon="lucide:layout-dashboard"
                  class="h-8 w-8 text-primary-600"
                />
                <span class="text-xl font-bold text-gray-900 dark:text-gray-100"
                  >Planify</span
                >
              </NuxtLink>
            </div>
            <nav class="mt-5 flex-1 px-2 space-y-1">
              <NuxtLink
                v-for="item in navigation"
                :key="item.name"
                :to="item.href"
                :class="[
                  isActive(item.href)
                    ? 'bg-primary-50 text-primary-600 dark:bg-primary-900/40 dark:text-primary-300'
                    : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700',
                  'group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors',
                ]"
              >
                <Icon :icon="item.icon" class="mr-3 h-5 w-5" />
                {{ item.name }}
              </NuxtLink>
            </nav>
          </div>
          <div
            class="flex-shrink-0 flex border-t border-gray-200 dark:border-gray-700 p-4"
          >
            <NuxtLink to="/profile" class="flex-shrink-0 w-full group block">
              <div class="flex items-center">
                <div
                  class="w-10 h-10 bg-primary-100 dark:bg-primary-900/50 rounded-full flex items-center justify-center text-primary-700 dark:text-primary-300 font-bold"
                >
                  {{ user?.full_name?.charAt(0)?.toUpperCase() || "U" }}
                </div>
                <div class="ml-3 min-w-0">
                  <p
                    class="text-sm font-medium text-gray-700 dark:text-gray-200 group-hover:text-gray-900 truncate"
                  >
                    {{ user?.full_name || "Usuário" }}
                  </p>
                  <p
                    class="text-xs font-medium text-gray-500 dark:text-gray-400 group-hover:text-gray-700"
                  >
                    Ver Perfil
                  </p>
                </div>
                <button
                  @click.stop.prevent="handleLogout"
                  class="ml-auto text-gray-400 hover:text-red-500"
                  title="Sair"
                >
                  <Icon icon="lucide:log-out" class="h-5 w-5" />
                </button>
              </div>
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- Conteúdo principal -->
      <div class="md:pl-64 flex flex-col flex-1">
        <div
          class="sticky top-0 z-10 md:hidden pl-1 pt-1 sm:pl-3 sm:pt-3 bg-gray-100 dark:bg-gray-900"
        >
          <button
            @click="toggleSidebar"
            type="button"
            class="-ml-0.5 -mt-0.5 h-12 w-12 inline-flex items-center justify-center rounded-md text-gray-500 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
          >
            <span class="sr-only">Abrir menu</span>
            <Icon icon="lucide:menu" class="h-6 w-6" />
          </button>
        </div>
        <main class="flex-1">
          <!-- AQUI é onde o Nuxt vai renderizar a página atual (ex: /dashboard) -->
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>
