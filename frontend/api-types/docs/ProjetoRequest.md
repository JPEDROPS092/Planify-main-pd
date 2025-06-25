# ProjetoRequest

Serializer completo para projetos.  Inclui informações detalhadas do projeto, membros, estatísticas de sprints e tarefas.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**titulo** | **string** |  | [default to undefined]
**descricao** | **string** |  | [default to undefined]
**data_inicio** | **string** |  | [default to undefined]
**data_fim** | **string** |  | [default to undefined]
**status** | [**Status18dEnum**](Status18dEnum.md) |  | [optional] [default to undefined]
**prioridade** | [**PrioridadeEnum**](PrioridadeEnum.md) |  | [optional] [default to undefined]
**arquivado** | **boolean** |  | [optional] [default to undefined]

## Example

```typescript
import { ProjetoRequest } from './api';

const instance: ProjetoRequest = {
    titulo,
    descricao,
    data_inicio,
    data_fim,
    status,
    prioridade,
    arquivado,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
