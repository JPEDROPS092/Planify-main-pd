# OrcamentoProjeto

Serializer para o modelo OrcamentoProjeto.  Inclui campos para o orçamento total e informações de aprovação. Adiciona campos de leitura para nomes relacionados (aprovador, projeto) e campos calculados (valor utilizado, valor restante, percentual utilizado).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**projeto** | **number** |  | [default to undefined]
**projeto_nome** | **string** |  | [readonly] [default to undefined]
**valor_total** | **string** |  | [default to undefined]
**data_aprovacao** | **string** |  | [readonly] [default to undefined]
**aprovado_por** | **number** |  | [optional] [default to undefined]
**aprovado_por_nome** | **string** |  | [readonly] [default to undefined]
**observacoes** | **string** |  | [optional] [default to undefined]
**valor_utilizado** | **string** |  | [readonly] [default to undefined]
**valor_restante** | **string** |  | [readonly] [default to undefined]
**percentual_utilizado** | **string** |  | [readonly] [default to undefined]

## Example

```typescript
import { OrcamentoProjeto } from './api';

const instance: OrcamentoProjeto = {
    id,
    projeto,
    projeto_nome,
    valor_total,
    data_aprovacao,
    aprovado_por,
    aprovado_por_nome,
    observacoes,
    valor_utilizado,
    valor_restante,
    percentual_utilizado,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
