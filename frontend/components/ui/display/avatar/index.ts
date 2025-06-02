/**
 * Componentes de Avatar
 *
 * Componentes para exibição de avatares de usuário, com suporte a imagens e fallback.
 */

// Importação dos componentes
import Avatar from './Avatar.vue';
import AvatarFallback from './AvatarFallback.vue';
import AvatarImage from './AvatarImage.vue';

// Importação das variantes
import { avatarVariant, type AvatarVariants } from './variants';

// Exportação explícita dos componentes
export {
  Avatar,
  AvatarFallback,
  AvatarImage,
  avatarVariant,
  type AvatarVariants
};

// Exportação padrão para uso com importações default
export default {
  Avatar,
  AvatarFallback,
  AvatarImage
};