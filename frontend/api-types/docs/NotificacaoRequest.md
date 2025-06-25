# NotificacaoRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usuario** | **number** | Usuário que receberá a notificação | [default to undefined]
**tipo** | [**NotificacaoTipoEnum**](NotificacaoTipoEnum.md) | Tipo de objeto relacionado à notificação  * &#x60;TAREFA&#x60; - Tarefa * &#x60;PROJETO&#x60; - Projeto * &#x60;EQUIPE&#x60; - Equipe * &#x60;RISCO&#x60; - Risco * &#x60;DOCUMENTO&#x60; - Documento * &#x60;SISTEMA&#x60; - Sistema | [default to undefined]
**titulo** | **string** | Título breve da notificação | [default to undefined]
**mensagem** | **string** | Conteúdo detalhado da notificação | [default to undefined]
**lida** | **boolean** | Indica se a notificação foi lida pelo usuário | [optional] [default to undefined]
**prioridade** | [**PrioridadeEnum**](PrioridadeEnum.md) | Nível de prioridade da notificação  * &#x60;BAIXA&#x60; - Baixa * &#x60;MEDIA&#x60; - Média * &#x60;ALTA&#x60; - Alta | [optional] [default to undefined]
**projeto** | **number** | Projeto relacionado à notificação (se aplicável) | [optional] [default to undefined]
**tarefa** | **number** | Tarefa relacionada à notificação (se aplicável) | [optional] [default to undefined]
**url** | **string** | URL para redirecionamento quando a notificação for clicada | [optional] [default to undefined]

## Example

```typescript
import { NotificacaoRequest } from './api';

const instance: NotificacaoRequest = {
    usuario,
    tipo,
    titulo,
    mensagem,
    lida,
    prioridade,
    projeto,
    tarefa,
    url,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
