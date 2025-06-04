<template>
  <div>
    <HeroSection />
    <div id="features"> <!-- Adiciona um ID para navegação interna -->
      <FeaturesSection />
    </div>
    <div id="mission"> <!-- Adiciona um ID para navegação interna -->
      <MissionSection />
    </div>
    <CallToAction />
    <!-- Você pode adicionar mais seções aqui, como "Tecnologias Utilizadas", "Como Contribuir", etc. -->
  </div>
</template>

<script setup>

 import HeroSection from '~/components/ui/LandingPage/HeroSection.vue';
 import FeaturesSection from '~/components/ui/LandingPage/FeaturesSection.vue';
 import MissionSection from '~/components/ui/LandingPage/MissionSection.vue';
 import CallToAction from '~/components/ui/LandingPage/CallToAction.vue';

// SEO e Metadados da Página
useHead({
  title: 'Planify - Gestão de Projetos de P&D Simplificada',
  meta: [
    { name: 'description', content: 'Planify: Organize projetos, equipes, tarefas, custos e riscos em um só lugar. Gestão visual, dashboards inteligentes e colaboração em tempo real para P&D.' },
    { name: 'keywords', content: 'Planify, gestão de projetos, P&D, pesquisa e desenvolvimento, kanban, tarefas, equipes, riscos, custos, colaboração' },
    { property: 'og:title', content: 'Planify - Gestão de Projetos de P&D Simplificada' },
    { property: 'og:description', content: 'Organize projetos, equipes, tarefas, custos e riscos em um só lugar com Planify.' },
    { property: 'og:image', content: '/image/README/1748802879852.png' }, // Caminho para sua imagem de preview
    { property: 'og:url', content: 'https://seusite.com' }, // Substitua pela URL real do seu site
    { name: 'twitter:card', content: 'summary_large_image' },
  ],
  link: [
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' } // Certifique-se de ter um favicon.ico em public/
  ]
})
</script>

<style>
/* Estilos globais que podem ser aplicados a esta página, se necessário. */
/* Por exemplo, para smooth scroll ao clicar nos links do footer: */
html {
  scroll-behavior: smooth;
}
</style>