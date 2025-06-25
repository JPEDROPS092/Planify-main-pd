# TasksTarefasAtualizarStatusCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **string** | Novo status da tarefa (A_FAZER, EM_ANDAMENTO, FEITO, BLOQUEADO, CANCELADO) | [default to undefined]
**comentario** | **string** | Comentário opcional sobre a mudança de status | [optional] [default to undefined]

## Example

```typescript
import { TasksTarefasAtualizarStatusCreateRequest } from './api';

const instance: TasksTarefasAtualizarStatusCreateRequest = {
    status,
    comentario,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
