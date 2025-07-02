// composables/useNotifications.ts
import { formatDistanceToNow } from "date-fns";
import { ptBR } from "date-fns/locale";
import type { Notificacao } from "@/api/schemas";

/**
 * Composable que fornece utilitários para trabalhar com notificações.
 */
export function useNotifications() {
  const getNotificationIcon = (type?: Notificacao["tipo"]) => {
    const icons: Record<string, string> = {
      TAREFA: "lucide:check-square",
      PROJETO: "lucide:briefcase",
      COMENTARIO: "lucide:message-square",
      DOCUMENTO: "lucide:file-text",
      RISCO: "lucide:shield-alert",
      EQUIPE: "lucide:users",
      CHAT: "lucide:messages-square",
      SISTEMA: "lucide:info",
    };
    return icons[type || ""] || "lucide:bell";
  };

  const formatRelativeDate = (dateString: string | null) => {
    if (!dateString) return "";
    try {
      return formatDistanceToNow(new Date(dateString), {
        addSuffix: true,
        locale: ptBR,
      });
    } catch (e) {
      return dateString;
    }
  };

  /**
   * Função para obter classe CSS do badge do tipo
   */
  const getTypeBadgeClass = (tipo: string) => {
    const classes: Record<string, string> = {
      TAREFA: "bg-blue-100 text-blue-800",
      PROJETO: "bg-green-100 text-green-800",
      COMENTARIO: "bg-yellow-100 text-yellow-800",
      DOCUMENTO: "bg-purple-100 text-purple-800",
      RISCO: "bg-red-100 text-red-800",
      EQUIPE: "bg-indigo-100 text-indigo-800",
      SISTEMA: "bg-gray-100 text-gray-800",
    };

    return classes[tipo] || "bg-gray-100 text-gray-800";
  };

  /**
   * Função para obter label do tipo
   */
  const getTypeLabel = (tipo: string) => {
    const labels: Record<string, string> = {
      TAREFA: "Tarefa",
      PROJETO: "Projeto",
      COMENTARIO: "Comentário",
      DOCUMENTO: "Documento",
      RISCO: "Risco",
      EQUIPE: "Equipe",
      SISTEMA: "Sistema",
    };

    return labels[tipo] || tipo;
  };

  return {
    // Funções utilitárias
    getNotificationIcon,
    formatRelativeDate,
    getTypeBadgeClass,
    getTypeLabel,
  };
}
