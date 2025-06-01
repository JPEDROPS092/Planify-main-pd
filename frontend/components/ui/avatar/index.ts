/**
 * Componentes de Avatar
 *
 * Estes componentes são usados para exibir avatares de usuários ou entidades.
 * Suportam imagens, fallbacks e diferentes tamanhos e formas.
 */
import { cva, type VariantProps } from 'class-variance-authority';

// Importação direta para evitar duplicação de componentes no registro automático do Nuxt
import Avatar from './Avatar.vue';
import AvatarFallback from './AvatarFallback.vue';
import AvatarImage from './AvatarImage.vue';

// Exportação explícita dos componentes
export { Avatar, AvatarFallback, AvatarImage };

/**
 * Variantes do Avatar
 *
 * Definem os diferentes estilos que podem ser aplicados ao componente Avatar.
 * - size: Controla o tamanho do avatar (sm, base, lg)
 * - shape: Controla a forma do avatar (circle, square)
 */
export const avatarVariant = cva(
  'inline-flex items-center justify-center font-normal text-foreground select-none shrink-0 bg-secondary overflow-hidden',
  {
    variants: {
      size: {
        sm: 'h-10 w-10 text-xs',
        base: 'h-16 w-16 text-2xl',
        lg: 'h-32 w-32 text-5xl',
      },
      shape: {
        circle: 'rounded-full',
        square: 'rounded-md',
      },
    },
    defaultVariants: {
      size: 'sm',
      shape: 'circle',
    },
  }
);

export type AvatarVariants = VariantProps<typeof avatarVariant>;
