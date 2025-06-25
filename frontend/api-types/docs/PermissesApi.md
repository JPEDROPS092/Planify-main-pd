# PermissesApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**authPermissionsCreate**](#authpermissionscreate) | **POST** /api/auth/permissions/ | Criar nova permissão|
|[**authPermissionsDestroy**](#authpermissionsdestroy) | **DELETE** /api/auth/permissions/{id}/ | Excluir permissão|
|[**authPermissionsList**](#authpermissionslist) | **GET** /api/auth/permissions/ | Listar permissões|
|[**authPermissionsPartialUpdate**](#authpermissionspartialupdate) | **PATCH** /api/auth/permissions/{id}/ | Atualizar permissão parcialmente|
|[**authPermissionsRetrieve**](#authpermissionsretrieve) | **GET** /api/auth/permissions/{id}/ | Obter detalhes da permissão|
|[**authPermissionsUpdate**](#authpermissionsupdate) | **PUT** /api/auth/permissions/{id}/ | Atualizar permissão|

# **authPermissionsCreate**
> Permission authPermissionsCreate(permissionRequest)

Cria uma nova permissão.

### Example

```typescript
import {
    PermissesApi,
    Configuration,
    PermissionRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesApi(configuration);

let permissionRequest: PermissionRequest; //

const { status, data } = await apiInstance.authPermissionsCreate(
    permissionRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **permissionRequest** | **PermissionRequest**|  | |


### Return type

**Permission**

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

# **authPermissionsDestroy**
> authPermissionsDestroy()

Remove uma permissão existente.

### Example

```typescript
import {
    PermissesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesApi(configuration);

let id: number; //A unique integer value identifying this permission. (default to undefined)

const { status, data } = await apiInstance.authPermissionsDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this permission. | defaults to undefined|


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

# **authPermissionsList**
> PaginatedPermissionList authPermissionsList()

Retorna uma lista paginada de permissões.

### Example

```typescript
import {
    PermissesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesApi(configuration);

let page: number; //A page number within the paginated result set. (optional) (default to undefined)

const { status, data } = await apiInstance.authPermissionsList(
    page
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|


### Return type

**PaginatedPermissionList**

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

# **authPermissionsPartialUpdate**
> Permission authPermissionsPartialUpdate()

Atualiza parcialmente uma permissão existente.

### Example

```typescript
import {
    PermissesApi,
    Configuration,
    PatchedPermissionRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesApi(configuration);

let id: number; //A unique integer value identifying this permission. (default to undefined)
let patchedPermissionRequest: PatchedPermissionRequest; // (optional)

const { status, data } = await apiInstance.authPermissionsPartialUpdate(
    id,
    patchedPermissionRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedPermissionRequest** | **PatchedPermissionRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this permission. | defaults to undefined|


### Return type

**Permission**

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

# **authPermissionsRetrieve**
> Permission authPermissionsRetrieve()

Retorna informações detalhadas de uma permissão específica.

### Example

```typescript
import {
    PermissesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesApi(configuration);

let id: number; //A unique integer value identifying this permission. (default to undefined)

const { status, data } = await apiInstance.authPermissionsRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this permission. | defaults to undefined|


### Return type

**Permission**

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

# **authPermissionsUpdate**
> Permission authPermissionsUpdate(permissionRequest)

Atualiza todos os campos de uma permissão existente.

### Example

```typescript
import {
    PermissesApi,
    Configuration,
    PermissionRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new PermissesApi(configuration);

let id: number; //A unique integer value identifying this permission. (default to undefined)
let permissionRequest: PermissionRequest; //

const { status, data } = await apiInstance.authPermissionsUpdate(
    id,
    permissionRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **permissionRequest** | **PermissionRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this permission. | defaults to undefined|


### Return type

**Permission**

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

