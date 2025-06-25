import { useApiClient } from '~/composables/useApiClient';

export const useCommunicationService = () => {
  const apiClient = useApiClient();

  /**
   * Obtém a lista de notificações
   * @param params Parâmetros de paginação e filtros
   */
  const getNotifications = async (params = {}) => {
    const response = await apiClient.get('communications/notificacoes/', { params });
    return response.data;
  };

  /**
   * Obtém notificações não lidas
   */
  const getUnreadNotifications = async () => {
    const response = await apiClient.get('communications/notificacoes/nao_lidas/');
    return response.data;
  };

  /**
   * Marca uma notificação como lida
   * @param id ID da notificação
   */
  const markNotificationAsRead = async (id: number) => {
    const response = await apiClient.post(`communications/notificacoes/${id}/marcar_como_lida/`);
    return response.data;
  };

  /**
   * Marca todas as notificações como lidas
   */
  const markAllNotificationsAsRead = async () => {
    const response = await apiClient.post('communications/notificacoes/marcar_todas_como_lidas/');
    return response.data;
  };

  /**
   * Cria uma nova notificação
   * @param data Dados da notificação
   */
  const createNotification = async (data: any) => {
    const response = await apiClient.post('communications/notificacoes/', data);
    return response.data;
  };

  /**
   * Obtém a lista de mensagens
   * @param params Parâmetros de paginação e filtros
   */
  const getMessages = async (params = {}) => {
    const response = await apiClient.get('communications/mensagens/', { params });
    return response.data;
  };

  /**
   * Obtém mensagens não lidas
   */
  const getUnreadMessages = async () => {
    const response = await apiClient.get('communications/mensagens/mensagens_nao_lidas/');
    return response.data;
  };

  /**
   * Marca uma mensagem como lida
   * @param id ID da mensagem
   */
  const markMessageAsRead = async (id: number) => {
    const response = await apiClient.post(`communications/mensagens/${id}/marcar_como_lida/`);
    return response.data;
  };

  /**
   * Cria uma nova mensagem
   * @param data Dados da mensagem
   */
  const createMessage = async (data: any) => {
    const response = await apiClient.post('communications/mensagens/', data);
    return response.data;
  };

  /**
   * Obtém configurações de comunicação
   */
  const getCommunicationSettings = async () => {
    const response = await apiClient.get('communications/configuracoes/minha_configuracao/');
    return response.data;
  };

  /**
   * Atualiza configurações de comunicação
   * @param data Dados das configurações
   */
  const updateCommunicationSettings = async (data: any) => {
    const response = await apiClient.post('communications/configuracoes/', data);
    return response.data;
  };

  return {
    getNotifications,
    getUnreadNotifications,
    markNotificationAsRead,
    markAllNotificationsAsRead,
    createNotification,
    getMessages,
    getUnreadMessages,
    markMessageAsRead,
    createMessage,
    getCommunicationSettings,
    updateCommunicationSettings
  };
};
