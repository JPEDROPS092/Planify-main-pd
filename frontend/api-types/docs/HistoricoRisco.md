# HistoricoRisco


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**risco** | **number** |  | [default to undefined]
**status_anterior** | [**NovoStatusA52Enum**](NovoStatusA52Enum.md) |  | [default to undefined]
**status_anterior_display** | **string** |  | [readonly] [default to undefined]
**novo_status** | [**NovoStatusA52Enum**](NovoStatusA52Enum.md) |  | [default to undefined]
**novo_status_display** | **string** |  | [readonly] [default to undefined]
**probabilidade_anterior** | [**ProbabilidadeAnteriorEnum**](ProbabilidadeAnteriorEnum.md) |  | [default to undefined]
**probabilidade_anterior_display** | **string** |  | [readonly] [default to undefined]
**nova_probabilidade** | [**NovaProbabilidadeEnum**](NovaProbabilidadeEnum.md) |  | [default to undefined]
**nova_probabilidade_display** | **string** |  | [readonly] [default to undefined]
**impacto_anterior** | [**ImpactoEnum**](ImpactoEnum.md) |  | [default to undefined]
**impacto_anterior_display** | **string** |  | [readonly] [default to undefined]
**novo_impacto** | [**ImpactoEnum**](ImpactoEnum.md) |  | [default to undefined]
**novo_impacto_display** | **string** |  | [readonly] [default to undefined]
**alterado_por** | **number** |  | [optional] [default to undefined]
**alterado_por_nome** | **string** |  | [readonly] [default to undefined]
**alterado_em** | **string** |  | [readonly] [default to undefined]
**observacao** | **string** |  | [optional] [default to undefined]

## Example

```typescript
import { HistoricoRisco } from './api';

const instance: HistoricoRisco = {
    id,
    risco,
    status_anterior,
    status_anterior_display,
    novo_status,
    novo_status_display,
    probabilidade_anterior,
    probabilidade_anterior_display,
    nova_probabilidade,
    nova_probabilidade_display,
    impacto_anterior,
    impacto_anterior_display,
    novo_impacto,
    novo_impacto_display,
    alterado_por,
    alterado_por_nome,
    alterado_em,
    observacao,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
