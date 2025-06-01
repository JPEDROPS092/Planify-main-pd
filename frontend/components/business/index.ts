/**
 * Componentes de Negócio
 *
 * Componentes específicos do domínio de negócio do Planify.
 */

// Importação dos componentes por categoria
import * as Cost from './cost';
import * as Risk from './risk';
import * as Dashboard from './dashboard';
import * as Project from './project';

// Exportação explícita dos componentes
export {
  Cost,
  Risk,
  Dashboard,
  Project
};

// Exportação padrão para uso com importações default
export default {
  Cost,
  Risk,
  Dashboard,
  Project
};
