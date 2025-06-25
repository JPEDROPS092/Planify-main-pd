# RiscosApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**risksHistoricoList**](#riskshistoricolist) | **GET** /api/risks/historico/ | Listar históricos do risco|
|[**risksHistoricoRetrieve**](#riskshistoricoretrieve) | **GET** /api/risks/historico/{id}/ | Obter detalhes do histórico do risco|
|[**risksRiscosAtualizarStatusCreate**](#risksriscosatualizarstatuscreate) | **POST** /api/risks/riscos/{id}/atualizar_status/ | Atualizar status do risco|
|[**risksRiscosCreate**](#risksriscoscreate) | **POST** /api/risks/riscos/ | Criar novo risco|
|[**risksRiscosDestroy**](#risksriscosdestroy) | **DELETE** /api/risks/riscos/{id}/ | Excluir risco|
|[**risksRiscosExcluirVariosDestroy**](#risksriscosexcluirvariosdestroy) | **DELETE** /api/risks/riscos/excluir_varios/ | Excluir múltiplos riscos|
|[**risksRiscosHistoricoRetrieve**](#risksriscoshistoricoretrieve) | **GET** /api/risks/riscos/{id}/historico/ | Retorna histórico do risco|
|[**risksRiscosList**](#risksriscoslist) | **GET** /api/risks/riscos/ | Listar riscos|
|[**risksRiscosPartialUpdate**](#risksriscospartialupdate) | **PATCH** /api/risks/riscos/{id}/ | Atualizar risco parcialmente|
|[**risksRiscosRetrieve**](#risksriscosretrieve) | **GET** /api/risks/riscos/{id}/ | Obter detalhes do risco|
|[**risksRiscosUpdate**](#risksriscosupdate) | **PUT** /api/risks/riscos/{id}/ | Atualizar risco|

# **risksHistoricoList**
> PaginatedHistoricoRiscoList risksHistoricoList()

Retorna uma lista paginada de históricos do risco.

### Example

```typescript
import {
    RiscosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new RiscosApi(configuration);

let alteradoPor: number; // (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let risco: number; // (optional) (default to undefined)

const { status, data } = await apiInstance.risksHistoricoList(
    alteradoPor,
    page,
    risco
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **alteradoPor** | [**number**] |  | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **risco** | [**number**] |  | (optional) defaults to undefined|


### Return type

**PaginatedHistoricoRiscoList**

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

# **risksHistoricoRetrieve**
> HistoricoRisco risksHistoricoRetrieve()

Retorna o histórico detalhado de um risco específico.

### Example

```typescript
import {
    RiscosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new RiscosApi(configuration);

let id: number; //A unique integer value identifying this Histórico de Risco. (default to undefined)

const { status, data } = await apiInstance.risksHistoricoRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Histórico de Risco. | defaults to undefined|


### Return type

**HistoricoRisco**

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

# **risksRiscosAtualizarStatusCreate**
> risksRiscosAtualizarStatusCreate(riscoRequest)

Atualiza o status de um risco.

### Example

```typescript
import {
    RiscosApi,
    Configuration,
    RiscoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new RiscosApi(configuration);

let id: number; //A unique integer value identifying this Risco. (default to undefined)
let riscoRequest: RiscoRequest; //

const { status, data } = await apiInstance.risksRiscosAtualizarStatusCreate(
    id,
    riscoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **riscoRequest** | **RiscoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Risco. | defaults to undefined|


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

# **risksRiscosCreate**
> RiscoList risksRiscosCreate(riscoRequest)

Cria um novo risco.

### Example

```typescript
import {
    RiscosApi,
    Configuration,
    RiscoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new RiscosApi(configuration);

let riscoRequest: RiscoRequest; //

const { status, data } = await apiInstance.risksRiscosCreate(
    riscoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **riscoRequest** | **RiscoRequest**|  | |


### Return type

**RiscoList**

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

# **risksRiscosDestroy**
> risksRiscosDestroy()

Remove um risco existente.

### Example

```typescript
import {
    RiscosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new RiscosApi(configuration);

let id: number; //A unique integer value identifying this Risco. (default to undefined)

const { status, data } = await apiInstance.risksRiscosDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Risco. | defaults to undefined|


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

# **risksRiscosExcluirVariosDestroy**
> risksRiscosExcluirVariosDestroy()

Exclui múltiplos riscos de uma vez.

### Example

```typescript
import {
    RiscosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new RiscosApi(configuration);

const { status, data } = await apiInstance.risksRiscosExcluirVariosDestroy();
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

# **risksRiscosHistoricoRetrieve**
> risksRiscosHistoricoRetrieve()

Retorna o histórico de alterações do risco.

### Example

```typescript
import {
    RiscosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new RiscosApi(configuration);

let id: number; //A unique integer value identifying this Risco. (default to undefined)

const { status, data } = await apiInstance.risksRiscosHistoricoRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Risco. | defaults to undefined|


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

# **risksRiscosList**
> PaginatedRiscoList risksRiscosList()

Retorna uma lista paginada de riscos.

### Example

```typescript
import {
    RiscosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new RiscosApi(configuration);

let impacto: 'ALTO' | 'BAIXO' | 'MEDIO'; //* `BAIXO` - Baixo * `MEDIO` - Médio * `ALTO` - Alto (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let probabilidade: 'ALTA' | 'BAIXA' | 'MEDIA'; //* `BAIXA` - Baixa * `MEDIA` - Média * `ALTA` - Alta (optional) (default to undefined)
let projeto: number; // (optional) (default to undefined)
let responsavelMitigacao: number; // (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let status: 'ACEITO' | 'ELIMINADO' | 'EM_ANALISE' | 'IDENTIFICADO' | 'MITIGADO'; //* `IDENTIFICADO` - Identificado * `EM_ANALISE` - Em Análise * `MITIGADO` - Mitigado * `ACEITO` - Aceito * `ELIMINADO` - Eliminado (optional) (default to undefined)

const { status, data } = await apiInstance.risksRiscosList(
    impacto,
    ordering,
    page,
    probabilidade,
    projeto,
    responsavelMitigacao,
    search,
    status
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **impacto** | [**&#39;ALTO&#39; | &#39;BAIXO&#39; | &#39;MEDIO&#39;**]**Array<&#39;ALTO&#39; &#124; &#39;BAIXO&#39; &#124; &#39;MEDIO&#39;>** | * &#x60;BAIXO&#x60; - Baixo * &#x60;MEDIO&#x60; - Médio * &#x60;ALTO&#x60; - Alto | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **probabilidade** | [**&#39;ALTA&#39; | &#39;BAIXA&#39; | &#39;MEDIA&#39;**]**Array<&#39;ALTA&#39; &#124; &#39;BAIXA&#39; &#124; &#39;MEDIA&#39;>** | * &#x60;BAIXA&#x60; - Baixa * &#x60;MEDIA&#x60; - Média * &#x60;ALTA&#x60; - Alta | (optional) defaults to undefined|
| **projeto** | [**number**] |  | (optional) defaults to undefined|
| **responsavelMitigacao** | [**number**] |  | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **status** | [**&#39;ACEITO&#39; | &#39;ELIMINADO&#39; | &#39;EM_ANALISE&#39; | &#39;IDENTIFICADO&#39; | &#39;MITIGADO&#39;**]**Array<&#39;ACEITO&#39; &#124; &#39;ELIMINADO&#39; &#124; &#39;EM_ANALISE&#39; &#124; &#39;IDENTIFICADO&#39; &#124; &#39;MITIGADO&#39;>** | * &#x60;IDENTIFICADO&#x60; - Identificado * &#x60;EM_ANALISE&#x60; - Em Análise * &#x60;MITIGADO&#x60; - Mitigado * &#x60;ACEITO&#x60; - Aceito * &#x60;ELIMINADO&#x60; - Eliminado | (optional) defaults to undefined|


### Return type

**PaginatedRiscoList**

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

# **risksRiscosPartialUpdate**
> Risco risksRiscosPartialUpdate()

Atualiza parcialmente um risco existente.

### Example

```typescript
import {
    RiscosApi,
    Configuration,
    PatchedRiscoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new RiscosApi(configuration);

let id: number; //A unique integer value identifying this Risco. (default to undefined)
let patchedRiscoRequest: PatchedRiscoRequest; // (optional)

const { status, data } = await apiInstance.risksRiscosPartialUpdate(
    id,
    patchedRiscoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedRiscoRequest** | **PatchedRiscoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Risco. | defaults to undefined|


### Return type

**Risco**

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

# **risksRiscosRetrieve**
> Risco risksRiscosRetrieve()

Retorna informações detalhadas de um risco específico.

### Example

```typescript
import {
    RiscosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new RiscosApi(configuration);

let id: number; //A unique integer value identifying this Risco. (default to undefined)

const { status, data } = await apiInstance.risksRiscosRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Risco. | defaults to undefined|


### Return type

**Risco**

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

# **risksRiscosUpdate**
> Risco risksRiscosUpdate(riscoRequest)

Atualiza todos os campos de um risco existente.

### Example

```typescript
import {
    RiscosApi,
    Configuration,
    RiscoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new RiscosApi(configuration);

let id: number; //A unique integer value identifying this Risco. (default to undefined)
let riscoRequest: RiscoRequest; //

const { status, data } = await apiInstance.risksRiscosUpdate(
    id,
    riscoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **riscoRequest** | **RiscoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Risco. | defaults to undefined|


### Return type

**Risco**

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

