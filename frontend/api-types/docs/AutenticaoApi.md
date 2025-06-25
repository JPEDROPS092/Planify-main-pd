# AutenticaoApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**authLoginCreate**](#authlogincreate) | **POST** /api/auth/login/ | Login de usuário|
|[**authLogoutCreate**](#authlogoutcreate) | **POST** /api/auth/logout/ | Logout de usuário|
|[**authTokenRefreshCreate**](#authtokenrefreshcreate) | **POST** /api/auth/token/refresh/ | Atualizar token de acesso|

# **authLoginCreate**
> LoginResponse authLoginCreate(loginRequestRequest)

     Realiza o login do usuário e retorna os tokens de acesso e refresh.          O token de acesso deve ser usado no header de todas as requisições:     `Authorization: JWT <access_token>`          Quando o token de acesso expirar (após 1 hora), use o token de refresh para obter um novo.     

### Example

```typescript
import {
    AutenticaoApi,
    Configuration,
    LoginRequestRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AutenticaoApi(configuration);

let loginRequestRequest: LoginRequestRequest; //

const { status, data } = await apiInstance.authLoginCreate(
    loginRequestRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **loginRequestRequest** | **LoginRequestRequest**|  | |


### Return type

**LoginResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**401** | Credenciais inválidas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **authLogoutCreate**
> LogoutResponse authLogoutCreate()

Realiza o logout do usuário invalidando o token atual.

### Example

```typescript
import {
    AutenticaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AutenticaoApi(configuration);

const { status, data } = await apiInstance.authLogoutCreate();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**LogoutResponse**

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

# **authTokenRefreshCreate**
> RefreshResponse authTokenRefreshCreate(refreshRequestRequest)

     Atualiza um token de acesso expirado usando o token de refresh.     

### Example

```typescript
import {
    AutenticaoApi,
    Configuration,
    RefreshRequestRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AutenticaoApi(configuration);

let refreshRequestRequest: RefreshRequestRequest; //

const { status, data } = await apiInstance.authTokenRefreshCreate(
    refreshRequestRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **refreshRequestRequest** | **RefreshRequestRequest**|  | |


### Return type

**RefreshResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

