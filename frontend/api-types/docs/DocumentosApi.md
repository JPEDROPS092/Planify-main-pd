# DocumentosApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**documentsAdicionarComentarioCreate**](#documentsadicionarcomentariocreate) | **POST** /api/documents/{id}/adicionar_comentario/ | Adicionar comentário ao documento|
|[**documentsAssociarTarefaCreate**](#documentsassociartarefacreate) | **POST** /api/documents/{id}/associar_tarefa/ | Associar documento a uma tarefa|
|[**documentsComentariosCreate**](#documentscomentarioscreate) | **POST** /api/documents/comentarios/ | Criar um novo comentário|
|[**documentsComentariosDestroy**](#documentscomentariosdestroy) | **DELETE** /api/documents/comentarios/{id}/ | Excluir um comentário|
|[**documentsComentariosList**](#documentscomentarioslist) | **GET** /api/documents/comentarios/ | Listar comentários de documentos|
|[**documentsComentariosPartialUpdate**](#documentscomentariospartialupdate) | **PATCH** /api/documents/comentarios/{id}/ | Atualizar parcialmente um comentário|
|[**documentsComentariosRetrieve**](#documentscomentariosretrieve) | **GET** /api/documents/comentarios/{id}/ | Detalhes de um comentário|
|[**documentsComentariosUpdate**](#documentscomentariosupdate) | **PUT** /api/documents/comentarios/{id}/ | Atualizar um comentário|
|[**documentsCreate**](#documentscreate) | **POST** /api/documents/ | Criar documento|
|[**documentsDestroy**](#documentsdestroy) | **DELETE** /api/documents/{id}/ | Excluir documento|
|[**documentsDocumentHistoryRetrieve**](#documentsdocumenthistoryretrieve) | **GET** /api/documents/{id}/document_history/ | Histórico do documento|
|[**documentsHistoricoList**](#documentshistoricolist) | **GET** /api/documents/historico/ | Listar histórico de alterações de documentos|
|[**documentsHistoricoRetrieve**](#documentshistoricoretrieve) | **GET** /api/documents/historico/{id}/ | Detalhes de um registro de histórico|
|[**documentsList**](#documentslist) | **GET** /api/documents/ | Listar documentos|
|[**documentsPartialUpdate**](#documentspartialupdate) | **PATCH** /api/documents/{id}/ | Atualizar documento parcialmente|
|[**documentsRetrieve**](#documentsretrieve) | **GET** /api/documents/{id}/ | Obter documento|
|[**documentsUpdate**](#documentsupdate) | **PUT** /api/documents/{id}/ | Atualizar documento|

# **documentsAdicionarComentarioCreate**
> Comentario documentsAdicionarComentarioCreate()

Adiciona um novo comentário a um documento específico.

### Example

```typescript
import {
    DocumentosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

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

# **documentsAssociarTarefaCreate**
> Documento documentsAssociarTarefaCreate()

Associa ou desassocia um documento a uma tarefa específica. Forneça \'tarefa_id\' para associar, ou \'tarefa_id: 0\' (ou nulo) para desassociar.

### Example

```typescript
import {
    DocumentosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

let id: number; //A unique integer value identifying this Documento. (default to undefined)
let body: any; // (optional)

const { status, data } = await apiInstance.documentsAssociarTarefaCreate(
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

**Documento**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Documento associado/desassociado com sucesso |  -  |
|**400** | Dados inválidos (ex: tarefa_id não fornecido) |  -  |
|**404** | Documento ou Tarefa não encontrada |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsComentariosCreate**
> Comentario documentsComentariosCreate(comentarioRequest)

Cria um novo comentário para um documento. O autor é automaticamente definido como o usuário autenticado.

### Example

```typescript
import {
    DocumentosApi,
    Configuration,
    ComentarioRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

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
    DocumentosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

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
    DocumentosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

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
    DocumentosApi,
    Configuration,
    PatchedComentarioRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

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
    DocumentosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

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
    DocumentosApi,
    Configuration,
    ComentarioRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

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

# **documentsCreate**
> Documento documentsCreate(documentoRequest)

Cria um novo documento no sistema.

### Example

```typescript
import {
    DocumentosApi,
    Configuration,
    DocumentoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

let documentoRequest: DocumentoRequest; //

const { status, data } = await apiInstance.documentsCreate(
    documentoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **documentoRequest** | **DocumentoRequest**|  | |


### Return type

**Documento**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** | Documento criado com sucesso |  -  |
|**400** | Dados inválidos |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsDestroy**
> documentsDestroy()

Remove um documento do sistema.

### Example

```typescript
import {
    DocumentosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

let id: number; //A unique integer value identifying this Documento. (default to undefined)

const { status, data } = await apiInstance.documentsDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Documento. | defaults to undefined|


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
|**204** | Documento excluído com sucesso |  -  |
|**404** | Documento não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsDocumentHistoryRetrieve**
> PaginatedHistoricoDocumentoList documentsDocumentHistoryRetrieve()

Retorna o histórico de versões do documento.

### Example

```typescript
import {
    DocumentosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

let id: number; //A unique integer value identifying this Documento. (default to undefined)

const { status, data } = await apiInstance.documentsDocumentHistoryRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Documento. | defaults to undefined|


### Return type

**PaginatedHistoricoDocumentoList**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Histórico de versões recuperado com sucesso |  -  |
|**404** | Documento não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsHistoricoList**
> PaginatedHistoricoDocumentoList documentsHistoricoList()

Retorna a lista de todas as alterações registradas para os documentos.

### Example

```typescript
import {
    DocumentosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

let alteradoPor: number; //Filtrar por ID do usuário que realizou a alteração (optional) (default to undefined)
let documento: number; //Filtrar por ID do documento (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)

const { status, data } = await apiInstance.documentsHistoricoList(
    alteradoPor,
    documento,
    page
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **alteradoPor** | [**number**] | Filtrar por ID do usuário que realizou a alteração | (optional) defaults to undefined|
| **documento** | [**number**] | Filtrar por ID do documento | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|


### Return type

**PaginatedHistoricoDocumentoList**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Lista de histórico de documentos recuperada com sucesso |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsHistoricoRetrieve**
> HistoricoDocumento documentsHistoricoRetrieve()

Retorna os detalhes de um registro específico do histórico de alterações de um documento.

### Example

```typescript
import {
    DocumentosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

let id: number; //A unique integer value identifying this Histórico de Documento. (default to undefined)

const { status, data } = await apiInstance.documentsHistoricoRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Histórico de Documento. | defaults to undefined|


### Return type

**HistoricoDocumento**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Detalhes do registro de histórico recuperados com sucesso |  -  |
|**404** | Registro de histórico não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsList**
> PaginatedDocumentoListList documentsList()

Retorna a lista de todos os documentos com filtros opcionais.

### Example

```typescript
import {
    DocumentosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

let enviadoPor: number; //Filtrar por ID do usuário que enviou (optional) (default to undefined)
let ordering: string; //Campo para ordenação (ex: data_upload, -titulo) (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let projeto: number; //Filtrar por projeto (ID) (optional) (default to undefined)
let search: string; //Termo de busca para título, descrição ou tipo de arquivo (optional) (default to undefined)
let tarefa: number; //Filtrar por tarefa (ID) (optional) (default to undefined)
let texto: string; //Buscar por texto no título ou descrição (optional) (default to undefined)
let tipo: 'ATA' | 'DESIGN' | 'MANUAL' | 'OUTRO' | 'RELATORIO' | 'REQUISITO'; //Filtrar por tipo de documento (optional) (default to undefined)
let tipoArquivo: string; //Filtrar por tipo MIME do arquivo (ex: application/pdf) (optional) (default to undefined)

const { status, data } = await apiInstance.documentsList(
    enviadoPor,
    ordering,
    page,
    projeto,
    search,
    tarefa,
    texto,
    tipo,
    tipoArquivo
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **enviadoPor** | [**number**] | Filtrar por ID do usuário que enviou | (optional) defaults to undefined|
| **ordering** | [**string**] | Campo para ordenação (ex: data_upload, -titulo) | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **projeto** | [**number**] | Filtrar por projeto (ID) | (optional) defaults to undefined|
| **search** | [**string**] | Termo de busca para título, descrição ou tipo de arquivo | (optional) defaults to undefined|
| **tarefa** | [**number**] | Filtrar por tarefa (ID) | (optional) defaults to undefined|
| **texto** | [**string**] | Buscar por texto no título ou descrição | (optional) defaults to undefined|
| **tipo** | [**&#39;ATA&#39; | &#39;DESIGN&#39; | &#39;MANUAL&#39; | &#39;OUTRO&#39; | &#39;RELATORIO&#39; | &#39;REQUISITO&#39;**]**Array<&#39;ATA&#39; &#124; &#39;DESIGN&#39; &#124; &#39;MANUAL&#39; &#124; &#39;OUTRO&#39; &#124; &#39;RELATORIO&#39; &#124; &#39;REQUISITO&#39;>** | Filtrar por tipo de documento | (optional) defaults to undefined|
| **tipoArquivo** | [**string**] | Filtrar por tipo MIME do arquivo (ex: application/pdf) | (optional) defaults to undefined|


### Return type

**PaginatedDocumentoListList**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Lista de documentos recuperada com sucesso |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsPartialUpdate**
> Documento documentsPartialUpdate()

Atualiza parcialmente um documento existente.

### Example

```typescript
import {
    DocumentosApi,
    Configuration,
    PatchedDocumentoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

let id: number; //A unique integer value identifying this Documento. (default to undefined)
let patchedDocumentoRequest: PatchedDocumentoRequest; // (optional)

const { status, data } = await apiInstance.documentsPartialUpdate(
    id,
    patchedDocumentoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedDocumentoRequest** | **PatchedDocumentoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Documento. | defaults to undefined|


### Return type

**Documento**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Documento atualizado parcialmente com sucesso |  -  |
|**400** | Dados inválidos |  -  |
|**404** | Documento não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsRetrieve**
> Documento documentsRetrieve()

Retorna os detalhes de um documento específico.

### Example

```typescript
import {
    DocumentosApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

let id: number; //A unique integer value identifying this Documento. (default to undefined)

const { status, data } = await apiInstance.documentsRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Documento. | defaults to undefined|


### Return type

**Documento**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Detalhes do documento recuperados com sucesso |  -  |
|**404** | Documento não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **documentsUpdate**
> Documento documentsUpdate(documentoRequest)

Atualiza todos os campos de um documento existente.

### Example

```typescript
import {
    DocumentosApi,
    Configuration,
    DocumentoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentosApi(configuration);

let id: number; //A unique integer value identifying this Documento. (default to undefined)
let documentoRequest: DocumentoRequest; //

const { status, data } = await apiInstance.documentsUpdate(
    id,
    documentoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **documentoRequest** | **DocumentoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Documento. | defaults to undefined|


### Return type

**Documento**

### Authorization

[JWT_Authentication](../README.md#JWT_Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Documento atualizado com sucesso |  -  |
|**400** | Dados inválidos |  -  |
|**404** | Documento não encontrado |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

