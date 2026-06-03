/**
 * Document Service
 *
 * Delegates to the generated `DocumentosService` client.
 * All transport/auth configuration is handled by `plugins/api.ts` via
 * `OpenAPI.BASE` and `OpenAPI.TOKEN` — do NOT add transport here.
 *
 * Call-sites:
 *   pages/documentos/index.vue
 *   pages/projetos/[id]/resources/documents/upload.vue
 *   components/business/project/resources/ProjectDocuments.vue
 *   components/business/risk/RiskForm.vue
 *   components/business/cost/CostForm.vue
 *   components/shared/forms/project/ProjectForm.vue
 *   components/business/project/tasks/TaskForm.vue (import only, no direct calls)
 */

import { DocumentosService } from '~/lib/api-client/services/DocumentosService';
import type {
  Documento,
  DocumentoRequest,
  PatchedDocumentoRequest,
  PaginatedDocumentoListList,
} from '~/lib/api-client';
import { createFormData } from '~/services/api/config';

// ── Parameter types ──────────────────────────────────────────────────────────

/**
 * Mirrors the optional query-string params accepted by `apiDocumentsList`.
 * All fields are optional so callers can pass a partial object.
 */
export interface ListDocumentosParams {
  enviadoPor?: number;
  ordering?: string;
  page?: number;
  projeto?: number;
  search?: string;
  tarefa?: number;
  texto?: string;
  tipo?: 'ATA' | 'DESIGN' | 'MANUAL' | 'OUTRO' | 'RELATORIO' | 'REQUISITO';
  tipoArquivo?: string;
  /** Legacy field used by CostForm – silently ignored (no matching API param). */
  related_to?: string;
  /** Legacy field used by CostForm – silently ignored (no matching API param). */
  related_id?: number;
}

// ── Composable ───────────────────────────────────────────────────────────────

export function useDocumentService() {
  /**
   * List documents with optional filters.
   *
   * Call-sites: pages/documentos/index.vue (`listDocumentos` destructured),
   * ProjectDocuments.vue (`fetchDocuments(projectId)`),
   * CostForm.vue (`fetchDocuments({ related_to, related_id })`).
   *
   * Maps to: `DocumentosService.apiDocumentsList`
   */
  function listDocumentos(
    params: ListDocumentosParams = {},
  ): Promise<PaginatedDocumentoListList> {
    return DocumentosService.apiDocumentsList(
      params.enviadoPor,
      params.ordering,
      params.page,
      params.projeto,
      params.search,
      params.tarefa,
      params.texto,
      params.tipo,
      params.tipoArquivo,
    );
  }

  /**
   * Alias for `listDocumentos` used by ProjectDocuments.vue which passes a
   * raw project-id scalar, and CostForm.vue which passes a filter object.
   *
   * Maps to: `DocumentosService.apiDocumentsList`
   */
  function fetchDocuments(
    projectIdOrParams: number | string | ListDocumentosParams,
  ): Promise<PaginatedDocumentoListList> {
    if (
      typeof projectIdOrParams === 'number' ||
      typeof projectIdOrParams === 'string'
    ) {
      return listDocumentos({ projeto: Number(projectIdOrParams) });
    }
    return listDocumentos(projectIdOrParams);
  }

  /**
   * List documents filtered by project ID.
   *
   * Call-sites: ProjectForm.vue (`getDocumentosByProjeto(projectId)`).
   *
   * Maps to: `DocumentosService.apiDocumentsList` with `projeto` filter.
   * Returns `{ data: DocumentoList[] }` to match the call-site destructuring
   * `response.data`.
   */
  async function getDocumentosByProjeto(
    projetoId: number,
  ): Promise<{ data: PaginatedDocumentoListList['results'] }> {
    const response = await DocumentosService.apiDocumentsList(
      undefined,
      undefined,
      undefined,
      projetoId,
    );
    return { data: response.results ?? [] };
  }

  /**
   * List documents filtered by a risk ID stored in the `tarefa` field.
   *
   * NOTE: The generated API has no dedicated `risco` filter parameter.
   * The call-site (RiskForm.vue) passes a risk ID. The best available
   * mapping is the `tarefa` query param; adjust if the backend exposes
   * a `risco` filter in a future schema update.
   *
   * Call-sites: RiskForm.vue (`getDocumentosByRisco(riskId)`).
   *
   * Maps to: `DocumentosService.apiDocumentsList` with `tarefa` param
   * (closest available filter – see "não-mapeado" section in final report).
   * Returns `{ data: DocumentoList[] }` to match `response.data`.
   */
  async function getDocumentosByRisco(
    riscoId: number,
  ): Promise<{ data: PaginatedDocumentoListList['results'] }> {
    const response = await DocumentosService.apiDocumentsList(
      undefined,
      undefined,
      undefined,
      undefined,
      undefined,
      riscoId, // tarefa param — closest mapping; no dedicated risco filter exists
    );
    return { data: response.results ?? [] };
  }

  /**
   * Retrieve a single document by ID.
   *
   * Maps to: `DocumentosService.apiDocumentsRetrieve`
   */
  function retrieveDocumento(id: number): Promise<Documento> {
    return DocumentosService.apiDocumentsRetrieve(id);
  }

  /**
   * Create a new document.
   * Accepts a plain object (converted to FormData) or a pre-built FormData.
   *
   * Call-sites:
   *   - pages/documentos/index.vue: `createDocument(formData)` (FormData)
   *   - ProjectDocuments.vue: `createDocument(formData)` (FormData)
   *   - RiskForm.vue: `createDocumento(formData)` (FormData)
   *   - ProjectForm.vue: `createDocumento(formData)` (FormData)
   *   - CostForm.vue: `createDocument({ title, description, ... })` (plain object)
   *
   * Maps to: `DocumentosService.apiDocumentsCreate`
   */
  function createDocumento(
    data: FormData | Record<string, any>,
  ): Promise<Documento> {
    const payload =
      data instanceof FormData ? data : createFormData(data);
    // The generated client accepts `DocumentoRequest` (JSON) but the endpoint
    // also handles multipart. We cast to `any` here because the generated type
    // uses `Blob` for `arquivo` and does not model FormData directly.
    return DocumentosService.apiDocumentsCreate(
      payload as unknown as DocumentoRequest,
    );
  }

  /** Alias used by pages/documentos/index.vue and ProjectDocuments.vue. */
  const createDocument = createDocumento;

  /**
   * Full update (PUT) of an existing document.
   * Accepts a plain object (converted to FormData) or a pre-built FormData.
   *
   * Call-sites: pages/documentos/index.vue (`updateDocument(id, formData)`).
   *
   * Maps to: `DocumentosService.apiDocumentsUpdate`
   */
  function updateDocumento(
    id: number,
    data: FormData | Record<string, any>,
  ): Promise<Documento> {
    const payload =
      data instanceof FormData ? data : createFormData(data);
    return DocumentosService.apiDocumentsUpdate(
      id,
      payload as unknown as DocumentoRequest,
    );
  }

  /** Alias used by pages/documentos/index.vue. */
  const updateDocument = updateDocumento;

  /**
   * Partial update (PATCH) of an existing document.
   *
   * Maps to: `DocumentosService.apiDocumentsPartialUpdate`
   */
  function partialUpdateDocumento(
    id: number,
    data: FormData | PatchedDocumentoRequest,
  ): Promise<Documento> {
    const payload =
      data instanceof FormData
        ? (data as unknown as PatchedDocumentoRequest)
        : data;
    return DocumentosService.apiDocumentsPartialUpdate(id, payload);
  }

  /**
   * Delete (destroy) a document by ID.
   *
   * Call-sites:
   *   - pages/documentos/index.vue: `deleteDocument(id)`
   *   - ProjectDocuments.vue: `deleteDocument(id)`
   *   - RiskForm.vue: `deleteDocumento(id)`
   *   - ProjectForm.vue: `deleteDocumento(id)`
   *   - CostForm.vue: `deleteDocument(id)`
   *
   * Maps to: `DocumentosService.apiDocumentsDestroy`
   */
  function deleteDocumento(id: number): Promise<void> {
    return DocumentosService.apiDocumentsDestroy(id);
  }

  /** Alias used by pages/documentos/index.vue, ProjectDocuments.vue, CostForm.vue. */
  const deleteDocument = deleteDocumento;

  /**
   * Upload a document.
   * Accepts a FormData (already built by the caller) or a plain object.
   *
   * Call-sites:
   *   - pages/projetos/[id]/resources/documents/upload.vue:
   *     `uploadDocumento(formData)` (FormData, destructured from composable)
   *
   * Maps to: `DocumentosService.apiDocumentsCreate` (multipart).
   */
  function uploadDocumento(
    data: FormData | Record<string, any>,
  ): Promise<Documento> {
    return createDocumento(data);
  }

  return {
    // List / query
    listDocumentos,
    fetchDocuments,
    getDocumentosByProjeto,
    getDocumentosByRisco,

    // Single-item reads
    retrieveDocumento,

    // Mutations
    createDocumento,
    createDocument,
    updateDocumento,
    updateDocument,
    partialUpdateDocumento,
    deleteDocumento,
    deleteDocument,
    uploadDocumento,
  };
}
