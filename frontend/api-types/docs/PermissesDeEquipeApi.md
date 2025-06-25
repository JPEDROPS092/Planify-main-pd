# PermissesDeEquipeApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**teamsPermissoesCreate**](#teamspermissoescreate) | **POST** /api/teams/permissoes/ | Criar permissão|
|[**teamsPermissoesDestroy**](#teamspermissoesdestroy) | **DELETE** /api/teams/permissoes/{id}/ | Excluir permissão|
|[**teamsPermissoesList**](#teamspermissoeslist) | **GET** /api/teams/permissoes/ | Listar permissões de equipe|
|[**teamsPermissoesPartialUpdate**](#teamspermissoespartialupdate) | **PATCH** /api/teams/permissoes/{id}/ | Atualizar permissão parcialmente|
|[**teamsPermissoesRetrieve**](#teamspermissoesretrieve) | **GET** /api/teams/permissoes/{id}/ | Obter detalhes da permissão|
|[**teamsPermissoesUpdate**](#teamspermissoesupdate) | **PUT** /api/teams/permissoes/{id}/ | Atualizar permissão|

# **teamsPermissoesCreate**
> PermissaoEquipe teamsPermissoesCreate(permissaoEquipeRequest)

Cria uma nova permissão de equipe.

### Example

```typescript
import {
    PermissesDeEquipeApi,
    Configuration,
    PermissaoEquipeRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesDeEquipeApi(configuration);

let permissaoEquipeRequest: PermissaoEquipeRequest; //

const { status, data } = await apiInstance.teamsPermissoesCreate(
    permissaoEquipeRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **permissaoEquipeRequest** | **PermissaoEquipeRequest**|  | |


### Return type

**PermissaoEquipe**

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

# **teamsPermissoesDestroy**
> teamsPermissoesDestroy()

Remove uma permissão de equipe.

### Example

```typescript
import {
    PermissesDeEquipeApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesDeEquipeApi(configuration);

let id: number; //A unique integer value identifying this Permissão de Equipe. (default to undefined)

const { status, data } = await apiInstance.teamsPermissoesDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Permissão de Equipe. | defaults to undefined|


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

# **teamsPermissoesList**
> PaginatedPermissaoEquipeList teamsPermissoesList()

Retorna uma lista de permissões de equipe.

### Example

```typescript
import {
    PermissesDeEquipeApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesDeEquipeApi(configuration);

let page: number; //A page number within the paginated result set. (optional) (default to undefined)

const { status, data } = await apiInstance.teamsPermissoesList(
    page
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|


### Return type

**PaginatedPermissaoEquipeList**

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

# **teamsPermissoesPartialUpdate**
> PermissaoEquipe teamsPermissoesPartialUpdate()

Atualiza parcialmente uma permissão de equipe.

### Example

```typescript
import {
    PermissesDeEquipeApi,
    Configuration,
    PatchedPermissaoEquipeRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesDeEquipeApi(configuration);

let id: number; //A unique integer value identifying this Permissão de Equipe. (default to undefined)
let patchedPermissaoEquipeRequest: PatchedPermissaoEquipeRequest; // (optional)

const { status, data } = await apiInstance.teamsPermissoesPartialUpdate(
    id,
    patchedPermissaoEquipeRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedPermissaoEquipeRequest** | **PatchedPermissaoEquipeRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Permissão de Equipe. | defaults to undefined|


### Return type

**PermissaoEquipe**

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

# **teamsPermissoesRetrieve**
> PermissaoEquipe teamsPermissoesRetrieve()

Retorna detalhes de uma permissão específica.

### Example

```typescript
import {
    PermissesDeEquipeApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesDeEquipeApi(configuration);

let id: number; //A unique integer value identifying this Permissão de Equipe. (default to undefined)

const { status, data } = await apiInstance.teamsPermissoesRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Permissão de Equipe. | defaults to undefined|


### Return type

**PermissaoEquipe**

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

# **teamsPermissoesUpdate**
> PermissaoEquipe teamsPermissoesUpdate(permissaoEquipeRequest)

Atualiza uma permissão de equipe existente.

### Example

```typescript
import {
    PermissesDeEquipeApi,
    Configuration,
    PermissaoEquipeRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesDeEquipeApi(configuration);

let id: number; //A unique integer value identifying this Permissão de Equipe. (default to undefined)
let permissaoEquipeRequest: PermissaoEquipeRequest; //

const { status, data } = await apiInstance.teamsPermissoesUpdate(
    id,
    permissaoEquipeRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **permissaoEquipeRequest** | **PermissaoEquipeRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Permissão de Equipe. | defaults to undefined|


### Return type

**PermissaoEquipe**

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

