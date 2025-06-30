import { ref, readonly, type Ref } from 'vue'

export interface Toast {
  id: string
  title: string
  description?: string
  type: 'success' | 'error' | 'warning' | 'info'
  duration?: number
}

export interface ToastAction {
  label: string
  onClick: () => void
}

interface UseToastReturn {
  toasts: Readonly<Ref<Toast[]>>
  toast: (options: Omit<Toast, 'id'>) => void
  dismissToast: (id: string) => void
  clearAllToasts: () => void
}

const toasts = ref<Toast[]>([])

let toastIdCounter = 0

function generateToastId(): string {
  return `toast-${++toastIdCounter}`
}

export function useToast(): UseToastReturn {
  const toast = (options: Omit<Toast, 'id'>) => {
    const id = generateToastId()
    const duration = options.duration ?? 5000

    const newToast: Toast = {
      id,
      ...options
    }

    toasts.value.push(newToast)

    // Auto-dismiss after duration
    if (duration > 0) {
      setTimeout(() => {
        dismissToast(id)
      }, duration)
    }
  }

  const dismissToast = (id: string) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  const clearAllToasts = () => {
    toasts.value = []
  }

  return {
    toasts: readonly(toasts),
    toast,
    dismissToast,
    clearAllToasts
  }
}

// Convenience methods
export function useToastHelpers() {
  const { toast } = useToast()

  return {
    success: (title: string, description?: string) => {
      toast({ title, description, type: 'success' })
    },
    error: (title: string, description?: string) => {
      toast({ title, description, type: 'error' })
    },
    warning: (title: string, description?: string) => {
      toast({ title, description, type: 'warning' })
    },
    info: (title: string, description?: string) => {
      toast({ title, description, type: 'info' })
    }
  }
}
