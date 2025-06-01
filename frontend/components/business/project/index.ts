/**
 * Componentes de Projeto
 *
 * Componentes específicos para projetos organizados por categorias.
 */

// Importação dos componentes por categoria
import * as Management from './management';
import * as Planning from './planning';
import * as Tasks from './tasks';
import * as Team from './team';
import * as Resources from './resources';

// Exportação explícita dos componentes
export {
  Management,
  Planning,
  Tasks,
  Team,
  Resources
};

// Exportação padrão para uso com importações default
export default {
  Management,
  Planning,
  Tasks,
  Team,
  Resources
};
