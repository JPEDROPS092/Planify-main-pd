# EquipesApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**teamsEquipesAdicionarMembroCreate**](#teamsequipesadicionarmembrocreate) | **POST** /api/teams/equipes/{id}/adicionar_membro/ | Adicionar membro à equipe|
|[**teamsEquipesAtualizarPapelMembroCreate**](#teamsequipesatualizarpapelmembrocreate) | **POST** /api/teams/equipes/{id}/atualizar_papel_membro/ | Atualizar papel do membro|
|[**teamsEquipesCreate**](#teamsequipescreate) | **POST** /api/teams/equipes/ | Criar nova equipe|
|[**teamsEquipesDestroy**](#teamsequipesdestroy) | **DELETE** /api/teams/equipes/{id}/ | Excluir equipe|
|[**teamsEquipesList**](#teamsequipeslist) | **GET** /api/teams/equipes/ | Listar equipes|
|[**teamsEquipesMembrosList**](#teamsequipesmembroslist) | **GET** /api/teams/equipes/{id}/membros/ | Listar membros da equipe|
|[**teamsEquipesPartialUpdate**](#teamsequipespartialupdate) | **PATCH** /api/teams/equipes/{id}/ | Atualizar equipe parcialmente|
|[**teamsEquipesRemoverMembroCreate**](#teamsequipesremovermembrocreate) | **POST** /api/teams/equipes/{id}/remover_membro/ | Remover membro da equipe|
|[**teamsEquipesRetrieve**](#teamsequipesretrieve) | **GET** /api/teams/equipes/{id}/ | Obter detalhes da equipe|
|[**teamsEquipesUpdate**](#teamsequipesupdate) | **PUT** /api/teams/equipes/{id}/ | Atualizar equipe|
|[**teamsEquipesUsuariosDisponiveisList**](#teamsequipesusuariosdisponiveislist) | **GET** /api/teams/equipes/usuarios_disponiveis/ | Retornar usuários disponíveis à equipe|

# **teamsEquipesAdicionarMembroCreate**
> MembroEquipe teamsEquipesAdicionarMembroCreate(membroEquipeRequest)

Adiciona um novo membro à equipe.

### Example

```typescript
import {
    EquipesApi,
    Configuration,
    MembroEquipeRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new EquipesApi(configuration);

let id: number; //A unique integer value identifying this Equipe. (default to undefined)
let membroEquipeRequest: MembroEquipeRequest; //

const { status, data } = await apiInstance.teamsEquipesAdicionarMembroCreate(
    id,
    membroEquipeRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **membroEquipeRequest** | **MembroEquipeRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Equipe. | defaults to undefined|


### Return type

**MembroEquipe**

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

# **teamsEquipesAtualizarPapelMembroCreate**
> MembroEquipe teamsEquipesAtualizarPapelMembroCreate(membroEquipeRequest)

Atualiza o papel de um membro na equipe.

### Example

```typescript
import {
    EquipesApi,
    Configuration,
    MembroEquipeRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new EquipesApi(configuration);

let id: number; //A unique integer value identifying this Equipe. (default to undefined)
let membroEquipeRequest: MembroEquipeRequest; //

const { status, data } = await apiInstance.teamsEquipesAtualizarPapelMembroCreate(
    id,
    membroEquipeRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **membroEquipeRequest** | **MembroEquipeRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Equipe. | defaults to undefined|


### Return type

**MembroEquipe**

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

# **teamsEquipesCreate**
> Equipe teamsEquipesCreate(equipeRequest)

Cria uma nova equipe.

### Example

```typescript
import {
    EquipesApi,
    Configuration,
    EquipeRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new EquipesApi(configuration);

let equipeRequest: EquipeRequest; //

const { status, data } = await apiInstance.teamsEquipesCreate(
    equipeRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **equipeRequest** | **EquipeRequest**|  | |


### Return type

**Equipe**

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

# **teamsEquipesDestroy**
> teamsEquipesDestroy()

Remove uma equipe existente.

### Example

```typescript
import {
    EquipesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new EquipesApi(configuration);

let id: number; //A unique integer value identifying this Equipe. (default to undefined)

const { status, data } = await apiInstance.teamsEquipesDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Equipe. | defaults to undefined|


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

# **teamsEquipesList**
> PaginatedEquipeListList teamsEquipesList()

Retorna uma lista paginada de equipes.

### Example

```typescript
import {
    EquipesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new EquipesApi(configuration);

let minhasEquipes: boolean; //Filtrar apenas minhas equipes (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)
let texto: string; //Filtrar por nome ou descrição (optional) (default to undefined)
let usuario: number; //Filtrar por membro da equipe (optional) (default to undefined)

const { status, data } = await apiInstance.teamsEquipesList(
    minhasEquipes,
    ordering,
    page,
    search,
    texto,
    usuario
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **minhasEquipes** | [**boolean**] | Filtrar apenas minhas equipes | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|
| **texto** | [**string**] | Filtrar por nome ou descrição | (optional) defaults to undefined|
| **usuario** | [**number**] | Filtrar por membro da equipe | (optional) defaults to undefined|


### Return type

**PaginatedEquipeListList**

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

# **teamsEquipesMembrosList**
> PaginatedMembroEquipeList teamsEquipesMembrosList()

Retorna a lista de membros de uma equipe específica.

### Example

```typescript
import {
    EquipesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new EquipesApi(configuration);

let id: number; //A unique integer value identifying this Equipe. (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)

const { status, data } = await apiInstance.teamsEquipesMembrosList(
    id,
    ordering,
    page,
    search
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Equipe. | defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **search** | [**string**] | A search term. | (optional) defaults to undefined|


### Return type

**PaginatedMembroEquipeList**

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

# **teamsEquipesPartialUpdate**
> Equipe teamsEquipesPartialUpdate()

Atualiza parcialmente uma equipe existente.

### Example

```typescript
import {
    EquipesApi,
    Configuration,
    PatchedEquipeRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new EquipesApi(configuration);

let id: number; //A unique integer value identifying this Equipe. (default to undefined)
let patchedEquipeRequest: PatchedEquipeRequest; // (optional)

const { status, data } = await apiInstance.teamsEquipesPartialUpdate(
    id,
    patchedEquipeRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedEquipeRequest** | **PatchedEquipeRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Equipe. | defaults to undefined|


### Return type

**Equipe**

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

# **teamsEquipesRemoverMembroCreate**
> teamsEquipesRemoverMembroCreate(equipeRequest)

Remove um membro da equipe.

### Example

```typescript
import {
    EquipesApi,
    Configuration,
    EquipeRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new EquipesApi(configuration);

let id: number; //A unique integer value identifying this Equipe. (default to undefined)
let equipeRequest: EquipeRequest; //

const { status, data } = await apiInstance.teamsEquipesRemoverMembroCreate(
    id,
    equipeRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **equipeRequest** | **EquipeRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Equipe. | defaults to undefined|


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
|**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **teamsEquipesRetrieve**
> Equipe teamsEquipesRetrieve()

Retorna informações detalhadas de uma equipe específica.

### Example

```typescript
import {
    EquipesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new EquipesApi(configuration);

let id: number; //A unique integer value identifying this Equipe. (default to undefined)

const { status, data } = await apiInstance.teamsEquipesRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Equipe. | defaults to undefined|


### Return type

**Equipe**

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

# **teamsEquipesUpdate**
> Equipe teamsEquipesUpdate(equipeRequest)

Atualiza todos os campos de uma equipe existente.

### Example

```typescript
import {
    EquipesApi,
    Configuration,
    EquipeRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new EquipesApi(configuration);

let id: number; //A unique integer value identifying this Equipe. (default to undefined)
let equipeRequest: EquipeRequest; //

const { status, data } = await apiInstance.teamsEquipesUpdate(
    id,
    equipeRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **equipeRequest** | **EquipeRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Equipe. | defaults to undefined|


### Return type

**Equipe**

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

# **teamsEquipesUsuariosDisponiveisList**
> PaginatedUserMinimalList teamsEquipesUsuariosDisponiveisList()

Retorna a lista de usuários que podem ser adicionados à equipe.

### Example

```typescript
import {
    EquipesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new EquipesApi(configuration);

let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let search: string; //A search term. (optional) (default to undefined)

const { status, data } = await apiInstance.teamsEquipesUsuariosDisponiveisList(
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

**PaginatedUserMinimalList**

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

