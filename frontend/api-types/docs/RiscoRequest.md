# RiscoRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**projeto** | **number** |  | [default to undefined]
**descricao** | **string** |  | [default to undefined]
**probabilidade** | [**ProbabilidadeEnum**](ProbabilidadeEnum.md) |  | [default to undefined]
**impacto** | [**ImpactoEnum**](ImpactoEnum.md) |  | [default to undefined]
**status** | [**NovoStatusA52Enum**](NovoStatusA52Enum.md) |  | [optional] [default to undefined]
**responsavel_mitigacao** | **number** |  | [optional] [default to undefined]
**plano_mitigacao** | **string** |  | [optional] [default to undefined]
**plano_contingencia** | **string** |  | [optional] [default to undefined]
**criado_por** | **number** |  | [optional] [default to undefined]

## Example

```typescript
import { RiscoRequest } from './api';

const instance: RiscoRequest = {
    projeto,
    descricao,
    probabilidade,
    impacto,
    status,
    responsavel_mitigacao,
    plano_mitigacao,
    plano_contingencia,
    criado_por,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
