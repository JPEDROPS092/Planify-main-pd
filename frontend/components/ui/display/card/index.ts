/**
 * Componentes de Card
 *
 * Componentes para criação de cards e seus elementos internos como cabeçalho,
 * conteúdo, título, descrição e rodapé.
 */

// Importação dos componentes
import Card from './Card.vue';
import CardContent from './CardContent.vue';
import CardDescription from './CardDescription.vue';
import CardFooter from './CardFooter.vue';
import CardHeader from './CardHeader.vue';
import CardTitle from './CardTitle.vue';

// Exportação explícita dos componentes
export {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle
};

// Exportação padrão para uso com importações default
export default {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle
};