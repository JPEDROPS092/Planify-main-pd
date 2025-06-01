/**
 * Componentes de Carregamento
 *
 * Componentes para exibir estados de carregamento e feedback visual durante operações assíncronas.
 */

// Importação direta para evitar duplicação de componentes no registro automático do Nuxt
import LoadingButton from './LoadingButton.vue';
import SkeletonLoader from './SkeletonLoader.vue';

// Exportação explícita dos componentes
export {
  LoadingButton,
  SkeletonLoader
};

// Exportação padrão para uso com importações default
export default {
  LoadingButton,
  SkeletonLoader
};
