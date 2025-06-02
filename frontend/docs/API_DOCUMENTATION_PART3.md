## Comunicações

### Configurações de Notificação

```typescript
// services/api/services/communicationService.ts
import { useApiService } from '../client/apiService';

export interface ConfiguracaoNotificacao {
  id: number;
  usuario: number;
  notificar_nova_tarefa: boolean;
  notificar_atualizacao_tarefa: boolean;
  notificar_comentario: boolean;
  notificar_prazo: boolean;
  notificar_email: boolean;
  notificar_sistema: boolean;
  criado_em: string;
  atualizado_em: string;
}

export const getMinhaConfiguracao = async (): Promise<ConfiguracaoNotificacao> => {
  const api = useApiService();
  const response = await api.get<ConfiguracaoNotificacao>('/communications/configuracoes/minha_configuracao/');
  return response.data;
};

export interface UpdateConfiguracaoNotificacaoRequest {
  notificar_nova_tarefa?: boolean;
  notificar_atualizacao_tarefa?: boolean;
  notificar_comentario?: boolean;
  notificar_prazo?: boolean;
  notificar_email?: boolean;
  notificar_sistema?: boolean;
}

export const updateConfiguracao = async (id: number, config: UpdateConfiguracaoNotificacaoRequest): Promise<ConfiguracaoNotificacao> => {
  const api = useApiService();
  const response = await api.patch<ConfiguracaoNotificacao>(`/communications/configuracoes/${id}/`, config);
  return response.data;
};
```

### Mensagens de Chat

```typescript
// services/api/services/communicationService.ts
export interface ChatMensagem {
  id: number;
  texto: string;
  autor: number;
  projeto: number;
  lida_por: number[];
  data_envio: string;
}

export interface ChatMensagemListParams {
  page?: number;
  projeto?: number;
  autor?: number;
  ordering?: string;
}

export interface PaginatedChatMensagemList {
  count: number;
  next: string | null;
  previous: string | null;
  results: ChatMensagem[];
}

export const listMensagens = async (params: ChatMensagemListParams = {}): Promise<PaginatedChatMensagemList> => {
  const api = useApiService();
  const response = await api.get<PaginatedChatMensagemList>('/communications/mensagens/', { params });
  return response.data;
};

export interface CreateChatMensagemRequest {
  texto: string;
  projeto: number;
}

export const createMensagem = async (mensagem: CreateChatMensagemRequest): Promise<ChatMensagem> => {
  const api = useApiService();
  const response = await api.post<ChatMensagem>('/communications/mensagens/', mensagem);
  return response.data;
};

export const marcarMensagemComoLida = async (mensagemId: number): Promise<ChatMensagem> => {
  const api = useApiService();
  const response = await api.post<ChatMensagem>(`/communications/mensagens/${mensagemId}/marcar_como_lida/`, {});
  return response.data;
};

export const getMensagensNaoLidas = async (): Promise<ChatMensagem[]> => {
  const api = useApiService();
  const response = await api.get<ChatMensagem[]>('/communications/mensagens/mensagens_nao_lidas/');
  return response.data;
};
```

### Notificações

```typescript
// services/api/services/communicationService.ts
export interface Notificacao {
  id: number;
  titulo: string;
  conteudo: string;
  tipo: 'SISTEMA' | 'TAREFA' | 'PROJETO' | 'PRAZO';
  prioridade: 'BAIXA' | 'MEDIA' | 'ALTA';
  destinatario: number;
  projeto: number | null;
  tarefa: number | null;
  lida: boolean;
  data_criacao: string;
}

export interface NotificacaoListParams {
  page?: number;
  lida?: boolean;
  prioridade?: 'BAIXA' | 'MEDIA' | 'ALTA';
  tipo?: 'SISTEMA' | 'TAREFA' | 'PROJETO' | 'PRAZO';
  projeto?: number;
  tarefa?: number;
  ordering?: string;
}

export interface PaginatedNotificacaoList {
  count: number;
  next: string | null;
  previous: string | null;
  results: Notificacao[];
}

export const listNotificacoes = async (params: NotificacaoListParams = {}): Promise<PaginatedNotificacaoList> => {
  const api = useApiService();
  const response = await api.get<PaginatedNotificacaoList>('/communications/notificacoes/', { params });
  return response.data;
};

export const marcarNotificacaoComoLida = async (notificacaoId: number): Promise<Notificacao> => {
  const api = useApiService();
  const response = await api.post<Notificacao>(`/communications/notificacoes/${notificacaoId}/marcar_como_lida/`, {});
  return response.data;
};

export const marcarTodasNotificacoesComoLidas = async (): Promise<void> => {
  const api = useApiService();
  await api.post('/communications/notificacoes/marcar_todas_como_lidas/', {});
};

export const getNotificacoesNaoLidas = async (): Promise<Notificacao[]> => {
  const api = useApiService();
  const response = await api.get<Notificacao[]>('/communications/notificacoes/nao_lidas/');
  return response.data;
};
```

## Documentos

### Listar Documentos

```typescript
// services/api/services/documentService.ts
import { useApiService } from '../client/apiService';

export interface Documento {
  id: number;
  titulo: string;
  descricao: string;
  arquivo: string;
  tipo: 'CONTRATO' | 'RELATORIO' | 'APRESENTACAO' | 'OUTRO';
  enviado_por: number;
  projeto: number | null;
  tarefa: number | null;
  data_upload: string;
  ultima_atualizacao: string;
}

export interface DocumentoListParams {
  page?: number;
  search?: string;
  projeto?: number;
  tarefa?: number;
  enviado_por?: number;
  tipo?: 'CONTRATO' | 'RELATORIO' | 'APRESENTACAO' | 'OUTRO';
  ordering?: string;
}

export interface PaginatedDocumentoList {
  count: number;
  next: string | null;
  previous: string | null;
  results: Documento[];
}

export const listDocumentos = async (params: DocumentoListParams = {}): Promise<PaginatedDocumentoList> => {
  const api = useApiService();
  const response = await api.get<PaginatedDocumentoList>('/documents/documentos/', { params });
  return response.data;
};
```

### Obter Documento por ID

```typescript
// services/api/services/documentService.ts
export const getDocumento = async (id: number): Promise<Documento> => {
  const api = useApiService();
  const response = await api.get<Documento>(`/documents/documentos/${id}/`);
  return response.data;
};
```

### Criar Documento (Upload)

```typescript
// services/api/services/documentService.ts
export interface CreateDocumentoRequest {
  titulo: string;
  descricao: string;
  arquivo: File;
  tipo: 'CONTRATO' | 'RELATORIO' | 'APRESENTACAO' | 'OUTRO';
  projeto?: number | null;
  tarefa?: number | null;
}

export const createDocumento = async (documento: CreateDocumentoRequest): Promise<Documento> => {
  const api = useApiService();
  
  // Criar um FormData para enviar arquivos
  const formData = new FormData();
  formData.append('titulo', documento.titulo);
  formData.append('descricao', documento.descricao);
  formData.append('arquivo', documento.arquivo);
  formData.append('tipo', documento.tipo);
  
  if (documento.projeto) {
    formData.append('projeto', documento.projeto.toString());
  }
  
  if (documento.tarefa) {
    formData.append('tarefa', documento.tarefa.toString());
  }
  
  const response = await api.post<Documento>('/documents/documentos/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return response.data;
};
```

### Atualizar Documento

```typescript
// services/api/services/documentService.ts
export interface UpdateDocumentoRequest {
  titulo?: string;
  descricao?: string;
  arquivo?: File;
  tipo?: 'CONTRATO' | 'RELATORIO' | 'APRESENTACAO' | 'OUTRO';
}

export const updateDocumento = async (id: number, documento: UpdateDocumentoRequest): Promise<Documento> => {
  const api = useApiService();
  
  // Criar um FormData para enviar arquivos
  const formData = new FormData();
  
  if (documento.titulo) {
    formData.append('titulo', documento.titulo);
  }
  
  if (documento.descricao) {
    formData.append('descricao', documento.descricao);
  }
  
  if (documento.arquivo) {
    formData.append('arquivo', documento.arquivo);
  }
  
  if (documento.tipo) {
    formData.append('tipo', documento.tipo);
  }
  
  const response = await api.patch<Documento>(`/documents/documentos/${id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return response.data;
};
```

### Excluir Documento

```typescript
// services/api/services/documentService.ts
export const deleteDocumento = async (id: number): Promise<void> => {
  const api = useApiService();
  await api.delete(`/documents/documentos/${id}/`);
};
```

### Associar Documento a Tarefa

```typescript
// services/api/services/documentService.ts
export const associarDocumentoTarefa = async (documentoId: number, tarefaId: number): Promise<void> => {
  const api = useApiService();
  await api.post(`/documents/documentos/${documentoId}/associar_tarefa/`, { tarefa: tarefaId });
};
```

### Comentários de Documentos

```typescript
// services/api/services/documentService.ts
export interface ComentarioDocumento {
  id: number;
  texto: string;
  documento: number;
  autor: number;
  data_criacao: string;
}

export interface ComentarioDocumentoListParams {
  page?: number;
  documento?: number;
  autor?: number;
  ordering?: string;
}

export interface PaginatedComentarioDocumentoList {
  count: number;
  next: string | null;
  previous: string | null;
  results: ComentarioDocumento[];
}

export const listComentariosDocumento = async (params: ComentarioDocumentoListParams = {}): Promise<PaginatedComentarioDocumentoList> => {
  const api = useApiService();
  const response = await api.get<PaginatedComentarioDocumentoList>('/documents/comentarios/', { params });
  return response.data;
};

export interface CreateComentarioDocumentoRequest {
  texto: string;
  documento: number;
}

export const createComentarioDocumento = async (comentario: CreateComentarioDocumentoRequest): Promise<ComentarioDocumento> => {
  const api = useApiService();
  const response = await api.post<ComentarioDocumento>('/documents/comentarios/', comentario);
  return response.data;
};

export const adicionarComentarioDocumento = async (documentoId: number, texto: string): Promise<void> => {
  const api = useApiService();
  await api.post(`/documents/documentos/${documentoId}/adicionar_comentario/`, { texto });
};
```

### Histórico de Documentos

```typescript
// services/api/services/documentService.ts
export interface HistoricoDocumento {
  id: number;
  documento: number;
  alterado_por: number;
  data_alteracao: string;
  tipo_alteracao: 'CRIACAO' | 'ATUALIZACAO' | 'EXCLUSAO';
  detalhes: string;
}

export interface HistoricoDocumentoListParams {
  page?: number;
  documento?: number;
  alterado_por?: number;
}

export interface PaginatedHistoricoDocumentoList {
  count: number;
  next: string | null;
  previous: string | null;
  results: HistoricoDocumento[];
}

export const listHistoricoDocumento = async (params: HistoricoDocumentoListParams = {}): Promise<PaginatedHistoricoDocumentoList> => {
  const api = useApiService();
  const response = await api.get<PaginatedHistoricoDocumentoList>('/documents/historico/', { params });
  return response.data;
};

export const getHistoricoDocumento = async (documentoId: number): Promise<HistoricoDocumento[]> => {
  const api = useApiService();
  const response = await api.get<HistoricoDocumento[]>(`/documents/documentos/${documentoId}/historico/`);
  return response.data;
};
```

## Custos

### Categorias de Custos

```typescript
// services/api/services/costService.ts
import { useApiService } from '../client/apiService';

export interface CategoriaCusto {
  id: number;
  nome: string;
  descricao: string;
  criado_por: number;
  criado_em: string;
}

export interface CategoriaListParams {
  page?: number;
  search?: string;
  ordering?: string;
}

export interface PaginatedCategoriaList {
  count: number;
  next: string | null;
  previous: string | null;
  results: CategoriaCusto[];
}

export const listCategorias = async (params: CategoriaListParams = {}): Promise<PaginatedCategoriaList> => {
  const api = useApiService();
  const response = await api.get<PaginatedCategoriaList>('/costs/categorias/', { params });
  return response.data;
};

export interface CreateCategoriaRequest {
  nome: string;
  descricao: string;
}

export const createCategoria = async (categoria: CreateCategoriaRequest): Promise<CategoriaCusto> => {
  const api = useApiService();
  const response = await api.post<CategoriaCusto>('/costs/categorias/', categoria);
  return response.data;
};
```

### Custos

```typescript
// services/api/services/costService.ts
export interface Custo {
  id: number;
  descricao: string;
  valor: number;
  data: string;
  tipo: 'FIXO' | 'VARIAVEL';
  categoria: number;
  projeto: number | null;
  tarefa: number | null;
  criado_por: number;
  criado_em: string;
  atualizado_em: string;
}

export interface CustoListParams {
  page?: number;
  search?: string;
  projeto?: number;
  tarefa?: number;
  categoria?: number;
  tipo?: 'FIXO' | 'VARIAVEL';
  data?: string;
  ordering?: string;
}

export interface PaginatedCustoList {
  count: number;
  next: string | null;
  previous: string | null;
  results: Custo[];
}

export const fetchCustos = async (params: CustoListParams = {}): Promise<PaginatedCustoList> => {
  const api = useApiService();
  const response = await api.get<PaginatedCustoList>('/costs/custos/', { params });
  return response.data;
};

export const getCusto = async (id: number): Promise<Custo> => {
  const api = useApiService();
  const response = await api.get<Custo>(`/costs/custos/${id}/`);
  return response.data;
};

export interface CreateCustoRequest {
  descricao: string;
  valor: number;
  data: string;
  tipo: 'FIXO' | 'VARIAVEL';
  categoria: number;
  projeto?: number | null;
  tarefa?: number | null;
}

export const createCusto = async (custo: CreateCustoRequest): Promise<Custo> => {
  const api = useApiService();
  const response = await api.post<Custo>('/costs/custos/', custo);
  return response.data;
};

export interface UpdateCustoRequest {
  descricao?: string;
  valor?: number;
  data?: string;
  tipo?: 'FIXO' | 'VARIAVEL';
  categoria?: number;
}

export const updateCusto = async (id: number, custo: UpdateCustoRequest): Promise<Custo> => {
  const api = useApiService();
  const response = await api.patch<Custo>(`/costs/custos/${id}/`, custo);
  return response.data;
};

export const deleteCusto = async (id: number): Promise<void> => {
  const api = useApiService();
  await api.delete(`/costs/custos/${id}/`);
};
```

### Orçamentos de Projeto

```typescript
// services/api/services/costService.ts
export interface OrcamentoProjeto {
  id: number;
  projeto: number;
  valor_total: number;
  data_inicio: string;
  data_fim: string;
  criado_por: number;
  criado_em: string;
  atualizado_em: string;
}

export interface OrcamentoProjetoListParams {
  page?: number;
  projeto?: number;
}

export interface PaginatedOrcamentoProjetoList {
  count: number;
  next: string | null;
  previous: string | null;
  results: OrcamentoProjeto[];
}

export const listOrcamentosProjeto = async (params: OrcamentoProjetoListParams = {}): Promise<PaginatedOrcamentoProjetoList> => {
  const api = useApiService();
  const response = await api.get<PaginatedOrcamentoProjetoList>('/costs/orcamentos-projeto/', { params });
  return response.data;
};

export interface CreateOrcamentoProjetoRequest {
  projeto: number;
  valor_total: number;
  data_inicio: string;
  data_fim: string;
}

export const createOrcamentoProjeto = async (orcamento: CreateOrcamentoProjetoRequest): Promise<OrcamentoProjeto> => {
  const api = useApiService();
  const response = await api.post<OrcamentoProjeto>('/costs/orcamentos-projeto/', orcamento);
  return response.data;
};

export const getProjetosSemOrcamento = async (): Promise<Projeto[]> => {
  const api = useApiService();
  const response = await api.get<Projeto[]>('/costs/orcamentos-projeto/projetos_sem_orcamento/');
  return response.data;
};
```

### Alertas de Orçamento

```typescript
// services/api/services/costService.ts
export interface Alerta {
  id: number;
  titulo: string;
  descricao: string;
  tipo: 'ORCAMENTO_EXCEDIDO' | 'ORCAMENTO_PROXIMO' | 'PRAZO_PROXIMO';
  status: 'ATIVO' | 'RESOLVIDO' | 'IGNORADO';
  projeto: number | null;
  tarefa: number | null;
  criado_em: string;
  atualizado_em: string;
}

export interface AlertaListParams {
  page?: number;
  projeto?: number;
  tarefa?: number;
  tipo?: 'ORCAMENTO_EXCEDIDO' | 'ORCAMENTO_PROXIMO' | 'PRAZO_PROXIMO';
  status?: 'ATIVO' | 'RESOLVIDO' | 'IGNORADO';
  ordering?: string;
}

export interface PaginatedAlertaList {
  count: number;
  next: string | null;
  previous: string | null;
  results: Alerta[];
}

export const listAlertas = async (params: AlertaListParams = {}): Promise<PaginatedAlertaList> => {
  const api = useApiService();
  const response = await api.get<PaginatedAlertaList>('/costs/alertas/', { params });
  return response.data;
};

export const ignorarAlerta = async (alertaId: number): Promise<Alerta> => {
  const api = useApiService();
  const response = await api.post<Alerta>(`/costs/alertas/${alertaId}/ignorar/`, {});
  return response.data;
};

export const resolverAlerta = async (alertaId: number): Promise<Alerta> => {
  const api = useApiService();
  const response = await api.post<Alerta>(`/costs/alertas/${alertaId}/resolver/`, {});
  return response.data;
};

export const getAlertasAtivos = async (): Promise<Alerta[]> => {
  const api = useApiService();
  const response = await api.get<Alerta[]>('/costs/alertas/alertas_ativos/');
  return response.data;
};
```
