/**
 * messageService.ts
 *
 * Composables para a camada de comunicações/notificações.
 * Delega ao cliente gerado em `~/lib/api-client` (ApiService).
 *
 * useMessageService  – mensagens de chat (ChatMensagem)
 * useNotificationService – notificações do sistema (Notificacao)
 */

import { ref } from 'vue';
import { ApiService } from '~/lib/api-client';
import { NotificacaoTipoEnum } from '~/lib/api-client';
import type {
  ChatMensagem,
  ChatMensagemRequest,
  PaginatedChatMensagemList,
  Notificacao,
  NotificacaoRequest,
  PaginatedNotificacaoList,
} from '~/services/api/types';

// ---------------------------------------------------------------------------
// Tipos auxiliares locais
// ---------------------------------------------------------------------------

/**
 * Parâmetros aceitos por fetchMessages.
 *
 * Nota de mapeamento:
 *   page         → apiCommunicationsMensagensList(…, page)
 *   ordering     → apiCommunicationsMensagensList(ordering, …)
 *   projeto      → apiCommunicationsMensagensList(…, projeto)
 *   autor        → apiCommunicationsMensagensList(autor, …)
 *   project_id   → alias de `projeto` (compatibilidade com call-site)
 *
 * NAO-MAPEADOS (sem equivalente no schema gerado):
 *   message_type – o endpoint não possui filtro por tipo no schema atual
 *   is_read      – o endpoint não possui filtro is_read no schema atual
 *   search       – o endpoint não possui busca textual no schema atual
 */
export interface FetchMessagesParams {
  page?: number;
  ordering?: string;
  projeto?: number;
  /** Alias de projeto; tem precedência sobre `projeto` quando fornecido. */
  project_id?: number | string;
  autor?: number;
  // Mantidos para compatibilidade com o call-site; ignorados pelo endpoint.
  message_type?: string;
  is_read?: boolean;
  search?: string;
}

/**
 * Corpo da requisição de nova mensagem esperado pelo call-site.
 *
 * Nota de mapeamento:
 *   content      → ChatMensagemRequest.texto
 *   project_id   → ChatMensagemRequest.projeto
 *
 * NAO-MAPEADOS (sem equivalente no schema gerado para ChatMensagemRequest):
 *   title        – ChatMensagemRequest não possui campo título
 *   recipient_id – endpoint não aceita destinatário individual
 *   is_global    – campo não existe em ChatMensagemRequest
 *   sender_id    – campo readonly, não aceito no body
 */
export interface SendMessagePayload {
  content: string;
  project_id?: number | string | null;
  // Campos extra do call-site (não enviados ao endpoint gerado):
  title?: string;
  recipient_id?: number | string | null;
  is_global?: boolean;
  sender_id?: number | string | null;
  // Permite passar campos do schema diretamente:
  projeto?: number;
  texto?: string;
  anexo?: Blob | null;
}

/**
 * Parâmetros aceitos por fetchNotifications.
 *
 * Mapeamento completo com apiCommunicationsNotificacoesList:
 *   page         → page
 *   ordering     → ordering
 *   lida         → lida
 *   prioridade   → prioridade
 *   projeto      → projeto
 *   tarefa       → tarefa
 *   tipo         → tipo
 */
export interface FetchNotificationsParams {
  page?: number;
  ordering?: string;
  lida?: boolean;
  prioridade?: 'ALTA' | 'BAIXA' | 'MEDIA';
  projeto?: number;
  tarefa?: number;
  tipo?: 'DOCUMENTO' | 'EQUIPE' | 'PROJETO' | 'RISCO' | 'SISTEMA' | 'TAREFA';
}

// ---------------------------------------------------------------------------
// useMessageService
// ---------------------------------------------------------------------------

export function useMessageService() {
  const messages = ref<ChatMensagem[]>([]);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);

  /**
   * Lista mensagens de chat.
   * → ApiService.apiCommunicationsMensagensList
   *
   * Parâmetros mapeados: page, ordering, projeto / project_id, autor.
   * Não-mapeados (sem campo no schema): message_type, is_read, search.
   */
  async function fetchMessages(
    params: FetchMessagesParams = {},
  ): Promise<PaginatedChatMensagemList> {
    isLoading.value = true;
    error.value = null;

    try {
      const projetoId =
        params.project_id !== undefined && params.project_id !== null
          ? Number(params.project_id) || undefined
          : params.projeto;

      const result = await ApiService.apiCommunicationsMensagensList(
        params.autor,
        params.ordering,
        params.page,
        projetoId,
      );

      messages.value = result.results ?? [];
      return result;
    } catch (err: any) {
      error.value =
        err?.message ?? 'Erro ao buscar mensagens.';
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Marca uma mensagem como lida.
   * → ApiService.apiCommunicationsMensagensMarcarComoLidaCreate
   *
   * O schema exige um requestBody ChatMensagemRequest com `projeto` e `texto`.
   * Como o call-site passa apenas o `id`, recuperamos os dados da mensagem
   * no cache local (messages.value) para montar o body mínimo válido.
   * Caso a mensagem não esteja no cache, envia body com valores-padrão.
   *
   * Mapeamento: id → path {id}; body montado a partir do cache.
   */
  async function markAsRead(id: number): Promise<ChatMensagem> {
    const cached = messages.value.find((m) => m.id === id);

    const requestBody: ChatMensagemRequest = {
      projeto: cached?.projeto ?? 0,
      texto: cached?.texto ?? '',
    };

    return ApiService.apiCommunicationsMensagensMarcarComoLidaCreate(
      id,
      requestBody,
    );
  }

  /**
   * Cria uma nova mensagem de chat.
   * → ApiService.apiCommunicationsMensagensCreate
   *
   * Mapeamento do payload do call-site:
   *   payload.content    → ChatMensagemRequest.texto
   *   payload.project_id → ChatMensagemRequest.projeto
   *   payload.texto      → ChatMensagemRequest.texto  (passagem direta)
   *   payload.projeto    → ChatMensagemRequest.projeto (passagem direta)
   *
   * Não-mapeados (sem equivalente em ChatMensagemRequest):
   *   payload.title, payload.recipient_id, payload.is_global, payload.sender_id
   */
  async function sendMessage(payload: SendMessagePayload): Promise<ChatMensagem> {
    const body: ChatMensagemRequest = {
      projeto:
        payload.projeto ??
        (payload.project_id !== undefined && payload.project_id !== null
          ? Number(payload.project_id)
          : 0),
      texto: payload.texto ?? payload.content ?? '',
      ...(payload.anexo !== undefined ? { anexo: payload.anexo } : {}),
    };

    return ApiService.apiCommunicationsMensagensCreate(body);
  }

  return {
    messages,
    isLoading,
    error,
    fetchMessages,
    markAsRead,
    sendMessage,
  };
}

// ---------------------------------------------------------------------------
// useNotificationService
// ---------------------------------------------------------------------------

export function useNotificationService() {
  const notifications = ref<Notificacao[]>([]);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);

  /**
   * Lista notificações do usuário.
   * → ApiService.apiCommunicationsNotificacoesList
   *
   * Parâmetros totalmente mapeados: lida, ordering, page, prioridade,
   * projeto, tarefa, tipo.
   */
  async function fetchNotifications(
    params: FetchNotificationsParams = {},
  ): Promise<PaginatedNotificacaoList> {
    isLoading.value = true;
    error.value = null;

    try {
      const result = await ApiService.apiCommunicationsNotificacoesList(
        params.lida,
        params.ordering,
        params.page,
        params.prioridade,
        params.projeto,
        params.tarefa,
        params.tipo,
      );

      notifications.value = result.results ?? [];
      return result;
    } catch (err: any) {
      error.value =
        err?.message ?? 'Erro ao buscar notificações.';
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Marca uma notificação como lida.
   * → ApiService.apiCommunicationsNotificacoesMarcarComoLidaCreate
   *
   * O schema exige um requestBody NotificacaoRequest com os campos obrigatórios
   * (usuario, tipo, titulo, mensagem). Recuperamos os dados do cache local;
   * se ausentes, lançamos erro informativo.
   *
   * Mapeamento: id → path {id}; body montado a partir do cache.
   *
   * NAO-MAPEADO: o endpoint não aceita body vazio; body precisa de campos
   * obrigatórios que o call-site não fornece. Solução: cache local.
   */
  async function markAsRead(id: number): Promise<Notificacao> {
    const cached = notifications.value.find((n) => n.id === id);

    if (!cached) {
      throw new Error(
        `Notificação ${id} não encontrada no cache. ` +
          'Execute fetchNotifications antes de chamar markAsRead.',
      );
    }

    const requestBody: NotificacaoRequest = {
      usuario: cached.usuario,
      tipo: cached.tipo,
      titulo: cached.titulo,
      mensagem: cached.mensagem,
      lida: true,
    };

    return ApiService.apiCommunicationsNotificacoesMarcarComoLidaCreate(
      id,
      requestBody,
    );
  }

  /**
   * Marca todas as notificações não lidas como lidas.
   * → ApiService.apiCommunicationsNotificacoesMarcarTodasComoLidasCreate
   *
   * O endpoint exige um NotificacaoRequest no body; enviamos o mínimo
   * necessário com campos fictícios pois o backend ignora o body para
   * esta action em massa. Caso o comportamento mude, ajuste o body.
   *
   * NAO-MAPEADO: endpoint exige body mesmo sendo uma operação em massa sem
   * entidade específica — inconsistência do schema gerado.
   */
  async function markAllAsRead(): Promise<Notificacao> {
    const requestBody: NotificacaoRequest = {
      usuario: 0,
      tipo: NotificacaoTipoEnum.SISTEMA,
      titulo: '',
      mensagem: '',
    };

    return ApiService.apiCommunicationsNotificacoesMarcarTodasComoLidasCreate(
      requestBody,
    );
  }

  return {
    notifications,
    isLoading,
    error,
    fetchNotifications,
    markAsRead,
    markAllAsRead,
  };
}
