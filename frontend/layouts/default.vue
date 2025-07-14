<!-- filepath: layouts/default.vue -->
<script setup lang="ts">
import { Icon } from "@iconify/vue";
import { useRoute } from "nuxt/app";
import { computed, ref, watch } from "vue";
import { useAuthStore } from "~/stores/auth";

const route = useRoute();
const authStore = useAuthStore();

const user = computed(() => authStore.user);

// Estado para a sidebar mobile (overlay)
const isMobileSidebarOpen = ref(false);
// Estado para a sidebar desktop colapsada
const isSidebarCollapsed = ref(false);

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: "lucide:layout-dashboard" },
  { name: "Projetos", href: "/projects", icon: "lucide:briefcase" },
  { name: "Tarefas", href: "/tasks", icon: "lucide:check-square" },
  { name: "Equipes", href: "/teams", icon: "lucide:users-2" },
  { name: "Usuários", href: "/users", icon: "lucide:user-cog" },
  { name: "Documentos", href: "/documents", icon: "lucide:file-text" },
  {
    name: "Comunicações",
    href: "/communications",
    icon: "lucide:message-circle",
  },
  { name: "Custos", href: "/costs", icon: "lucide:dollar-sign" },
  { name: "Riscos", href: "/risks", icon: "lucide:alert-triangle" },
  { name: "Notificações", href: "/notifications", icon: "lucide:bell" },
  { name: "Alertas", href: "/alerts", icon: "lucide:shield-alert" },
];

const isActive = (path: string) => {
  // A lógica de "ativo" considera o início do caminho para sub-rotas
  return route.path === path || (path !== "/" && route.path.startsWith(path));
};

const toggleMobileSidebar = () => {
  isMobileSidebarOpen.value = !isMobileSidebarOpen.value;
};

const toggleDesktopSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};

// Fecha a sidebar mobile ao navegar para uma nova rota
watch(route, () => {
  isMobileSidebarOpen.value = false;
});

const handleLogout = async () => {
  await authStore.logout();
  await navigateTo("/login");
};
</script>

<template>
  <div
    class="min-h-screen bg-slate-100 dark:bg-slate-900 text-slate-800 dark:text-slate-200"
  >
    <!-- Sidebar Mobile (Overlay) -->
    <div
      v-if="isMobileSidebarOpen"
      class="md:hidden"
      role="dialog"
      aria-modal="true"
    >
      <!-- Fundo Overlay -->
      <div
        class="fixed inset-0 bg-slate-900/60 z-30"
        @click="toggleMobileSidebar"
      ></div>

      <!-- Painel da Sidebar Mobile -->
      <div class="fixed inset-y-0 left-0 z-40 flex w-72 max-w-full">
        <div class="flex-1 flex flex-col bg-white dark:bg-slate-800">
          <div class="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
            <div
              class="flex items-center justify-between flex-shrink-0 px-4 mb-5"
            >
              <NuxtLink to="/dashboard" class="flex items-center gap-3">
                <Icon icon="lucide:layout-grid" class="h-7 w-7 text-blue-500" />
                <span
                  class="text-2xl font-bold text-slate-900 dark:text-slate-100"
                  >Planify</span
                >
              </NuxtLink>
              <button
                @click="toggleMobileSidebar"
                class="p-1 rounded-md text-slate-400 hover:text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-700"
              >
                <Icon icon="lucide:x" class="h-6 w-6" />
              </button>
            </div>
            <!-- Navegação Mobile -->
            <nav class="flex-1 px-3 space-y-1">
              <NuxtLink
                v-for="item in navigation"
                :key="item.name"
                :to="item.href"
                :class="[
                  isActive(item.href)
                    ? 'bg-blue-50 text-blue-600 dark:bg-blue-500/10 dark:text-blue-400'
                    : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700',
                  'group flex items-center px-3 py-2.5 text-base font-medium rounded-lg transition-colors',
                ]"
              >
                <Icon :icon="item.icon" class="mr-4 h-6 w-6" />
                <span>{{ item.name }}</span>
              </NuxtLink>
            </nav>
          </div>
          <!-- Perfil do Usuário Mobile -->
          <div
            class="flex-shrink-0 flex border-t border-slate-200 dark:border-slate-700 p-4"
          >
            <NuxtLink to="/profile" class="flex-shrink-0 w-full group block">
              <div class="flex items-center">
                <div
                  class="w-10 h-10 bg-blue-100 dark:bg-blue-500/20 rounded-full flex items-center justify-center text-blue-600 dark:text-blue-300 font-bold text-lg"
                >
                  {{ user?.full_name?.charAt(0)?.toUpperCase() || "U" }}
                </div>
                <div class="ml-3 min-w-0">
                  <p
                    class="text-base font-semibold text-slate-700 dark:text-slate-200 truncate"
                  >
                    {{ user?.full_name || "Usuário" }}
                  </p>
                  <p
                    class="text-sm font-medium text-slate-500 dark:text-slate-400 group-hover:text-blue-500 transition-colors"
                  >
                    Ver Perfil
                  </p>
                </div>
                <button
                  @click.prevent="handleLogout"
                  class="ml-auto p-2 text-slate-400 hover:text-red-500 dark:hover:text-red-400 rounded-md transition-colors"
                  title="Sair"
                >
                  <Icon icon="lucide:log-out" class="h-5 w-5" />
                </button>
              </div>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Container Flex Principal -->
    <div class="flex">
      <!-- Sidebar para Desktop (Colapsável) -->
      <aside
        :class="[
          'hidden md:flex md:flex-col md:fixed md:inset-y-0 bg-white dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 transition-all duration-300 ease-in-out',
          isSidebarCollapsed ? 'md:w-20' : 'md:w-64',
        ]"
      >
        <div class="flex-1 flex flex-col min-h-0">
          <div
            class="flex items-center justify-between h-20 px-4 flex-shrink-0"
          >
            <!-- Logo -->
            <NuxtLink
              to="/dashboard"
              :class="[
                'flex items-center gap-3 transition-opacity duration-200',
                isSidebarCollapsed
                  ? 'opacity-0 pointer-events-none'
                  : 'opacity-100',
              ]"
            >
              <Icon icon="lucide:layout-grid" class="h-7 w-7 text-blue-500" />
              <span
                class="text-2xl font-bold text-slate-900 dark:text-slate-100"
                >Planify</span
              >
            </NuxtLink>
            <!-- Botão de Colapsar -->
            <button
              @click="toggleDesktopSidebar"
              class="p-2 rounded-full text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-300"
              :class="isSidebarCollapsed && 'rotate-180'"
            >
              <Icon icon="lucide:chevrons-left" class="h-5 w-5" />
            </button>
          </div>
          <!-- Navegação Desktop -->
          <nav class="flex-1 mt-2 px-3 space-y-1.5 overflow-y-auto">
            <NuxtLink
              v-for="item in navigation"
              :key="item.name"
              :to="item.href"
              :title="isSidebarCollapsed ? item.name : ''"
              :class="[
                'group flex items-center relative py-2.5 rounded-lg transition-all duration-200',
                isSidebarCollapsed ? 'px-3 justify-center' : 'px-4',
                isActive(item.href)
                  ? 'bg-blue-50 text-blue-600 dark:bg-blue-500/10 dark:text-blue-400 font-semibold'
                  : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 hover:text-slate-800 dark:hover:bg-slate-700 dark:hover:text-slate-100',
              ]"
            >
              <div
                v-if="isActive(item.href)"
                class="absolute left-0 top-1 bottom-1 w-1 bg-blue-500 rounded-r-full"
              ></div>
              <Icon
                :icon="item.icon"
                class="h-6 w-6 transition-all"
                :class="isSidebarCollapsed ? '' : 'mr-4'"
              />
              <span
                :class="[
                  'transition-opacity',
                  isSidebarCollapsed ? 'opacity-0 w-0' : 'opacity-100',
                ]"
                >{{ item.name }}</span
              >
            </NuxtLink>
          </nav>
          <!-- Perfil do Usuário Desktop -->
          <div
            class="flex-shrink-0 flex border-t border-slate-200 dark:border-slate-700 p-4"
          >
            <NuxtLink to="/profile" class="flex-shrink-0 w-full group block">
              <div
                class="flex items-center"
                :class="isSidebarCollapsed && 'justify-center'"
              >
                <div
                  class="w-10 h-10 bg-blue-100 dark:bg-blue-500/20 rounded-full flex items-center justify-center text-blue-600 dark:text-blue-300 font-bold text-lg"
                >
                  {{ user?.full_name?.charAt(0)?.toUpperCase() || "U" }}
                </div>
                <div
                  class="ml-3 min-w-0 transition-all duration-200"
                  :class="
                    isSidebarCollapsed ? 'opacity-0 w-0 h-0' : 'opacity-100'
                  "
                >
                  <p
                    class="text-sm font-semibold text-slate-700 dark:text-slate-200 truncate"
                  >
                    {{ user?.full_name || "Usuário" }}
                  </p>
                  <p
                    class="text-xs font-medium text-slate-500 dark:text-slate-400 group-hover:text-blue-500 transition-colors"
                  >
                    Ver Perfil
                  </p>
                </div>
                <button
                  @click.prevent="handleLogout"
                  :title="isSidebarCollapsed ? 'Sair' : ''"
                  :class="[
                    'p-2 text-slate-400 hover:text-red-500 dark:hover:text-red-400 rounded-md transition-colors',
                    isSidebarCollapsed ? '' : 'ml-auto',
                  ]"
                >
                  <Icon icon="lucide:log-out" class="h-5 w-5" />
                </button>
              </div>
            </NuxtLink>
          </div>
        </div>
      </aside>

      <!-- Conteúdo Principal -->
      <div
        :class="[
          'flex flex-col flex-1 transition-all duration-300 ease-in-out',
          isSidebarCollapsed ? 'md:pl-20' : 'md:pl-64',
        ]"
      >
        <!-- Header Mobile com botão de menu -->
        <div
          class="sticky top-0 z-10 md:hidden flex items-center justify-between pl-3 pr-4 h-16 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm border-b border-slate-200 dark:border-slate-700"
        >
          <button
            @click="toggleMobileSidebar"
            type="button"
            class="p-2 rounded-md text-slate-500 hover:text-slate-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
          >
            <span class="sr-only">Abrir menu</span>
            <Icon icon="lucide:menu" class="h-6 w-6" />
          </button>
          <span class="text-lg font-bold text-slate-800 dark:text-slate-100"
            >Planify</span
          >
        </div>
        <main class="flex-1">
          <!-- O Nuxt renderiza a página atual aqui -->
          <slot />
        </main>
      </div>
    </div>
  </div>
</template>
