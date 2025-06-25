# EquipeList

Serializer simplificado para listagem de equipes

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**nome** | **string** |  | [default to undefined]
**criado_por_nome** | **string** | Nome completo do criador da equipe. | [readonly] [default to undefined]
**criado_em** | **string** |  | [readonly] [default to undefined]
**total_membros** | **number** | Número total de membros nesta equipe. | [readonly] [default to undefined]

## Example

```typescript
import { EquipeList } from './api';

const instance: EquipeList = {
    id,
    nome,
    criado_por_nome,
    criado_em,
    total_membros,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
