/**
 * Componente Timeline
 *
 * Este componente exibe eventos em ordem cronológica.
 * Útil para históricos de projetos, atividades e marcos.
 */

// Importação direta para evitar duplicação de componentes no registro automático do Nuxt
import Timeline from './Timeline.vue';
import type { TimelineItem } from './Timeline.vue';

// Exportação explícita do componente e tipos
export { Timeline };
export type { TimelineItem };
