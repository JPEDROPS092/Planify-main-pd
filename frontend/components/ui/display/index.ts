/**
 * Componentes de Exibição
 *
 * Este arquivo centraliza a importação e exportação dos componentes
 * visuais (UI) que são utilizados para exibição de informações.
 *
 * Componentes incluídos:
 * - Avatar: Imagem ou iniciais do usuário
 * - Card: Container visual estilizado
 * - Timeline: Linha do tempo com eventos
 * - Modal: Janela modal com conteúdo customizável
 */

// Importações organizadas por categoria

// Componentes do diretório de Avatar
import * as Avatar from '~/components/ui/display/avatar/Avatar.vue';

// Componentes de cartão
import * as Card from '~/components/ui/display/card/Card.vue';

// Timeline agrupada em um diretório (pode conter múltiplos arquivos)
import * as Timeline from '~/components/ui/display/timeline/Timeline.vue';

// Componente Modal direto
import Modal from './Modal.vue';

// Exportação nomeada dos componentes (recomendada)
export {
  Avatar,
  Card,
  Timeline,
  Modal
};

// Exportação padrão (para facilitar importações por objeto agrupado)
export default {
  Avatar,
  Card,
  Timeline,
  Modal
};
