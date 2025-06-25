# HistoricoDocumentoRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**documento** | **number** |  | [default to undefined]
**versao_anterior** | **string** |  | [default to undefined]
**arquivo_anterior** | **File** |  | [default to undefined]
**tamanho_arquivo** | **number** | Tamanho em bytes | [default to undefined]
**alterado_por** | **number** |  | [optional] [default to undefined]
**observacao** | **string** |  | [optional] [default to undefined]

## Example

```typescript
import { HistoricoDocumentoRequest } from './api';

const instance: HistoricoDocumentoRequest = {
    documento,
    versao_anterior,
    arquivo_anterior,
    tamanho_arquivo,
    alterado_por,
    observacao,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
