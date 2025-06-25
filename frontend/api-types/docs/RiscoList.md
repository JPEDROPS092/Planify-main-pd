# RiscoList

Serializer simplificado para listagem de riscos

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
**data_identificacao** | **string** |  | [readonly] [default to undefined]
**nivel_risco** | **string** |  | [readonly] [default to undefined]

## Example

```typescript
import { RiscoList } from './api';

const instance: RiscoList = {
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
    data_identificacao,
    nivel_risco,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
