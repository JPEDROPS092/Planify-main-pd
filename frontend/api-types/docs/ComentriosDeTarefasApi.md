# ComentriosDeTarefasApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**tasksComentariosCreate**](#taskscomentarioscreate) | **POST** /api/tasks/comentarios/ | Criar comentário|
|[**tasksComentariosDestroy**](#taskscomentariosdestroy) | **DELETE** /api/tasks/comentarios/{id}/ | Excluir comentário|
|[**tasksComentariosList**](#taskscomentarioslist) | **GET** /api/tasks/comentarios/ | Listar comentários de tarefas|
|[**tasksComentariosPartialUpdate**](#taskscomentariospartialupdate) | **PATCH** /api/tasks/comentarios/{id}/ | Atualizar comentário parcialmente|
|[**tasksComentariosRetrieve**](#taskscomentariosretrieve) | **GET** /api/tasks/comentarios/{id}/ | Obter detalhes de comentário|
|[**tasksComentariosUpdate**](#taskscomentariosupdate) | **PUT** /api/tasks/comentarios/{id}/ | Atualizar comentário|

# **tasksComentariosCreate**
> ComentarioTarefa tasksComentariosCreate(comentarioTarefaRequest)

Adiciona um novo comentário a uma tarefa.

### Example

```typescript
import {
    ComentriosDeTarefasApi,
    Configuration,
    ComentarioTarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosDeTarefasApi(configuration);

let comentarioTarefaRequest: ComentarioTarefaRequest; //

const { status, data } = await apiInstance.tasksComentariosCreate(
    comentarioTarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **comentarioTarefaRequest** | **ComentarioTarefaRequest**|  | |


### Return type

**ComentarioTarefa**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasksComentariosDestroy**
> tasksComentariosDestroy()

Remove permanentemente um comentário.

### Example

```typescript
import {
    ComentriosDeTarefasApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosDeTarefasApi(configuration);

let id: number; //A unique integer value identifying this Comentário. (default to undefined)

const { status, data } = await apiInstance.tasksComentariosDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Comentário. | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasksComentariosList**
> PaginatedComentarioTarefaList tasksComentariosList()

Retorna uma lista de comentários de tarefas.

### Example

```typescript
import {
    ComentriosDeTarefasApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosDeTarefasApi(configuration);

let autor: number; //Filtrar por ID do autor (optional) (default to undefined)
let ordering: string; //Ordenar resultados (ex: -criado_em) (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let tarefa: number; //Filtrar por ID da tarefa (optional) (default to undefined)

const { status, data } = await apiInstance.tasksComentariosList(
    autor,
    ordering,
    page,
    search,
    tarefa
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **autor** | [**number**] | Filtrar por ID do autor | (optional) defaults to undefined|
| **ordering** | [**string**] | Ordenar resultados (ex: -criado_em) | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **tarefa** | [**number**] | Filtrar por ID da tarefa | (optional) defaults to undefined|


### Return type

**PaginatedComentarioTarefaList**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasksComentariosPartialUpdate**
> ComentarioTarefa tasksComentariosPartialUpdate()

Atualiza parcialmente o texto de um comentário existente.

### Example

```typescript
import {
    ComentriosDeTarefasApi,
    Configuration,
    PatchedComentarioTarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosDeTarefasApi(configuration);

let id: number; //A unique integer value identifying this Comentário. (default to undefined)
let patchedComentarioTarefaRequest: PatchedComentarioTarefaRequest; // (optional)

const { status, data } = await apiInstance.tasksComentariosPartialUpdate(
    id,
    patchedComentarioTarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedComentarioTarefaRequest** | **PatchedComentarioTarefaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Comentário. | defaults to undefined|


### Return type

**ComentarioTarefa**

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

# **tasksComentariosRetrieve**
> ComentarioTarefa tasksComentariosRetrieve()

Retorna informações detalhadas de um comentário específico.

### Example

```typescript
import {
    ComentriosDeTarefasApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosDeTarefasApi(configuration);

let id: number; //A unique integer value identifying this Comentário. (default to undefined)

const { status, data } = await apiInstance.tasksComentariosRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Comentário. | defaults to undefined|


### Return type

**ComentarioTarefa**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasksComentariosUpdate**
> ComentarioTarefa tasksComentariosUpdate(comentarioTarefaRequest)

Atualiza o texto de um comentário existente.

### Example

```typescript
import {
    ComentriosDeTarefasApi,
    Configuration,
    ComentarioTarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosDeTarefasApi(configuration);

let id: number; //A unique integer value identifying this Comentário. (default to undefined)
let comentarioTarefaRequest: ComentarioTarefaRequest; //

const { status, data } = await apiInstance.tasksComentariosUpdate(
    id,
    comentarioTarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **comentarioTarefaRequest** | **ComentarioTarefaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Comentário. | defaults to undefined|


### Return type

**ComentarioTarefa**

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

