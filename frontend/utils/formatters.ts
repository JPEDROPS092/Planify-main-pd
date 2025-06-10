/**
 * Utilitários para formatação de dados
 * Funções para formatar datas, moedas, números e outros tipos de dados
 */

/**
 * Formata uma data para exibição no formato brasileiro
 * @param date Data a ser formatada (string ISO ou objeto Date)
 * @param includeTime Se deve incluir o horário
 * @returns String formatada (DD/MM/YYYY ou DD/MM/YYYY HH:MM)
 */
export const formatDate = (date: string | Date | null | undefined, includeTime = false): string => {
  if (!date) return '-';
  
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  
  if (isNaN(dateObj.getTime())) {
    return '-';
  }
  
  const day = dateObj.getDate().toString().padStart(2, '0');
  const month = (dateObj.getMonth() + 1).toString().padStart(2, '0');
  const year = dateObj.getFullYear();
  
  if (!includeTime) {
    return `${day}/${month}/${year}`;
  }
  
  const hours = dateObj.getHours().toString().padStart(2, '0');
  const minutes = dateObj.getMinutes().toString().padStart(2, '0');
  
  return `${day}/${month}/${year} ${hours}:${minutes}`;
};

/**
 * Formata um valor monetário para o formato brasileiro
 * @param value Valor a ser formatado
 * @param currency Símbolo da moeda (padrão: R$)
 * @returns String formatada (R$ 1.234,56)
 */
export const formatCurrency = (value: number | string | null | undefined, currency = 'R$'): string => {
  if (value === null || value === undefined) return '-';
  
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(numValue)) {
    return '-';
  }
  
  return `${currency} ${numValue.toLocaleString('pt-BR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}`;
};

/**
 * Formata um número para o formato brasileiro
 * @param value Valor a ser formatado
 * @param decimals Número de casas decimais
 * @returns String formatada (1.234,56)
 */
export const formatNumber = (
  value: number | string | null | undefined,
  decimals = 2
): string => {
  if (value === null || value === undefined) return '-';
  
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(numValue)) {
    return '-';
  }
  
  return numValue.toLocaleString('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  });
};

/**
 * Formata uma porcentagem para o formato brasileiro
 * @param value Valor a ser formatado (0-100 ou 0-1)
 * @param decimals Número de casas decimais
 * @returns String formatada (12,34%)
 */
export const formatPercent = (
  value: number | string | null | undefined,
  decimals = 1
): string => {
  if (value === null || value === undefined) return '-';
  
  let numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  if (isNaN(numValue)) {
    return '-';
  }
  
  // Se o valor estiver entre 0 e 1, multiplicar por 100
  if (numValue > 0 && numValue < 1) {
    numValue = numValue * 100;
  }
  
  return `${numValue.toLocaleString('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  })}%`;
};

/**
 * Formata horas para exibição
 * @param hours Número de horas
 * @returns String formatada (1h 30min)
 */
export const formatHours = (hours: number | string | null | undefined): string => {
  if (hours === null || hours === undefined) return '-';
  
  const numHours = typeof hours === 'string' ? parseFloat(hours) : hours;
  
  if (isNaN(numHours)) {
    return '-';
  }
  
  const wholeHours = Math.floor(numHours);
  const minutes = Math.round((numHours - wholeHours) * 60);
  
  if (wholeHours === 0) {
    return `${minutes}min`;
  }
  
  if (minutes === 0) {
    return `${wholeHours}h`;
  }
  
  return `${wholeHours}h ${minutes}min`;
};

/**
 * Trunca um texto para um tamanho máximo
 * @param text Texto a ser truncado
 * @param maxLength Tamanho máximo
 * @param suffix Sufixo a adicionar (padrão: ...)
 * @returns Texto truncado
 */
export const truncateText = (
  text: string | null | undefined,
  maxLength = 100,
  suffix = '...'
): string => {
  if (!text) return '';
  
  if (text.length <= maxLength) {
    return text;
  }
  
  return text.substring(0, maxLength - suffix.length) + suffix;
};

/**
 * Formata um nome para exibir as iniciais
 * @param name Nome completo
 * @returns Iniciais (ex: JD para John Doe)
 */
export const getInitials = (name: string | null | undefined): string => {
  if (!name) return '';
  
  const parts = name.trim().split(' ');
  
  if (parts.length === 1) {
    return parts[0].substring(0, 2).toUpperCase();
  }
  
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
};

/**
 * Formata um nome para exibição
 * @param firstName Nome
 * @param lastName Sobrenome
 * @returns Nome formatado
 */
export const formatName = (
  firstName: string | null | undefined,
  lastName: string | null | undefined
): string => {
  if (!firstName && !lastName) return '';
  if (!firstName) return lastName || '';
  if (!lastName) return firstName;
  
  return `${firstName} ${lastName}`;
};

/**
 * Formata um telefone para o formato brasileiro
 * @param phone Número de telefone
 * @returns Telefone formatado ((11) 98765-4321)
 */
export const formatPhone = (phone: string | null | undefined): string => {
  if (!phone) return '';
  
  // Remover caracteres não numéricos
  const cleaned = phone.replace(/\D/g, '');
  
  if (cleaned.length === 11) {
    // Celular: (11) 98765-4321
    return `(${cleaned.substring(0, 2)}) ${cleaned.substring(2, 7)}-${cleaned.substring(7, 11)}`;
  } else if (cleaned.length === 10) {
    // Fixo: (11) 3456-7890
    return `(${cleaned.substring(0, 2)}) ${cleaned.substring(2, 6)}-${cleaned.substring(6, 10)}`;
  }
  
  return phone;
};

/**
 * Formata um tamanho de arquivo para exibição
 * @param bytes Tamanho em bytes
 * @param decimals Número de casas decimais
 * @returns Tamanho formatado (1.23 MB)
 */
export const formatFileSize = (bytes: number, decimals = 2): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(decimals))} ${sizes[i]}`;
};
