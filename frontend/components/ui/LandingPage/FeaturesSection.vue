<template>
  <section class="py-16 bg-gradient-to-b from-gray-100 to-white dark:from-gray-900 dark:to-gray-800">
    <div class="container mx-auto px-6">
      <h2 class="text-3xl font-bold text-center mb-4 bg-gradient-to-r from-blue-600 to-blue-800 dark:from-blue-400 dark:to-blue-600 text-transparent bg-clip-text">Principais Funcionalidades</h2>
      <p class="text-center text-gray-600 dark:text-gray-300 mb-12 max-w-2xl mx-auto">
        Descubra como o Planify pode transformar a gestão dos seus projetos de P&D com ferramentas poderosas e intuitivas.
      </p>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="(feature, index) in features" 
          :key="feature.title" 
          class="hover-card bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg overflow-hidden relative"
          :class="{'animate-delay-100': index % 3 === 0, 'animate-delay-200': index % 3 === 1, 'animate-delay-300': index % 3 === 2}"
        >
          <!-- Gradient background overlay -->
          <div class="absolute inset-0 bg-gradient-to-br from-blue-50 to-transparent dark:from-blue-900/20 dark:to-transparent opacity-50"></div>
          
          <!-- Content -->
          <div class="relative z-10">
            <div class="flex items-center justify-center w-14 h-14 bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-800 dark:to-blue-900 text-blue-600 dark:text-blue-300 rounded-lg mb-4 transform transition-transform duration-300 group-hover:scale-110">
              <Icon :name="feature.icon" class="w-7 h-7" />
            </div>
            <h3 class="text-xl font-semibold text-blue-700 dark:text-blue-300 mb-2">{{ feature.title }}</h3>
            <p class="text-gray-600 dark:text-gray-400">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const features = [
  {
    icon: 'ph:lock-key-bold',
    title: 'Autenticação e Controle de Acesso',
    description: 'Gerenciamento de usuários com permissões baseadas em papéis para segurança robusta.',
  },
  {
    icon: 'ph:clipboard-text-bold',
    title: 'Gerenciamento de Projetos',
    description: 'Criação, acompanhamento detalhado e análise aprofundada de todos os seus projetos.',
  },
  {
    icon: 'ph:trello-logo-bold',
    title: 'Tarefas e Kanban',
    description: 'Gestão eficiente de tarefas com visualização intuitiva em quadro Kanban.',
  },
  {
    icon: 'ph:users-three-bold',
    title: 'Gestão de Equipes',
    description: 'Organização de equipes, atribuição de papéis e fomento à colaboração.',
  },
  {
    icon: 'ph:warning-octagon-bold',
    title: 'Gestão de Riscos',
    description: 'Identificação proativa, análise e estratégias de mitigação de riscos.',
  },
  {
    icon: 'ph:money-bold',
    title: 'Controle de Custos',
    description: 'Orçamento preciso, acompanhamento de despesas e relatórios financeiros claros.',
  },
  {
    icon: 'ph:folder-simple-bold',
    title: 'Repositório de Documentos',
    description: 'Upload seguro, versionamento e controle de acesso para sua documentação.',
  },
  {
    icon: 'ph:chats-circle-bold',
    title: 'Comunicação Integrada',
    description: 'Chat e notificações em tempo real para manter todos alinhados e informados.',
  },
  {
    icon: 'ph:calendar-blank-bold',
    title: 'Calendário de Projetos',
    description: 'Visualização clara de eventos importantes, marcos e prazos de projetos.',
  },
];

// Add animation delay classes
const animateDelayClasses = {
  'animate-delay-100': 'animation-delay: 100ms;',
  'animate-delay-200': 'animation-delay: 200ms;',
  'animate-delay-300': 'animation-delay: 300ms;',
};
</script>

<style scoped>
.animate-delay-100 {
  animation-delay: 100ms;
}
.animate-delay-200 {
  animation-delay: 200ms;
}
.animate-delay-300 {
  animation-delay: 300ms;
}

/* Card hover effect */
.hover-card {
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: rgba(59, 130, 246, 0.2);
}
</style>