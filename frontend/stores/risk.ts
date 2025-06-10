import { defineStore } from 'pinia';

interface Risk {
  id: number;
  titulo: string;
  descricao?: string;
  categoria: string;
  impacto: string;
  probabilidade: string;
  status: string;
  projeto: number | object;
  criado_por?: number | object;
  data_identificacao: string;
  estrategia_mitigacao?: string;
  [key: string]: any;
}

interface RiskState {
  risks: Risk[];
  riskDetails: Record<number, Risk>;
  lastFetch: number;
  lastDetailsFetch: Record<number, number>;
  isFetching: boolean;
  cacheTTL: number; // Tempo de vida do cache em milissegundos
}

export const useRiskStore = defineStore('risk', {
  state: (): RiskState => ({
    risks: [],
    riskDetails: {},
    lastFetch: 0,
    lastDetailsFetch: {},
    isFetching: false,
    cacheTTL: 5 * 60 * 1000, // 5 minutos em milissegundos
  }),

  getters: {
    /**
     * Verifica se o cache da lista de riscos é válido
     */
    isRisksCacheValid(): boolean {
      return (
        this.risks.length > 0 &&
        Date.now() - this.lastFetch < this.cacheTTL
      );
    },

    /**
     * Verifica se o cache de um risco específico é válido
     */
    isRiskDetailCacheValid(): (id: number) => boolean {
      return (id: number) => {
        return (
          !!this.riskDetails[id] &&
          !!this.lastDetailsFetch[id] &&
          Date.now() - this.lastDetailsFetch[id] < this.cacheTTL
        );
      };
    },
  },

  actions: {
    /**
     * Adiciona ou atualiza a lista de riscos no cache
     */
    setRisks(risks: Risk[]) {
      this.risks = risks;
      this.lastFetch = Date.now();
    },

    /**
     * Adiciona ou atualiza um risco específico no cache
     */
    setRiskDetail(risk: Risk) {
      if (!risk || !risk.id) return;
      
      this.riskDetails[risk.id] = { ...risk };
      this.lastDetailsFetch[risk.id] = Date.now();
      
      // Atualiza também na lista se existir
      const index = this.risks.findIndex(r => r.id === risk.id);
      if (index !== -1) {
        this.risks[index] = { ...risk };
      }
    },

    /**
     * Remove um risco do cache
     */
    removeRisk(id: number) {
      if (!id) return;
      
      // Remove da lista
      this.risks = this.risks.filter(r => r.id !== id);
      
      // Remove dos detalhes
      if (this.riskDetails[id]) {
        delete this.riskDetails[id];
      }
      
      // Remove do registro de timestamp
      if (this.lastDetailsFetch[id]) {
        delete this.lastDetailsFetch[id];
      }
    },

    /**
     * Limpa todo o cache de riscos
     */
    clearCache() {
      this.risks = [];
      this.riskDetails = {};
      this.lastFetch = 0;
      this.lastDetailsFetch = {};
    },

    /**
     * Atualiza o status de carregamento
     */
    setFetching(status: boolean) {
      this.isFetching = status;
    },
  },
});
