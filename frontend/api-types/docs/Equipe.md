# Equipe


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**nome** | **string** |  | [default to undefined]
**descricao** | **string** |  | [optional] [default to undefined]
**criado_por** | **number** |  | [optional] [default to undefined]
**criado_por_nome** | **string** | Nome completo do usuário que criou a equipe. | [readonly] [default to undefined]
**criado_em** | **string** |  | [readonly] [default to undefined]
**atualizado_em** | **string** |  | [readonly] [default to undefined]
**membros** | [**Array&lt;MembroEquipe&gt;**](MembroEquipe.md) | Lista de membros desta equipe. | [readonly] [default to undefined]
**permissoes** | [**Array&lt;PermissaoEquipe&gt;**](PermissaoEquipe.md) | Lista de permissões associadas a esta equipe. | [readonly] [default to undefined]
**total_membros** | **number** | Número total de membros nesta equipe. | [readonly] [default to undefined]

## Example

```typescript
import { Equipe } from './api';

const instance: Equipe = {
    id,
    nome,
    descricao,
    criado_por,
    criado_por_nome,
    criado_em,
    atualizado_em,
    membros,
    permissoes,
    total_membros,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
