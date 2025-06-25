# TarefaList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**titulo** | **string** |  | [default to undefined]
**projeto** | **number** |  | [default to undefined]
**sprint** | **number** |  | [optional] [default to undefined]
**status** | [**NovoStatus607Enum**](NovoStatus607Enum.md) |  | [optional] [default to undefined]
**prioridade** | [**PrioridadeEnum**](PrioridadeEnum.md) |  | [optional] [default to undefined]
**data_termino** | **string** |  | [default to undefined]
**criado_por** | [**User**](User.md) |  | [readonly] [default to undefined]
**atribuicoes** | [**Array&lt;AtribuicaoTarefa&gt;**](AtribuicaoTarefa.md) | Lista de usuários atribuídos a esta tarefa. | [readonly] [default to undefined]

## Example

```typescript
import { TarefaList } from './api';

const instance: TarefaList = {
    id,
    titulo,
    projeto,
    sprint,
    status,
    prioridade,
    data_termino,
    criado_por,
    atribuicoes,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
