/**
 * index.ts para o componente CostForm
 *
 * Este arquivo exporta explicitamente o componente CostForm e seus tipos relacionados,
 * facilitando a importação e uso em outros componentes do projeto.
 */

import CostForm from './CostForm.vue';
import type { PropType } from 'vue';
import type { Custo } from '~/services/api/types';

export { CostForm };

// Tipos para as props do componente
export interface CostFormProps {
  projectId: number;
  cost: Custo | null;
}

// Tipos para os eventos emitidos pelo componente
export interface CostFormEmits {
  (e: 'submit', cost: Custo): void;
  (e: 'cancel'): void;
}

// Definição de props para uso em componentes que usam o CostForm
export const costFormProps = {
  projectId: {
    type: Number as PropType<number>,
    required: true,
  },
  cost: {
    type: Object as PropType<Custo | null>,
    default: null,
  },
};

export default CostForm;
