<template>
  <div
    :class="[
      'animate-pulse rounded-md bg-gray-200 dark:bg-gray-700',
      className,
    ]"
    :style="{
      width: width,
      height: height,
    }"
  ></div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'SkeletonLoader',
  props: {
    width: {
      type: String,
      default: '100%',
    },
    height: {
      type: String,
      default: '1rem',
    },
    className: {
      type: String,
      default: '',
    },
  },
});
</script>
