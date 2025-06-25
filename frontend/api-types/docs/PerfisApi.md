# PerfisApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**authProfilesCreate**](#authprofilescreate) | **POST** /api/auth/profiles/ | Criar novo perfil|
|[**authProfilesDestroy**](#authprofilesdestroy) | **DELETE** /api/auth/profiles/{id}/ | Excluir perfil|
|[**authProfilesList**](#authprofileslist) | **GET** /api/auth/profiles/ | Listar perfis|
|[**authProfilesPartialUpdate**](#authprofilespartialupdate) | **PATCH** /api/auth/profiles/{id}/ | Atualizar perfil parcialmente|
|[**authProfilesRetrieve**](#authprofilesretrieve) | **GET** /api/auth/profiles/{id}/ | Obter detalhes do perfil|
|[**authProfilesUpdate**](#authprofilesupdate) | **PUT** /api/auth/profiles/{id}/ | Atualizar perfil|

# **authProfilesCreate**
> UserProfile authProfilesCreate()

Cria um novo perfil.

### Example

```typescript
import {
    PerfisApi,
    Configuration,
    UserProfileRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new PerfisApi(configuration);

let userProfileRequest: UserProfileRequest; // (optional)

const { status, data } = await apiInstance.authProfilesCreate(
    userProfileRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userProfileRequest** | **UserProfileRequest**|  | |


### Return type

**UserProfile**

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

# **authProfilesDestroy**
> authProfilesDestroy()

Remove um perfil existente.

### Example

```typescript
import {
    PerfisApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PerfisApi(configuration);

let id: number; //A unique integer value identifying this user profile. (default to undefined)

const { status, data } = await apiInstance.authProfilesDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this user profile. | defaults to undefined|


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

# **authProfilesList**
> PaginatedUserProfileList authProfilesList()

Retorna uma lista paginada de perfis.

### Example

```typescript
import {
    PerfisApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PerfisApi(configuration);

let page: number; //A page number within the paginated result set. (optional) (default to undefined)

const { status, data } = await apiInstance.authProfilesList(
    page
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|


### Return type

**PaginatedUserProfileList**

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

# **authProfilesPartialUpdate**
> UserProfile authProfilesPartialUpdate()

Atualiza parcialmente um perfil existente.

### Example

```typescript
import {
    PerfisApi,
    Configuration,
    PatchedUserProfileRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new PerfisApi(configuration);

let id: number; //A unique integer value identifying this user profile. (default to undefined)
let patchedUserProfileRequest: PatchedUserProfileRequest; // (optional)

const { status, data } = await apiInstance.authProfilesPartialUpdate(
    id,
    patchedUserProfileRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedUserProfileRequest** | **PatchedUserProfileRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user profile. | defaults to undefined|


### Return type

**UserProfile**

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

# **authProfilesRetrieve**
> UserProfile authProfilesRetrieve()

Retorna informações detalhadas de um perfil específico.

### Example

```typescript
import {
    PerfisApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PerfisApi(configuration);

let id: number; //A unique integer value identifying this user profile. (default to undefined)

const { status, data } = await apiInstance.authProfilesRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this user profile. | defaults to undefined|


### Return type

**UserProfile**

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

# **authProfilesUpdate**
> UserProfile authProfilesUpdate()

Atualiza todos os campos de um perfil existente.

### Example

```typescript
import {
    PerfisApi,
    Configuration,
    UserProfileRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new PerfisApi(configuration);

let id: number; //A unique integer value identifying this user profile. (default to undefined)
let userProfileRequest: UserProfileRequest; // (optional)

const { status, data } = await apiInstance.authProfilesUpdate(
    id,
    userProfileRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userProfileRequest** | **UserProfileRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user profile. | defaults to undefined|


### Return type

**UserProfile**

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

