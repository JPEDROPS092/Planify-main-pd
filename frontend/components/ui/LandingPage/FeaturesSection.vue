<template>
  <section class="py-16 bg-gray-100">
    <div class="container mx-auto px-6">
      <h2 class="text-3xl font-bold text-center text-blue-700 mb-4">Principais Funcionalidades</h2>
      <p class="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
        Descubra como o Planify pode transformar a gestão dos seus projetos de P&D com ferramentas poderosas e intuitivas.
      </p>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="feature in features" :key="feature.title" class="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div class="flex items-center justify-center w-12 h-12 bg-blue-100 text-blue-600 rounded-full mb-4">
            <Icon :name="feature.icon" class="w-6 h-6" />
          </div>
          <h3 class="text-xl font-semibold text-blue-700 mb-2">{{ feature.title }}</h3>
          <p class="text-gray-600 text-sm">{{ feature.description }}</p>
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
</script>

<style scoped>
/* Estilos para Features, se necessário */
</style>