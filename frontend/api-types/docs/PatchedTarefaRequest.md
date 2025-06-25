# PatchedTarefaRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**titulo** | **string** |  | [optional] [default to undefined]
**descricao** | **string** |  | [optional] [default to undefined]
**projeto** | **number** |  | [optional] [default to undefined]
**sprint** | **number** |  | [optional] [default to undefined]
**data_inicio** | **string** |  | [optional] [default to undefined]
**data_termino** | **string** |  | [optional] [default to undefined]
**prioridade** | [**PrioridadeEnum**](PrioridadeEnum.md) |  | [optional] [default to undefined]
**status** | [**NovoStatus607Enum**](NovoStatus607Enum.md) |  | [optional] [default to undefined]

## Example

```typescript
import { PatchedTarefaRequest } from './api';

const instance: PatchedTarefaRequest = {
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
