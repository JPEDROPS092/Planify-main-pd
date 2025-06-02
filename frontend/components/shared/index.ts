/**
 * Componentes Compartilhados
 *
 * Este arquivo exporta componentes compartilhados que podem ser usados em diferentes partes da aplicação.
 */

// Importação dos componentes por categoria
import * as Auth from '~/components/shared/auth/role-based';
import * as Data from '~/components/shared/data';
import * as Feedback from '~/components/shared/feedback';
import * as Forms from '~/components/shared/forms/project';
import * as Layout from '~/components/shared/layout/lazy';
import * as Examples from '~/components/shared/examples/api';

// Exportação explícita dos componentes
export {
  Auth,
  Data,
  Feedback,
  Forms,
  Layout,
  Examples
};

// Exportação padrão para uso com importações default
export default {
  Auth,
  Data,
  Feedback,
  Forms,
  Layout,
  Examples
};
