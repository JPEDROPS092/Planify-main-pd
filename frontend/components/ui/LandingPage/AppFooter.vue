<template>
  <footer class="bg-gray-800 text-gray-300 py-12">
    <div class="container mx-auto px-6">
      <div class="grid md:grid-cols-3 gap-8 mb-8">
        <div>
          <h3 class="text-xl font-semibold text-white mb-4">Planify</h3>
          <p class="text-sm text-gray-400">
            Solução completa para gerenciamento de projetos de P&D.
          </p>
          <div class="mt-4 flex space-x-4">
            <a href="https://github.com/jpedrops092/Planify-main-pd" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-blue-400 transition-colors">
              <Icon name="mdi:github" class="w-6 h-6" />
            </a>
            <!-- Adicione mais links de redes sociais se necessário -->
            <!-- Exemplo: Discord (precisa de um ícone como mdi:discord ou simple-icons:discord) -->
            <!-- <a href="https://discord.gg/planify" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-blue-400 transition-colors">
              <Icon name="mdi:discord" class="w-6 h-6" />
            </a> -->
          </div>
        </div>

        <div>
          <h4 class="text-lg font-semibold text-white mb-4">Links Rápidos</h4>
          <ul class="space-y-2">
            <li><NuxtLink to="/auth/login" class="hover:text-blue-400 transition-colors text-sm">Login</NuxtLink></li>
            <li><NuxtLink to="/auth/registro" class="hover:text-blue-400 transition-colors text-sm">Criar Conta</NuxtLink></li>
            <li><NuxtLink to="/#features" class="hover:text-blue-400 transition-colors text-sm">Funcionalidades</NuxtLink></li>
            <li><NuxtLink to="/#mission" class="hover:text-blue-400 transition-colors text-sm">Nossa Missão</NuxtLink></li>
            <!-- Adicione link para Documentação se existir -->
            <!-- <li><a href="https://planify-docs.com" target="_blank" rel="noopener noreferrer" class="hover:text-blue-400 transition-colors text-sm">Documentação</a></li> -->
          </ul>
        </div>

        <div>
          <h4 class="text-lg font-semibold text-white mb-4">Contato</h4>
          <ul class="space-y-2 text-sm">
            <!-- <li><p>Email: contato@planify.com</p></li> -->
            <!-- <li><p>Telefone: (XX) XXXX-XXXX</p></li> -->
            <li>
              <a href="https://github.com/jpedrops092/Planify-main-pd/issues" target="_blank" rel="noopener noreferrer" class="hover:text-blue-400 transition-colors">
                Reportar um Problema
              </a>
            </li>
          </ul>
        </div>
      </div>
      <div class="border-t border-gray-700 pt-8 text-center text-sm text-gray-500">
        <p>© {{ new Date().getFullYear() }} Planify. Todos os direitos reservados.</p>
        <p>Licenciado sob a <a href="https://github.com/jpedrops092/Planify-main-pd/blob/main/LICENSE" target="_blank" rel="noopener noreferrer" class="text-blue-400 hover:underline">Licença MIT</a>.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
// Nenhum script específico necessário aqui
</script>

<style scoped>
/* Estilos para o Footer, se necessário */
</style>