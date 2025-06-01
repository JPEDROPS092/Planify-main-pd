/**
 * Componentes de Dashboard baseados em papel
 *
 * Dashboards específicos para cada papel de usuário no sistema.
 */

// Importação dos componentes
import AdminDashboard from './AdminDashboard.vue';
import AuditorDashboard from './AuditorDashboard.vue';
import ProjectManagerDashboard from './ProjectManagerDashboard.vue';
import StakeholderDashboard from './StakeholderDashboard.vue';
import TeamLeaderDashboard from './TeamLeaderDashboard.vue';
import TeamMemberDashboard from './TeamMemberDashboard.vue';

// Exportação explícita dos componentes
export {
  AdminDashboard,
  AuditorDashboard,
  ProjectManagerDashboard,
  StakeholderDashboard,
  TeamLeaderDashboard,
  TeamMemberDashboard
};

// Exportação padrão para uso com importações default
export default {
  AdminDashboard,
  AuditorDashboard,
  ProjectManagerDashboard,
  StakeholderDashboard,
  TeamLeaderDashboard,
  TeamMemberDashboard
};
