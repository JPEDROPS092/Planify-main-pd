<template>
  <div class="w-full overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700">
    <!-- Cabeçalho da tabela -->
    <div class="bg-gray-50 dark:bg-gray-800 px-4 py-3 flex items-center justify-between">
      <SkeletonLoader width="150px" height="24px" />
      <SkeletonLoader width="120px" height="32px" />
    </div>
    
    <!-- Corpo da tabela -->
    <div class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
      <div v-for="i in rows" :key="i" class="px-4 py-4">
        <div class="flex items-center space-x-4">
          <SkeletonLoader v-if="showCheckbox" width="20px" height="20px" className="rounded" />
          <div class="flex-1 space-y-2">
            <div class="flex justify-between">
              <SkeletonLoader width="40%" height="20px" />
              <SkeletonLoader width="20%" height="20px" />
            </div>
            <div v-if="showDescription" class="flex">
              <SkeletonLoader width="70%" height="16px" />
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Rodapé com paginação -->
    <div v-if="showPagination" class="bg-gray-50 dark:bg-gray-800 px-4 py-3 flex items-center justify-between">
      <SkeletonLoader width="100px" height="20px" />
      <div class="flex space-x-2">
        <SkeletonLoader width="32px" height="32px" className="rounded" />
        <SkeletonLoader width="32px" height="32px" className="rounded" />
        <SkeletonLoader width="32px" height="32px" className="rounded" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import SkeletonLoader from '~/components/shared/feedback/loading';

defineProps({
  rows: {
    type: Number,
    default: 5
  },
  showCheckbox: {
    type: Boolean,
    default: false
  },
  showDescription: {
    type: Boolean,
    default: true
  },
  showPagination: {
    type: Boolean,
    default: true
  }
});
</script>
