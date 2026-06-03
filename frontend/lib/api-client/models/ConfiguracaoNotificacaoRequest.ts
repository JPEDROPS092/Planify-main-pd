/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DocumentoNovoEnum } from './DocumentoNovoEnum';
import type { EquipeAlteracaoEnum } from './EquipeAlteracaoEnum';
import type { MensagemChatEnum } from './MensagemChatEnum';
import type { ProjetoStatusEnum } from './ProjetoStatusEnum';
import type { RiscoNovoEnum } from './RiscoNovoEnum';
import type { TarefaAtribuidaEnum } from './TarefaAtribuidaEnum';
import type { TarefaComentarioEnum } from './TarefaComentarioEnum';
import type { TarefaPrazoEnum } from './TarefaPrazoEnum';
export type ConfiguracaoNotificacaoRequest = {
    /**
     * Usuário ao qual estas configurações pertencem
     */
    usuario: number;
    /**
     * Canal de notificação quando uma tarefa é atribuída ao usuário
     *
     * * `EMAIL` - E-mail
     * * `SISTEMA` - Sistema
     * * `AMBOS` - Ambos
     * * `NENHUM` - Nenhum
     */
    tarefa_atribuida?: TarefaAtribuidaEnum;
    /**
     * Canal de notificação quando há um novo comentário em uma tarefa do usuário
     *
     * * `EMAIL` - E-mail
     * * `SISTEMA` - Sistema
     * * `AMBOS` - Ambos
     * * `NENHUM` - Nenhum
     */
    tarefa_comentario?: TarefaComentarioEnum;
    /**
     * Canal de notificação para lembretes de prazo de tarefas
     *
     * * `EMAIL` - E-mail
     * * `SISTEMA` - Sistema
     * * `AMBOS` - Ambos
     * * `NENHUM` - Nenhum
     */
    tarefa_prazo?: TarefaPrazoEnum;
    /**
     * Canal de notificação quando o status de um projeto é alterado
     *
     * * `EMAIL` - E-mail
     * * `SISTEMA` - Sistema
     * * `AMBOS` - Ambos
     * * `NENHUM` - Nenhum
     */
    projeto_status?: ProjetoStatusEnum;
    /**
     * Canal de notificação quando há alterações na equipe de um projeto
     *
     * * `EMAIL` - E-mail
     * * `SISTEMA` - Sistema
     * * `AMBOS` - Ambos
     * * `NENHUM` - Nenhum
     */
    equipe_alteracao?: EquipeAlteracaoEnum;
    /**
     * Canal de notificação quando um novo documento é adicionado
     *
     * * `EMAIL` - E-mail
     * * `SISTEMA` - Sistema
     * * `AMBOS` - Ambos
     * * `NENHUM` - Nenhum
     */
    documento_novo?: DocumentoNovoEnum;
    /**
     * Canal de notificação quando um novo risco é registrado
     *
     * * `EMAIL` - E-mail
     * * `SISTEMA` - Sistema
     * * `AMBOS` - Ambos
     * * `NENHUM` - Nenhum
     */
    risco_novo?: RiscoNovoEnum;
    /**
     * Canal de notificação para novas mensagens de chat
     *
     * * `EMAIL` - E-mail
     * * `SISTEMA` - Sistema
     * * `AMBOS` - Ambos
     * * `NENHUM` - Nenhum
     */
    mensagem_chat?: MensagemChatEnum;
};

