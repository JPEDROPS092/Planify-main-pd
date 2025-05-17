/**
 * Tipos base para os serviços da API
 * Gerados a partir da especificação OpenAPI
 */

// Enums
export enum RoleEnum {
  ADMIN = 'ADMIN',
  PROJECT_MANAGER = 'PROJECT_MANAGER',
  TEAM_MEMBER = 'TEAM_MEMBER'
}

export enum ActionEnum {
  VIEW = 'VIEW',
  CREATE = 'CREATE',
  EDIT = 'EDIT',
  DELETE = 'DELETE'
}

export enum AlertaStatusEnum {
  ATIVO = 'ATIVO',
  RESOLVIDO = 'RESOLVIDO',
  IGNORADO = 'IGNORADO'
}

export enum AlertaTipoEnum {
  PROJETO = 'PROJETO',
  TAREFA = 'TAREFA'
}

export enum ThemePreferenceEnum {
  LIGHT = 'LIGHT',
  DARK = 'DARK',
  SYSTEM = 'SYSTEM'
}

export enum PrioridadeEnum {
  BAIXA = 'BAIXA',
  MEDIA = 'MEDIA',
  ALTA = 'ALTA',
  CRITICA = 'CRITICA'
}

export enum StatusEnum {
  PENDENTE = 'PENDENTE',
  EM_ANDAMENTO = 'EM_ANDAMENTO',
  CONCLUIDO = 'CONCLUIDO',
  BLOQUEADO = 'BLOQUEADO',
  CANCELADO = 'CANCELADO'
}

export enum NovoStatusEnum {
  IDENTIFICADO = 'IDENTIFICADO',
  EM_ANALISE = 'EM_ANALISE',
  MITIGADO = 'MITIGADO',
  ACEITO = 'ACEITO',
  TRANSFERIDO = 'TRANSFERIDO',
  FECHADO = 'FECHADO'
}

export enum ProbabilidadeEnum {
  MUITO_BAIXA = 'MUITO_BAIXA',
  BAIXA = 'BAIXA',
  MEDIA = 'MEDIA',
  ALTA = 'ALTA',
  MUITO_ALTA = 'MUITO_ALTA'
}

export enum ImpactoEnum {
  MUITO_BAIXO = 'MUITO_BAIXO',
  BAIXO = 'BAIXO',
  MEDIO = 'MEDIO',
  ALTO = 'ALTO',
  MUITO_ALTO = 'MUITO_ALTO'
}

export enum MembroProjetoPapelEnum {
  GERENTE = 'GERENTE',
  DESENVOLVEDOR = 'DESENVOLVEDOR',
  TESTADOR = 'TESTADOR'
}

export enum CustoTipoEnum {
  FIXO = 'FIXO',
  VARIAVEL = 'VARIAVEL'
}

export enum DocumentoTipoEnum {
  REQUISITOS = 'REQUISITOS',
  DESIGN = 'DESIGN',
  TECNICO = 'TECNICO',
  TESTE = 'TESTE',
  USUARIO = 'USUARIO',
  OUTRO = 'OUTRO'
}

// Interfaces para paginação
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Interfaces para autenticação
export interface TokenObtainPairRequest {
  username: string;
  password: string;
}

export interface TokenObtainPair {
  access: string;
  refresh: string;
}

export interface TokenRefreshRequest {
  refresh: string;
}

export interface TokenRefresh {
  access: string;
  refresh: string;
}

// Interface para usuário
export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: RoleEnum;
  is_active: boolean;
  profile: UserProfile;
  last_login: string | null;
  date_joined: string;
}

export interface UserProfile {
  phone: string | null;
  profile_picture: string | null;
  theme_preference: ThemePreferenceEnum;
  email_notifications: boolean;
  system_notifications: boolean;
}

export interface UserProfileRequest {
  phone?: string | null;
  profile_picture?: File | null;
  theme_preference?: ThemePreferenceEnum;
  email_notifications?: boolean;
  system_notifications?: boolean;
}

export interface UserRequest {
  username: string;
  email: string;
  full_name: string;
  role?: RoleEnum;
  is_active?: boolean;
  profile?: UserProfileRequest;
  password?: string;
}

export interface UserCreatePasswordRetypeRequest {
  email: string;
  full_name: string;
  username: string;
  password: string;
  re_password: string;
}

export interface UserCreatePasswordRetype {
  email: string;
  full_name: string;
  username: string;
  id: number;
}

export interface SetPasswordRetypeRequest {
  new_password: string;
  re_new_password: string;
  current_password: string;
}

export interface SendEmailResetRequest {
  email: string;
}

export interface SetNewPasswordRequest {
  password: string;
  token: string;
}

// Interfaces para projetos
export interface Projeto {
  id: number;
  nome: string;
  descricao: string | null;
  data_inicio: string;
  data_fim: string | null;
  status: StatusEnum;
  status_display: string;
  gerente: number;
  gerente_nome: string;
  criado_por: number;
  criado_por_nome: string;
  data_criacao: string;
  data_atualizacao: string;
  progresso: number;
  arquivado: boolean;
}

export interface ProjetoRequest {
  nome: string;
  descricao?: string | null;
  data_inicio: string;
  data_fim?: string | null;
  status: StatusEnum;
  gerente: number;
  criado_por?: number | null;
}

export interface ProjetoList {
  id: number;
  nome: string;
  descricao: string | null;
  data_inicio: string;
  data_fim: string | null;
  status: StatusEnum;
  status_display: string;
  gerente: number;
  gerente_nome: string;
  progresso: number;
  arquivado: boolean;
}

// Interfaces para tarefas
export interface Tarefa {
  id: number;
  titulo: string;
  descricao: string | null;
  projeto: number;
  projeto_nome: string;
  sprint: number | null;
  sprint_nome: string | null;
  responsavel: number | null;
  responsavel_nome: string | null;
  prioridade: PrioridadeEnum;
  prioridade_display: string;
  status: StatusEnum;
  status_display: string;
  data_inicio: string | null;
  data_fim: string | null;
  estimativa_horas: number | null;
  horas_trabalhadas: number;
  progresso: number;
  criado_por: number;
  criado_por_nome: string;
  data_criacao: string;
  data_atualizacao: string;
}

export interface TarefaRequest {
  titulo: string;
  descricao?: string | null;
  projeto: number;
  sprint?: number | null;
  responsavel?: number | null;
  prioridade: PrioridadeEnum;
  status: StatusEnum;
  data_inicio?: string | null;
  data_fim?: string | null;
  estimativa_horas?: number | null;
  criado_por?: number | null;
}

export interface TarefaList {
  id: number;
  titulo: string;
  projeto: number;
  projeto_nome: string;
  responsavel: number | null;
  responsavel_nome: string | null;
  prioridade: PrioridadeEnum;
  prioridade_display: string;
  status: StatusEnum;
  status_display: string;
  data_inicio: string | null;
  data_fim: string | null;
  progresso: number;
}

// Interfaces para comunicações
export interface ChatMensagem {
  id: number;
  projeto: number;
  projeto_nome: string;
  autor: number;
  autor_nome: string;
  texto: string;
  anexo: string | null;
  data_criacao: string;
  lida_por: number[];
}

export interface ChatMensagemRequest {
  projeto: number;
  texto: string;
  anexo?: File | null;
}

export interface Notificacao {
  id: number;
  usuario: number;
  titulo: string;
  mensagem: string;
  lida: boolean;
  data_criacao: string;
  link: string | null;
}

export interface NotificacaoRequest {
  usuario: number;
  titulo: string;
  mensagem: string;
  lida?: boolean;
  link?: string | null;
}

// Interfaces para documentos
export interface Documento {
  id: number;
  projeto: number;
  projeto_nome: string;
  tarefa: number | null;
  tarefa_titulo: string | null;
  titulo: string;
  descricao: string | null;
  tipo: DocumentoTipoEnum;
  tipo_display: string;
  arquivo: string;
  versao: string;
  criado_por: number;
  criado_por_nome: string;
  data_criacao: string;
  data_atualizacao: string;
}

export interface DocumentoRequest {
  projeto: number;
  tarefa?: number | null;
  titulo: string;
  descricao?: string | null;
  tipo: DocumentoTipoEnum;
  arquivo: File;
  versao?: string;
  criado_por?: number | null;
}

// Interfaces para riscos
export interface Risco {
  id: number;
  projeto: number;
  projeto_nome: string;
  descricao: string;
  probabilidade: ProbabilidadeEnum;
  probabilidade_display: string;
  impacto: ImpactoEnum;
  impacto_display: string;
  status: NovoStatusEnum;
  status_display: string;
  responsavel_mitigacao: number | null;
  responsavel_mitigacao_nome: string;
  plano_mitigacao: string | null;
  plano_contingencia: string | null;
  data_identificacao: string;
  nivel_risco: string;
  criado_por: number | null;
  criado_por_nome: string;
}

export interface RiscoRequest {
  projeto: number;
  descricao: string;
  probabilidade: ProbabilidadeEnum;
  impacto: ImpactoEnum;
  status: NovoStatusEnum;
  responsavel_mitigacao?: number | null;
  plano_mitigacao?: string | null;
  plano_contingencia?: string | null;
  criado_por?: number | null;
}

// Interfaces para custos
export interface Custo {
  id: number;
  projeto: number;
  projeto_nome: string;
  tarefa: number | null;
  tarefa_titulo: string | null;
  categoria: number | null;
  categoria_nome: string | null;
  descricao: string;
  valor: string;
  tipo: CustoTipoEnum;
  tipo_display: string;
  data: string;
  comprovante: string | null;
  observacoes: string | null;
  criado_por: number | null;
  criado_por_nome: string;
  data_criacao: string;
  data_atualizacao: string;
}

export interface CustoRequest {
  projeto: number;
  tarefa?: number | null;
  categoria?: number | null;
  descricao: string;
  valor: string;
  tipo: CustoTipoEnum;
  data: string;
  comprovante?: File | null;
  observacoes?: string | null;
  criado_por?: number | null;
}

export interface Categoria {
  id: number;
  nome: string;
  descricao: string | null;
}

export interface CategoriaRequest {
  nome: string;
  descricao?: string | null;
}

export interface Alerta {
  id: number;
  tipo: AlertaTipoEnum;
  tipo_display: string;
  projeto: number;
  projeto_nome: string;
  tarefa: number | null;
  tarefa_titulo: string;
  percentual: string;
  mensagem: string;
  status: AlertaStatusEnum;
  status_display: string;
  data_criacao: string;
  data_resolucao: string | null;
  resolvido_por: number | null;
  resolvido_por_nome: string;
}

export interface AlertaRequest {
  tipo: AlertaTipoEnum;
  projeto: number;
  tarefa?: number | null;
  percentual: string;
  mensagem: string;
  status: AlertaStatusEnum;
  resolvido_por?: number | null;
}

// Interfaces para equipes
export interface Equipe {
  id: number;
  nome: string;
  descricao: string | null;
  projeto: number;
  projeto_nome: string;
  criado_por: number;
  criado_por_nome: string;
  data_criacao: string;
  membros_count: number;
}

export interface EquipeRequest {
  nome: string;
  descricao?: string | null;
  projeto: number;
  criado_por?: number | null;
}

export interface MembroEquipe {
  id: number;
  usuario: number;
  usuario_nome: string;
  equipe: number;
  equipe_nome: string;
  papel: string;
  papel_display: string;
  data_adicao: string;
}

export interface MembroEquipeRequest {
  usuario: number;
  equipe: number;
  papel: string;
}

export interface PermissaoEquipe {
  id: number;
  equipe: number;
  equipe_nome: string;
  modulo: string;
  modulo_display: string;
  papel: string;
  papel_display: string;
  permissao: string;
  permissao_display: string;
}

export interface PermissaoEquipeRequest {
  equipe: number;
  modulo: string;
  papel: string;
  permissao: string;
}
