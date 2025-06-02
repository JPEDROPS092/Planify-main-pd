/**
 * useFormValidation.ts
 *
 * Composable para validação de formulários com suporte a:
 * - Validação em tempo real com debounce
 * - Auto-save com debounce
 * - Feedback visual de status (salvo, salvando, erro)
 */

import { ref, watch, computed, onUnmounted } from 'vue';
import { z } from 'zod';

export type FormStatus =
  | 'idle'
  | 'validating'
  | 'valid'
  | 'invalid'
  | 'saving'
  | 'saved'
  | 'error';

export interface UseFormValidationOptions<T> {
  initialData: T;
  schema: z.ZodType<T>;
  onSave?: (data: T) => Promise<any> | any;
  autoSave?: boolean;
  autoSaveDebounce?: number;
  debounceValidation?: number;
}

export function useFormValidation<T extends Record<string, any>>(
  options: UseFormValidationOptions<T>
) {
  const {
    initialData,
    schema,
    onSave,
    autoSave = true,
    autoSaveDebounce = 2000,
    debounceValidation = 300,
  } = options;

  // Estado do formulário
  const formData = ref<T>({ ...initialData } as T);
  const errors = ref<Partial<Record<keyof T, string>>>({});
  const status = ref<FormStatus>('idle');
  const isDirty = ref(false);
  const lastSavedData = ref<T>({ ...initialData } as T);

  // Timers para debounce
  let validationTimer: ReturnType<typeof setTimeout> | null = null;
  let saveTimer: ReturnType<typeof setTimeout> | null = null;

  // Validar o formulário
  const validateForm = () => {
    status.value = 'validating';

    const result = schema.safeParse(formData.value);

    if (!result.success) {
      status.value = 'invalid';
      errors.value = result.error.issues.reduce(
        (acc, issue) => {
          const path = issue.path.join('.') as keyof T;
          acc[path] = issue.message;
          return acc;
        },
        {} as Partial<Record<keyof T, string>>
      );
      return false;
    }

    errors.value = {};
    status.value = 'valid';
    return true;
  };

  // Validar com debounce
  const debouncedValidate = () => {
    if (validationTimer) {
      clearTimeout(validationTimer);
    }

    validationTimer = setTimeout(() => {
      validateForm();

      // Iniciar auto-save se necessário
      if (autoSave && onSave && status.value === 'valid' && isDirty.value) {
        debouncedSave();
      }
    }, debounceValidation);
  };

  // Salvar com debounce
  const debouncedSave = () => {
    if (saveTimer) {
      clearTimeout(saveTimer);
    }

    saveTimer = setTimeout(async () => {
      if (!validateForm()) return;

      try {
        status.value = 'saving';
        const result = await onSave?.(formData.value);
        status.value = 'saved';
        lastSavedData.value = JSON.parse(JSON.stringify(formData.value));
        isDirty.value = false;
        return result;
      } catch (error) {
        console.error('Erro ao salvar formulário:', error);
        status.value = 'error';
        throw error;
      }
    }, autoSaveDebounce);
  };

  // Salvar manualmente
  const saveForm = async () => {
    if (!validateForm()) return null;

    try {
      status.value = 'saving';
      const result = await onSave?.(formData.value);
      status.value = 'saved';
      lastSavedData.value = JSON.parse(JSON.stringify(formData.value));
      isDirty.value = false;
      return result;
    } catch (error) {
      console.error('Erro ao salvar formulário:', error);
      status.value = 'error';
      throw error;
    }
  };

  // Resetar o formulário
  const resetForm = (newData?: T) => {
    formData.value = { ...(newData || initialData) } as T;
    errors.value = {};
    status.value = 'idle';
    isDirty.value = false;
    lastSavedData.value = JSON.parse(JSON.stringify(formData.value));
  };

  // Atualizar um campo específico
  const updateField = <K extends keyof T>(field: K, value: T[K]) => {
    formData.value[field] = value;
    isDirty.value = true;
    debouncedValidate();
  };

  // Verificar se o formulário é válido
  const isValid = computed(() => status.value === 'valid');

  // Verificar se o formulário está sendo salvo
  const isSaving = computed(() => status.value === 'saving');

  // Verificar se o formulário foi salvo
  const isSaved = computed(() => status.value === 'saved');

  // Verificar se houve erro
  const hasError = computed(() => status.value === 'error');

  // Observar mudanças no formData
  watch(
    formData,
    () => {
      isDirty.value = true;
      status.value = 'idle';
      debouncedValidate();
    },
    { deep: true }
  );

  // Limpar timers ao desmontar
  onUnmounted(() => {
    if (validationTimer) clearTimeout(validationTimer);
    if (saveTimer) clearTimeout(saveTimer);
  });

  return {
    formData,
    errors,
    status,
    isDirty,
    isValid,
    isSaving,
    isSaved,
    hasError,
    validateForm,
    saveForm,
    resetForm,
    updateField,
    formState: {
      formData: formData.value,
      errors: errors.value,
      isDirty,
      isValid: isValid.value,
      isSaving: isSaving.value,
      isSaved: isSaved.value,
      hasError: hasError.value,
    },
  };
}
