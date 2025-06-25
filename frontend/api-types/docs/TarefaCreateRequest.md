# TarefaCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**titulo** | **string** | Título da tarefa | [default to undefined]
**descricao** | **string** | Descrição da tarefa | [optional] [default to undefined]
**data_inicio** | **string** | Data de início da tarefa | [default to undefined]
**data_fim** | **string** | Data de término prevista da tarefa | [default to undefined]
**prioridade** | [**PrioridadeEnum**](PrioridadeEnum.md) | Prioridade da tarefa  * &#x60;BAIXA&#x60; - BAIXA * &#x60;MEDIA&#x60; - MEDIA * &#x60;ALTA&#x60; - ALTA | [default to undefined]
**status** | [**TarefaCreateStatusEnum**](TarefaCreateStatusEnum.md) | Status inicial da tarefa  * &#x60;PENDENTE&#x60; - PENDENTE * &#x60;EM_ANDAMENTO&#x60; - EM_ANDAMENTO * &#x60;CONCLUIDA&#x60; - CONCLUIDA * &#x60;BLOQUEADA&#x60; - BLOQUEADA | [default to undefined]
**responsaveis** | **Array&lt;number&gt;** | IDs dos usuários responsáveis pela tarefa | [optional] [default to undefined]

## Example

```typescript
import { TarefaCreateRequest } from './api';

const instance: TarefaCreateRequest = {
    titulo,
    descricao,
    data_inicio,
    data_fim,
    prioridade,
    status,
    responsaveis,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
