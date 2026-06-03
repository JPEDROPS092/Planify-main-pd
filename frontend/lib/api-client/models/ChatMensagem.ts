/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ChatMensagemLeitura } from './ChatMensagemLeitura';
export type ChatMensagem = {
    readonly id: number;
    /**
     * Projeto ao qual a mensagem pertence
     */
    projeto: number;
    readonly projeto_nome: string;
    /**
     * Usuário que enviou a mensagem
     */
    readonly autor: number;
    readonly autor_nome: string;
    readonly autor_username: string;
    /**
     * Conteúdo da mensagem
     */
    texto: string;
    /**
     * Arquivo opcional anexado à mensagem
     */
    anexo?: string | null;
    /**
     * Data e hora em que a mensagem foi enviada
     */
    readonly enviado_em: string;
    /**
     * Indica se a mensagem foi editada após o envio inicial
     */
    readonly editado: boolean;
    readonly leituras: Array<ChatMensagemLeitura>;
};

