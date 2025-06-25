<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
    <!-- Navigation -->
    <nav class="relative z-10 bg-white/80 backdrop-blur-md border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center">
            <div class="flex-shrink-0 flex items-center">
              <div class="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Icon name="lucide:cube" class="w-6 h-6 text-white" />
              </div>
              <span class="ml-3 text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Planify
              </span>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="showLoginModal = true"
              class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Entrar
            </button>
            <button
              @click="showRegisterModal = true"
              class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-2 rounded-lg text-sm font-medium transition-all transform hover:scale-105"
            >
              Criar Conta
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative overflow-hidden">
      <!-- Background Elements -->
      <div class="absolute inset-0">
        <div class="absolute top-20 left-10 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div class="absolute top-40 right-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div class="absolute bottom-20 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div class="text-center">
          <h1 class="text-5xl md:text-7xl font-bold text-gray-900 mb-8">
            Gerencie seus
            <span class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Projetos
            </span>
            <br />
            com Inteligência
          </h1>
          <p class="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
            A plataforma completa para gestão de projetos, equipes e recursos. 
            Simplifique seu fluxo de trabalho e aumente a produtividade da sua equipe.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              @click="showRegisterModal = true"
              class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 rounded-xl text-lg font-semibold transition-all transform hover:scale-105 shadow-lg hover:shadow-xl"
            >
              Começar Gratuitamente
            </button>
            <button
              @click="scrollToFeatures"
              class="border-2 border-gray-300 hover:border-blue-600 text-gray-700 hover:text-blue-600 px-8 py-4 rounded-xl text-lg font-semibold transition-all"
            >
              Conhecer Recursos
            </button>
          </div>
        </div>

        <!-- Hero Image/Dashboard Preview -->
        <div class="mt-20 relative">
          <div class="bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden transform rotate-1 hover:rotate-0 transition-transform duration-500">
            <div class="bg-gray-50 px-6 py-4 border-b border-gray-200">
              <div class="flex items-center space-x-2">
                <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div class="w-3 h-3 bg-green-500 rounded-full"></div>
              </div>
            </div>
            <div class="p-6">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div class="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-4 text-white">
                  <div class="text-2xl font-bold">127</div>
                  <div class="text-blue-100">Projetos Ativos</div>
                </div>
                <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-4 text-white">
                  <div class="text-2xl font-bold">89%</div>
                  <div class="text-green-100">Taxa de Conclusão</div>
                </div>
                <div class="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-4 text-white">
                  <div class="text-2xl font-bold">42</div>
                  <div class="text-purple-100">Membros da Equipe</div>
                </div>
              </div>
              <div class="space-y-3">
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-blue-500 rounded-full"></div>
                    <div>
                      <div class="font-medium">Redesign do Website</div>
                      <div class="text-sm text-gray-500">Em andamento</div>
                    </div>
                  </div>
                  <div class="text-sm text-gray-500">75%</div>
                </div>
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-green-500 rounded-full"></div>
                    <div>
                      <div class="font-medium">App Mobile</div>
                      <div class="text-sm text-gray-500">Concluído</div>
                    </div>
                  </div>
                  <div class="text-sm text-gray-500">100%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-24 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-gray-900 mb-4">
            Recursos Poderosos para Sua Equipe
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            Tudo que você precisa para gerenciar projetos de forma eficiente e colaborativa.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="group p-8 rounded-2xl border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Icon name="lucide:folder" class="w-6 h-6 text-white" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Gestão de Projetos</h3>
            <p class="text-gray-600">
              Organize e acompanhe todos os seus projetos em um só lugar. Defina metas, prazos e monitore o progresso em tempo real.
            </p>
          </div>

          <div class="group p-8 rounded-2xl border border-gray-200 hover:border-purple-300 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Icon name="lucide:users" class="w-6 h-6 text-white" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Colaboração em Equipe</h3>
            <p class="text-gray-600">
              Trabalhe em conjunto com sua equipe. Compartilhe arquivos, comunique-se e mantenha todos alinhados.
            </p>
          </div>

          <div class="group p-8 rounded-2xl border border-gray-200 hover:border-green-300 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-green-600 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Icon name="lucide:bar-chart-3" class="w-6 h-6 text-white" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Relatórios e Analytics</h3>
            <p class="text-gray-600">
              Obtenha insights valiosos com relatórios detalhados e métricas de desempenho para tomar decisões informadas.
            </p>
          </div>

          <div class="group p-8 rounded-2xl border border-gray-200 hover:border-yellow-300 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-gradient-to-r from-yellow-500 to-yellow-600 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Icon name="lucide:clock" class="w-6 h-6 text-white" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Controle de Tempo</h3>
            <p class="text-gray-600">
              Monitore o tempo gasto em cada tarefa e projeto. Otimize a produtividade e melhore a gestão de recursos.
            </p>
          </div>

          <div class="group p-8 rounded-2xl border border-gray-200 hover:border-red-300 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-gradient-to-r from-red-500 to-red-600 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Icon name="lucide:shield-check" class="w-6 h-6 text-white" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Segurança Avançada</h3>
            <p class="text-gray-600">
              Seus dados estão protegidos com criptografia de ponta e controles de acesso granulares.
            </p>
          </div>

          <div class="group p-8 rounded-2xl border border-gray-200 hover:border-indigo-300 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-gradient-to-r from-indigo-500 to-indigo-600 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Icon name="lucide:smartphone" class="w-6 h-6 text-white" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Acesso Mobile</h3>
            <p class="text-gray-600">
              Gerencie seus projetos de qualquer lugar com nosso app mobile responsivo e intuitivo.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-24 bg-gradient-to-r from-blue-600 to-purple-600">
      <div class="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
        <h2 class="text-4xl font-bold text-white mb-6">
          Pronto para Transformar Sua Gestão de Projetos?
        </h2>
        <p class="text-xl text-blue-100 mb-8">
          Junte-se a milhares de equipes que já estão usando o Planify para alcançar seus objetivos.
        </p>
        <button
          @click="showRegisterModal = true"
          class="bg-white hover:bg-gray-100 text-blue-600 px-8 py-4 rounded-xl text-lg font-semibold transition-all transform hover:scale-105 shadow-lg"
        >
          Começar Agora - É Grátis
        </button>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div class="flex items-center mb-4">
              <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Icon name="lucide:cube" class="w-5 h-5 text-white" />
              </div>
              <span class="ml-2 text-lg font-bold">Planify</span>
            </div>
            <p class="text-gray-400">
              A plataforma completa para gestão de projetos e equipes.
            </p>
          </div>
          <div>
            <h3 class="font-semibold mb-4">Produto</h3>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white transition-colors">Recursos</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Preços</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Integrações</a></li>
            </ul>
          </div>
          <div>
            <h3 class="font-semibold mb-4">Empresa</h3>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white transition-colors">Sobre</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Blog</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Carreiras</a></li>
            </ul>
          </div>
          <div>
            <h3 class="font-semibold mb-4">Suporte</h3>
            <ul class="space-y-2 text-gray-400">
              <li><a href="#" class="hover:text-white transition-colors">Central de Ajuda</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Contato</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Status</a></li>
            </ul>
          </div>
        </div>
        <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2024 Planify. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>

    <!-- Login Modal -->
    <LoginModal
      v-if="showLoginModal"
      @close="showLoginModal = false"
      @success="onLoginSuccess"
      @switch-to-register="switchToRegister"
    />

    <!-- Register Modal -->
    <RegisterModal
      v-if="showRegisterModal"
      @close="showRegisterModal = false"
      @success="onRegisterSuccess"
      @switch-to-login="switchToLogin"
    />
  </div>
</template>

<script setup lang="ts">
import LoginModal from '~/components/LoginModal.vue'
import RegisterModal from '~/components/RegisterModal.vue'

definePageMeta({
  middleware: 'guest',
  layout: false
})

// State
const showLoginModal = ref(false)
const showRegisterModal = ref(false)

// Methods
const scrollToFeatures = () => {
  document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })
}

const onLoginSuccess = () => {
  showLoginModal.value = false
  navigateTo('/dashboard')
}

const onRegisterSuccess = () => {
  showRegisterModal.value = false
  navigateTo('/dashboard')
}

const switchToRegister = () => {
  showLoginModal.value = false
  showRegisterModal.value = true
}

const switchToLogin = () => {
  showRegisterModal.value = false
  showLoginModal.value = true
}
</script>

<style scoped>
@keyframes blob {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}
</style>
