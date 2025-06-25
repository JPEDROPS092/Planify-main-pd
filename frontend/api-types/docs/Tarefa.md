# Tarefa


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**titulo** | **string** |  | [default to undefined]
**descricao** | **string** |  | [default to undefined]
**projeto** | **number** |  | [default to undefined]
**sprint** | **number** |  | [optional] [default to undefined]
**data_inicio** | **string** |  | [default to undefined]
**data_termino** | **string** |  | [default to undefined]
**prioridade** | [**PrioridadeEnum**](PrioridadeEnum.md) |  | [optional] [default to undefined]
**status** | [**NovoStatus607Enum**](NovoStatus607Enum.md) |  | [optional] [default to undefined]
**criado_por** | [**User**](User.md) |  | [readonly] [default to undefined]
**criado_em** | **string** |  | [readonly] [default to undefined]
**atualizado_em** | **string** |  | [readonly] [default to undefined]
**atribuicoes** | [**Array&lt;AtribuicaoTarefa&gt;**](AtribuicaoTarefa.md) | Lista de usuários atribuídos a esta tarefa. | [readonly] [default to undefined]

## Example

```typescript
import { Tarefa } from './api';

const instance: Tarefa = {
    id,
    titulo,
    descricao,
    projeto,
    sprint,
    data_inicio,
    data_termino,
    prioridade,
    status,
    criado_por,
    criado_em,
    atualizado_em,
    atribuicoes,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
