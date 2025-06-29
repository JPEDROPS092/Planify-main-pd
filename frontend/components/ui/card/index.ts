import { cva } from 'class-variance-authority';

export const cardVariants = cva('rounded-lg border bg-card text-card-foreground shadow-sm', {
  variants: {
    variant: {
      default: '',
      destructive: 'border-destructive',
      success: 'border-green-500',
    },
  },
  defaultVariants: {
    variant: 'default',
  },
});

// Export main Card component as default
export { default } from './Card.vue';

// Export sub-components individually
export { default as CardHeader } from './CardHeader.vue';
export { default as CardTitle } from './CardTitle.vue';
export { default as CardDescription } from './CardDescription.vue';
export { default as CardContent } from './CardContent.vue';
export { default as CardFooter } from './CardFooter.vue';
