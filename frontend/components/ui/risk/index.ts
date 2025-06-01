/**
 * index.ts para o componente RiskForm
 * 
 * Este arquivo exporta explicitamente o componente RiskForm e seus tipos relacionados,
 * facilitando a importação e uso em outros componentes do projeto.
 */

import RiskForm from './RiskForm.vue';
import type { PropType } from 'vue';
import type { Risco } from '~/services/api/types';

export { RiskForm };

// Tipos para as props do componente
export interface RiskFormProps {
  projectId: number;
  risk: Risco | null;
}

// Tipos para os eventos emitidos pelo componente
export interface RiskFormEmits {
  (e: 'submit', risk: Risco): void;
  (e: 'cancel'): void;
}

// Definição de props para uso em componentes que usam o RiskForm
export const riskFormProps = {
  projectId: {
    type: Number as PropType<number>,
    required: true,
  },
  risk: {
    type: Object as PropType<Risco | null>,
    default: null,
  },
};

export default RiskForm;
