<template>
  <div>
    <HeroSection class="fade-in" />
    
    <div id="features" class="scroll-mt-20"> 
      <FeaturesSection class="slide-up" />
    </div>
    
    <div id="mission" class="scroll-mt-20"> 
      <MissionSection class="scale-in" />
    </div>
    
    <CallToAction class="fade-in" />
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'landing',
  title: 'Planify - Planeje seu futuro com inteligência',
  meta: [
    { name: 'description', content: 'Planify é a plataforma que transforma seus sonhos em planos concretos. Descubra como planejar seu futuro de forma inteligente e eficiente.' },
    { name: 'keywords', content: 'planejamento, futuro, metas, produtividade, inteligência' },
    { property: 'og:title', content: 'Planify - Planeje seu futuro com inteligência' },
    { property: 'og:description', content: 'Planify é a plataforma que transforma seus sonhos em planos concretos. Descubra como planejar seu futuro de forma inteligente e eficiente.' },
    { property: 'og:image', content: '/images/og-image.png' },
    { property: 'og:url', content: '/' }
  ]
});

import HeroSection from '~/components/ui/LandingPage/HeroSection.vue';
import FeaturesSection from '~/components/ui/LandingPage/FeaturesSection.vue';
import MissionSection from '~/components/ui/LandingPage/MissionSection.vue';
import CallToAction from '~/components/ui/LandingPage/CallToAction.vue';
import { useAuth } from '~/composables/useAuth';
import { useRouter } from 'vue-router';

// Inserção para observer trigger de animação ao rolar a página
import { onMounted } from 'vue';

const { isAuthenticated, checkAuth } = useAuth();
const router = useRouter();

onMounted(async () => {
  // Primeiro, configuramos a animação de scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.slide-up, .fade-in, .scale-in').forEach(el => {
    observer.observe(el);
  });

  // Verificamos o estado de autenticação
  await checkAuth();
});

// Função que será chamada quando o usuário clicar em botões de ação que necessitam autenticação
const redirectToDashboardOrLogin = () => {
  if (isAuthenticated.value) {
    router.push('/dashboard');
  } else {
    router.push('/auth/login');
  }
};

// Exposição da função para uso nos componentes filhos
defineExpose({
  redirectToDashboardOrLogin
});

// SEO and metadata remain the same
useHead({
  // ...existing head properties...
})
</script>

<style>
/* For animation on scroll */
.slide-up, .fade-in, .scale-in {
  opacity: 0;
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.slide-up {
  transform: translateY(30px);
}

.scale-in {
  transform: scale(0.95);
}

.animate {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* Existing styles */
html {
  scroll-behavior: smooth;
}

/* Add scroll margin for anchor links to account for fixed header */
.scroll-mt-20 {
  scroll-margin-top: 5rem;
}
</style>