<template>
  <Suspense>
    <template #default>
      <slot />
    </template>
    <template #fallback>
      <slot name="fallback">
        <div class="p-4 space-y-4">
          <SkeletonLoader v-if="type === 'form'" height="24px" width="30%" />
          <SkeletonLoader v-if="type === 'form'" height="100px" />
          <SkeletonLoader v-if="type === 'form'" height="40px" />
          
          <TableSkeleton 
            v-if="type === 'table'" 
            :rows="rows" 
            :showCheckbox="showCheckbox" 
            :showDescription="showDescription" 
            :showPagination="showPagination" 
          />
          
          <div v-if="type === 'card'" class="space-y-3">
            <SkeletonLoader height="24px" width="50%" />
            <SkeletonLoader height="80px" />
            <div class="flex justify-between">
              <SkeletonLoader height="32px" width="120px" />
              <SkeletonLoader height="32px" width="80px" />
            </div>
          </div>
          
          <div v-if="type === 'chart'" class="flex flex-col items-center">
            <SkeletonLoader height="24px" width="50%" class="mb-4" />
            <SkeletonLoader height="300px" width="100%" class="rounded-lg" />
          </div>
          
          <div v-if="type === 'custom'" class="flex flex-col">
            <slot name="custom-skeleton" />
          </div>
        </div>
      </slot>
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import SkeletonLoader from './SkeletonLoader.vue';
import TableSkeleton from './TableSkeleton.vue';

defineProps({
  /**
   * Tipo de componente que está sendo carregado
   * Determina qual skeleton será exibido durante o carregamento
   */
  type: {
    type: String,
    default: 'form',
    validator: (value: string) => ['form', 'table', 'card', 'chart', 'custom'].includes(value)
  },
  
  /**
   * Número de linhas para o skeleton de tabela
   */
  rows: {
    type: Number,
    default: 5
  },
  
  /**
   * Exibir checkbox no skeleton de tabela
   */
  showCheckbox: {
    type: Boolean,
    default: false
  },
  
  /**
   * Exibir descrição no skeleton de tabela
   */
  showDescription: {
    type: Boolean,
    default: true
  },
  
  /**
   * Exibir paginação no skeleton de tabela
   */
  showPagination: {
    type: Boolean,
    default: true
  }
});
</script>
