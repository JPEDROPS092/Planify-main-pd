# ProjetosApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**projectsAdicionarMembroCreate**](#projectsadicionarmembrocreate) | **POST** /api/projects/{id}/adicionar_membro/ | Adicionar membro ao projeto|
|[**projectsArchiveCreate**](#projectsarchivecreate) | **POST** /api/projects/{id}/archive/ | Arquivar projeto|
|[**projectsCreate**](#projectscreate) | **POST** /api/projects/ | Criar novo projeto|
|[**projectsCriarSprintCreate**](#projectscriarsprintcreate) | **POST** /api/projects/{id}/criar_sprint/ | Criar Sprint no projeto|
|[**projectsDashboardRetrieve**](#projectsdashboardretrieve) | **GET** /api/projects/{projeto_id}/dashboard/ | Dashboard do projeto|
|[**projectsDestroy**](#projectsdestroy) | **DELETE** /api/projects/{id}/ | Excluir projeto|
|[**projectsExportProjectRetrieve**](#projectsexportprojectretrieve) | **GET** /api/projects/{id}/export_project/ | Exportar dados do projeto|
|[**projectsExportarRetrieve**](#projectsexportarretrieve) | **GET** /api/projects/{projeto_id}/exportar/ | Exportar dados do projeto|
|[**projectsGanttRetrieve**](#projectsganttretrieve) | **GET** /api/projects/{projeto_id}/gantt/ | Visualização Gantt do projeto|
|[**projectsHistoricoStatusRetrieve**](#projectshistoricostatusretrieve) | **GET** /api/projects/{id}/historico_status/ | Histórico de status do projeto|
|[**projectsKanbanPartialUpdate**](#projectskanbanpartialupdate) | **PATCH** /api/projects/{projeto_id}/kanban/ | Atualizar Kanban do projeto|
|[**projectsKanbanRetrieve**](#projectskanbanretrieve) | **GET** /api/projects/{projeto_id}/kanban/ | Visualização Kanban do projeto|
|[**projectsList**](#projectslist) | **GET** /api/projects/ | Listar projetos|
|[**projectsListarMembrosList**](#projectslistarmembroslist) | **GET** /api/projects/{id}/listar_membros/ | Listar membros do projeto|
|[**projectsMetricsRetrieve**](#projectsmetricsretrieve) | **GET** /api/projects/{id}/metrics/ | Métricas Detalhadas do Projeto|
|[**projectsMyProjectsList**](#projectsmyprojectslist) | **GET** /api/projects/my_projects/ | Listar meus projetos|
|[**projectsPartialUpdate**](#projectspartialupdate) | **PATCH** /api/projects/{id}/ | Atualizar projeto parcialmente|
|[**projectsRemoverMembroDestroy**](#projectsremovermembrodestroy) | **DELETE** /api/projects/{id}/remover_membro/ | Remover membro do projeto|
|[**projectsRetrieve**](#projectsretrieve) | **GET** /api/projects/{id}/ | Obter detalhes do projeto|
|[**projectsSprintsRetrieve**](#projectssprintsretrieve) | **GET** /api/projects/{id}/sprints/ | Sprints do projeto|
|[**projectsTarefasCriarCreate**](#projectstarefascriarcreate) | **POST** /api/projects/{projeto_id}/tarefas/criar/ | Criar tarefa no projeto|
|[**projectsTarefasCriarMultiplasCreate**](#projectstarefascriarmultiplascreate) | **POST** /api/projects/{projeto_id}/tarefas/criar-multiplas/ | Criar múltiplas tarefas no projeto|
|[**projectsUpdate**](#projectsupdate) | **PUT** /api/projects/{id}/ | Atualizar projeto|

# **projectsAdicionarMembroCreate**
> MembroProjeto projectsAdicionarMembroCreate(membroProjetoRequest)

Adiciona um novo membro ao projeto com o papel especificado.

### Example

```typescript
import {
    ProjetosApi,
    Configuration,
    MembroProjetoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)
let membroProjetoRequest: MembroProjetoRequest; //

const { status, data } = await apiInstance.projectsAdicionarMembroCreate(
    id,
    membroProjetoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **membroProjetoRequest** | **MembroProjetoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|


### Return type

**MembroProjeto**

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

# **projectsArchiveCreate**
> { [key: string]: any; } projectsArchiveCreate(projetoRequest)

Arquiva ou desarquiva um projeto.

### Example

```typescript
import {
    ProjetosApi,
    Configuration,
    ProjetoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)
let projetoRequest: ProjetoRequest; //

const { status, data } = await apiInstance.projectsArchiveCreate(
    id,
    projetoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projetoRequest** | **ProjetoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|


### Return type

**{ [key: string]: any; }**

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

# **projectsCreate**
> Projeto projectsCreate(projetoRequest)

Cria um novo projeto.

### Example

```typescript
import {
    ProjetosApi,
    Configuration,
    ProjetoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let projetoRequest: ProjetoRequest; //

const { status, data } = await apiInstance.projectsCreate(
    projetoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projetoRequest** | **ProjetoRequest**|  | |


### Return type

**Projeto**

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

# **projectsCriarSprintCreate**
> Projeto projectsCriarSprintCreate(projetoRequest)

Cria uma nova sprint para um projeto.

### Example

```typescript
import {
    ProjetosApi,
    Configuration,
    ProjetoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)
let projetoRequest: ProjetoRequest; //

const { status, data } = await apiInstance.projectsCriarSprintCreate(
    id,
    projetoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projetoRequest** | **ProjetoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|


### Return type

**Projeto**

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

# **projectsDashboardRetrieve**
> ProjetoDashboardResponse projectsDashboardRetrieve()

Fornece dados para o dashboard de um projeto específico, incluindo visualizações Kanban e Gantt

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let projetoId: number; // (default to undefined)
let projetoId2: number; //ID do projeto (default to undefined)

const { status, data } = await apiInstance.projectsDashboardRetrieve(
    projetoId,
    projetoId2
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projetoId** | [**number**] |  | defaults to undefined|
| **projetoId2** | [**number**] | ID do projeto | defaults to undefined|


### Return type

**ProjetoDashboardResponse**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**403** |  |  -  |
|**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projectsDestroy**
> projectsDestroy()

Remove um projeto existente.

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)

const { status, data } = await apiInstance.projectsDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|


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

# **projectsExportProjectRetrieve**
> Projeto projectsExportProjectRetrieve()

Exporta os dados do projeto.

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)

const { status, data } = await apiInstance.projectsExportProjectRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|


### Return type

**Projeto**

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

# **projectsExportarRetrieve**
> File projectsExportarRetrieve()

Exporta dados detalhados de um projeto específico em formatos CSV ou JSON. O usuário deve ser membro do projeto ou um administrador para acessá-lo. É possível selecionar diferentes seções de dados para incluir na exportação, como informações básicas do projeto, lista de tarefas, equipe, riscos e custos.

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let projetoId: number; //ID do projeto a ser exportado. (default to undefined)
let format: string; //Formato de exportação desejado. Opções: \"csv\" ou \"json\". (optional) (default to 'csv')
let includeCosts: boolean; //Define se os custos associados ao projeto devem ser incluídos. (optional) (default to false)
let includeProject: boolean; //Define se os dados básicos do projeto devem ser incluídos. (optional) (default to true)
let includeRisks: boolean; //Define se os riscos associados ao projeto devem ser incluídos. (optional) (default to false)
let includeTasks: boolean; //Define se as tarefas (incluindo dados para Kanban e Gantt) do projeto devem ser incluídas. (optional) (default to true)
let includeTeam: boolean; //Define se os dados da equipe do projeto devem ser incluídos. (optional) (default to false)

const { status, data } = await apiInstance.projectsExportarRetrieve(
    projetoId,
    format,
    includeCosts,
    includeProject,
    includeRisks,
    includeTasks,
    includeTeam
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projetoId** | [**number**] | ID do projeto a ser exportado. | defaults to undefined|
| **format** | [**string**] | Formato de exportação desejado. Opções: \&quot;csv\&quot; ou \&quot;json\&quot;. | (optional) defaults to 'csv'|
| **includeCosts** | [**boolean**] | Define se os custos associados ao projeto devem ser incluídos. | (optional) defaults to false|
| **includeProject** | [**boolean**] | Define se os dados básicos do projeto devem ser incluídos. | (optional) defaults to true|
| **includeRisks** | [**boolean**] | Define se os riscos associados ao projeto devem ser incluídos. | (optional) defaults to false|
| **includeTasks** | [**boolean**] | Define se as tarefas (incluindo dados para Kanban e Gantt) do projeto devem ser incluídas. | (optional) defaults to true|
| **includeTeam** | [**boolean**] | Define se os dados da equipe do projeto devem ser incluídos. | (optional) defaults to false|


### Return type

**File**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**400** |  |  -  |
|**403** |  |  -  |
|**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projectsGanttRetrieve**
> GanttResponse projectsGanttRetrieve()

Fornece dados para a visualização Gantt de um projeto, com tarefas e suas dependências

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let projetoId: number; // (default to undefined)
let projetoId2: number; //ID do projeto (default to undefined)

const { status, data } = await apiInstance.projectsGanttRetrieve(
    projetoId,
    projetoId2
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projetoId** | [**number**] |  | defaults to undefined|
| **projetoId2** | [**number**] | ID do projeto | defaults to undefined|


### Return type

**GanttResponse**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**403** |  |  -  |
|**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projectsHistoricoStatusRetrieve**
> Projeto projectsHistoricoStatusRetrieve()

Visualizar o histórico de mudanças de status do projeto.

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)

const { status, data } = await apiInstance.projectsHistoricoStatusRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|


### Return type

**Projeto**

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

# **projectsKanbanPartialUpdate**
> KanbanResponse projectsKanbanPartialUpdate()

Atualiza os quadro Kanban de um projeto existente.

### Example

```typescript
import {
    ProjetosApi,
    Configuration,
    PatchedKanbanResponseRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let projetoId: number; // (default to undefined)
let patchedKanbanResponseRequest: PatchedKanbanResponseRequest; // (optional)

const { status, data } = await apiInstance.projectsKanbanPartialUpdate(
    projetoId,
    patchedKanbanResponseRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedKanbanResponseRequest** | **PatchedKanbanResponseRequest**|  | |
| **projetoId** | [**number**] |  | defaults to undefined|


### Return type

**KanbanResponse**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**403** |  |  -  |
|**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projectsKanbanRetrieve**
> KanbanResponse projectsKanbanRetrieve()

Fornece dados para a visualização Kanban de um projeto, com tarefas agrupadas por status

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let projetoId: number; // (default to undefined)

const { status, data } = await apiInstance.projectsKanbanRetrieve(
    projetoId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projetoId** | [**number**] |  | defaults to undefined|


### Return type

**KanbanResponse**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**403** |  |  -  |
|**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projectsList**
> PaginatedProjetoListList projectsList()

Retorna uma lista paginada de projetos.

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let arquivado: boolean; // (optional) (default to undefined)
let atrasado: boolean; //Filtra projetos atrasados (data_fim < hoje e status != CONCLUIDO) (optional) (default to undefined)
let dataFimAntesAfter: string; //Filtra projetos com data de fim antes da data especificada (optional) (default to undefined)
let dataFimAntesBefore: string; //Filtra projetos com data de fim antes da data especificada (optional) (default to undefined)
let dataFimAposAfter: string; //Filtra projetos com data de fim após a data especificada (optional) (default to undefined)
let dataFimAposBefore: string; //Filtra projetos com data de fim após a data especificada (optional) (default to undefined)
let dataInicioAntesAfter: string; //Filtra projetos com data de início antes da data especificada (optional) (default to undefined)
let dataInicioAntesBefore: string; //Filtra projetos com data de início antes da data especificada (optional) (default to undefined)
let dataInicioAposAfter: string; //Filtra projetos com data de início após a data especificada (optional) (default to undefined)
let dataInicioAposBefore: string; //Filtra projetos com data de início após a data especificada (optional) (default to undefined)
let descricao: string; //Filtra por descrição (case insensitive) (optional) (default to undefined)
let membro: string; //Filtra projetos que contenham o membro especificado (ID do usuário) (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let prioridade: string; //Filtra por prioridade (pode ser múltiplas, separadas por vírgula) (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let status: string; //Filtra por status (pode ser múltiplos, separados por vírgula) (optional) (default to undefined)
let titulo: string; //Filtra por título (case insensitive) (optional) (default to undefined)

const { status, data } = await apiInstance.projectsList(
    arquivado,
    atrasado,
    dataFimAntesAfter,
    dataFimAntesBefore,
    dataFimAposAfter,
    dataFimAposBefore,
    dataInicioAntesAfter,
    dataInicioAntesBefore,
    dataInicioAposAfter,
    dataInicioAposBefore,
    descricao,
    membro,
    ordering,
    page,
    prioridade,
    search,
    status,
    titulo
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **arquivado** | [**boolean**] |  | (optional) defaults to undefined|
| **atrasado** | [**boolean**] | Filtra projetos atrasados (data_fim &lt; hoje e status !&#x3D; CONCLUIDO) | (optional) defaults to undefined|
| **dataFimAntesAfter** | [**string**] | Filtra projetos com data de fim antes da data especificada | (optional) defaults to undefined|
| **dataFimAntesBefore** | [**string**] | Filtra projetos com data de fim antes da data especificada | (optional) defaults to undefined|
| **dataFimAposAfter** | [**string**] | Filtra projetos com data de fim após a data especificada | (optional) defaults to undefined|
| **dataFimAposBefore** | [**string**] | Filtra projetos com data de fim após a data especificada | (optional) defaults to undefined|
| **dataInicioAntesAfter** | [**string**] | Filtra projetos com data de início antes da data especificada | (optional) defaults to undefined|
| **dataInicioAntesBefore** | [**string**] | Filtra projetos com data de início antes da data especificada | (optional) defaults to undefined|
| **dataInicioAposAfter** | [**string**] | Filtra projetos com data de início após a data especificada | (optional) defaults to undefined|
| **dataInicioAposBefore** | [**string**] | Filtra projetos com data de início após a data especificada | (optional) defaults to undefined|
| **descricao** | [**string**] | Filtra por descrição (case insensitive) | (optional) defaults to undefined|
| **membro** | [**string**] | Filtra projetos que contenham o membro especificado (ID do usuário) | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **prioridade** | [**string**] | Filtra por prioridade (pode ser múltiplas, separadas por vírgula) | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **status** | [**string**] | Filtra por status (pode ser múltiplos, separados por vírgula) | (optional) defaults to undefined|
| **titulo** | [**string**] | Filtra por título (case insensitive) | (optional) defaults to undefined|


### Return type

**PaginatedProjetoListList**

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

# **projectsListarMembrosList**
> PaginatedMembroProjetoList projectsListarMembrosList()

Retorna todos os membros associados ao projeto.

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)
let arquivado: boolean; // (optional) (default to undefined)
let atrasado: boolean; //Filtra projetos atrasados (data_fim < hoje e status != CONCLUIDO) (optional) (default to undefined)
let dataFimAntesAfter: string; //Filtra projetos com data de fim antes da data especificada (optional) (default to undefined)
let dataFimAntesBefore: string; //Filtra projetos com data de fim antes da data especificada (optional) (default to undefined)
let dataFimAposAfter: string; //Filtra projetos com data de fim após a data especificada (optional) (default to undefined)
let dataFimAposBefore: string; //Filtra projetos com data de fim após a data especificada (optional) (default to undefined)
let dataInicioAntesAfter: string; //Filtra projetos com data de início antes da data especificada (optional) (default to undefined)
let dataInicioAntesBefore: string; //Filtra projetos com data de início antes da data especificada (optional) (default to undefined)
let dataInicioAposAfter: string; //Filtra projetos com data de início após a data especificada (optional) (default to undefined)
let dataInicioAposBefore: string; //Filtra projetos com data de início após a data especificada (optional) (default to undefined)
let descricao: string; //Filtra por descrição (case insensitive) (optional) (default to undefined)
let membro: string; //Filtra projetos que contenham o membro especificado (ID do usuário) (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let prioridade: string; //Filtra por prioridade (pode ser múltiplas, separadas por vírgula) (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let status: string; //Filtra por status (pode ser múltiplos, separados por vírgula) (optional) (default to undefined)
let titulo: string; //Filtra por título (case insensitive) (optional) (default to undefined)

const { status, data } = await apiInstance.projectsListarMembrosList(
    id,
    arquivado,
    atrasado,
    dataFimAntesAfter,
    dataFimAntesBefore,
    dataFimAposAfter,
    dataFimAposBefore,
    dataInicioAntesAfter,
    dataInicioAntesBefore,
    dataInicioAposAfter,
    dataInicioAposBefore,
    descricao,
    membro,
    ordering,
    page,
    prioridade,
    search,
    status,
    titulo
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|
| **arquivado** | [**boolean**] |  | (optional) defaults to undefined|
| **atrasado** | [**boolean**] | Filtra projetos atrasados (data_fim &lt; hoje e status !&#x3D; CONCLUIDO) | (optional) defaults to undefined|
| **dataFimAntesAfter** | [**string**] | Filtra projetos com data de fim antes da data especificada | (optional) defaults to undefined|
| **dataFimAntesBefore** | [**string**] | Filtra projetos com data de fim antes da data especificada | (optional) defaults to undefined|
| **dataFimAposAfter** | [**string**] | Filtra projetos com data de fim após a data especificada | (optional) defaults to undefined|
| **dataFimAposBefore** | [**string**] | Filtra projetos com data de fim após a data especificada | (optional) defaults to undefined|
| **dataInicioAntesAfter** | [**string**] | Filtra projetos com data de início antes da data especificada | (optional) defaults to undefined|
| **dataInicioAntesBefore** | [**string**] | Filtra projetos com data de início antes da data especificada | (optional) defaults to undefined|
| **dataInicioAposAfter** | [**string**] | Filtra projetos com data de início após a data especificada | (optional) defaults to undefined|
| **dataInicioAposBefore** | [**string**] | Filtra projetos com data de início após a data especificada | (optional) defaults to undefined|
| **descricao** | [**string**] | Filtra por descrição (case insensitive) | (optional) defaults to undefined|
| **membro** | [**string**] | Filtra projetos que contenham o membro especificado (ID do usuário) | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **prioridade** | [**string**] | Filtra por prioridade (pode ser múltiplas, separadas por vírgula) | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **status** | [**string**] | Filtra por status (pode ser múltiplos, separados por vírgula) | (optional) defaults to undefined|
| **titulo** | [**string**] | Filtra por título (case insensitive) | (optional) defaults to undefined|


### Return type

**PaginatedMembroProjetoList**

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

# **projectsMetricsRetrieve**
> { [key: string]: any; } projectsMetricsRetrieve()

Retorna métricas detalhadas sobre o projeto, incluindo progresso, custos, prazos e qualidade.

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)

const { status, data } = await apiInstance.projectsMetricsRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|


### Return type

**{ [key: string]: any; }**

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

# **projectsMyProjectsList**
> PaginatedProjetoList projectsMyProjectsList()

Retorna os projetos dos quais o usuário é membro.

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let arquivado: boolean; // (optional) (default to undefined)
let atrasado: boolean; //Filtra projetos atrasados (data_fim < hoje e status != CONCLUIDO) (optional) (default to undefined)
let dataFimAntesAfter: string; //Filtra projetos com data de fim antes da data especificada (optional) (default to undefined)
let dataFimAntesBefore: string; //Filtra projetos com data de fim antes da data especificada (optional) (default to undefined)
let dataFimAposAfter: string; //Filtra projetos com data de fim após a data especificada (optional) (default to undefined)
let dataFimAposBefore: string; //Filtra projetos com data de fim após a data especificada (optional) (default to undefined)
let dataInicioAntesAfter: string; //Filtra projetos com data de início antes da data especificada (optional) (default to undefined)
let dataInicioAntesBefore: string; //Filtra projetos com data de início antes da data especificada (optional) (default to undefined)
let dataInicioAposAfter: string; //Filtra projetos com data de início após a data especificada (optional) (default to undefined)
let dataInicioAposBefore: string; //Filtra projetos com data de início após a data especificada (optional) (default to undefined)
let descricao: string; //Filtra por descrição (case insensitive) (optional) (default to undefined)
let membro: string; //Filtra projetos que contenham o membro especificado (ID do usuário) (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let prioridade: string; //Filtra por prioridade (pode ser múltiplas, separadas por vírgula) (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let status: string; //Filtra por status (pode ser múltiplos, separados por vírgula) (optional) (default to undefined)
let titulo: string; //Filtra por título (case insensitive) (optional) (default to undefined)

const { status, data } = await apiInstance.projectsMyProjectsList(
    arquivado,
    atrasado,
    dataFimAntesAfter,
    dataFimAntesBefore,
    dataFimAposAfter,
    dataFimAposBefore,
    dataInicioAntesAfter,
    dataInicioAntesBefore,
    dataInicioAposAfter,
    dataInicioAposBefore,
    descricao,
    membro,
    ordering,
    page,
    prioridade,
    search,
    status,
    titulo
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **arquivado** | [**boolean**] |  | (optional) defaults to undefined|
| **atrasado** | [**boolean**] | Filtra projetos atrasados (data_fim &lt; hoje e status !&#x3D; CONCLUIDO) | (optional) defaults to undefined|
| **dataFimAntesAfter** | [**string**] | Filtra projetos com data de fim antes da data especificada | (optional) defaults to undefined|
| **dataFimAntesBefore** | [**string**] | Filtra projetos com data de fim antes da data especificada | (optional) defaults to undefined|
| **dataFimAposAfter** | [**string**] | Filtra projetos com data de fim após a data especificada | (optional) defaults to undefined|
| **dataFimAposBefore** | [**string**] | Filtra projetos com data de fim após a data especificada | (optional) defaults to undefined|
| **dataInicioAntesAfter** | [**string**] | Filtra projetos com data de início antes da data especificada | (optional) defaults to undefined|
| **dataInicioAntesBefore** | [**string**] | Filtra projetos com data de início antes da data especificada | (optional) defaults to undefined|
| **dataInicioAposAfter** | [**string**] | Filtra projetos com data de início após a data especificada | (optional) defaults to undefined|
| **dataInicioAposBefore** | [**string**] | Filtra projetos com data de início após a data especificada | (optional) defaults to undefined|
| **descricao** | [**string**] | Filtra por descrição (case insensitive) | (optional) defaults to undefined|
| **membro** | [**string**] | Filtra projetos que contenham o membro especificado (ID do usuário) | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **prioridade** | [**string**] | Filtra por prioridade (pode ser múltiplas, separadas por vírgula) | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **status** | [**string**] | Filtra por status (pode ser múltiplos, separados por vírgula) | (optional) defaults to undefined|
| **titulo** | [**string**] | Filtra por título (case insensitive) | (optional) defaults to undefined|


### Return type

**PaginatedProjetoList**

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

# **projectsPartialUpdate**
> Projeto projectsPartialUpdate()

Atualiza parcialmente um projeto existente.

### Example

```typescript
import {
    ProjetosApi,
    Configuration,
    PatchedProjetoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)
let patchedProjetoRequest: PatchedProjetoRequest; // (optional)

const { status, data } = await apiInstance.projectsPartialUpdate(
    id,
    patchedProjetoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedProjetoRequest** | **PatchedProjetoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|


### Return type

**Projeto**

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

# **projectsRemoverMembroDestroy**
> projectsRemoverMembroDestroy()

Remove um membro do projeto pelo ID.

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)
let membroId: number; //ID do membro a ser removido (default to undefined)

const { status, data } = await apiInstance.projectsRemoverMembroDestroy(
    id,
    membroId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|
| **membroId** | [**number**] | ID do membro a ser removido | defaults to undefined|


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

# **projectsRetrieve**
> Projeto projectsRetrieve()

Retorna informações detalhadas de um projeto específico.

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)

const { status, data } = await apiInstance.projectsRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|


### Return type

**Projeto**

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

# **projectsSprintsRetrieve**
> Projeto projectsSprintsRetrieve()

Listar sprints do projeto.

### Example

```typescript
import {
    ProjetosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)

const { status, data } = await apiInstance.projectsSprintsRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|


### Return type

**Projeto**

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

# **projectsTarefasCriarCreate**
> Tarefa projectsTarefasCriarCreate(tarefaCreateRequest)

Cria uma nova tarefa no contexto de um projeto específico

### Example

```typescript
import {
    ProjetosApi,
    Configuration,
    TarefaCreateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let projetoId: number; // (default to undefined)
let projetoId2: number; //ID do projeto (default to undefined)
let tarefaCreateRequest: TarefaCreateRequest; //

const { status, data } = await apiInstance.projectsTarefasCriarCreate(
    projetoId,
    projetoId2,
    tarefaCreateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tarefaCreateRequest** | **TarefaCreateRequest**|  | |
| **projetoId** | [**number**] |  | defaults to undefined|
| **projetoId2** | [**number**] | ID do projeto | defaults to undefined|


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
|**400** |  |  -  |
|**403** |  |  -  |
|**404** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projectsTarefasCriarMultiplasCreate**
> { [key: string]: any; } projectsTarefasCriarMultiplasCreate(tarefasBulkCreateRequest)

Cria múltiplas tarefas em lote no contexto de um projeto específico

### Example

```typescript
import {
    ProjetosApi,
    Configuration,
    TarefasBulkCreateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let projetoId: number; // (default to undefined)
let projetoId2: number; //ID do projeto (default to undefined)
let tarefasBulkCreateRequest: TarefasBulkCreateRequest; //

const { status, data } = await apiInstance.projectsTarefasCriarMultiplasCreate(
    projetoId,
    projetoId2,
    tarefasBulkCreateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tarefasBulkCreateRequest** | **TarefasBulkCreateRequest**|  | |
| **projetoId** | [**number**] |  | defaults to undefined|
| **projetoId2** | [**number**] | ID do projeto | defaults to undefined|


### Return type

**{ [key: string]: any; }**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |
|**207** | Criação parcial - algumas tarefas foram criadas com sucesso, outras falharam |  -  |
|**400** |  |  -  |
|**403** |  |  -  |
|**404** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **projectsUpdate**
> Projeto projectsUpdate(projetoRequest)

Atualiza todos os campos de um projeto existente.

### Example

```typescript
import {
    ProjetosApi,
    Configuration,
    ProjetoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProjetosApi(configuration);

let id: number; //A unique integer value identifying this Projeto. (default to undefined)
let projetoRequest: ProjetoRequest; //

const { status, data } = await apiInstance.projectsUpdate(
    id,
    projetoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **projetoRequest** | **ProjetoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Projeto. | defaults to undefined|


### Return type

**Projeto**

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

