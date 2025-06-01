/**
 * Componentes Compartilhados
 *
 * Este arquivo exporta componentes compartilhados que podem ser usados em diferentes partes da aplicação.
 */

// Importação dos componentes por categoria
import * as Auth from './auth';
import * as Data from './data';
import * as Feedback from './feedback';
import * as Forms from './forms';
import * as Layout from './layout';
import * as Examples from './examples';

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
