# TarefasApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**documentsAssociarTarefaCreate**](#documentsassociartarefacreate) | **POST** /api/documents/{id}/associar_tarefa/ | Associar documento a uma tarefa|
|[**tasksTarefasAdicionarComentarioCreate**](#taskstarefasadicionarcomentariocreate) | **POST** /api/tasks/tarefas/{id}/adicionar_comentario/ | Adicionar comentário à tarefa|
|[**tasksTarefasAssociarSprintCreate**](#taskstarefasassociarsprintcreate) | **POST** /api/tasks/tarefas/{id}/associar_sprint/ | Associar tarefa a uma sprint|
|[**tasksTarefasAtualizarStatusCreate**](#taskstarefasatualizarstatuscreate) | **POST** /api/tasks/tarefas/{id}/atualizar_status/ | Atualizar status da tarefa|
|[**tasksTarefasCreate**](#taskstarefascreate) | **POST** /api/tasks/tarefas/ | Criar tarefa|
|[**tasksTarefasDestroy**](#taskstarefasdestroy) | **DELETE** /api/tasks/tarefas/{id}/ | Excluir tarefa|
|[**tasksTarefasHistoricoStatusList**](#taskstarefashistoricostatuslist) | **GET** /api/tasks/tarefas/{id}/historico_status/ | Obter histórico de status da tarefa|
|[**tasksTarefasList**](#taskstarefaslist) | **GET** /api/tasks/tarefas/ | Listar tarefas|
|[**tasksTarefasPartialUpdate**](#taskstarefaspartialupdate) | **PATCH** /api/tasks/tarefas/{id}/ | Atualizar tarefa parcialmente|
|[**tasksTarefasRetrieve**](#taskstarefasretrieve) | **GET** /api/tasks/tarefas/{id}/ | Obter detalhes da tarefa|
|[**tasksTarefasUpdate**](#taskstarefasupdate) | **PUT** /api/tasks/tarefas/{id}/ | Atualizar tarefa|

# **documentsAssociarTarefaCreate**
> Documento documentsAssociarTarefaCreate()

Associa ou desassocia um documento a uma tarefa específica. Forneça \'tarefa_id\' para associar, ou \'tarefa_id: 0\' (ou nulo) para desassociar.

### Example

```typescript
import {
    TarefasApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new TarefasApi(configuration);

let id: number; //A unique integer value identifying this Documento. (default to undefined)
let body: any; // (optional)

const { status, data } = await apiInstance.documentsAssociarTarefaCreate(
    id,
    body
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **body** | **any**|  | |
| **id** | [**number**] | A unique integer value identifying this Documento. | defaults to undefined|


### Return type

**Documento**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Documento associado/desassociado com sucesso |  -  |
|**400** | Dados inválidos (ex: tarefa_id não fornecido) |  -  |
|**404** | Documento ou Tarefa não encontrada |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasksTarefasAdicionarComentarioCreate**
> ComentarioTarefa tasksTarefasAdicionarComentarioCreate()

Adiciona um novo comentário à tarefa.

### Example

```typescript
import {
    TarefasApi,
    Configuration,
    TasksTarefasAdicionarComentarioCreateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new TarefasApi(configuration);

let id: number; //A unique integer value identifying this Tarefa. (default to undefined)
let tasksTarefasAdicionarComentarioCreateRequest: TasksTarefasAdicionarComentarioCreateRequest; // (optional)

const { status, data } = await apiInstance.tasksTarefasAdicionarComentarioCreate(
    id,
    tasksTarefasAdicionarComentarioCreateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tasksTarefasAdicionarComentarioCreateRequest** | **TasksTarefasAdicionarComentarioCreateRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Tarefa. | defaults to undefined|


### Return type

**ComentarioTarefa**

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

# **tasksTarefasAssociarSprintCreate**
> Tarefa tasksTarefasAssociarSprintCreate()

Associa a tarefa a uma sprint ou remove a associação existente.

### Example

```typescript
import {
    TarefasApi,
    Configuration,
    TasksTarefasAssociarSprintCreateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new TarefasApi(configuration);

let id: number; //A unique integer value identifying this Tarefa. (default to undefined)
let tasksTarefasAssociarSprintCreateRequest: TasksTarefasAssociarSprintCreateRequest; // (optional)

const { status, data } = await apiInstance.tasksTarefasAssociarSprintCreate(
    id,
    tasksTarefasAssociarSprintCreateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tasksTarefasAssociarSprintCreateRequest** | **TasksTarefasAssociarSprintCreateRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Tarefa. | defaults to undefined|


### Return type

**Tarefa**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**400** |  |  -  |
|**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasksTarefasAtualizarStatusCreate**
> Tarefa tasksTarefasAtualizarStatusCreate()

Atualiza o status de uma tarefa e registra a alteração no histórico.

### Example

```typescript
import {
    TarefasApi,
    Configuration,
    TasksTarefasAtualizarStatusCreateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new TarefasApi(configuration);

let id: number; //A unique integer value identifying this Tarefa. (default to undefined)
let tasksTarefasAtualizarStatusCreateRequest: TasksTarefasAtualizarStatusCreateRequest; // (optional)

const { status, data } = await apiInstance.tasksTarefasAtualizarStatusCreate(
    id,
    tasksTarefasAtualizarStatusCreateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tasksTarefasAtualizarStatusCreateRequest** | **TasksTarefasAtualizarStatusCreateRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Tarefa. | defaults to undefined|


### Return type

**Tarefa**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**400** |  |  -  |
|**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasksTarefasCreate**
> Tarefa tasksTarefasCreate(tarefaRequest)

Cria uma nova tarefa com os dados fornecidos.

### Example

```typescript
import {
    TarefasApi,
    Configuration,
    TarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new TarefasApi(configuration);

let tarefaRequest: TarefaRequest; //

const { status, data } = await apiInstance.tasksTarefasCreate(
    tarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tarefaRequest** | **TarefaRequest**|  | |


### Return type

**Tarefa**

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

# **tasksTarefasDestroy**
> tasksTarefasDestroy()

Remove permanentemente uma tarefa.

### Example

```typescript
import {
    TarefasApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new TarefasApi(configuration);

let id: number; //A unique integer value identifying this Tarefa. (default to undefined)

const { status, data } = await apiInstance.tasksTarefasDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Tarefa. | defaults to undefined|


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

# **tasksTarefasHistoricoStatusList**
> PaginatedHistoricoStatusTarefaList tasksTarefasHistoricoStatusList()

Retorna o histórico de alterações de status da tarefa.

### Example

```typescript
import {
    TarefasApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new TarefasApi(configuration);

let id: number; //A unique integer value identifying this Tarefa. (default to undefined)
let atrasada: boolean; //Filtra tarefas atrasadas (data_termino < hoje e status != FEITO) (optional) (default to undefined)
let dataInicioAntesAfter: string; //Filtra tarefas com data de início antes da data especificada (optional) (default to undefined)
let dataInicioAntesBefore: string; //Filtra tarefas com data de início antes da data especificada (optional) (default to undefined)
let dataInicioAposAfter: string; //Filtra tarefas com data de início após a data especificada (optional) (default to undefined)
let dataInicioAposBefore: string; //Filtra tarefas com data de início após a data especificada (optional) (default to undefined)
let dataTerminoAntesAfter: string; //Filtra tarefas com data de término antes da data especificada (optional) (default to undefined)
let dataTerminoAntesBefore: string; //Filtra tarefas com data de término antes da data especificada (optional) (default to undefined)
let dataTerminoAposAfter: string; //Filtra tarefas com data de término após a data especificada (optional) (default to undefined)
let dataTerminoAposBefore: string; //Filtra tarefas com data de término após a data especificada (optional) (default to undefined)
let descricao: string; //Filtra por descrição (case insensitive) (optional) (default to undefined)
let minhasTarefas: boolean; //Filtra tarefas do usuário autenticado (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let prioridade: string; //Filtra por prioridade (pode ser múltiplas, separadas por vírgula) (optional) (default to undefined)
let projeto: number; // (optional) (default to undefined)
let responsavel: string; //Filtra tarefas pelo ID do usuário responsável (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let semResponsavel: boolean; //Filtra tarefas sem responsáveis atribuídos (optional) (default to undefined)
let semSprint: boolean; //Filtra tarefas que não estão associadas a nenhuma sprint (optional) (default to undefined)
let sprint: number; // (optional) (default to undefined)
let status: string; //Filtra por status (pode ser múltiplos, separados por vírgula) (optional) (default to undefined)
let titulo: string; //Filtra por título (case insensitive) (optional) (default to undefined)

const { status, data } = await apiInstance.tasksTarefasHistoricoStatusList(
    id,
    atrasada,
    dataInicioAntesAfter,
    dataInicioAntesBefore,
    dataInicioAposAfter,
    dataInicioAposBefore,
    dataTerminoAntesAfter,
    dataTerminoAntesBefore,
    dataTerminoAposAfter,
    dataTerminoAposBefore,
    descricao,
    minhasTarefas,
    ordering,
    page,
    prioridade,
    projeto,
    responsavel,
    search,
    semResponsavel,
    semSprint,
    sprint,
    status,
    titulo
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Tarefa. | defaults to undefined|
| **atrasada** | [**boolean**] | Filtra tarefas atrasadas (data_termino &lt; hoje e status !&#x3D; FEITO) | (optional) defaults to undefined|
| **dataInicioAntesAfter** | [**string**] | Filtra tarefas com data de início antes da data especificada | (optional) defaults to undefined|
| **dataInicioAntesBefore** | [**string**] | Filtra tarefas com data de início antes da data especificada | (optional) defaults to undefined|
| **dataInicioAposAfter** | [**string**] | Filtra tarefas com data de início após a data especificada | (optional) defaults to undefined|
| **dataInicioAposBefore** | [**string**] | Filtra tarefas com data de início após a data especificada | (optional) defaults to undefined|
| **dataTerminoAntesAfter** | [**string**] | Filtra tarefas com data de término antes da data especificada | (optional) defaults to undefined|
| **dataTerminoAntesBefore** | [**string**] | Filtra tarefas com data de término antes da data especificada | (optional) defaults to undefined|
| **dataTerminoAposAfter** | [**string**] | Filtra tarefas com data de término após a data especificada | (optional) defaults to undefined|
| **dataTerminoAposBefore** | [**string**] | Filtra tarefas com data de término após a data especificada | (optional) defaults to undefined|
| **descricao** | [**string**] | Filtra por descrição (case insensitive) | (optional) defaults to undefined|
| **minhasTarefas** | [**boolean**] | Filtra tarefas do usuário autenticado | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **prioridade** | [**string**] | Filtra por prioridade (pode ser múltiplas, separadas por vírgula) | (optional) defaults to undefined|
| **projeto** | [**number**] |  | (optional) defaults to undefined|
| **responsavel** | [**string**] | Filtra tarefas pelo ID do usuário responsável | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **semResponsavel** | [**boolean**] | Filtra tarefas sem responsáveis atribuídos | (optional) defaults to undefined|
| **semSprint** | [**boolean**] | Filtra tarefas que não estão associadas a nenhuma sprint | (optional) defaults to undefined|
| **sprint** | [**number**] |  | (optional) defaults to undefined|
| **status** | [**string**] | Filtra por status (pode ser múltiplos, separados por vírgula) | (optional) defaults to undefined|
| **titulo** | [**string**] | Filtra por título (case insensitive) | (optional) defaults to undefined|


### Return type

**PaginatedHistoricoStatusTarefaList**

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

# **tasksTarefasList**
> PaginatedTarefaListList tasksTarefasList()

Retorna uma lista paginada de tarefas com opções de filtragem e ordenação.

### Example

```typescript
import {
    TarefasApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new TarefasApi(configuration);

let atrasada: boolean; //Filtrar tarefas atrasadas (optional) (default to undefined)
let dataInicioAntesAfter: string; //Filtra tarefas com data de início antes da data especificada (optional) (default to undefined)
let dataInicioAntesBefore: string; //Filtra tarefas com data de início antes da data especificada (optional) (default to undefined)
let dataInicioAposAfter: string; //Filtra tarefas com data de início após a data especificada (optional) (default to undefined)
let dataInicioAposBefore: string; //Filtra tarefas com data de início após a data especificada (optional) (default to undefined)
let dataTerminoAntesAfter: string; //Filtra tarefas com data de término antes da data especificada (optional) (default to undefined)
let dataTerminoAntesBefore: string; //Filtra tarefas com data de término antes da data especificada (optional) (default to undefined)
let dataTerminoAposAfter: string; //Filtra tarefas com data de término após a data especificada (optional) (default to undefined)
let dataTerminoAposBefore: string; //Filtra tarefas com data de término após a data especificada (optional) (default to undefined)
let descricao: string; //Filtra por descrição (case insensitive) (optional) (default to undefined)
let minhasTarefas: boolean; //Filtrar minhas tarefas (optional) (default to undefined)
let ordering: string; //Ordenar resultados (ex: -data_termino) (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let prioridade: string; //Filtrar por prioridade (separadas por vírgula) (optional) (default to undefined)
let projeto: number; //Filtrar por ID do projeto (optional) (default to undefined)
let responsavel: number; //Filtrar por ID do usuário responsável (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let semResponsavel: boolean; //Filtra tarefas sem responsáveis atribuídos (optional) (default to undefined)
let semSprint: boolean; //Filtrar tarefas sem sprint (optional) (default to undefined)
let sprint: number; //Filtrar por ID da sprint (optional) (default to undefined)
let status: string; //Filtrar por status (separados por vírgula) (optional) (default to undefined)
let titulo: string; //Filtra por título (case insensitive) (optional) (default to undefined)

const { status, data } = await apiInstance.tasksTarefasList(
    atrasada,
    dataInicioAntesAfter,
    dataInicioAntesBefore,
    dataInicioAposAfter,
    dataInicioAposBefore,
    dataTerminoAntesAfter,
    dataTerminoAntesBefore,
    dataTerminoAposAfter,
    dataTerminoAposBefore,
    descricao,
    minhasTarefas,
    ordering,
    page,
    prioridade,
    projeto,
    responsavel,
    search,
    semResponsavel,
    semSprint,
    sprint,
    status,
    titulo
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **atrasada** | [**boolean**] | Filtrar tarefas atrasadas | (optional) defaults to undefined|
| **dataInicioAntesAfter** | [**string**] | Filtra tarefas com data de início antes da data especificada | (optional) defaults to undefined|
| **dataInicioAntesBefore** | [**string**] | Filtra tarefas com data de início antes da data especificada | (optional) defaults to undefined|
| **dataInicioAposAfter** | [**string**] | Filtra tarefas com data de início após a data especificada | (optional) defaults to undefined|
| **dataInicioAposBefore** | [**string**] | Filtra tarefas com data de início após a data especificada | (optional) defaults to undefined|
| **dataTerminoAntesAfter** | [**string**] | Filtra tarefas com data de término antes da data especificada | (optional) defaults to undefined|
| **dataTerminoAntesBefore** | [**string**] | Filtra tarefas com data de término antes da data especificada | (optional) defaults to undefined|
| **dataTerminoAposAfter** | [**string**] | Filtra tarefas com data de término após a data especificada | (optional) defaults to undefined|
| **dataTerminoAposBefore** | [**string**] | Filtra tarefas com data de término após a data especificada | (optional) defaults to undefined|
| **descricao** | [**string**] | Filtra por descrição (case insensitive) | (optional) defaults to undefined|
| **minhasTarefas** | [**boolean**] | Filtrar minhas tarefas | (optional) defaults to undefined|
| **ordering** | [**string**] | Ordenar resultados (ex: -data_termino) | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **prioridade** | [**string**] | Filtrar por prioridade (separadas por vírgula) | (optional) defaults to undefined|
| **projeto** | [**number**] | Filtrar por ID do projeto | (optional) defaults to undefined|
| **responsavel** | [**number**] | Filtrar por ID do usuário responsável | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **semResponsavel** | [**boolean**] | Filtra tarefas sem responsáveis atribuídos | (optional) defaults to undefined|
| **semSprint** | [**boolean**] | Filtrar tarefas sem sprint | (optional) defaults to undefined|
| **sprint** | [**number**] | Filtrar por ID da sprint | (optional) defaults to undefined|
| **status** | [**string**] | Filtrar por status (separados por vírgula) | (optional) defaults to undefined|
| **titulo** | [**string**] | Filtra por título (case insensitive) | (optional) defaults to undefined|


### Return type

**PaginatedTarefaListList**

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

# **tasksTarefasPartialUpdate**
> Tarefa tasksTarefasPartialUpdate()

Atualiza parcialmente os campos de uma tarefa existente.

### Example

```typescript
import {
    TarefasApi,
    Configuration,
    PatchedTarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new TarefasApi(configuration);

let id: number; //A unique integer value identifying this Tarefa. (default to undefined)
let patchedTarefaRequest: PatchedTarefaRequest; // (optional)

const { status, data } = await apiInstance.tasksTarefasPartialUpdate(
    id,
    patchedTarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedTarefaRequest** | **PatchedTarefaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Tarefa. | defaults to undefined|


### Return type

**Tarefa**

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

# **tasksTarefasRetrieve**
> Tarefa tasksTarefasRetrieve()

Retorna informações detalhadas de uma tarefa específica.

### Example

```typescript
import {
    TarefasApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new TarefasApi(configuration);

let id: number; //A unique integer value identifying this Tarefa. (default to undefined)

const { status, data } = await apiInstance.tasksTarefasRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Tarefa. | defaults to undefined|


### Return type

**Tarefa**

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

# **tasksTarefasUpdate**
> Tarefa tasksTarefasUpdate(tarefaRequest)

Atualiza todos os campos de uma tarefa existente.

### Example

```typescript
import {
    TarefasApi,
    Configuration,
    TarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new TarefasApi(configuration);

let id: number; //A unique integer value identifying this Tarefa. (default to undefined)
let tarefaRequest: TarefaRequest; //

const { status, data } = await apiInstance.tasksTarefasUpdate(
    id,
    tarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tarefaRequest** | **TarefaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Tarefa. | defaults to undefined|


### Return type

**Tarefa**

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

