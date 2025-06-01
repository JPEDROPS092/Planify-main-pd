/**
 * Componentes UI
 *
 * Este arquivo exporta todos os componentes UI organizados por categorias.
 * Facilita a importação desses componentes em outros lugares do projeto.
 */

// Importação dos componentes por categoria
import * as Display from './display';
import * as Feedback from './feedback';
import * as Input from './input';
import * as Navigation from './navigation';
import * as Theme from './theme';

// Exportação explícita dos componentes
export {
  Display,
  Feedback,
  Input,
  Navigation,
  Theme
};

// Exportação padrão para uso com importações default
export default {
  Display,
  Feedback,
  Input,
  Navigation,
  Theme
};
