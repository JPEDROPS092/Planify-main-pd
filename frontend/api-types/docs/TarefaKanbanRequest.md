# TarefaKanbanRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** | ID da tarefa | [default to undefined]
**titulo** | **string** | Título da tarefa | [default to undefined]
**descricao** | **string** | Descrição da tarefa | [default to undefined]
**status** | **string** | Status atual da tarefa | [default to undefined]
**prioridade** | **string** | Prioridade da tarefa | [default to undefined]
**data_inicio** | **string** | Data de início da tarefa | [default to undefined]
**data_fim** | **string** | Data de término prevista da tarefa | [default to undefined]
**responsaveis** | **Array&lt;{ [key: string]: any; }&gt;** | Lista de usuários responsáveis pela tarefa | [default to undefined]

## Example

```typescript
import { TarefaKanbanRequest } from './api';

const instance: TarefaKanbanRequest = {
    id,
    titulo,
    descricao,
    status,
    prioridade,
    data_inicio,
    data_fim,
    responsaveis,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
