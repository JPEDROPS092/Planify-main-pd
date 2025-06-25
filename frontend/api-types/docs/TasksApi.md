# TasksApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**tasksAtribuicoesPartialUpdate**](#tasksatribuicoespartialupdate) | **PATCH** /api/tasks/atribuicoes/{id}/ | |
|[**tasksAtribuicoesUpdate**](#tasksatribuicoesupdate) | **PUT** /api/tasks/atribuicoes/{id}/ | |

# **tasksAtribuicoesPartialUpdate**
> AtribuicaoTarefa tasksAtribuicoesPartialUpdate()

ViewSet para gerenciamento de atribuições de tarefas a usuários.  Permite criar, listar, visualizar e remover atribuições de tarefas a usuários. O usuário que faz a atribuição é automaticamente registrado.

### Example

```typescript
import {
    TasksApi,
    Configuration,
    PatchedAtribuicaoTarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new TasksApi(configuration);

let id: number; //A unique integer value identifying this Atribuição de Tarefa. (default to undefined)
let patchedAtribuicaoTarefaRequest: PatchedAtribuicaoTarefaRequest; // (optional)

const { status, data } = await apiInstance.tasksAtribuicoesPartialUpdate(
    id,
    patchedAtribuicaoTarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedAtribuicaoTarefaRequest** | **PatchedAtribuicaoTarefaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Atribuição de Tarefa. | defaults to undefined|


### Return type

**AtribuicaoTarefa**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasksAtribuicoesUpdate**
> AtribuicaoTarefa tasksAtribuicoesUpdate(atribuicaoTarefaRequest)

ViewSet para gerenciamento de atribuições de tarefas a usuários.  Permite criar, listar, visualizar e remover atribuições de tarefas a usuários. O usuário que faz a atribuição é automaticamente registrado.

### Example

```typescript
import {
    TasksApi,
    Configuration,
    AtribuicaoTarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new TasksApi(configuration);

let id: number; //A unique integer value identifying this Atribuição de Tarefa. (default to undefined)
let atribuicaoTarefaRequest: AtribuicaoTarefaRequest; //

const { status, data } = await apiInstance.tasksAtribuicoesUpdate(
    id,
    atribuicaoTarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **atribuicaoTarefaRequest** | **AtribuicaoTarefaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Atribuição de Tarefa. | defaults to undefined|


### Return type

**AtribuicaoTarefa**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

