<!--
  Breadcrumbs.vue
  
  Componente para navegação hierárquica de páginas.
  Exibe o caminho de navegação atual e permite retornar a páginas anteriores.
  
  Props:
  - items: Array de itens de navegação (links)
  - separator: Separador entre os itens
  - homeHref: URL da página inicial
  - homeLabel: Texto para o link da página inicial
  - class: Classes CSS adicionais
  
  Slots:
  - item: Slot para personalizar a renderização de cada item
  - separator: Slot para personalizar o separador
  - home: Slot para personalizar o link da página inicial
-->

<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '@/lib/utils';
import { ChevronRight, Home } from 'lucide-vue-next';

// Definir tipos para os itens de navegação
export interface BreadcrumbItem {
  label: string;
  href?: string;
  icon?: any; // Componente Lucide
  active?: boolean;
}

// Props do componente
const props = withDefaults(
  defineProps<{
    items: BreadcrumbItem[];
    separator?: string | any; // String ou componente Lucide
    homeHref?: string;
    homeLabel?: string;
    class?: string;
  }>(),
  {
    separator: ChevronRight,
    homeHref: '/',
    homeLabel: 'Início',
  }
);

// Verificar se deve exibir o link da página inicial
const showHome = computed(() => {
  return props.homeHref && props.homeLabel;
});

// Verificar se o item é o último (ativo)
const isLastItem = (index: number): boolean => {
  return index === props.items.length - 1;
};
</script>

<template>
  <nav
    :class="cn('flex items-center text-sm', props.class)"
    aria-label="Navegação de breadcrumb"
  >
    <ol class="flex flex-wrap items-center gap-1.5">
      <!-- Link da página inicial -->
      <li v-if="showHome" class="flex items-center">
        <slot name="home">
          <a
            :href="homeHref"
            class="flex items-center text-muted-foreground hover:text-foreground transition-colors"
          >
            <Home class="h-4 w-4" />
            <span v-if="homeLabel" class="sr-only">{{ homeLabel }}</span>
          </a>
        </slot>

        <!-- Separador após o link da página inicial -->
        <span class="mx-1.5 text-muted-foreground">
          <slot name="separator">
            <component
              :is="typeof separator === 'string' ? 'span' : separator"
              v-if="typeof separator === 'string'"
              class="h-4 w-4"
            >
              {{ separator }}
            </component>
            <component :is="separator" v-else class="h-4 w-4" />
          </slot>
        </span>
      </li>

      <!-- Itens de navegação -->
      <template v-for="(item, index) in items" :key="index">
        <li class="flex items-center">
          <!-- Slot para personalizar o item -->
          <slot name="item" :item="item" :is-last="isLastItem(index)">
            <a
              v-if="item.href && !isLastItem(index)"
              :href="item.href"
              class="flex items-center text-muted-foreground hover:text-foreground transition-colors"
            >
              <component
                v-if="item.icon"
                :is="item.icon"
                class="h-4 w-4 mr-1"
              />
              <span>{{ item.label }}</span>
            </a>
            <span
              v-else
              class="flex items-center font-medium"
              :class="{
                'text-foreground': isLastItem(index),
                'text-muted-foreground': !isLastItem(index),
              }"
            >
              <component
                v-if="item.icon"
                :is="item.icon"
                class="h-4 w-4 mr-1"
              />
              <span>{{ item.label }}</span>
            </span>
          </slot>

          <!-- Separador entre itens (exceto o último) -->
          <span v-if="!isLastItem(index)" class="mx-1.5 text-muted-foreground">
            <slot name="separator">
              <component
                :is="typeof separator === 'string' ? 'span' : separator"
                v-if="typeof separator === 'string'"
                class="h-4 w-4"
              >
                {{ separator }}
              </component>
              <component :is="separator" v-else class="h-4 w-4" />
            </slot>
          </span>
        </li>
      </template>
    </ol>
  </nav>
</template>

<style scoped>
/* Estilos específicos para o componente, se necessário */
</style>
