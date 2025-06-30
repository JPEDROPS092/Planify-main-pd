// Service para gerenciar notificações usando a API 
export const useNotificationService = () => {
  // Mock service para desenvolvimento - substitua pelas chamadas reais da API
  const getNotifications = async (params = {}) => {
    // TODO: Implementar chamada real para /api/communications/notificacoes/
    // Por enquanto, simulando dados
    return {
      results: [
        {
          id: 1,
          titulo: 'Nova tarefa atribuída',
          mensagem: 'Você foi atribuído à tarefa "Implementar login"',
          lida: false,
          criada_em: new Date().toISOString(),
          tipo: 'TAREFA'
        },
        {
          id: 2,
          titulo: 'Projeto atualizado',
          mensagem: 'O projeto "Planify" foi atualizado',
          lida: false,
          criada_em: new Date().toISOString(),
          tipo: 'PROJETO'
        }
      ]
    };
  };

  const markNotificationAsRead = async (notificationId: number) => {
    // TODO: Implementar chamada real para /api/communications/notificacoes/{id}/marcar_como_lida/
    return { success: true };
  };

  const markAllNotificationsAsRead = async () => {
    // TODO: Implementar chamada real para /api/communications/notificacoes/marcar_todas_como_lidas/
    return { success: true };
  };

  return {
    getNotifications,
    markNotificationAsRead,
    markAllNotificationsAsRead
  };
};
