/**
 * Componentes Dashboard
 *
 * Estes componentes são usados para criar diferentes tipos de dashboards
 * baseados no papel do usuário no sistema.
 */

// Importação direta para evitar duplicação de componentes no registro automático do Nuxt
import AdminDashboard from './AdminDashboard.vue';
import AuditorDashboard from './AuditorDashboard.vue';
import ProjectManagerDashboard from './ProjectManagerDashboard.vue';
import RoleBasedDashboard from './RoleBasedDashboard.vue';
import StakeholderDashboard from './StakeholderDashboard.vue';
import TeamLeaderDashboard from './TeamLeaderDashboard.vue';
import TeamMemberDashboard from './TeamMemberDashboard.vue';

// Exportação explícita dos componentes
export {
  AdminDashboard,
  AuditorDashboard,
  ProjectManagerDashboard,
  RoleBasedDashboard,
  StakeholderDashboard,
  TeamLeaderDashboard,
  TeamMemberDashboard
};

// Exportação padrão para uso com importações default
export default {
  AdminDashboard,
  AuditorDashboard,
  ProjectManagerDashboard,
  RoleBasedDashboard,
  StakeholderDashboard,
  TeamLeaderDashboard,
  TeamMemberDashboard
};
