# ComentriosApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**documentsAdicionarComentarioCreate**](#documentsadicionarcomentariocreate) | **POST** /api/documents/{id}/adicionar_comentario/ | Adicionar comentário ao documento|
|[**documentsComentariosCreate**](#documentscomentarioscreate) | **POST** /api/documents/comentarios/ | Criar um novo comentário|
|[**documentsComentariosDestroy**](#documentscomentariosdestroy) | **DELETE** /api/documents/comentarios/{id}/ | Excluir um comentário|
|[**documentsComentariosList**](#documentscomentarioslist) | **GET** /api/documents/comentarios/ | Listar comentários de documentos|
|[**documentsComentariosPartialUpdate**](#documentscomentariospartialupdate) | **PATCH** /api/documents/comentarios/{id}/ | Atualizar parcialmente um comentário|
|[**documentsComentariosRetrieve**](#documentscomentariosretrieve) | **GET** /api/documents/comentarios/{id}/ | Detalhes de um comentário|
|[**documentsComentariosUpdate**](#documentscomentariosupdate) | **PUT** /api/documents/comentarios/{id}/ | Atualizar um comentário|

# **documentsAdicionarComentarioCreate**
> Comentario documentsAdicionarComentarioCreate()

Adiciona um novo comentário a um documento específico.

### Example

```typescript
import {
    ComentriosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosApi(configuration);

let id: number; //A unique integer value identifying this Documento. (default to undefined)
let body: any; // (optional)

const { status, data } = await apiInstance.documentsAdicionarComentarioCreate(
    id,
    body
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **body** | **any**|  | |
| **id** | [**number**] | A unique integer value identifying this Documento. | defaults to undefined|


### Return type

**Comentario**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** | Comentário adicionado com sucesso |  -  |
|**400** | Dados inválidos (ex: texto não fornecido) |  -  |
|**404** | Documento não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsComentariosCreate**
> Comentario documentsComentariosCreate(comentarioRequest)

Cria um novo comentário para um documento. O autor é automaticamente definido como o usuário autenticado.

### Example

```typescript
import {
    ComentriosApi,
    Configuration,
    ComentarioRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosApi(configuration);

let comentarioRequest: ComentarioRequest; //

const { status, data } = await apiInstance.documentsComentariosCreate(
    comentarioRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **comentarioRequest** | **ComentarioRequest**|  | |


### Return type

**Comentario**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** | Comentário criado com sucesso |  -  |
|**400** | Dados inválidos |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsComentariosDestroy**
> documentsComentariosDestroy()

Remove um comentário do sistema. Somente o autor ou um administrador pode excluí-lo.

### Example

```typescript
import {
    ComentriosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosApi(configuration);

let id: number; //A unique integer value identifying this Comentário. (default to undefined)

const { status, data } = await apiInstance.documentsComentariosDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Comentário. | defaults to undefined|


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
|**204** | Comentário excluído com sucesso |  -  |
|**403** | Permissão negada para excluir o comentário |  -  |
|**404** | Comentário não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsComentariosList**
> PaginatedComentarioList documentsComentariosList()

Retorna a lista de todos os comentários associados a documentos.

### Example

```typescript
import {
    ComentriosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosApi(configuration);

let autor: number; //Filtrar por ID do autor do comentário (optional) (default to undefined)
let documento: number; //Filtrar por ID do documento ao qual o comentário pertence (optional) (default to undefined)
let ordering: string; //Campo para ordenação (ex: criado_em, -criado_em) (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)

const { status, data } = await apiInstance.documentsComentariosList(
    autor,
    documento,
    ordering,
    page
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **autor** | [**number**] | Filtrar por ID do autor do comentário | (optional) defaults to undefined|
| **documento** | [**number**] | Filtrar por ID do documento ao qual o comentário pertence | (optional) defaults to undefined|
| **ordering** | [**string**] | Campo para ordenação (ex: criado_em, -criado_em) | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|


### Return type

**PaginatedComentarioList**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Lista de comentários recuperada com sucesso |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsComentariosPartialUpdate**
> Comentario documentsComentariosPartialUpdate()

Atualiza parcialmente um comentário existente. Somente o autor ou um administrador pode atualizá-lo.

### Example

```typescript
import {
    ComentriosApi,
    Configuration,
    PatchedComentarioRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosApi(configuration);

let id: number; //A unique integer value identifying this Comentário. (default to undefined)
let patchedComentarioRequest: PatchedComentarioRequest; // (optional)

const { status, data } = await apiInstance.documentsComentariosPartialUpdate(
    id,
    patchedComentarioRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedComentarioRequest** | **PatchedComentarioRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Comentário. | defaults to undefined|


### Return type

**Comentario**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Comentário atualizado parcialmente com sucesso |  -  |
|**400** | Dados inválidos |  -  |
|**403** | Permissão negada para atualizar o comentário |  -  |
|**404** | Comentário não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsComentariosRetrieve**
> Comentario documentsComentariosRetrieve()

Retorna os detalhes de um comentário específico.

### Example

```typescript
import {
    ComentriosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosApi(configuration);

let id: number; //A unique integer value identifying this Comentário. (default to undefined)

const { status, data } = await apiInstance.documentsComentariosRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Comentário. | defaults to undefined|


### Return type

**Comentario**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Detalhes do comentário recuperados com sucesso |  -  |
|**404** | Comentário não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsComentariosUpdate**
> Comentario documentsComentariosUpdate(comentarioRequest)

Atualiza um comentário existente. Somente o autor do comentário ou um administrador pode atualizá-lo.

### Example

```typescript
import {
    ComentriosApi,
    Configuration,
    ComentarioRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComentriosApi(configuration);

let id: number; //A unique integer value identifying this Comentário. (default to undefined)
let comentarioRequest: ComentarioRequest; //

const { status, data } = await apiInstance.documentsComentariosUpdate(
    id,
    comentarioRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **comentarioRequest** | **ComentarioRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Comentário. | defaults to undefined|


### Return type

**Comentario**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Comentário atualizado com sucesso |  -  |
|**400** | Dados inválidos |  -  |
|**403** | Permissão negada para atualizar o comentário |  -  |
|**404** | Comentário não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

