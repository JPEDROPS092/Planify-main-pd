/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type PatchedChatMensagemRequest = {
    /**
     * Projeto ao qual a mensagem pertence
     */
    projeto?: number;
    /**
     * Conteúdo da mensagem
     */
    texto?: string;
    /**
     * Arquivo opcional anexado à mensagem
     */
    anexo?: Blob | null;
};

