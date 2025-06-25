import { useApiClients } from '~/composables/useApiClients';

export const notificationService = {
  /**
   * Obtém a lista de notificações do usuário atual
   * @param params Parâmetros de paginação e filtros
   */
  async getNotifications(params = {}) {
    const { communicationsApi } = useApiClients();
    const response = await communicationsApi.communicationsNotificacoesList(params);
    return response.data;
  },

  /**
   * Marca uma notificação como lida
   * @param id ID da notificação
   */
  async markNotificationAsRead(id: number) {
    const { communicationsApi } = useApiClients();
    const response = await communicationsApi.communicationsNotificacoesMarcarComoLidaCreate(id);
    return response.data;
  },

  /**
   * Marca todas as notificações como lidas
   */
  async markAllNotificationsAsRead() {
    const { communicationsApi } = useApiClients();
    const response = await communicationsApi.communicationsNotificacoesMarcarTodasComoLidasCreate();
    return response.data;
  },

  /**
   * Obtém notificações não lidas
   */
  async getUnreadNotifications() {
    const { communicationsApi } = useApiClients();
    const response = await communicationsApi.communicationsNotificacoesNaoLidasList();
    return response.data;
  },

  /**
   * Obtém uma notificação específica
   * @param id ID da notificação
   */
  async getNotification(id: number) {
    const { communicationsApi } = useApiClients();
    const response = await communicationsApi.communicationsNotificacoesRetrieve(id);
    return response.data;
  },

  /**
   * Cria uma nova notificação
   * @param data Dados da notificação
   */
  async createNotification(data: any) {
    const { communicationsApi } = useApiClients();
    const response = await communicationsApi.communicationsNotificacoesCreate(data);
    return response.data;
  },

  /**
   * Atualiza uma notificação
   * @param id ID da notificação
   * @param data Dados para atualização
   */
  async updateNotification(id: number, data: any) {
    const { communicationsApi } = useApiClients();
    const response = await communicationsApi.communicationsNotificacoesUpdate(id, data);
    return response.data;
  },

  /**
   * Atualiza parcialmente uma notificação
   * @param id ID da notificação
   * @param data Dados para atualização parcial
   */
  async patchNotification(id: number, data: any) {
    const { communicationsApi } = useApiClients();
    const response = await communicationsApi.communicationsNotificacoesPartialUpdate(id, data);
    return response.data;
  },

  /**
   * Exclui uma notificação
   * @param id ID da notificação
   */
  async deleteNotification(id: number) {
    const { communicationsApi } = useApiClients();
    await communicationsApi.communicationsNotificacoesDestroy(id);
  },

  /**
   * Obtém as configurações de notificação do usuário
   */
  async getNotificationSettings() {
    const { communicationsApi } = useApiClients();
    const response = await communicationsApi.communicationsConfiguracoesNotificacaoRetrieve();
    return response.data;
  },

  /**
   * Atualiza as configurações de notificação do usuário
   * @param data Configurações de notificação
   */
  async updateNotificationSettings(data: any) {
    const { communicationsApi } = useApiClients();
    const response = await communicationsApi.communicationsConfiguracoesNotificacaoUpdate(data);
    return response.data;
  }
};

// Manter compatibilidade com o composable existente
export const useNotificationService = () => notificationService;
