<template>
  <!-- 
    Container que recebe largura e altura via props, e ainda pode receber classes 
    extras para estilização. A classe "animate-pulse" gera um efeito de pulsar.
  -->
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
    /**
     * Largura do placeholder (pode ser '100%', '80px', '2rem' etc.).
     * @default '100%'
     */
    width: {
      type: String,
      default: '100%',
    },

    /**
     * Altura do placeholder (pode ser '1rem', '20px', '50px' etc.).
     * @default '1rem'
     */
    height: {
      type: String,
      default: '1rem',
    },

    /**
     * Classes adicionais para customizar o SkeletonLoader, se necessário.
     * @default ''
     */
    className: {
      type: String,
      default: '',
    },
  },
});
</script>

<style scoped>
/* 
  Se desejar, você pode adicionar estilos específicos, 
  por exemplo, para variar a cor ou bordas no modo escuro. 
  Mas as classes já aplicam um fundo cinza claro/escuro e bordas arredondadas.
*/
</style>
