# TarefaGantt


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** | ID da tarefa | [default to undefined]
**titulo** | **string** | Título da tarefa | [default to undefined]
**data_inicio** | **string** | Data de início da tarefa | [default to undefined]
**data_fim** | **string** | Data de término prevista da tarefa | [default to undefined]
**progresso** | **number** | Percentual de conclusão da tarefa | [default to undefined]
**dependencias** | **Array&lt;number&gt;** | IDs das tarefas das quais esta tarefa depende | [default to undefined]

## Example

```typescript
import { TarefaGantt } from './api';

const instance: TarefaGantt = {
    id,
    titulo,
    data_inicio,
    data_fim,
    progresso,
    dependencias,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
