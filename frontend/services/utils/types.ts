/**
 * Tipos utilitários da camada de autenticação + reexport dos tipos de domínio.
 *
 * Fonte única: o cliente gerado em `~/lib/api-client`. Reexportamos tudo aqui
 * porque parte dos componentes importa tipos de domínio (User, Tarefa, Projeto,
 * Documento, MembroEquipe…) a partir deste módulo. Acrescentamos os tipos de
 * auth que não fazem parte dos serializers base.
 */
import type { User as ApiUser } from '~/lib/api-client';

export * from '~/lib/api-client';

/** Credenciais de login (= corpo de POST /api/auth/token/). */
export type { CustomTokenObtainPairRequest as LoginCredentials } from '~/lib/api-client';

/** Par de tokens retornado pelo endpoint de login. */
export interface TokenObtainPair {
  access: string;
  refresh: string;
}

/**
 * Usuário autenticado. `GET /api/auth/users/me/` retorna `User`; estendemos
 * com campos opcionais consumidos na interface (nomes separados, permissões).
 */
export interface ExtendedUserProfile extends ApiUser {
  first_name?: string | null;
  last_name?: string | null;
  permissions?: string[];
  groups?: Array<{ name: string }>;
}
