/**
 * Componentes Planify
 *
 * Este arquivo exporta todos os componentes organizados do projeto Planify.
 * Facilita a importação de componentes em qualquer lugar do projeto.
 */

// Importação dos componentes organizados
import * as UI from './ui';
import * as Shared from './shared';
import * as Business from './business';

// Exportação explícita dos componentes
export { UI, Shared, Business };

// Exportação padrão para uso com importações default
export default { UI, Shared, Business };
