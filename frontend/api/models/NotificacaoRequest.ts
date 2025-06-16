/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { NotificacaoTipoEnum } from './NotificacaoTipoEnum';
import type { PrioridadeEnum } from './PrioridadeEnum';
export type NotificacaoRequest = {
    /**
     * Usuário que receberá a notificação
     */
    usuario: number;
    /**
     * Tipo de objeto relacionado à notificação
     *
     * * `TAREFA` - Tarefa
     * * `PROJETO` - Projeto
     * * `EQUIPE` - Equipe
     * * `RISCO` - Risco
     * * `DOCUMENTO` - Documento
     * * `SISTEMA` - Sistema
     */
    tipo: NotificacaoTipoEnum;
    /**
     * Título breve da notificação
     */
    titulo: string;
    /**
     * Conteúdo detalhado da notificação
     */
    mensagem: string;
    /**
     * Indica se a notificação foi lida pelo usuário
     */
    lida?: boolean;
    /**
     * Nível de prioridade da notificação
     *
     * * `BAIXA` - Baixa
     * * `MEDIA` - Média
     * * `ALTA` - Alta
     */
    prioridade?: PrioridadeEnum;
    /**
     * Projeto relacionado à notificação (se aplicável)
     */
    projeto?: number | null;
    /**
     * Tarefa relacionada à notificação (se aplicável)
     */
    tarefa?: number | null;
    /**
     * URL para redirecionamento quando a notificação for clicada
     */
    url?: string | null;
};

