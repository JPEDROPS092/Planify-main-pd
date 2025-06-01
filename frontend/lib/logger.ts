/**
 * Utilitário de logging para o frontend
 * Fornece funções para logging formatado e consistente
 */

// Tipos de log
type LogLevel = 'info' | 'debug' | 'warn' | 'error';

// Cores para diferentes níveis de log
const LOG_COLORS = {
  info: '#4CAF50', // Verde
  debug: '#2196F3', // Azul
  warn: '#FF9800', // Laranja
  error: '#F44336', // Vermelho
};

// Prefixos para diferentes módulos
export type LogModule = 'auth' | 'api' | 'projects' | 'app' | 'router';

/**
 * Cria um logger para um módulo específico
 * @param module Nome do módulo
 * @returns Objeto com funções de logging
 */
export function createLogger(module: LogModule) {
  const prefix = `[Planify:${module}]`;

  // Verificar se estamos em produção
  const isProduction = process.env.NODE_ENV === 'production';

  // Em produção, não exibimos logs de debug
  const shouldLog = (level: LogLevel) => {
    if (isProduction && level === 'debug') return false;
    return true;
  };

  return {
    /**
     * Log de informação
     * @param message Mensagem ou objeto para logar
     */
    info: (...args: any[]) => {
      if (!shouldLog('info')) return;
      console.log(
        `%c${prefix}`,
        `color: ${LOG_COLORS.info}; font-weight: bold;`,
        ...args
      );
    },

    /**
     * Log de debug (apenas em desenvolvimento)
     * @param message Mensagem ou objeto para logar
     */
    debug: (...args: any[]) => {
      if (!shouldLog('debug')) return;
      console.log(
        `%c${prefix}`,
        `color: ${LOG_COLORS.debug}; font-weight: bold;`,
        ...args
      );
    },

    /**
     * Log de aviso
     * @param message Mensagem ou objeto para logar
     */
    warn: (...args: any[]) => {
      if (!shouldLog('warn')) return;
      console.warn(
        `%c${prefix}`,
        `color: ${LOG_COLORS.warn}; font-weight: bold;`,
        ...args
      );
    },

    /**
     * Log de erro
     * @param message Mensagem ou objeto para logar
     */
    error: (...args: any[]) => {
      if (!shouldLog('error')) return;
      console.error(
        `%c${prefix}`,
        `color: ${LOG_COLORS.error}; font-weight: bold;`,
        ...args
      );
    },

    /**
     * Log de requisição HTTP
     * @param method Método HTTP
     * @param url URL da requisição
     * @param status Código de status (opcional)
     */
    http: (method: string, url: string, status?: number) => {
      if (!shouldLog('info')) return;

      const statusColor = status
        ? status >= 200 && status < 300
          ? LOG_COLORS.info
          : LOG_COLORS.error
        : LOG_COLORS.debug;

      const statusText = status ? `[${status}]` : '';
      console.log(
        `%c${prefix} %c${method} %c${url} %c${statusText}`,
        `color: ${LOG_COLORS.info}; font-weight: bold;`,
        'color: #9C27B0; font-weight: bold;',
        'color: #607D8B;',
        `color: ${statusColor};`
      );
    },
  };
}

// Exportar instâncias pré-configuradas para uso comum
export const authLogger = createLogger('auth');
export const apiLogger = createLogger('api');
export const appLogger = createLogger('app');
