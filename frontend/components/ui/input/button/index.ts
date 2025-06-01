/**
 * Componente Button
 *
 * Este componente é usado para ações interativas como submissão de formulários,
 * navegação, ou qualquer interação que requeira um botão.
 * Suporta diferentes variantes visuais e tamanhos.
 */
import { cva, type VariantProps } from 'class-variance-authority';

// Importação direta para evitar duplicação de componentes no registro automático do Nuxt
import Button from './Button.vue';

// Exportação explícita do componente
export { Button };

/**
 * Variantes do Button
 *
 * Definem os diferentes estilos que podem ser aplicados ao componente Button.
 * - variant: Controla o estilo visual (default, secondary, outline, ghost, link, destructive, success)
 * - size: Controla o tamanho do botão (default, sm, lg, icon)
 */
export const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default:
          'bg-primary text-primary-foreground shadow hover:bg-primary/90',
        destructive:
          'bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90',
        outline:
          'border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground',
        secondary:
          'bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
        success: 'bg-green-500 text-white shadow-sm hover:bg-green-600',
      },
      size: {
        default: 'h-9 px-4 py-2',
        sm: 'h-8 rounded-md px-3 text-xs',
        lg: 'h-10 rounded-md px-8',
        icon: 'h-9 w-9',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export type ButtonVariants = VariantProps<typeof buttonVariants>;
