import { cva, type VariantProps } from 'class-variance-authority';

// Define os estilos variantes usando class-variance-authority (cva)
export const avatarVariant = cva(
  'inline-flex items-center justify-center overflow-hidden', // classes base
  {
    variants: {
      size: {
        sm: 'h-8 w-8 text-sm',
        base: 'h-10 w-10 text-base',
        lg: 'h-14 w-14 text-lg',
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

// Exporta a tipagem baseada nas variantes do avatar
export type AvatarVariants = VariantProps<typeof avatarVariant>;
