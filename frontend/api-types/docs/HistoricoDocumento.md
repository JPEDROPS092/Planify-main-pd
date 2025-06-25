# HistoricoDocumento


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**documento** | **number** |  | [default to undefined]
**versao_anterior** | **string** |  | [default to undefined]
**arquivo_anterior** | **string** |  | [default to undefined]
**tamanho_arquivo** | **number** | Tamanho em bytes | [default to undefined]
**alterado_por** | **number** |  | [optional] [default to undefined]
**alterado_por_nome** | **string** |  | [readonly] [default to undefined]
**data_alteracao** | **string** |  | [readonly] [default to undefined]
**observacao** | **string** |  | [optional] [default to undefined]

## Example

```typescript
import { HistoricoDocumento } from './api';

const instance: HistoricoDocumento = {
    id,
    documento,
    versao_anterior,
    arquivo_anterior,
    tamanho_arquivo,
    alterado_por,
    alterado_por_nome,
    data_alteracao,
    observacao,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
