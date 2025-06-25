# CustoApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**costsAlertasCreate**](#costsalertascreate) | **POST** /api/costs/alertas/ | Criar nova alerta|
|[**costsAlertasDestroy**](#costsalertasdestroy) | **DELETE** /api/costs/alertas/{id}/ | Excluir alerta|
|[**costsAlertasIgnorarCreate**](#costsalertasignorarcreate) | **POST** /api/costs/alertas/{id}/ignorar/ | Marcar alertas como ignorado|
|[**costsAlertasList**](#costsalertaslist) | **GET** /api/costs/alertas/ | Listar alertas|
|[**costsAlertasPartialUpdate**](#costsalertaspartialupdate) | **PATCH** /api/costs/alertas/{id}/ | Atualizar alerta parcialmente|
|[**costsAlertasPendentesRetrieve**](#costsalertaspendentesretrieve) | **GET** /api/costs/alertas/pendentes/ | Listar alertas com status ATIVO|
|[**costsAlertasResolverCreate**](#costsalertasresolvercreate) | **POST** /api/costs/alertas/{id}/resolver/ | Marcar alertas como resolvido|
|[**costsAlertasRetrieve**](#costsalertasretrieve) | **GET** /api/costs/alertas/{id}/ | Obter detalhes da alerta|
|[**costsAlertasUpdate**](#costsalertasupdate) | **PUT** /api/costs/alertas/{id}/ | Atualizar alerta|
|[**costsCategoriasCreate**](#costscategoriascreate) | **POST** /api/costs/categorias/ | Criar nova categoria|
|[**costsCategoriasDestroy**](#costscategoriasdestroy) | **DELETE** /api/costs/categorias/{id}/ | Excluir categoria|
|[**costsCategoriasList**](#costscategoriaslist) | **GET** /api/costs/categorias/ | Listar categorias|
|[**costsCategoriasPartialUpdate**](#costscategoriaspartialupdate) | **PATCH** /api/costs/categorias/{id}/ | Atualizar categoria parcialmente|
|[**costsCategoriasRetrieve**](#costscategoriasretrieve) | **GET** /api/costs/categorias/{id}/ | Obter detalhes da categoria|
|[**costsCategoriasUpdate**](#costscategoriasupdate) | **PUT** /api/costs/categorias/{id}/ | Atualizar categoria|
|[**costsCustosCreate**](#costscustoscreate) | **POST** /api/costs/custos/ | Criar novo custo|
|[**costsCustosDashboardRetrieve**](#costscustosdashboardretrieve) | **GET** /api/costs/custos/dashboard/ | Dashboard financeiro|
|[**costsCustosDestroy**](#costscustosdestroy) | **DELETE** /api/costs/custos/{id}/ | Excluir custo|
|[**costsCustosList**](#costscustoslist) | **GET** /api/costs/custos/ | Listar custos|
|[**costsCustosPartialUpdate**](#costscustospartialupdate) | **PATCH** /api/costs/custos/{id}/ | Atualizar custo parcialmente|
|[**costsCustosRelatorioMensalRetrieve**](#costscustosrelatoriomensalretrieve) | **GET** /api/costs/custos/relatorio_mensal/ | Relatório de gastos mensais|
|[**costsCustosRelatorioPorCategoriaRetrieve**](#costscustosrelatorioporcategoriaretrieve) | **GET** /api/costs/custos/relatorio_por_categoria/ | Relatório de gastos por categoria|
|[**costsCustosRelatorioPorProjetoRetrieve**](#costscustosrelatorioporprojetoretrieve) | **GET** /api/costs/custos/relatorio_por_projeto/ | Relatório de gastos por projeto|
|[**costsCustosRetrieve**](#costscustosretrieve) | **GET** /api/costs/custos/{id}/ | Obter detalhes do custo|
|[**costsCustosUpdate**](#costscustosupdate) | **PUT** /api/costs/custos/{id}/ | Atualizar custo|
|[**costsOrcamentosProjetoAjustarOrcamentoCreate**](#costsorcamentosprojetoajustarorcamentocreate) | **POST** /api/costs/orcamentos-projeto/{id}/ajustar_orcamento/ | Ajustar orçamento de um projeto|
|[**costsOrcamentosProjetoCreate**](#costsorcamentosprojetocreate) | **POST** /api/costs/orcamentos-projeto/ | Criar novo custo|
|[**costsOrcamentosProjetoDestroy**](#costsorcamentosprojetodestroy) | **DELETE** /api/costs/orcamentos-projeto/{id}/ | Excluir custo|
|[**costsOrcamentosProjetoList**](#costsorcamentosprojetolist) | **GET** /api/costs/orcamentos-projeto/ | Listar custos|
|[**costsOrcamentosProjetoPartialUpdate**](#costsorcamentosprojetopartialupdate) | **PATCH** /api/costs/orcamentos-projeto/{id}/ | Atualizar custo parcialmente|
|[**costsOrcamentosProjetoProjetosSemOrcamentoRetrieve**](#costsorcamentosprojetoprojetossemorcamentoretrieve) | **GET** /api/costs/orcamentos-projeto/projetos_sem_orcamento/ | Listar projetos sem orçamento definido|
|[**costsOrcamentosProjetoRetrieve**](#costsorcamentosprojetoretrieve) | **GET** /api/costs/orcamentos-projeto/{id}/ | Obter detalhes do custo|
|[**costsOrcamentosProjetoUpdate**](#costsorcamentosprojetoupdate) | **PUT** /api/costs/orcamentos-projeto/{id}/ | Atualizar custo|
|[**costsOrcamentosTarefaAjustarOrcamentoCreate**](#costsorcamentostarefaajustarorcamentocreate) | **POST** /api/costs/orcamentos-tarefa/{id}/ajustar_orcamento/ | Ajustar orçamento de uma tarefas|
|[**costsOrcamentosTarefaCreate**](#costsorcamentostarefacreate) | **POST** /api/costs/orcamentos-tarefa/ | Criar nova tarefa|
|[**costsOrcamentosTarefaDestroy**](#costsorcamentostarefadestroy) | **DELETE** /api/costs/orcamentos-tarefa/{id}/ | Excluir tarefa|
|[**costsOrcamentosTarefaList**](#costsorcamentostarefalist) | **GET** /api/costs/orcamentos-tarefa/ | Listar tarefas|
|[**costsOrcamentosTarefaPartialUpdate**](#costsorcamentostarefapartialupdate) | **PATCH** /api/costs/orcamentos-tarefa/{id}/ | Atualizar tarefa parcialmente|
|[**costsOrcamentosTarefaRetrieve**](#costsorcamentostarefaretrieve) | **GET** /api/costs/orcamentos-tarefa/{id}/ | Obter detalhes da tarefa|
|[**costsOrcamentosTarefaTarefasSemOrcamentoRetrieve**](#costsorcamentostarefatarefassemorcamentoretrieve) | **GET** /api/costs/orcamentos-tarefa/tarefas_sem_orcamento/ | Listar tarefas sem orçamento|
|[**costsOrcamentosTarefaUpdate**](#costsorcamentostarefaupdate) | **PUT** /api/costs/orcamentos-tarefa/{id}/ | Atualizar tarefa|

# **costsAlertasCreate**
> Alerta costsAlertasCreate(alertaRequest)

Cria uma novo alerta.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    AlertaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let alertaRequest: AlertaRequest; //

const { status, data } = await apiInstance.costsAlertasCreate(
    alertaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **alertaRequest** | **AlertaRequest**|  | |


### Return type

**Alerta**

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

# **costsAlertasDestroy**
> costsAlertasDestroy()

Remove uma alerta existente.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Alerta de Orçamento. (default to undefined)

const { status, data } = await apiInstance.costsAlertasDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Alerta de Orçamento. | defaults to undefined|


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

# **costsAlertasIgnorarCreate**
> costsAlertasIgnorarCreate(alertaRequest)

Marca um alerta como ignorado. Opcionalmente, pode incluir uma justificativa para ignorar o alerta.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    AlertaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Alerta de Orçamento. (default to undefined)
let alertaRequest: AlertaRequest; //

const { status, data } = await apiInstance.costsAlertasIgnorarCreate(
    id,
    alertaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **alertaRequest** | **AlertaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Alerta de Orçamento. | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **costsAlertasList**
> PaginatedAlertaList costsAlertasList()

Retorna uma lista paginada de alertas.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let projeto: number; // (optional) (default to undefined)
let status: 'ATIVO' | 'IGNORADO' | 'RESOLVIDO'; //* `ATIVO` - Ativo * `RESOLVIDO` - Resolvido * `IGNORADO` - Ignorado (optional) (default to undefined)
let tarefa: number; // (optional) (default to undefined)
let tipo: 'PROJETO' | 'TAREFA'; //* `PROJETO` - Projeto * `TAREFA` - Tarefa (optional) (default to undefined)

const { status, data } = await apiInstance.costsAlertasList(
    ordering,
    page,
    projeto,
    status,
    tarefa,
    tipo
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **projeto** | [**number**] |  | (optional) defaults to undefined|
| **status** | [**&#39;ATIVO&#39; | &#39;IGNORADO&#39; | &#39;RESOLVIDO&#39;**]**Array<&#39;ATIVO&#39; &#124; &#39;IGNORADO&#39; &#124; &#39;RESOLVIDO&#39;>** | * &#x60;ATIVO&#x60; - Ativo * &#x60;RESOLVIDO&#x60; - Resolvido * &#x60;IGNORADO&#x60; - Ignorado | (optional) defaults to undefined|
| **tarefa** | [**number**] |  | (optional) defaults to undefined|
| **tipo** | [**&#39;PROJETO&#39; | &#39;TAREFA&#39;**]**Array<&#39;PROJETO&#39; &#124; &#39;TAREFA&#39;>** | * &#x60;PROJETO&#x60; - Projeto * &#x60;TAREFA&#x60; - Tarefa | (optional) defaults to undefined|


### Return type

**PaginatedAlertaList**

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

# **costsAlertasPartialUpdate**
> Alerta costsAlertasPartialUpdate()

Atualiza parcialmente uma alerta existente.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    PatchedAlertaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Alerta de Orçamento. (default to undefined)
let patchedAlertaRequest: PatchedAlertaRequest; // (optional)

const { status, data } = await apiInstance.costsAlertasPartialUpdate(
    id,
    patchedAlertaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedAlertaRequest** | **PatchedAlertaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Alerta de Orçamento. | defaults to undefined|


### Return type

**Alerta**

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

# **costsAlertasPendentesRetrieve**
> costsAlertasPendentesRetrieve()

Retorna apenas os alertas pendentes (status ATIVO). Permite filtrar por projeto, tarefa e tipo.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

const { status, data } = await apiInstance.costsAlertasPendentesRetrieve();
```

### Parameters
This endpoint does not have any parameters.


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
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **costsAlertasResolverCreate**
> costsAlertasResolverCreate(alertaRequest)

Marca um alerta como resolvido. Opcionalmente, pode incluir uma observação sobre a resolução.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    AlertaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Alerta de Orçamento. (default to undefined)
let alertaRequest: AlertaRequest; //

const { status, data } = await apiInstance.costsAlertasResolverCreate(
    id,
    alertaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **alertaRequest** | **AlertaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Alerta de Orçamento. | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **costsAlertasRetrieve**
> Alerta costsAlertasRetrieve()

Retorna informações detalhadas de uma alerta específica.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Alerta de Orçamento. (default to undefined)

const { status, data } = await apiInstance.costsAlertasRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Alerta de Orçamento. | defaults to undefined|


### Return type

**Alerta**

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

# **costsAlertasUpdate**
> Alerta costsAlertasUpdate(alertaRequest)

Atualiza todos os campos de uma alerta existente.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    AlertaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Alerta de Orçamento. (default to undefined)
let alertaRequest: AlertaRequest; //

const { status, data } = await apiInstance.costsAlertasUpdate(
    id,
    alertaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **alertaRequest** | **AlertaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Alerta de Orçamento. | defaults to undefined|


### Return type

**Alerta**

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

# **costsCategoriasCreate**
> Categoria costsCategoriasCreate(categoriaRequest)

Cria uma novo categoria.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    CategoriaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let categoriaRequest: CategoriaRequest; //

const { status, data } = await apiInstance.costsCategoriasCreate(
    categoriaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **categoriaRequest** | **CategoriaRequest**|  | |


### Return type

**Categoria**

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

# **costsCategoriasDestroy**
> costsCategoriasDestroy()

Remove uma categoria existente.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Categoria. (default to undefined)

const { status, data } = await apiInstance.costsCategoriasDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Categoria. | defaults to undefined|


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

# **costsCategoriasList**
> PaginatedCategoriaList costsCategoriasList()

Retorna uma lista paginada de categorias.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)

const { status, data } = await apiInstance.costsCategoriasList(
    ordering,
    page,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|


### Return type

**PaginatedCategoriaList**

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

# **costsCategoriasPartialUpdate**
> Categoria costsCategoriasPartialUpdate()

Atualiza parcialmente uma categoria existente.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    PatchedCategoriaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Categoria. (default to undefined)
let patchedCategoriaRequest: PatchedCategoriaRequest; // (optional)

const { status, data } = await apiInstance.costsCategoriasPartialUpdate(
    id,
    patchedCategoriaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedCategoriaRequest** | **PatchedCategoriaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Categoria. | defaults to undefined|


### Return type

**Categoria**

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

# **costsCategoriasRetrieve**
> Categoria costsCategoriasRetrieve()

Retorna informações detalhadas de uma categoria específica.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Categoria. (default to undefined)

const { status, data } = await apiInstance.costsCategoriasRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Categoria. | defaults to undefined|


### Return type

**Categoria**

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

# **costsCategoriasUpdate**
> Categoria costsCategoriasUpdate(categoriaRequest)

Atualiza todos os campos de uma categoria existente.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    CategoriaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Categoria. (default to undefined)
let categoriaRequest: CategoriaRequest; //

const { status, data } = await apiInstance.costsCategoriasUpdate(
    id,
    categoriaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **categoriaRequest** | **CategoriaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Categoria. | defaults to undefined|


### Return type

**Categoria**

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

# **costsCustosCreate**
> Custo costsCustosCreate(custoRequest)

Cria um novo custo.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    CustoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let custoRequest: CustoRequest; //

const { status, data } = await apiInstance.costsCustosCreate(
    custoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **custoRequest** | **CustoRequest**|  | |


### Return type

**Custo**

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

# **costsCustosDashboardRetrieve**
> costsCustosDashboardRetrieve()

Endpoint para dashboard financeiro: retorna dados resumidos de custos. Inclui total gasto, gasto mensal, top categorias e alertas recentes.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

const { status, data } = await apiInstance.costsCustosDashboardRetrieve();
```

### Parameters
This endpoint does not have any parameters.


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
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **costsCustosDestroy**
> costsCustosDestroy()

Remove um custo existente.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Custo. (default to undefined)

const { status, data } = await apiInstance.costsCustosDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Custo. | defaults to undefined|


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

# **costsCustosList**
> PaginatedCustoListList costsCustosList()

Retorna uma lista paginada de custos.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let categoria: number; // (optional) (default to undefined)
let data: string; // (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let projeto: number; // (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let tarefa: number; // (optional) (default to undefined)
let tipo: 'FIXO' | 'RECORRENTE' | 'VARIAVEL'; //* `FIXO` - Custo Fixo * `VARIAVEL` - Custo Variável * `RECORRENTE` - Custo Recorrente (optional) (default to undefined)

const { status, data } = await apiInstance.costsCustosList(
    categoria,
    data,
    ordering,
    page,
    projeto,
    search,
    tarefa,
    tipo
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **categoria** | [**number**] |  | (optional) defaults to undefined|
| **data** | [**string**] |  | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **projeto** | [**number**] |  | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **tarefa** | [**number**] |  | (optional) defaults to undefined|
| **tipo** | [**&#39;FIXO&#39; | &#39;RECORRENTE&#39; | &#39;VARIAVEL&#39;**]**Array<&#39;FIXO&#39; &#124; &#39;RECORRENTE&#39; &#124; &#39;VARIAVEL&#39;>** | * &#x60;FIXO&#x60; - Custo Fixo * &#x60;VARIAVEL&#x60; - Custo Variável * &#x60;RECORRENTE&#x60; - Custo Recorrente | (optional) defaults to undefined|


### Return type

**PaginatedCustoListList**

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

# **costsCustosPartialUpdate**
> Custo costsCustosPartialUpdate()

Atualiza parcialmente um custo existente.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    PatchedCustoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Custo. (default to undefined)
let patchedCustoRequest: PatchedCustoRequest; // (optional)

const { status, data } = await apiInstance.costsCustosPartialUpdate(
    id,
    patchedCustoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedCustoRequest** | **PatchedCustoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Custo. | defaults to undefined|


### Return type

**Custo**

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

# **costsCustosRelatorioMensalRetrieve**
> costsCustosRelatorioMensalRetrieve()

Gera um relatório de gastos mensais para análise de tendências. Agrupa os custos por mês e retorna série temporal.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

const { status, data } = await apiInstance.costsCustosRelatorioMensalRetrieve();
```

### Parameters
This endpoint does not have any parameters.


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
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **costsCustosRelatorioPorCategoriaRetrieve**
> costsCustosRelatorioPorCategoriaRetrieve()

Gera um relatório de gastos por categoria. Utiliza anotações para calcular percentuais diretamente no banco de dados.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

const { status, data } = await apiInstance.costsCustosRelatorioPorCategoriaRetrieve();
```

### Parameters
This endpoint does not have any parameters.


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
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **costsCustosRelatorioPorProjetoRetrieve**
> costsCustosRelatorioPorProjetoRetrieve()

Gera um relatório de gastos por projeto.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

const { status, data } = await apiInstance.costsCustosRelatorioPorProjetoRetrieve();
```

### Parameters
This endpoint does not have any parameters.


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
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **costsCustosRetrieve**
> Custo costsCustosRetrieve()

Retorna informações detalhadas de um custo específico.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Custo. (default to undefined)

const { status, data } = await apiInstance.costsCustosRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Custo. | defaults to undefined|


### Return type

**Custo**

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

# **costsCustosUpdate**
> Custo costsCustosUpdate(custoRequest)

Atualiza todos os campos de um custo existente.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    CustoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Custo. (default to undefined)
let custoRequest: CustoRequest; //

const { status, data } = await apiInstance.costsCustosUpdate(
    id,
    custoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **custoRequest** | **CustoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Custo. | defaults to undefined|


### Return type

**Custo**

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

# **costsOrcamentosProjetoAjustarOrcamentoCreate**
> costsOrcamentosProjetoAjustarOrcamentoCreate(orcamentoProjetoRequest)

Permite ajustar o orçamento de um projeto com justificativa. Mantém histórico da alteração no campo de observações.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    OrcamentoProjetoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Orçamento de Projeto. (default to undefined)
let orcamentoProjetoRequest: OrcamentoProjetoRequest; //

const { status, data } = await apiInstance.costsOrcamentosProjetoAjustarOrcamentoCreate(
    id,
    orcamentoProjetoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orcamentoProjetoRequest** | **OrcamentoProjetoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Orçamento de Projeto. | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **costsOrcamentosProjetoCreate**
> OrcamentoProjeto costsOrcamentosProjetoCreate(orcamentoProjetoRequest)

Cria um novo custo.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    OrcamentoProjetoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let orcamentoProjetoRequest: OrcamentoProjetoRequest; //

const { status, data } = await apiInstance.costsOrcamentosProjetoCreate(
    orcamentoProjetoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orcamentoProjetoRequest** | **OrcamentoProjetoRequest**|  | |


### Return type

**OrcamentoProjeto**

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

# **costsOrcamentosProjetoDestroy**
> costsOrcamentosProjetoDestroy()

Remove um custo existente.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Orçamento de Projeto. (default to undefined)

const { status, data } = await apiInstance.costsOrcamentosProjetoDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Orçamento de Projeto. | defaults to undefined|


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

# **costsOrcamentosProjetoList**
> PaginatedOrcamentoProjetoList costsOrcamentosProjetoList()

Retorna uma lista paginada de custos.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let projeto: number; // (optional) (default to undefined)

const { status, data } = await apiInstance.costsOrcamentosProjetoList(
    page,
    projeto
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **projeto** | [**number**] |  | (optional) defaults to undefined|


### Return type

**PaginatedOrcamentoProjetoList**

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

# **costsOrcamentosProjetoPartialUpdate**
> OrcamentoProjeto costsOrcamentosProjetoPartialUpdate()

Atualiza parcialmente um custo existente.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    PatchedOrcamentoProjetoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Orçamento de Projeto. (default to undefined)
let patchedOrcamentoProjetoRequest: PatchedOrcamentoProjetoRequest; // (optional)

const { status, data } = await apiInstance.costsOrcamentosProjetoPartialUpdate(
    id,
    patchedOrcamentoProjetoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedOrcamentoProjetoRequest** | **PatchedOrcamentoProjetoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Orçamento de Projeto. | defaults to undefined|


### Return type

**OrcamentoProjeto**

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

# **costsOrcamentosProjetoProjetosSemOrcamentoRetrieve**
> costsOrcamentosProjetoProjetosSemOrcamentoRetrieve()

Retorna a lista de projetos que ainda não possuem orçamento definido.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

const { status, data } = await apiInstance.costsOrcamentosProjetoProjetosSemOrcamentoRetrieve();
```

### Parameters
This endpoint does not have any parameters.


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
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **costsOrcamentosProjetoRetrieve**
> OrcamentoProjeto costsOrcamentosProjetoRetrieve()

Retorna informações detalhadas de um custo específico.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Orçamento de Projeto. (default to undefined)

const { status, data } = await apiInstance.costsOrcamentosProjetoRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Orçamento de Projeto. | defaults to undefined|


### Return type

**OrcamentoProjeto**

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

# **costsOrcamentosProjetoUpdate**
> OrcamentoProjeto costsOrcamentosProjetoUpdate(orcamentoProjetoRequest)

Atualiza todos os campos de um custo existente.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    OrcamentoProjetoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Orçamento de Projeto. (default to undefined)
let orcamentoProjetoRequest: OrcamentoProjetoRequest; //

const { status, data } = await apiInstance.costsOrcamentosProjetoUpdate(
    id,
    orcamentoProjetoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orcamentoProjetoRequest** | **OrcamentoProjetoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Orçamento de Projeto. | defaults to undefined|


### Return type

**OrcamentoProjeto**

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

# **costsOrcamentosTarefaAjustarOrcamentoCreate**
> costsOrcamentosTarefaAjustarOrcamentoCreate(orcamentoTarefaRequest)

Permite ajustar o orçamento de uma tarefa com justificativa. Mantém histórico da alteração no campo de observações.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    OrcamentoTarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Orçamento de Tarefa. (default to undefined)
let orcamentoTarefaRequest: OrcamentoTarefaRequest; //

const { status, data } = await apiInstance.costsOrcamentosTarefaAjustarOrcamentoCreate(
    id,
    orcamentoTarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orcamentoTarefaRequest** | **OrcamentoTarefaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Orçamento de Tarefa. | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **costsOrcamentosTarefaCreate**
> OrcamentoTarefa costsOrcamentosTarefaCreate(orcamentoTarefaRequest)

Cria uma novo tarefa.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    OrcamentoTarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let orcamentoTarefaRequest: OrcamentoTarefaRequest; //

const { status, data } = await apiInstance.costsOrcamentosTarefaCreate(
    orcamentoTarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orcamentoTarefaRequest** | **OrcamentoTarefaRequest**|  | |


### Return type

**OrcamentoTarefa**

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

# **costsOrcamentosTarefaDestroy**
> costsOrcamentosTarefaDestroy()

Remove uma tarefa existente.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Orçamento de Tarefa. (default to undefined)

const { status, data } = await apiInstance.costsOrcamentosTarefaDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Orçamento de Tarefa. | defaults to undefined|


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

# **costsOrcamentosTarefaList**
> PaginatedOrcamentoTarefaList costsOrcamentosTarefaList()

Retorna uma lista paginada de tarefas.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let tarefa: number; // (optional) (default to undefined)
let tarefaProjeto: number; // (optional) (default to undefined)

const { status, data } = await apiInstance.costsOrcamentosTarefaList(
    page,
    tarefa,
    tarefaProjeto
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **tarefa** | [**number**] |  | (optional) defaults to undefined|
| **tarefaProjeto** | [**number**] |  | (optional) defaults to undefined|


### Return type

**PaginatedOrcamentoTarefaList**

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

# **costsOrcamentosTarefaPartialUpdate**
> OrcamentoTarefa costsOrcamentosTarefaPartialUpdate()

Atualiza parcialmente uma tarefa existente.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    PatchedOrcamentoTarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Orçamento de Tarefa. (default to undefined)
let patchedOrcamentoTarefaRequest: PatchedOrcamentoTarefaRequest; // (optional)

const { status, data } = await apiInstance.costsOrcamentosTarefaPartialUpdate(
    id,
    patchedOrcamentoTarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedOrcamentoTarefaRequest** | **PatchedOrcamentoTarefaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Orçamento de Tarefa. | defaults to undefined|


### Return type

**OrcamentoTarefa**

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

# **costsOrcamentosTarefaRetrieve**
> OrcamentoTarefa costsOrcamentosTarefaRetrieve()

Retorna informações detalhadas de uma tarefa específica.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Orçamento de Tarefa. (default to undefined)

const { status, data } = await apiInstance.costsOrcamentosTarefaRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Orçamento de Tarefa. | defaults to undefined|


### Return type

**OrcamentoTarefa**

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

# **costsOrcamentosTarefaTarefasSemOrcamentoRetrieve**
> costsOrcamentosTarefaTarefasSemOrcamentoRetrieve()

Retorna a lista de tarefas que ainda não possuem orçamento definido.

### Example

```typescript
import {
    CustoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

const { status, data } = await apiInstance.costsOrcamentosTarefaTarefasSemOrcamentoRetrieve();
```

### Parameters
This endpoint does not have any parameters.


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
|**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **costsOrcamentosTarefaUpdate**
> OrcamentoTarefa costsOrcamentosTarefaUpdate(orcamentoTarefaRequest)

Atualiza todos os campos de uma tarefa existente.

### Example

```typescript
import {
    CustoApi,
    Configuration,
    OrcamentoTarefaRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new CustoApi(configuration);

let id: number; //A unique integer value identifying this Orçamento de Tarefa. (default to undefined)
let orcamentoTarefaRequest: OrcamentoTarefaRequest; //

const { status, data } = await apiInstance.costsOrcamentosTarefaUpdate(
    id,
    orcamentoTarefaRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **orcamentoTarefaRequest** | **OrcamentoTarefaRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Orçamento de Tarefa. | defaults to undefined|


### Return type

**OrcamentoTarefa**

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

