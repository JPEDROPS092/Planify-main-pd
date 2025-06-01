/**
 * Componente Breadcrumbs
 *
 * Este componente exibe a navegação hierárquica de páginas.
 * Útil para mostrar o caminho de navegação atual e permitir retornar a páginas anteriores.
 */

// Importação direta para evitar duplicação de componentes no registro automático do Nuxt
import Breadcrumbs from './Breadcrumbs.vue';
import type { BreadcrumbItem } from './Breadcrumbs.vue';

// Exportação explícita do componente e tipos
export { Breadcrumbs };
export type { BreadcrumbItem };
