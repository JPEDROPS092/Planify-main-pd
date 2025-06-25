# Risco


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**projeto** | **number** |  | [default to undefined]
**projeto_nome** | **string** |  | [readonly] [default to undefined]
**descricao** | **string** |  | [default to undefined]
**probabilidade** | [**ProbabilidadeEnum**](ProbabilidadeEnum.md) |  | [default to undefined]
**probabilidade_display** | **string** |  | [readonly] [default to undefined]
**impacto** | [**ImpactoEnum**](ImpactoEnum.md) |  | [default to undefined]
**impacto_display** | **string** |  | [readonly] [default to undefined]
**status** | [**NovoStatusA52Enum**](NovoStatusA52Enum.md) |  | [optional] [default to undefined]
**status_display** | **string** |  | [readonly] [default to undefined]
**responsavel_mitigacao** | **number** |  | [optional] [default to undefined]
**responsavel_mitigacao_nome** | **string** |  | [readonly] [default to undefined]
**plano_mitigacao** | **string** |  | [optional] [default to undefined]
**plano_contingencia** | **string** |  | [optional] [default to undefined]
**data_identificacao** | **string** |  | [readonly] [default to undefined]
**criado_por** | **number** |  | [optional] [default to undefined]
**criado_por_nome** | **string** |  | [readonly] [default to undefined]
**atualizado_em** | **string** |  | [readonly] [default to undefined]
**nivel_risco** | **string** |  | [readonly] [default to undefined]
**historico** | [**Array&lt;HistoricoRisco&gt;**](HistoricoRisco.md) |  | [readonly] [default to undefined]

## Example

```typescript
import { Risco } from './api';

const instance: Risco = {
    id,
    projeto,
    projeto_nome,
    descricao,
    probabilidade,
    probabilidade_display,
    impacto,
    impacto_display,
    status,
    status_display,
    responsavel_mitigacao,
    responsavel_mitigacao_nome,
    plano_mitigacao,
    plano_contingencia,
    data_identificacao,
    criado_por,
    criado_por_nome,
    atualizado_em,
    nivel_risco,
    historico,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
