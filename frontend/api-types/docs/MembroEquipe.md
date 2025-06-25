# MembroEquipe


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**equipe** | **number** |  | [default to undefined]
**usuario** | **number** |  | [default to undefined]
**usuario_nome** | **string** |  | [readonly] [default to undefined]
**usuario_email** | **string** |  | [readonly] [default to undefined]
**papel** | [**PapelF38Enum**](PapelF38Enum.md) |  | [default to undefined]
**papel_display** | **string** |  | [readonly] [default to undefined]
**adicionado_em** | **string** |  | [readonly] [default to undefined]
**adicionado_por** | **number** |  | [optional] [default to undefined]
**adicionado_por_nome** | **string** |  | [readonly] [default to undefined]

## Example

```typescript
import { MembroEquipe } from './api';

const instance: MembroEquipe = {
    id,
    equipe,
    usuario,
    usuario_nome,
    usuario_email,
    papel,
    papel_display,
    adicionado_em,
    adicionado_por,
    adicionado_por_nome,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
