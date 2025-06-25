# TarefaRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**titulo** | **string** |  | [default to undefined]
**descricao** | **string** |  | [default to undefined]
**projeto** | **number** |  | [default to undefined]
**sprint** | **number** |  | [optional] [default to undefined]
**data_inicio** | **string** |  | [default to undefined]
**data_termino** | **string** |  | [default to undefined]
**prioridade** | [**PrioridadeEnum**](PrioridadeEnum.md) |  | [optional] [default to undefined]
**status** | [**NovoStatus607Enum**](NovoStatus607Enum.md) |  | [optional] [default to undefined]

## Example

```typescript
import { TarefaRequest } from './api';

const instance: TarefaRequest = {
    titulo,
    descricao,
    projeto,
    sprint,
    data_inicio,
    data_termino,
    prioridade,
    status,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
