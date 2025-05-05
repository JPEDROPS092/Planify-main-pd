<template>
  <div class="min-h-screen bg-background font-sans antialiased">
    <LayoutHeader />
    <main class="container mx-auto py-6 px-4 md:px-6">
      <slot />
    </main>
    <footer class="border-t py-6 md:py-0">
      <div class="container flex flex-col items-center justify-between gap-4 md:h-16 md:flex-row">
        <p class="text-sm text-muted-foreground md:text-base">
          &copy; {{ new Date().getFullYear() }} Planify. Todos os direitos reservados.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Layout padrão
</script>
