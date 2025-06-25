# HistoricoStatusTarefa


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**tarefa** | **number** |  | [default to undefined]
**status_anterior** | [**NovoStatus607Enum**](NovoStatus607Enum.md) |  | [default to undefined]
**status_anterior_display** | **string** |  | [readonly] [default to undefined]
**novo_status** | [**NovoStatus607Enum**](NovoStatus607Enum.md) |  | [default to undefined]
**novo_status_display** | **string** |  | [readonly] [default to undefined]
**alterado_por** | **number** |  | [optional] [default to undefined]
**alterado_por_nome** | **string** |  | [readonly] [default to undefined]
**alterado_em** | **string** |  | [readonly] [default to undefined]

## Example

```typescript
import { HistoricoStatusTarefa } from './api';

const instance: HistoricoStatusTarefa = {
    id,
    tarefa,
    status_anterior,
    status_anterior_display,
    novo_status,
    novo_status_display,
    alterado_por,
    alterado_por_nome,
    alterado_em,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
