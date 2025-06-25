# ProjetoDashboardResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**projeto** | **{ [key: string]: any; }** | Detalhes do projeto | [default to undefined]
**sprints** | **Array&lt;any&gt;** | Lista de sprints do projeto | [default to undefined]
**tarefas_kanban** | **{ [key: string]: any; }** | Tarefas agrupadas por status para visualização Kanban | [default to undefined]
**metricas** | **{ [key: string]: any; }** | Métricas do projeto | [default to undefined]
**atividades_recentes** | **Array&lt;any&gt;** | Atividades recentes no projeto | [default to undefined]

## Example

```typescript
import { ProjetoDashboardResponse } from './api';

const instance: ProjetoDashboardResponse = {
    projeto,
    sprints,
    tarefas_kanban,
    metricas,
    atividades_recentes,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
