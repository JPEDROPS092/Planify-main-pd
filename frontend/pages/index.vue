<template>
  <div class="space-y-8">
    <section class="py-12 md:py-24 lg:py-32 xl:py-48">
      <div class="container px-4 md:px-6">
        <div class="flex flex-col items-center space-y-4 text-center">
          <div class="space-y-2">
            <h1 class="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
              Planify - Gerenciamento de Projetos de P&D
            </h1>
            <p class="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
              Simplifique o gerenciamento de seus projetos de Pesquisa e Desenvolvimento com nossa plataforma completa.
            </p>
          </div>
          <div class="flex flex-wrap items-center justify-center gap-4">
            <NuxtLink to="/projetos">
              <Button variant="default" size="lg">Ver Projetos</Button>
            </NuxtLink>
            <NuxtLink to="/login">
              <Button variant="outline" size="lg">Entrar</Button>
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <section class="py-12 md:py-24 lg:py-32 bg-muted/50">
      <div class="container px-4 md:px-6">
        <div class="flex flex-col items-center justify-center space-y-4 text-center">
          <div class="space-y-2">
            <h2 class="text-3xl font-bold tracking-tighter md:text-4xl/tight">
              Recursos Principais
            </h2>
            <p class="mx-auto max-w-[600px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              Conheça os recursos que tornam o Planify a escolha ideal para gerenciamento de projetos de P&D.
            </p>
          </div>
        </div>
        <div class="mx-auto grid max-w-5xl grid-cols-1 gap-6 py-12 md:grid-cols-2 lg:grid-cols-3">
          <Card class="p-6">
            <div class="flex flex-col items-center space-y-2 text-center">
              <div class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
                <span class="text-xl">📊</span>
              </div>
              <h3 class="text-xl font-bold">Projetos</h3>
              <p class="text-muted-foreground">
                Gerencie seus projetos com facilidade, definindo sprints e acompanhando o progresso.
              </p>
            </div>
          </Card>
          <Card class="p-6">
            <div class="flex flex-col items-center space-y-2 text-center">
              <div class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
                <span class="text-xl">✅</span>
              </div>
              <h3 class="text-xl font-bold">Tarefas</h3>
              <p class="text-muted-foreground">
                Organize tarefas, atribua responsáveis e acompanhe o status de cada atividade.
              </p>
            </div>
          </Card>
          <Card class="p-6">
            <div class="flex flex-col items-center space-y-2 text-center">
              <div class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
                <span class="text-xl">👥</span>
              </div>
              <h3 class="text-xl font-bold">Equipes</h3>
              <p class="text-muted-foreground">
                Gerencie membros da equipe, atribuições e responsabilidades de forma eficiente.
              </p>
            </div>
          </Card>
          <Card class="p-6">
            <div class="flex flex-col items-center space-y-2 text-center">
              <div class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
                <span class="text-xl">⚠️</span>
              </div>
              <h3 class="text-xl font-bold">Riscos</h3>
              <p class="text-muted-foreground">
                Identifique, avalie e mitigue riscos para garantir o sucesso do projeto.
              </p>
            </div>
          </Card>
          <Card class="p-6">
            <div class="flex flex-col items-center space-y-2 text-center">
              <div class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
                <span class="text-xl">💰</span>
              </div>
              <h3 class="text-xl font-bold">Custos</h3>
              <p class="text-muted-foreground">
                Controle orçamentos e gastos do projeto com ferramentas de gestão financeira.
              </p>
            </div>
          </Card>
          <Card class="p-6">
            <div class="flex flex-col items-center space-y-2 text-center">
              <div class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
                <span class="text-xl">📄</span>
              </div>
              <h3 class="text-xl font-bold">Documentos</h3>
              <p class="text-muted-foreground">
                Gerencie documentação de projetos de forma centralizada e organizada.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
// Página inicial
</script>
