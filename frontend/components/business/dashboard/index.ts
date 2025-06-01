/**
 * Componentes de Dashboard
 *
 * Componentes específicos para dashboards e painéis de controle.
 */

// Importação dos componentes
import RoleBasedDashboard from './RoleBasedDashboard.vue';
import ProjectDashboard from './ProjectDashboard.vue';

// Importação dos componentes baseados em papel
import * as RoleBased from './role-based';

// Exportação explícita dos componentes
export { 
  RoleBasedDashboard,
  ProjectDashboard,
  RoleBased
};

// Exportação padrão para uso com importações default
export default { 
  RoleBasedDashboard,
  ProjectDashboard,
  RoleBased
};
