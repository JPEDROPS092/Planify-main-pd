/**
 * Componentes Card
 *
 * Estes componentes são usados para criar cartões de conteúdo com diferentes seções.
 * Suportam cabeçalho, conteúdo, rodapé, título e descrição.
 */

// Importação direta para evitar duplicação de componentes no registro automático do Nuxt
import Card from './Card.vue';
import CardHeader from './CardHeader.vue';
import CardFooter from './CardFooter.vue';
import CardTitle from './CardTitle.vue';
import CardDescription from './CardDescription.vue';
import CardContent from './CardContent.vue';

// Exportação explícita dos componentes
export {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardDescription,
  CardContent,
};
