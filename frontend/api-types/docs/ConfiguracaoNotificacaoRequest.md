# ConfiguracaoNotificacaoRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usuario** | **number** | Usuário ao qual estas configurações pertencem | [default to undefined]
**tarefa_atribuida** | [**TarefaAtribuidaEnum**](TarefaAtribuidaEnum.md) | Canal de notificação quando uma tarefa é atribuída ao usuário  * &#x60;EMAIL&#x60; - E-mail * &#x60;SISTEMA&#x60; - Sistema * &#x60;AMBOS&#x60; - Ambos * &#x60;NENHUM&#x60; - Nenhum | [optional] [default to undefined]
**tarefa_comentario** | [**TarefaComentarioEnum**](TarefaComentarioEnum.md) | Canal de notificação quando há um novo comentário em uma tarefa do usuário  * &#x60;EMAIL&#x60; - E-mail * &#x60;SISTEMA&#x60; - Sistema * &#x60;AMBOS&#x60; - Ambos * &#x60;NENHUM&#x60; - Nenhum | [optional] [default to undefined]
**tarefa_prazo** | [**TarefaPrazoEnum**](TarefaPrazoEnum.md) | Canal de notificação para lembretes de prazo de tarefas  * &#x60;EMAIL&#x60; - E-mail * &#x60;SISTEMA&#x60; - Sistema * &#x60;AMBOS&#x60; - Ambos * &#x60;NENHUM&#x60; - Nenhum | [optional] [default to undefined]
**projeto_status** | [**ProjetoStatusEnum**](ProjetoStatusEnum.md) | Canal de notificação quando o status de um projeto é alterado  * &#x60;EMAIL&#x60; - E-mail * &#x60;SISTEMA&#x60; - Sistema * &#x60;AMBOS&#x60; - Ambos * &#x60;NENHUM&#x60; - Nenhum | [optional] [default to undefined]
**equipe_alteracao** | [**EquipeAlteracaoEnum**](EquipeAlteracaoEnum.md) | Canal de notificação quando há alterações na equipe de um projeto  * &#x60;EMAIL&#x60; - E-mail * &#x60;SISTEMA&#x60; - Sistema * &#x60;AMBOS&#x60; - Ambos * &#x60;NENHUM&#x60; - Nenhum | [optional] [default to undefined]
**documento_novo** | [**DocumentoNovoEnum**](DocumentoNovoEnum.md) | Canal de notificação quando um novo documento é adicionado  * &#x60;EMAIL&#x60; - E-mail * &#x60;SISTEMA&#x60; - Sistema * &#x60;AMBOS&#x60; - Ambos * &#x60;NENHUM&#x60; - Nenhum | [optional] [default to undefined]
**risco_novo** | [**RiscoNovoEnum**](RiscoNovoEnum.md) | Canal de notificação quando um novo risco é registrado  * &#x60;EMAIL&#x60; - E-mail * &#x60;SISTEMA&#x60; - Sistema * &#x60;AMBOS&#x60; - Ambos * &#x60;NENHUM&#x60; - Nenhum | [optional] [default to undefined]
**mensagem_chat** | [**MensagemChatEnum**](MensagemChatEnum.md) | Canal de notificação para novas mensagens de chat  * &#x60;EMAIL&#x60; - E-mail * &#x60;SISTEMA&#x60; - Sistema * &#x60;AMBOS&#x60; - Ambos * &#x60;NENHUM&#x60; - Nenhum | [optional] [default to undefined]

## Example

```typescript
import { ConfiguracaoNotificacaoRequest } from './api';

const instance: ConfiguracaoNotificacaoRequest = {
    usuario,
    tarefa_atribuida,
    tarefa_comentario,
    tarefa_prazo,
    projeto_status,
    equipe_alteracao,
    documento_novo,
    risco_novo,
    mensagem_chat,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
