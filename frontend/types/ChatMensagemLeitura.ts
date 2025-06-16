/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type ChatMensagemLeitura = {
    readonly id: number;
    /**
     * Mensagem que foi lida
     */
    mensagem: number;
    /**
     * Usuário que leu a mensagem
     */
    usuario: number;
    readonly usuario_nome: string;
    /**
     * Data e hora em que a mensagem foi lida
     */
    readonly lido_em: string;
};

