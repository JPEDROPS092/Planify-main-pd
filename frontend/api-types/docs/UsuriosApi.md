# UsuriosApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**authUsersActivateCreate**](#authusersactivatecreate) | **POST** /api/auth/users/{id}/activate/ | Ativar usuário|
|[**authUsersCreate**](#authuserscreate) | **POST** /api/auth/users/ | Criar novo usuário|
|[**authUsersDeactivateCreate**](#authusersdeactivatecreate) | **POST** /api/auth/users/{id}/deactivate/ | Desativar usuário|
|[**authUsersDestroy**](#authusersdestroy) | **DELETE** /api/auth/users/{id}/ | Excluir usuário|
|[**authUsersList**](#authuserslist) | **GET** /api/auth/users/ | Listar usuários|
|[**authUsersPartialUpdate**](#authuserspartialupdate) | **PATCH** /api/auth/users/{id}/ | Atualizar usuário parcialmente|
|[**authUsersResetPasswordCreate**](#authusersresetpasswordcreate) | **POST** /api/auth/users/{id}/reset-password/ | Redefinir senha|
|[**authUsersResetPasswordCreate2**](#authusersresetpasswordcreate2) | **POST** /api/auth/users/{id}/reset_password/ | Redefinir senha|
|[**authUsersRetrieve**](#authusersretrieve) | **GET** /api/auth/users/{id}/ | Obter detalhes do usuário|
|[**authUsersUnlockCreate**](#authusersunlockcreate) | **POST** /api/auth/users/{id}/unlock/ | Desbloquear usuário|
|[**authUsersUpdate**](#authusersupdate) | **PUT** /api/auth/users/{id}/ | Atualizar usuário|

# **authUsersActivateCreate**
> authUsersActivateCreate(userRequest)

Ativa um usuário inativo.

### Example

```typescript
import {
    UsuriosApi,
    Configuration,
    UserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsuriosApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let userRequest: UserRequest; //

const { status, data } = await apiInstance.authUsersActivateCreate(
    id,
    userRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userRequest** | **UserRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


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

# **authUsersCreate**
> UserCreate authUsersCreate(userCreateRequest)

Cria um novo usuário.

### Example

```typescript
import {
    UsuriosApi,
    Configuration,
    UserCreateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsuriosApi(configuration);

let userCreateRequest: UserCreateRequest; //

const { status, data } = await apiInstance.authUsersCreate(
    userCreateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userCreateRequest** | **UserCreateRequest**|  | |


### Return type

**UserCreate**

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

# **authUsersDeactivateCreate**
> authUsersDeactivateCreate(userRequest)

Desativa um usuário ativo.

### Example

```typescript
import {
    UsuriosApi,
    Configuration,
    UserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsuriosApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let userRequest: UserRequest; //

const { status, data } = await apiInstance.authUsersDeactivateCreate(
    id,
    userRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userRequest** | **UserRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


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

# **authUsersDestroy**
> authUsersDestroy()

Remove um usuário existente.

### Example

```typescript
import {
    UsuriosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsuriosApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)

const { status, data } = await apiInstance.authUsersDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


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

# **authUsersList**
> PaginatedUserList authUsersList()

Retorna uma lista paginada de usuários.

### Example

```typescript
import {
    UsuriosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsuriosApi(configuration);

let page: number; //A page number within the paginated result set. (optional) (default to undefined)

const { status, data } = await apiInstance.authUsersList(
    page
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|


### Return type

**PaginatedUserList**

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

# **authUsersPartialUpdate**
> User authUsersPartialUpdate()

Atualiza parcialmente um usuário existente.

### Example

```typescript
import {
    UsuriosApi,
    Configuration,
    PatchedUserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsuriosApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let patchedUserRequest: PatchedUserRequest; // (optional)

const { status, data } = await apiInstance.authUsersPartialUpdate(
    id,
    patchedUserRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedUserRequest** | **PatchedUserRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


### Return type

**User**

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

# **authUsersResetPasswordCreate**
> authUsersResetPasswordCreate(userRequest)

Redefine a senha do usuário para uma senha temporária.

### Example

```typescript
import {
    UsuriosApi,
    Configuration,
    UserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsuriosApi(configuration);

let id: number; // (default to undefined)
let userRequest: UserRequest; //

const { status, data } = await apiInstance.authUsersResetPasswordCreate(
    id,
    userRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userRequest** | **UserRequest**|  | |
| **id** | [**number**] |  | defaults to undefined|


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

# **authUsersResetPasswordCreate2**
> authUsersResetPasswordCreate2(userRequest)

Redefine a senha do usuário para uma senha temporária.

### Example

```typescript
import {
    UsuriosApi,
    Configuration,
    UserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsuriosApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let userRequest: UserRequest; //

const { status, data } = await apiInstance.authUsersResetPasswordCreate2(
    id,
    userRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userRequest** | **UserRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


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

# **authUsersRetrieve**
> User authUsersRetrieve()

Retorna informações detalhadas de um usuário específico.

### Example

```typescript
import {
    UsuriosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsuriosApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)

const { status, data } = await apiInstance.authUsersRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


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

# **authUsersUnlockCreate**
> authUsersUnlockCreate(userRequest)

Desbloqueia um usuário após tentativas de login malsucedidas.

### Example

```typescript
import {
    UsuriosApi,
    Configuration,
    UserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsuriosApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let userRequest: UserRequest; //

const { status, data } = await apiInstance.authUsersUnlockCreate(
    id,
    userRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userRequest** | **UserRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


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

# **authUsersUpdate**
> User authUsersUpdate(userRequest)

Atualiza todos os campos de um usuário existente.

### Example

```typescript
import {
    UsuriosApi,
    Configuration,
    UserRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new UsuriosApi(configuration);

let id: number; //A unique integer value identifying this user. (default to undefined)
let userRequest: UserRequest; //

const { status, data } = await apiInstance.authUsersUpdate(
    id,
    userRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userRequest** | **UserRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this user. | defaults to undefined|


### Return type

**User**

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

