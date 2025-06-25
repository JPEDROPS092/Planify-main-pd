# PatchedOrcamentoProjetoRequest

Serializer para o modelo OrcamentoProjeto.  Inclui campos para o orçamento total e informações de aprovação. Adiciona campos de leitura para nomes relacionados (aprovador, projeto) e campos calculados (valor utilizado, valor restante, percentual utilizado).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**projeto** | **number** |  | [optional] [default to undefined]
**valor_total** | **string** |  | [optional] [default to undefined]
**aprovado_por** | **number** |  | [optional] [default to undefined]
**observacoes** | **string** |  | [optional] [default to undefined]

## Example

```typescript
import { PatchedOrcamentoProjetoRequest } from './api';

const instance: PatchedOrcamentoProjetoRequest = {
    projeto,
    valor_total,
    aprovado_por,
    observacoes,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
