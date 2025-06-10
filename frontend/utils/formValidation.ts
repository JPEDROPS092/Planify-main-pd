/**
 * Utilitários para validação de formulários
 * Funções para validar campos de formulários e exibir mensagens de erro
 */

/**
 * Interface para regras de validação
 */
export interface ValidationRule {
  validate: (value: any) => boolean;
  message: string;
}

/**
 * Interface para resultado de validação
 */
export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

/**
 * Valida um valor com base em um conjunto de regras
 * @param value Valor a validar
 * @param rules Regras de validação
 * @returns Resultado da validação
 */
export const validateField = (value: any, rules: ValidationRule[]): ValidationResult => {
  const errors: string[] = [];
  
  for (const rule of rules) {
    if (!rule.validate(value)) {
      errors.push(rule.message);
    }
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
};

/**
 * Regras de validação comuns
 */
export const validationRules = {
  /**
   * Verifica se um campo é obrigatório
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  required: (message = 'Este campo é obrigatório'): ValidationRule => ({
    validate: (value) => {
      if (value === null || value === undefined) return false;
      if (typeof value === 'string') return value.trim() !== '';
      if (Array.isArray(value)) return value.length > 0;
      return true;
    },
    message
  }),
  
  /**
   * Verifica se um campo tem um comprimento mínimo
   * @param min Comprimento mínimo
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  minLength: (min: number, message?: string): ValidationRule => ({
    validate: (value) => {
      if (value === null || value === undefined) return false;
      if (typeof value !== 'string') return false;
      return value.length >= min;
    },
    message: message || `Este campo deve ter pelo menos ${min} caracteres`
  }),
  
  /**
   * Verifica se um campo tem um comprimento máximo
   * @param max Comprimento máximo
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  maxLength: (max: number, message?: string): ValidationRule => ({
    validate: (value) => {
      if (value === null || value === undefined) return true;
      if (typeof value !== 'string') return false;
      return value.length <= max;
    },
    message: message || `Este campo deve ter no máximo ${max} caracteres`
  }),
  
  /**
   * Verifica se um campo é um email válido
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  email: (message = 'Digite um email válido'): ValidationRule => ({
    validate: (value) => {
      if (!value) return true; // Permitir vazio (use required para tornar obrigatório)
      if (typeof value !== 'string') return false;
      
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(value);
    },
    message
  }),
  
  /**
   * Verifica se um campo é um número
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  number: (message = 'Digite um número válido'): ValidationRule => ({
    validate: (value) => {
      if (value === null || value === undefined || value === '') return true;
      return !isNaN(Number(value));
    },
    message
  }),
  
  /**
   * Verifica se um número está dentro de um intervalo
   * @param min Valor mínimo
   * @param max Valor máximo
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  range: (min: number, max: number, message?: string): ValidationRule => ({
    validate: (value) => {
      if (value === null || value === undefined || value === '') return true;
      const num = Number(value);
      return !isNaN(num) && num >= min && num <= max;
    },
    message: message || `O valor deve estar entre ${min} e ${max}`
  }),
  
  /**
   * Verifica se um campo corresponde a um padrão regex
   * @param pattern Padrão regex
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  pattern: (pattern: RegExp, message = 'Formato inválido'): ValidationRule => ({
    validate: (value) => {
      if (!value) return true; // Permitir vazio (use required para tornar obrigatório)
      if (typeof value !== 'string') return false;
      return pattern.test(value);
    },
    message
  }),
  
  /**
   * Verifica se um campo é igual a outro
   * @param compareValue Valor para comparação
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  equals: (compareValue: any, message = 'Os valores não correspondem'): ValidationRule => ({
    validate: (value) => value === compareValue,
    message
  }),
  
  /**
   * Verifica se uma data é válida
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  date: (message = 'Digite uma data válida'): ValidationRule => ({
    validate: (value) => {
      if (!value) return true; // Permitir vazio (use required para tornar obrigatório)
      const date = new Date(value);
      return !isNaN(date.getTime());
    },
    message
  }),
  
  /**
   * Verifica se uma data é posterior a outra
   * @param compareDate Data para comparação
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  dateAfter: (compareDate: Date | string, message?: string): ValidationRule => ({
    validate: (value) => {
      if (!value) return true; // Permitir vazio (use required para tornar obrigatório)
      
      const date = new Date(value);
      if (isNaN(date.getTime())) return false;
      
      const comparison = new Date(compareDate);
      if (isNaN(comparison.getTime())) return false;
      
      return date > comparison;
    },
    message: message || 'A data deve ser posterior à data de referência'
  }),
  
  /**
   * Verifica se um arquivo tem um tamanho máximo
   * @param maxSizeInMB Tamanho máximo em MB
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  fileSize: (maxSizeInMB: number, message?: string): ValidationRule => ({
    validate: (value) => {
      if (!value) return true; // Permitir vazio (use required para tornar obrigatório)
      if (!(value instanceof File)) return false;
      
      const maxSizeInBytes = maxSizeInMB * 1024 * 1024;
      return value.size <= maxSizeInBytes;
    },
    message: message || `O arquivo deve ter no máximo ${maxSizeInMB}MB`
  }),
  
  /**
   * Verifica se um arquivo tem uma extensão permitida
   * @param allowedExtensions Array de extensões permitidas (sem ponto)
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  fileType: (allowedExtensions: string[], message?: string): ValidationRule => ({
    validate: (value) => {
      if (!value) return true; // Permitir vazio (use required para tornar obrigatório)
      if (!(value instanceof File)) return false;
      
      const extension = value.name.split('.').pop()?.toLowerCase() || '';
      return allowedExtensions.includes(extension);
    },
    message: message || `Tipos de arquivo permitidos: ${allowedExtensions.join(', ')}`
  }),
  
  /**
   * Verifica se um CPF é válido
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  cpf: (message = 'Digite um CPF válido'): ValidationRule => ({
    validate: (value) => {
      if (!value) return true; // Permitir vazio (use required para tornar obrigatório)
      if (typeof value !== 'string') return false;
      
      // Remover caracteres não numéricos
      const cpf = value.replace(/[^\d]/g, '');
      
      // Verificar se tem 11 dígitos
      if (cpf.length !== 11) return false;
      
      // Verificar se todos os dígitos são iguais
      if (/^(\d)\1+$/.test(cpf)) return false;
      
      // Validar dígitos verificadores
      let sum = 0;
      let remainder;
      
      // Primeiro dígito verificador
      for (let i = 1; i <= 9; i++) {
        sum += parseInt(cpf.substring(i - 1, i)) * (11 - i);
      }
      
      remainder = (sum * 10) % 11;
      if (remainder === 10 || remainder === 11) remainder = 0;
      if (remainder !== parseInt(cpf.substring(9, 10))) return false;
      
      // Segundo dígito verificador
      sum = 0;
      for (let i = 1; i <= 10; i++) {
        sum += parseInt(cpf.substring(i - 1, i)) * (12 - i);
      }
      
      remainder = (sum * 10) % 11;
      if (remainder === 10 || remainder === 11) remainder = 0;
      if (remainder !== parseInt(cpf.substring(10, 11))) return false;
      
      return true;
    },
    message
  }),
  
  /**
   * Verifica se um CNPJ é válido
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  cnpj: (message = 'Digite um CNPJ válido'): ValidationRule => ({
    validate: (value) => {
      if (!value) return true; // Permitir vazio (use required para tornar obrigatório)
      if (typeof value !== 'string') return false;
      
      // Remover caracteres não numéricos
      const cnpj = value.replace(/[^\d]/g, '');
      
      // Verificar se tem 14 dígitos
      if (cnpj.length !== 14) return false;
      
      // Verificar se todos os dígitos são iguais
      if (/^(\d)\1+$/.test(cnpj)) return false;
      
      // Validar dígitos verificadores
      let size = cnpj.length - 2;
      let numbers = cnpj.substring(0, size);
      const digits = cnpj.substring(size);
      let sum = 0;
      let pos = size - 7;
      
      // Primeiro dígito verificador
      for (let i = size; i >= 1; i--) {
        sum += parseInt(numbers.charAt(size - i)) * pos--;
        if (pos < 2) pos = 9;
      }
      
      let result = sum % 11 < 2 ? 0 : 11 - (sum % 11);
      if (result !== parseInt(digits.charAt(0))) return false;
      
      // Segundo dígito verificador
      size += 1;
      numbers = cnpj.substring(0, size);
      sum = 0;
      pos = size - 7;
      
      for (let i = size; i >= 1; i--) {
        sum += parseInt(numbers.charAt(size - i)) * pos--;
        if (pos < 2) pos = 9;
      }
      
      result = sum % 11 < 2 ? 0 : 11 - (sum % 11);
      if (result !== parseInt(digits.charAt(1))) return false;
      
      return true;
    },
    message
  }),
  
  /**
   * Verifica se um telefone é válido
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  phone: (message = 'Digite um telefone válido'): ValidationRule => ({
    validate: (value) => {
      if (!value) return true; // Permitir vazio (use required para tornar obrigatório)
      if (typeof value !== 'string') return false;
      
      // Remover caracteres não numéricos
      const phone = value.replace(/[^\d]/g, '');
      
      // Verificar se tem entre 10 e 11 dígitos (fixo ou celular)
      return phone.length >= 10 && phone.length <= 11;
    },
    message
  }),
  
  /**
   * Verifica se um CEP é válido
   * @param message Mensagem de erro personalizada
   * @returns Regra de validação
   */
  cep: (message = 'Digite um CEP válido'): ValidationRule => ({
    validate: (value) => {
      if (!value) return true; // Permitir vazio (use required para tornar obrigatório)
      if (typeof value !== 'string') return false;
      
      // Remover caracteres não numéricos
      const cep = value.replace(/[^\d]/g, '');
      
      // Verificar se tem 8 dígitos
      return cep.length === 8;
    },
    message
  })
};
