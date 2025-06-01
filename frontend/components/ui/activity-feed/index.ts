/**
 * Componente ActivityFeed
 *
 * Este componente exibe atividades e atualizações recentes.
 * Útil para feeds de notificações, histórico de atividades e atualizações de projetos.
 */

// Importação direta para evitar duplicação de componentes no registro automático do Nuxt
import ActivityFeed from './ActivityFeed.vue';
import type { Activity } from './ActivityFeed.vue';

// Exportação explícita do componente e tipos
export { ActivityFeed };
export type { Activity };
