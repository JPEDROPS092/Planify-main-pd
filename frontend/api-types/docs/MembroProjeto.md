# MembroProjeto

Serializer para membros de projeto.  Inclui informações básicas do usuário e seu papel no projeto.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**usuario_id** | **number** |  | [readonly] [default to undefined]
**username** | **string** |  | [readonly] [default to undefined]
**full_name** | **string** |  | [readonly] [default to undefined]
**papel** | [**MembroProjetoPapelEnum**](MembroProjetoPapelEnum.md) |  | [default to undefined]
**papel_display** | **string** | Nome do papel para exibição | [readonly] [default to undefined]

## Example

```typescript
import { MembroProjeto } from './api';

const instance: MembroProjeto = {
    id,
    usuario_id,
    username,
    full_name,
    papel,
    papel_display,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
