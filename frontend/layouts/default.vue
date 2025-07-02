<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import AuthLoadingScreen from "~/components/AuthLoadingScreen.vue";

const route = useRoute();
const router = useRouter();
const { user, isAuthenticated, verifyToken, logout } = useAuth();

// Configuração de rotas
const authConfig = {
  protectedRoutes: [
    "/dashboard",
    "/projects",
    "/profile",
    "/admin",
    "/tasks",
    "/teams",
    "/users",
    "/documents",
    "/costs",
    "/risks",
    "/notifications",
    "/alerts",
  ],
  publicRoutes: ["/login", "/register", "/", "/about"],
  redirectAfterLogin: "/dashboard",
  redirectAfterLogout: "/login",
};

// Estado da sidebar
const isSidebarOpen = ref(false);

// Navegação
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
  // Removing finances as it doesn't have a page yet
];

// Computeds para controle de UI
const shouldCheckAuth = computed(() =>
  authConfig.protectedRoutes.some((path) => route.path.startsWith(path))
);

const showNavigation = computed(
  () => !route.path.startsWith("/login") && !route.path.startsWith("/register")
);

const mainClasses = computed(() => ({
  "min-h-screen": !showNavigation.value,
  "pt-0": showNavigation.value,
  "bg-gray-50": true,
}));

// Query de verificação de autenticação usando Vue Query
const { isLoading: isCheckingAuth } = useQuery({
  queryKey: ["auth-verification", route.path],
  queryFn: async () => {
    // Se não tem token, redirecionar para login
    if (!isAuthenticated.value) {
      await router.push(authConfig.redirectAfterLogout);
      throw new Error("Not authenticated");
    }

    // Verificar se token é válido
    const isValid = await verifyToken();
    if (!isValid) {
      await router.push(authConfig.redirectAfterLogout);
      throw new Error("Invalid token");
    }

    return true;
  },
  enabled: shouldCheckAuth,
  retry: false,
  staleTime: 3 * 60 * 1000, // Cache por 3 minutos
  gcTime: 5 * 60 * 1000,
});

// Funções auxiliares
const isActive = (path) => {
  return route.path === path || route.path.startsWith(`${path}/`);
};

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const handleLogout = async () => {
  await logout();
};

// Watcher para redirecionamentos automáticos
watch(
  [() => route.path],
  async () => {
    // Redirecionar usuário logado tentando acessar login/register
    if (
      (route.path === "/login" || route.path === "/register") &&
      isAuthenticated.value
    ) {
      await router.push(authConfig.redirectAfterLogin);
    }
  },
  { immediate: true }
);
</script>

<template>
  <div>
    <!-- Loading Screen durante verificação de auth -->
    <AuthLoadingScreen v-if="shouldCheckAuth && isCheckingAuth" />

    <!-- Conteúdo normal quando auth verificada ou não necessária -->
    <div v-else :class="mainClasses">
      <!-- Layout com navegação para páginas protegidas -->
      <div v-if="showNavigation" class="min-h-screen bg-gray-50">
        <!-- Barra de navegação superior para dispositivos móveis -->
        <MainNavigation class="md:hidden" />

        <div class="flex">
          <!-- Sidebar para desktop -->
          <div class="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
            <div
              class="flex-1 flex flex-col min-h-0 bg-white border-r border-gray-200"
            >
              <div class="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
                <div class="flex items-center flex-shrink-0 px-4 mb-5">
                  <NuxtLink to="/" class="flex items-center">
                    <Icon
                      icon="lucide:layout-dashboard"
                      class="h-8 w-8 text-primary mr-2"
                    />
                    <span class="text-xl font-semibold text-gray-900"
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
                        ? 'bg-primary-50 text-primary-600'
                        : 'text-gray-600 hover:bg-gray-50',
                      'group flex items-center px-2 py-2 text-sm font-medium rounded-md',
                    ]"
                  >
                    <Icon
                      :icon="item.icon"
                      class="mr-3 h-5 w-5"
                      :class="
                        isActive(item.href) ? 'text-primary' : 'text-gray-400'
                      "
                    />
                    {{ item.name }}
                  </NuxtLink>
                </nav>
              </div>

              <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
                <div class="flex-shrink-0 w-full group block">
                  <div class="flex items-center">
                    <div
                      class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center text-primary"
                    >
                      {{
                        user?.first_name?.charAt(0) ||
                        user?.username?.charAt(0) ||
                        "U"
                      }}
                    </div>
                    <div class="ml-3 flex-1">
                      <p
                        class="text-sm font-medium text-gray-700 group-hover:text-gray-900"
                      >
                        {{ user?.first_name || user?.username || "Usuário" }}
                      </p>
                      <p
                        class="text-xs font-medium text-gray-500 group-hover:text-gray-700"
                      >
                        {{ user?.email || "" }}
                      </p>
                    </div>
                    <button
                      @click="handleLogout"
                      class="text-gray-400 hover:text-gray-500"
                    >
                      <Icon icon="lucide:log-out" class="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Sidebar móvel -->
          <div v-if="isSidebarOpen" class="fixed inset-0 flex z-40 md:hidden">
            <div
              class="fixed inset-0 bg-gray-600 bg-opacity-75"
              @click="toggleSidebar"
            ></div>

            <div class="relative flex-1 flex flex-col max-w-xs w-full bg-white">
              <div class="absolute top-0 right-0 -mr-12 pt-2">
                <button
                  @click="toggleSidebar"
                  class="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                >
                  <span class="sr-only">Fechar menu</span>
                  <Icon icon="lucide:x" class="h-6 w-6 text-white" />
                </button>
              </div>

              <div class="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
                <div class="flex-shrink-0 flex items-center px-4">
                  <Icon
                    icon="lucide:layout-dashboard"
                    class="h-8 w-8 text-primary mr-2"
                  />
                  <span class="text-xl font-semibold text-gray-900"
                    >Planify</span
                  >
                </div>
                <nav class="mt-5 px-2 space-y-1">
                  <NuxtLink
                    v-for="item in navigation"
                    :key="item.name"
                    :to="item.href"
                    :class="[
                      isActive(item.href)
                        ? 'bg-primary-50 text-primary-600'
                        : 'text-gray-600 hover:bg-gray-50',
                      'group flex items-center px-2 py-2 text-base font-medium rounded-md',
                    ]"
                    @click="toggleSidebar"
                  >
                    <Icon
                      :icon="item.icon"
                      class="mr-3 h-6 w-6"
                      :class="
                        isActive(item.href) ? 'text-primary' : 'text-gray-400'
                      "
                    />
                    {{ item.name }}
                  </NuxtLink>
                </nav>
              </div>

              <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
                <div class="flex-shrink-0 w-full group block">
                  <div class="flex items-center">
                    <div
                      class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center text-primary"
                    >
                      {{
                        user?.first_name?.charAt(0) ||
                        user?.username?.charAt(0) ||
                        "U"
                      }}
                    </div>
                    <div class="ml-3 flex-1">
                      <p class="text-sm font-medium text-gray-700">
                        {{ user?.first_name || user?.username || "Usuário" }}
                      </p>
                      <p class="text-xs text-gray-500">
                        {{ user?.email || "" }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Conteúdo principal -->
          <div class="md:pl-64 flex flex-col flex-1">
            <div
              class="sticky top-0 z-10 md:hidden pl-1 pt-1 sm:pl-3 sm:pt-3 bg-white"
            >
              <button
                @click="toggleSidebar"
                type="button"
                class="-ml-0.5 -mt-0.5 h-12 w-12 inline-flex items-center justify-center rounded-md text-gray-500 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary"
              >
                <span class="sr-only">Abrir menu</span>
                <Icon icon="lucide:menu" class="h-6 w-6" />
              </button>
            </div>

            <main class="flex-1">
              <NuxtPage />
            </main>
          </div>
        </div>
      </div>

      <!-- Layout simples para páginas públicas -->
      <div v-else>
        <slot />
      </div>
    </div>
  </div>
</template>
