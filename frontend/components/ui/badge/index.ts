/**
 * Componente Badge
 *
 * Este componente é usado para exibir etiquetas, status ou pequenas informações destacadas.
 * Suporta diferentes variantes visuais para diferentes contextos de uso.
 */
import { cva, type VariantProps } from 'class-variance-authority';

// Importação direta para evitar duplicação de componentes no registro automático do Nuxt
import Badge from './Badge.vue';

// Exportação explícita do componente
export { Badge };

/**
 * Variantes do Badge
 *
 * Definem os diferentes estilos que podem ser aplicados ao componente Badge.
 * - default: Estilo padrão com fundo escuro
 * - secondary: Estilo secundário com fundo mais claro
 * - outline: Estilo com apenas borda
 * - destructive: Estilo para ações destrutivas ou alertas
 * - success: Estilo para indicar sucesso ou conclusão
 */
export const badgeVariants = cva(
  'inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:
          'border-transparent bg-primary text-primary-foreground shadow hover:bg-primary/80',
        secondary:
          'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
        outline: 'text-foreground',
        destructive:
          'border-transparent bg-destructive text-destructive-foreground shadow hover:bg-destructive/80',
        success:
          'border-transparent bg-green-500 text-white shadow hover:bg-green-600',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export type BadgeVariants = VariantProps<typeof badgeVariants>;
