# AtribuiesApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**tasksAtribuicoesCreate**](#tasksatribuicoescreate) | **POST** /api/tasks/atribuicoes/ | Criar atribuição de tarefa|
|[**tasksAtribuicoesDestroy**](#tasksatribuicoesdestroy) | **DELETE** /api/tasks/atribuicoes/{id}/ | Remover atribuição|
|[**tasksAtribuicoesList**](#tasksatribuicoeslist) | **GET** /api/tasks/atribuicoes/ | Listar atribuições de tarefas|
|[**tasksAtribuicoesRetrieve**](#tasksatribuicoesretrieve) | **GET** /api/tasks/atribuicoes/{id}/ | Obter detalhes de atribuição|
|[**tasksTarefasAtribuirResponsavelCreate**](#taskstarefasatribuirresponsavelcreate) | **POST** /api/tasks/tarefas/{id}/atribuir_responsavel/ | Atribuir responsável à tarefa|
|[**tasksTarefasRemoverResponsavelCreate**](#taskstarefasremoverresponsavelcreate) | **POST** /api/tasks/tarefas/{id}/remover_responsavel/ | Remover responsável da tarefa|

# **tasksAtribuicoesCreate**
> AtribuicaoTarefa tasksAtribuicoesCreate(atribuicaoTarefaRequest)

Atribui uma tarefa a um usuário.

### Example

```typescript
import {
    AtribuiesApi,
    Configuration,
    AtribuicaoTarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AtribuiesApi(configuration);

let atribuicaoTarefaRequest: AtribuicaoTarefaRequest; //

const { status, data } = await apiInstance.tasksAtribuicoesCreate(
    atribuicaoTarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **atribuicaoTarefaRequest** | **AtribuicaoTarefaRequest**|  | |


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
|**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasksAtribuicoesDestroy**
> tasksAtribuicoesDestroy()

Remove a atribuição de uma tarefa a um usuário.

### Example

```typescript
import {
    AtribuiesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AtribuiesApi(configuration);

let id: number; //A unique integer value identifying this Atribuição de Tarefa. (default to undefined)

const { status, data } = await apiInstance.tasksAtribuicoesDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Atribuição de Tarefa. | defaults to undefined|


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

# **tasksAtribuicoesList**
> PaginatedAtribuicaoTarefaList tasksAtribuicoesList()

Retorna uma lista de atribuições de tarefas a usuários.

### Example

```typescript
import {
    AtribuiesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AtribuiesApi(configuration);

let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let tarefa: number; //Filtrar por ID da tarefa (optional) (default to undefined)
let usuario: number; //Filtrar por ID do usuário (optional) (default to undefined)

const { status, data } = await apiInstance.tasksAtribuicoesList(
    ordering,
    page,
    tarefa,
    usuario
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **tarefa** | [**number**] | Filtrar por ID da tarefa | (optional) defaults to undefined|
| **usuario** | [**number**] | Filtrar por ID do usuário | (optional) defaults to undefined|


### Return type

**PaginatedAtribuicaoTarefaList**

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

# **tasksAtribuicoesRetrieve**
> AtribuicaoTarefa tasksAtribuicoesRetrieve()

Retorna informações detalhadas de uma atribuição específica.

### Example

```typescript
import {
    AtribuiesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AtribuiesApi(configuration);

let id: number; //A unique integer value identifying this Atribuição de Tarefa. (default to undefined)

const { status, data } = await apiInstance.tasksAtribuicoesRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Atribuição de Tarefa. | defaults to undefined|


### Return type

**AtribuicaoTarefa**

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

# **tasksTarefasAtribuirResponsavelCreate**
> AtribuicaoTarefa tasksTarefasAtribuirResponsavelCreate()

Atribui um usuário como responsável pela tarefa.

### Example

```typescript
import {
    AtribuiesApi,
    Configuration,
    TasksTarefasAtribuirResponsavelCreateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AtribuiesApi(configuration);

let id: number; //A unique integer value identifying this Tarefa. (default to undefined)
let tasksTarefasAtribuirResponsavelCreateRequest: TasksTarefasAtribuirResponsavelCreateRequest; // (optional)

const { status, data } = await apiInstance.tasksTarefasAtribuirResponsavelCreate(
    id,
    tasksTarefasAtribuirResponsavelCreateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tasksTarefasAtribuirResponsavelCreateRequest** | **TasksTarefasAtribuirResponsavelCreateRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Tarefa. | defaults to undefined|


### Return type

**AtribuicaoTarefa**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |
|**400** |  |  -  |
|**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasksTarefasRemoverResponsavelCreate**
> tasksTarefasRemoverResponsavelCreate()

Remove um usuário como responsável pela tarefa.

### Example

```typescript
import {
    AtribuiesApi,
    Configuration,
    TasksTarefasRemoverResponsavelCreateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AtribuiesApi(configuration);

let id: number; //A unique integer value identifying this Tarefa. (default to undefined)
let tasksTarefasRemoverResponsavelCreateRequest: TasksTarefasRemoverResponsavelCreateRequest; // (optional)

const { status, data } = await apiInstance.tasksTarefasRemoverResponsavelCreate(
    id,
    tasksTarefasRemoverResponsavelCreateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tasksTarefasRemoverResponsavelCreateRequest** | **TasksTarefasRemoverResponsavelCreateRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Tarefa. | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**204** | No response body |  -  |
|**400** |  |  -  |
|**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

