export const useToast = () => {
  const showToast = (message: string, type: 'success' | 'error' | 'info' = 'info') => {
    // Esta é uma implementação simples
    // Em um projeto real, você usaria o composable do Shadcn para toast
    alert(`${type.toUpperCase()}: ${message}`);
  };

  return {
    toast: (options: { title: string; description?: string; variant?: 'default' | 'destructive' }) => {
      const type = options.variant === 'destructive' ? 'error' : 'info';
      showToast(`${options.title} - ${options.description || ''}`, type);
    },
    success: (message: string) => showToast(message, 'success'),
    error: (message: string) => showToast(message, 'error'),
    info: (message: string) => showToast(message, 'info'),
  };
};
