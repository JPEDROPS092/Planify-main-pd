# ProjetoList

Serializer otimizado para listagem de projetos.  Inclui informações resumidas e estatísticas básicas para listagem eficiente.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **number** |  | [readonly] [default to undefined]
**titulo** | **string** |  | [default to undefined]
**descricao** | **string** |  | [default to undefined]
**data_inicio** | **string** |  | [default to undefined]
**data_fim** | **string** |  | [default to undefined]
**status** | [**Status18dEnum**](Status18dEnum.md) |  | [optional] [default to undefined]
**status_display** | **string** | Nome do status para exibição | [readonly] [default to undefined]
**prioridade** | [**PrioridadeEnum**](PrioridadeEnum.md) |  | [optional] [default to undefined]
**prioridade_display** | **string** | Nome da prioridade para exibição | [readonly] [default to undefined]
**criado_em** | **string** |  | [readonly] [default to undefined]
**atualizado_em** | **string** |  | [readonly] [default to undefined]
**arquivado** | **boolean** |  | [optional] [default to undefined]
**membros_count** | **number** | Número total de membros neste projeto | [readonly] [default to undefined]
**tasks_count** | **number** | Número total de tarefas neste projeto | [readonly] [default to undefined]
**progresso** | **number** | Progresso do projeto em percentual (0-100) | [readonly] [default to undefined]
**criador_username** | **string** | Nome de usuário do criador | [readonly] [default to undefined]
**atrasado** | **boolean** | Indica se o projeto está atrasado | [readonly] [default to undefined]

## Example

```typescript
import { ProjetoList } from './api';

const instance: ProjetoList = {
    id,
    titulo,
    descricao,
    data_inicio,
    data_fim,
    status,
    status_display,
    prioridade,
    prioridade_display,
    criado_em,
    atualizado_em,
    arquivado,
    membros_count,
    tasks_count,
    progresso,
    criador_username,
    atrasado,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
