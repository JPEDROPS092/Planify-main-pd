import { shallowRef, markRaw, type Component } from 'vue';

/**
 * Utilitários para otimização de performance no Vue 3
 * Implementa técnicas para reduzir reatividade desnecessária e melhorar a renderização
 */

/**
 * Marca um componente como raw para evitar que o Vue o torne reativo
 * Útil para componentes que não precisam de reatividade interna
 * @param component Componente a ser marcado como raw
 */
export function markComponentRaw<T extends Component>(component: T): T {
  return markRaw(component);
}

/**
 * Cria uma referência superficial (shallow) para evitar reatividade profunda
 * Útil para grandes objetos de dados que não precisam de reatividade profunda
 * @param value Valor inicial
 */
export function createShallowState<T>(value: T) {
  return shallowRef(value);
}

/**
 * Gera uma chave única para uso em v-for
 * Importante para ajudar o Vue a otimizar a renderização de listas
 * @param item Item da lista
 * @param index Índice do item na lista
 * @param prefix Prefixo opcional para a chave
 */
export function getUniqueKey(item: any, index: number, prefix = 'item'): string {
  // Tenta usar um ID existente primeiro
  if (item?.id) {
    return `${prefix}-${item.id}`;
  }
  
  // Usa uma combinação de propriedades se disponíveis
  if (item?.nome && item?.data) {
    return `${prefix}-${item.nome}-${item.data}`;
  }
  
  // Fallback para índice com timestamp para garantir unicidade
  return `${prefix}-${index}-${Date.now()}`;
}

/**
 * Memoiza uma função para evitar recálculos desnecessários
 * Útil para funções de cálculo pesado que são chamadas frequentemente com os mesmos argumentos
 * @param fn Função a ser memoizada
 * @param resolver Função opcional para resolver a chave do cache
 */
export function memoize<T extends (...args: any[]) => any>(
  fn: T,
  resolver?: (...args: Parameters<T>) => string
): T {
  const cache = new Map<string, ReturnType<T>>();
  
  return ((...args: Parameters<T>): ReturnType<T> => {
    const key = resolver ? resolver(...args) : JSON.stringify(args);
    
    if (cache.has(key)) {
      return cache.get(key) as ReturnType<T>;
    }
    
    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
}

/**
 * Cria uma versão debounced de uma função
 * Útil para eventos que disparam muitas vezes como resize, scroll, input, etc.
 * @param fn Função a ser debounced
 * @param delay Tempo de espera em ms
 */
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay = 300
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout>;
  
  return function(...args: Parameters<T>): void {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

/**
 * Cria uma versão throttled de uma função
 * Útil para limitar a taxa de execução de funções em eventos frequentes
 * @param fn Função a ser throttled
 * @param limit Limite de tempo em ms
 */
export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  limit = 300
): (...args: Parameters<T>) => void {
  let inThrottle = false;
  
  return function(...args: Parameters<T>): void {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    }
  };
}
