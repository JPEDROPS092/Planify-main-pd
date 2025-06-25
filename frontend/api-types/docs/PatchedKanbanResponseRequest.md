# PatchedKanbanResponseRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**projeto** | **number** | ID do projeto | [optional] [default to undefined]
**titulo** | **string** | Título do projeto | [optional] [default to undefined]
**colunas** | [**Array&lt;ColunaKanbanRequest&gt;**](ColunaKanbanRequest.md) | Colunas do quadro Kanban | [optional] [default to undefined]

## Example

```typescript
import { PatchedKanbanResponseRequest } from './api';

const instance: PatchedKanbanResponseRequest = {
    projeto,
    titulo,
    colunas,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
