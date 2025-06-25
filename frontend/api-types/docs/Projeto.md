# Projeto

Serializer completo para projetos.  Inclui informações detalhadas do projeto, membros, estatísticas de sprints e tarefas.

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
**criado_por** | **number** |  | [readonly] [default to undefined]
**criador_username** | **string** | Nome de usuário do criador | [readonly] [default to undefined]
**criador_nome** | **string** | Nome completo do criador | [readonly] [default to undefined]
**criado_em** | **string** |  | [readonly] [default to undefined]
**atualizado_em** | **string** |  | [readonly] [default to undefined]
**arquivado** | **boolean** |  | [optional] [default to undefined]
**membros** | [**Array&lt;MembroProjeto&gt;**](MembroProjeto.md) | Lista de membros associados ao projeto | [readonly] [default to undefined]
**sprints_count** | **number** | Número total de sprints neste projeto | [readonly] [default to undefined]
**tasks_count** | **number** | Número total de tarefas neste projeto | [readonly] [default to undefined]
**progresso** | **number** | Progresso do projeto em percentual (0-100) | [readonly] [default to undefined]
**dias_restantes** | **number** | Dias restantes até a data de fim | [readonly] [default to undefined]
**atrasado** | **boolean** | Indica se o projeto está atrasado | [readonly] [default to undefined]

## Example

```typescript
import { Projeto } from './api';

const instance: Projeto = {
    id,
    titulo,
    descricao,
    data_inicio,
    data_fim,
    status,
    status_display,
    prioridade,
    prioridade_display,
    criado_por,
    criador_username,
    criador_nome,
    criado_em,
    atualizado_em,
    arquivado,
    membros,
    sprints_count,
    tasks_count,
    progresso,
    dias_restantes,
    atrasado,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
