/**
 * Composable para gerenciar notificações
 *
 * Nota: Este composable fornece utilitários para trabalhar com notificações
 * As importações da API serão feitas onde necessário para evitar problemas de path mapping
 */
export function useNotifications() {
  /**
   * Função para obter ícone baseado no tipo de notificação
   */
  const getNotificationIcon = (type: string) => {
    const icons: Record<string, string> = {
      TAREFA: "lucide:check-square",
      COMENTARIO: "lucide:message-square",
      PROJETO: "lucide:briefcase",
      DOCUMENTO: "lucide:file-text",
      RISCO: "lucide:alert-triangle",
      EQUIPE: "lucide:users",
      SISTEMA: "lucide:info",
    };

    return icons[type] || "lucide:bell";
  };

  /**
   * Função para formatar data relativa
   */
  const formatRelativeDate = (dateString: string) => {
    if (!dateString) return "";

    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.round(diffMs / 60000);
    const diffHours = Math.round(diffMs / 3600000);
    const diffDays = Math.round(diffMs / 86400000);

    if (diffMins < 1) {
      return "Agora";
    } else if (diffMins < 60) {
      return `${diffMins} min atrás`;
    } else if (diffHours < 24) {
      return `${diffHours} h atrás`;
    } else if (diffDays < 7) {
      return `${diffDays} dias atrás`;
    } else {
      return date.toLocaleDateString("pt-BR");
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
