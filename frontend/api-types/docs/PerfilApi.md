# PerfilApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**authUsersChangePasswordCreate**](#authuserschangepasswordcreate) | **POST** /api/auth/users/change-password/ | Alterar senha|
|[**authUsersChangePasswordCreate2**](#authuserschangepasswordcreate2) | **POST** /api/auth/users/change_password/ | Alterar senha|
|[**authUsersMeRetrieve**](#authusersmeretrieve) | **GET** /api/auth/users/me/ | Retornar minhas informações|
|[**authUsersPermissionsRetrieve**](#authuserspermissionsretrieve) | **GET** /api/auth/users/permissions/ | Retornar minhas permissões|

# **authUsersChangePasswordCreate**
> authUsersChangePasswordCreate(changePasswordRequest)

Altera a senha do usuário autenticado.

### Example

```typescript
import {
    PerfilApi,
    Configuration,
    ChangePasswordRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new PerfilApi(configuration);

let changePasswordRequest: ChangePasswordRequest; //

const { status, data } = await apiInstance.authUsersChangePasswordCreate(
    changePasswordRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **changePasswordRequest** | **ChangePasswordRequest**|  | |


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

# **authUsersChangePasswordCreate2**
> authUsersChangePasswordCreate2(changePasswordRequest)

Altera a senha do usuário autenticado.

### Example

```typescript
import {
    PerfilApi,
    Configuration,
    ChangePasswordRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new PerfilApi(configuration);

let changePasswordRequest: ChangePasswordRequest; //

const { status, data } = await apiInstance.authUsersChangePasswordCreate2(
    changePasswordRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **changePasswordRequest** | **ChangePasswordRequest**|  | |


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

# **authUsersMeRetrieve**
> User authUsersMeRetrieve()

Retorna as informações do usuário autenticado.

### Example

```typescript
import {
    PerfilApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PerfilApi(configuration);

const { status, data } = await apiInstance.authUsersMeRetrieve();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**User**

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

# **authUsersPermissionsRetrieve**
> authUsersPermissionsRetrieve()

Retorna as permissões do usuário autenticado.

### Example

```typescript
import {
    PerfilApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PerfilApi(configuration);

const { status, data } = await apiInstance.authUsersPermissionsRetrieve();
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

