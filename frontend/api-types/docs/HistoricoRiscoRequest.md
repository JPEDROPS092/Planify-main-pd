# HistoricoRiscoRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**risco** | **number** |  | [default to undefined]
**status_anterior** | [**NovoStatusA52Enum**](NovoStatusA52Enum.md) |  | [default to undefined]
**novo_status** | [**NovoStatusA52Enum**](NovoStatusA52Enum.md) |  | [default to undefined]
**probabilidade_anterior** | [**ProbabilidadeAnteriorEnum**](ProbabilidadeAnteriorEnum.md) |  | [default to undefined]
**nova_probabilidade** | [**NovaProbabilidadeEnum**](NovaProbabilidadeEnum.md) |  | [default to undefined]
**impacto_anterior** | [**ImpactoEnum**](ImpactoEnum.md) |  | [default to undefined]
**novo_impacto** | [**ImpactoEnum**](ImpactoEnum.md) |  | [default to undefined]
**alterado_por** | **number** |  | [optional] [default to undefined]
**observacao** | **string** |  | [optional] [default to undefined]

## Example

```typescript
import { HistoricoRiscoRequest } from './api';

const instance: HistoricoRiscoRequest = {
    risco,
    status_anterior,
    novo_status,
    probabilidade_anterior,
    nova_probabilidade,
    impacto_anterior,
    novo_impacto,
    alterado_por,
    observacao,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
