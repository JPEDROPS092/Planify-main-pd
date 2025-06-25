# MembroProjetoRequest

Serializer para membros de projeto.  Inclui informações básicas do usuário e seu papel no projeto.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usuario** | **number** |  | [default to undefined]
**papel** | [**MembroProjetoPapelEnum**](MembroProjetoPapelEnum.md) |  | [default to undefined]

## Example

```typescript
import { MembroProjetoRequest } from './api';

const instance: MembroProjetoRequest = {
    usuario,
    papel,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
