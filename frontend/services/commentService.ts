import { useApiClient } from '~/composables/useApiClient';

export const useCommentService = () => {
  const apiClient = useApiClient();

  /**
   * Obtém a lista de comentários
   * @param params Parâmetros de paginação e filtros
   */
  const getComments = async (params = {}) => {
    const response = await apiClient.get('comentarios/', { params });
    return response.data;
  };

  /**
   * Obtém um comentário específico pelo ID
   * @param id ID do comentário
   */
  const getComment = async (id: number) => {
    const response = await apiClient.get(`comentarios/${id}/`);
    return response.data;
  };

  /**
   * Cria um novo comentário
   * @param data Dados do comentário
   */
  const createComment = async (data: any) => {
    const response = await apiClient.post('comentarios/', data);
    return response.data;
  };

  /**
   * Atualiza um comentário existente
   * @param id ID do comentário
   * @param data Dados do comentário
   */
  const updateComment = async (id: number, data: any) => {
    const response = await apiClient.patch(`comentarios/${id}/`, data);
    return response.data;
  };

  /**
   * Exclui um comentário
   * @param id ID do comentário
   */
  const deleteComment = async (id: number) => {
    const response = await apiClient.delete(`comentarios/${id}/`);
    return response.data;
  };

  /**
   * Obtém a lista de comentários de uma tarefa
   * @param taskId ID da tarefa
   * @param params Parâmetros de paginação e filtros
   */
  const getTaskComments = async (taskId: number, params = {}) => {
    const response = await apiClient.get('comentarios-tarefas/', { 
      params: { 
        tarefa_id: taskId,
        ...params 
      } 
    });
    return response.data;
  };

  /**
   * Cria um novo comentário em uma tarefa
   * @param data Dados do comentário
   */
  const createTaskComment = async (data: any) => {
    const response = await apiClient.post('comentarios-tarefas/', data);
    return response.data;
  };

  /**
   * Obtém as mensagens de chat
   * @param params Parâmetros de paginação e filtros
   */
  const getChatMessages = async (params = {}) => {
    const response = await apiClient.get('comunicacao/mensagens/', { params });
    return response.data;
  };

  /**
   * Envia uma nova mensagem de chat
   * @param data Dados da mensagem
   */
  const sendChatMessage = async (data: any) => {
    const response = await apiClient.post('comunicacao/mensagens/', data);
    return response.data;
  };

  /**
   * Marca mensagens como lidas
   * @param messageIds IDs das mensagens
   */
  const markMessagesAsRead = async (messageIds: number[]) => {
    const response = await apiClient.post('comunicacao/mensagens/leituras/', {
      mensagens: messageIds
    });
    return response.data;
  };

  return {
    getComments,
    getComment,
    createComment,
    updateComment,
    deleteComment,
    getTaskComments,
    createTaskComment,
    getChatMessages,
    sendChatMessage,
    markMessagesAsRead
  };
};
