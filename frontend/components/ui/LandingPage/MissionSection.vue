<template>
  <section class="py-20 relative overflow-hidden">
    <!-- Fundo com gradiente animado -->
    <div class="absolute inset-0 bg-gradient-to-r from-blue-800 via-blue-700 to-blue-900 dark:from-blue-900 dark:via-blue-800 dark:to-blue-950"></div>
    
    <!-- Padrão de círculos decorativos -->
    <div class="absolute inset-0 opacity-10">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
    
    <div class="container mx-auto px-6 text-center relative z-10">
      <div class="max-w-3xl mx-auto">
        <Icon name="ph:rocket-launch-bold" class="w-16 h-16 text-blue-300 mx-auto mb-8 animate-pulse" />
        
        <h2 class="text-4xl font-bold mb-6 text-white">Nossa Missão</h2>
        
        <p class="text-xl leading-relaxed text-blue-100 mb-10">
          Impulsionar o setor de tecnologia da informação, promovendo colaboração e eficiência, enquanto fornece suporte às tomadas de decisão entre lideranças.
        </p>
        
        <div class="grid md:grid-cols-3 gap-8 mt-12">
          <div class="bg-white/10 backdrop-blur-sm p-6 rounded-xl hover-card">
            <Icon name="ph:lightbulb-bold" class="w-10 h-10 text-yellow-300 mx-auto mb-4" />
            <h3 class="text-xl font-semibold text-white mb-2">Inovação</h3>
            <p class="text-blue-100">Incentivamos novas ideias e abordagens criativas para resolver desafios complexos.</p>
          </div>
          
          <div class="bg-white/10 backdrop-blur-sm p-6 rounded-xl hover-card">
            <Icon name="ph:users-three-bold" class="w-10 h-10 text-green-300 mx-auto mb-4" />
            <h3 class="text-xl font-semibold text-white mb-2">Colaboração</h3>
            <p class="text-blue-100">Facilitamos a comunicação e o trabalho em equipe para alcançar resultados excepcionais.</p>
          </div>
          
          <div class="bg-white/10 backdrop-blur-sm p-6 rounded-xl hover-card">
            <Icon name="ph:chart-line-up-bold" class="w-10 h-10 text-purple-300 mx-auto mb-4" />
            <h3 class="text-xl font-semibold text-white mb-2">Eficiência</h3>
            <p class="text-blue-100">Otimizamos processos para que equipes possam focar no que realmente importa.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Não é necessário script adicional
</script>

<style scoped>
.circle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 70%);
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -150px;
  left: -150px;
}

.circle-2 {
  width: 500px;
  height: 500px;
  top: 50%;
  right: -250px;
  transform: translateY(-50%);
}

.circle-3 {
  width: 200px;
  height: 200px;
  bottom: -100px;
  left: 30%;
}

.hover-card {
  transition: all 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
  background-color: rgba(255, 255, 255, 0.15);
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.animate-pulse {
  animation: pulse 3s infinite;
}
</style>