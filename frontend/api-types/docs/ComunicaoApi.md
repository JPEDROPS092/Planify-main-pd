# ComunicaoApi

All URIs are relative to *http://localhost:8000*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**communicationsConfiguracoesCreate**](#communicationsconfiguracoescreate) | **POST** /api/communications/configuracoes/ | Criar nova configuração|
|[**communicationsConfiguracoesDestroy**](#communicationsconfiguracoesdestroy) | **DELETE** /api/communications/configuracoes/{id}/ | Excluir configuração|
|[**communicationsConfiguracoesList**](#communicationsconfiguracoeslist) | **GET** /api/communications/configuracoes/ | Listar configurações|
|[**communicationsConfiguracoesMinhaConfiguracaoRetrieve**](#communicationsconfiguracoesminhaconfiguracaoretrieve) | **GET** /api/communications/configuracoes/minha_configuracao/ | Ver minha configuração|
|[**communicationsConfiguracoesPartialUpdate**](#communicationsconfiguracoespartialupdate) | **PATCH** /api/communications/configuracoes/{id}/ | Atualizar configuração parcialmente|
|[**communicationsConfiguracoesRetrieve**](#communicationsconfiguracoesretrieve) | **GET** /api/communications/configuracoes/{id}/ | Obter detalhes da configuração|
|[**communicationsConfiguracoesUpdate**](#communicationsconfiguracoesupdate) | **PUT** /api/communications/configuracoes/{id}/ | Atualizar configuração|
|[**communicationsMensagensCreate**](#communicationsmensagenscreate) | **POST** /api/communications/mensagens/ | Criar nova mensagem|
|[**communicationsMensagensDestroy**](#communicationsmensagensdestroy) | **DELETE** /api/communications/mensagens/{id}/ | Excluir mensagem|
|[**communicationsMensagensList**](#communicationsmensagenslist) | **GET** /api/communications/mensagens/ | Listar mensagens|
|[**communicationsMensagensMarcarComoLidaCreate**](#communicationsmensagensmarcarcomolidacreate) | **POST** /api/communications/mensagens/{id}/marcar_como_lida/ | Marcar mensagem como lida|
|[**communicationsMensagensMensagensNaoLidasRetrieve**](#communicationsmensagensmensagensnaolidasretrieve) | **GET** /api/communications/mensagens/mensagens_nao_lidas/ | Listar mensagens não lidas|
|[**communicationsMensagensPartialUpdate**](#communicationsmensagenspartialupdate) | **PATCH** /api/communications/mensagens/{id}/ | Atualizar mensagem parcialmente|
|[**communicationsMensagensRetrieve**](#communicationsmensagensretrieve) | **GET** /api/communications/mensagens/{id}/ | Obter detalhes da mensagem|
|[**communicationsMensagensUpdate**](#communicationsmensagensupdate) | **PUT** /api/communications/mensagens/{id}/ | Atualizar mensagem|
|[**communicationsNotificacoesCreate**](#communicationsnotificacoescreate) | **POST** /api/communications/notificacoes/ | Criar nova notificação|
|[**communicationsNotificacoesDestroy**](#communicationsnotificacoesdestroy) | **DELETE** /api/communications/notificacoes/{id}/ | Excluir notificação|
|[**communicationsNotificacoesList**](#communicationsnotificacoeslist) | **GET** /api/communications/notificacoes/ | Listar notificações|
|[**communicationsNotificacoesMarcarComoLidaCreate**](#communicationsnotificacoesmarcarcomolidacreate) | **POST** /api/communications/notificacoes/{id}/marcar_como_lida/ | Marcar notificação como lida|
|[**communicationsNotificacoesMarcarTodasComoLidasCreate**](#communicationsnotificacoesmarcartodascomolidascreate) | **POST** /api/communications/notificacoes/marcar_todas_como_lidas/ | Marcar todas as notificações como lidas|
|[**communicationsNotificacoesNaoLidasRetrieve**](#communicationsnotificacoesnaolidasretrieve) | **GET** /api/communications/notificacoes/nao_lidas/ | Listar notificações não lidas|
|[**communicationsNotificacoesPartialUpdate**](#communicationsnotificacoespartialupdate) | **PATCH** /api/communications/notificacoes/{id}/ | Atualizar notificação parcialmente|
|[**communicationsNotificacoesRetrieve**](#communicationsnotificacoesretrieve) | **GET** /api/communications/notificacoes/{id}/ | Obter detalhes da notificação|
|[**communicationsNotificacoesUpdate**](#communicationsnotificacoesupdate) | **PUT** /api/communications/notificacoes/{id}/ | Atualizar notificação|

# **communicationsConfiguracoesCreate**
> ConfiguracaoNotificacao communicationsConfiguracoesCreate(configuracaoNotificacaoRequest)

Cria um nova configuração.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    ConfiguracaoNotificacaoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let configuracaoNotificacaoRequest: ConfiguracaoNotificacaoRequest; //

const { status, data } = await apiInstance.communicationsConfiguracoesCreate(
    configuracaoNotificacaoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **configuracaoNotificacaoRequest** | **ConfiguracaoNotificacaoRequest**|  | |


### Return type

**ConfiguracaoNotificacao**

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

# **communicationsConfiguracoesDestroy**
> communicationsConfiguracoesDestroy()

Remove uma configuração existente.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Configuração de Notificação. (default to undefined)

const { status, data } = await apiInstance.communicationsConfiguracoesDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Configuração de Notificação. | defaults to undefined|


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

# **communicationsConfiguracoesList**
> PaginatedConfiguracaoNotificacaoList communicationsConfiguracoesList()

Retorna uma lista paginada de configurações.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let page: number; //A page number within the paginated result set. (optional) (default to undefined)

const { status, data } = await apiInstance.communicationsConfiguracoesList(
    page
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|


### Return type

**PaginatedConfiguracaoNotificacaoList**

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

# **communicationsConfiguracoesMinhaConfiguracaoRetrieve**
> ConfiguracaoNotificacao communicationsConfiguracoesMinhaConfiguracaoRetrieve()

Retorna a configuração do usuário atual ou cria uma padrão se não existir.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

const { status, data } = await apiInstance.communicationsConfiguracoesMinhaConfiguracaoRetrieve();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**ConfiguracaoNotificacao**

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

# **communicationsConfiguracoesPartialUpdate**
> ConfiguracaoNotificacao communicationsConfiguracoesPartialUpdate()

Atualiza parcialmente uma configuração existente.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    PatchedConfiguracaoNotificacaoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Configuração de Notificação. (default to undefined)
let patchedConfiguracaoNotificacaoRequest: PatchedConfiguracaoNotificacaoRequest; // (optional)

const { status, data } = await apiInstance.communicationsConfiguracoesPartialUpdate(
    id,
    patchedConfiguracaoNotificacaoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedConfiguracaoNotificacaoRequest** | **PatchedConfiguracaoNotificacaoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Configuração de Notificação. | defaults to undefined|


### Return type

**ConfiguracaoNotificacao**

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

# **communicationsConfiguracoesRetrieve**
> ConfiguracaoNotificacao communicationsConfiguracoesRetrieve()

Retorna informações detalhadas de uma configuração específica.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Configuração de Notificação. (default to undefined)

const { status, data } = await apiInstance.communicationsConfiguracoesRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Configuração de Notificação. | defaults to undefined|


### Return type

**ConfiguracaoNotificacao**

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

# **communicationsConfiguracoesUpdate**
> ConfiguracaoNotificacao communicationsConfiguracoesUpdate(configuracaoNotificacaoRequest)

Atualiza todos os campos de uma configuração existente.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    ConfiguracaoNotificacaoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Configuração de Notificação. (default to undefined)
let configuracaoNotificacaoRequest: ConfiguracaoNotificacaoRequest; //

const { status, data } = await apiInstance.communicationsConfiguracoesUpdate(
    id,
    configuracaoNotificacaoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **configuracaoNotificacaoRequest** | **ConfiguracaoNotificacaoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Configuração de Notificação. | defaults to undefined|


### Return type

**ConfiguracaoNotificacao**

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

# **communicationsMensagensCreate**
> ChatMensagem communicationsMensagensCreate(chatMensagemRequest)

Cria um nova mensagem.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    ChatMensagemRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let chatMensagemRequest: ChatMensagemRequest; //

const { status, data } = await apiInstance.communicationsMensagensCreate(
    chatMensagemRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **chatMensagemRequest** | **ChatMensagemRequest**|  | |


### Return type

**ChatMensagem**

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

# **communicationsMensagensDestroy**
> communicationsMensagensDestroy()

Remove uma mensagem existente.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Mensagem de Chat. (default to undefined)

const { status, data } = await apiInstance.communicationsMensagensDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Mensagem de Chat. | defaults to undefined|


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

# **communicationsMensagensList**
> PaginatedChatMensagemList communicationsMensagensList()

Retorna uma lista paginada de mensagens.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let autor: number; // (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let projeto: number; // (optional) (default to undefined)

const { status, data } = await apiInstance.communicationsMensagensList(
    autor,
    ordering,
    page,
    projeto
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **autor** | [**number**] |  | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **projeto** | [**number**] |  | (optional) defaults to undefined|


### Return type

**PaginatedChatMensagemList**

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

# **communicationsMensagensMarcarComoLidaCreate**
> ConfiguracaoNotificacao communicationsMensagensMarcarComoLidaCreate(chatMensagemRequest)

Marca uma mensagem como lida pelo usuário atual.  Args:     request: Objeto de requisição     pk: ID da mensagem a ser marcada como lida  Returns:     Response: Detalhes do registro de leitura ou mensagem de status

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    ChatMensagemRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Mensagem de Chat. (default to undefined)
let chatMensagemRequest: ChatMensagemRequest; //

const { status, data } = await apiInstance.communicationsMensagensMarcarComoLidaCreate(
    id,
    chatMensagemRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **chatMensagemRequest** | **ChatMensagemRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Mensagem de Chat. | defaults to undefined|


### Return type

**ConfiguracaoNotificacao**

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

# **communicationsMensagensMensagensNaoLidasRetrieve**
> ConfiguracaoNotificacao communicationsMensagensMensagensNaoLidasRetrieve()

Retorna as mensagens não lidas pelo usuário atual.  Suporta filtro por projeto através do parâmetro \'projeto\' na query string. Exclui mensagens enviadas pelo próprio usuário, pois estas não precisam ser lidas.  Args:     request: Objeto de requisição  Returns:     Response: Lista de mensagens não lidas

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

const { status, data } = await apiInstance.communicationsMensagensMensagensNaoLidasRetrieve();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**ConfiguracaoNotificacao**

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

# **communicationsMensagensPartialUpdate**
> ChatMensagem communicationsMensagensPartialUpdate()

Atualiza parcialmente uma mensagem existente.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    PatchedChatMensagemRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Mensagem de Chat. (default to undefined)
let patchedChatMensagemRequest: PatchedChatMensagemRequest; // (optional)

const { status, data } = await apiInstance.communicationsMensagensPartialUpdate(
    id,
    patchedChatMensagemRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedChatMensagemRequest** | **PatchedChatMensagemRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Mensagem de Chat. | defaults to undefined|


### Return type

**ChatMensagem**

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

# **communicationsMensagensRetrieve**
> ChatMensagem communicationsMensagensRetrieve()

Retorna informações detalhadas de uma mensagem específica.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Mensagem de Chat. (default to undefined)

const { status, data } = await apiInstance.communicationsMensagensRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Mensagem de Chat. | defaults to undefined|


### Return type

**ChatMensagem**

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

# **communicationsMensagensUpdate**
> ChatMensagem communicationsMensagensUpdate(chatMensagemRequest)

Atualiza todos os campos de uma mensagem existente.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    ChatMensagemRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Mensagem de Chat. (default to undefined)
let chatMensagemRequest: ChatMensagemRequest; //

const { status, data } = await apiInstance.communicationsMensagensUpdate(
    id,
    chatMensagemRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **chatMensagemRequest** | **ChatMensagemRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Mensagem de Chat. | defaults to undefined|


### Return type

**ChatMensagem**

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

# **communicationsNotificacoesCreate**
> Notificacao communicationsNotificacoesCreate(notificacaoRequest)

Cria um nova notificação.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    NotificacaoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let notificacaoRequest: NotificacaoRequest; //

const { status, data } = await apiInstance.communicationsNotificacoesCreate(
    notificacaoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **notificacaoRequest** | **NotificacaoRequest**|  | |


### Return type

**Notificacao**

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

# **communicationsNotificacoesDestroy**
> communicationsNotificacoesDestroy()

Remove uma notificação existente.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Notificação. (default to undefined)

const { status, data } = await apiInstance.communicationsNotificacoesDestroy(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Notificação. | defaults to undefined|


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

# **communicationsNotificacoesList**
> PaginatedNotificacaoList communicationsNotificacoesList()

Retorna uma lista paginada de notificações.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let lida: boolean; // (optional) (default to undefined)
let ordering: string; //Which field to use when ordering the results. (optional) (default to undefined)
let page: number; //A page number within the paginated result set. (optional) (default to undefined)
let prioridade: 'ALTA' | 'BAIXA' | 'MEDIA'; //Nível de prioridade da notificação  * `BAIXA` - Baixa * `MEDIA` - Média * `ALTA` - Alta (optional) (default to undefined)
let projeto: number; // (optional) (default to undefined)
let tarefa: number; // (optional) (default to undefined)
let tipo: 'DOCUMENTO' | 'EQUIPE' | 'PROJETO' | 'RISCO' | 'SISTEMA' | 'TAREFA'; //Tipo de objeto relacionado à notificação  * `TAREFA` - Tarefa * `PROJETO` - Projeto * `EQUIPE` - Equipe * `RISCO` - Risco * `DOCUMENTO` - Documento * `SISTEMA` - Sistema (optional) (default to undefined)

const { status, data } = await apiInstance.communicationsNotificacoesList(
    lida,
    ordering,
    page,
    prioridade,
    projeto,
    tarefa,
    tipo
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **lida** | [**boolean**] |  | (optional) defaults to undefined|
| **ordering** | [**string**] | Which field to use when ordering the results. | (optional) defaults to undefined|
| **page** | [**number**] | A page number within the paginated result set. | (optional) defaults to undefined|
| **prioridade** | [**&#39;ALTA&#39; | &#39;BAIXA&#39; | &#39;MEDIA&#39;**]**Array<&#39;ALTA&#39; &#124; &#39;BAIXA&#39; &#124; &#39;MEDIA&#39;>** | Nível de prioridade da notificação  * &#x60;BAIXA&#x60; - Baixa * &#x60;MEDIA&#x60; - Média * &#x60;ALTA&#x60; - Alta | (optional) defaults to undefined|
| **projeto** | [**number**] |  | (optional) defaults to undefined|
| **tarefa** | [**number**] |  | (optional) defaults to undefined|
| **tipo** | [**&#39;DOCUMENTO&#39; | &#39;EQUIPE&#39; | &#39;PROJETO&#39; | &#39;RISCO&#39; | &#39;SISTEMA&#39; | &#39;TAREFA&#39;**]**Array<&#39;DOCUMENTO&#39; &#124; &#39;EQUIPE&#39; &#124; &#39;PROJETO&#39; &#124; &#39;RISCO&#39; &#124; &#39;SISTEMA&#39; &#124; &#39;TAREFA&#39;>** | Tipo de objeto relacionado à notificação  * &#x60;TAREFA&#x60; - Tarefa * &#x60;PROJETO&#x60; - Projeto * &#x60;EQUIPE&#x60; - Equipe * &#x60;RISCO&#x60; - Risco * &#x60;DOCUMENTO&#x60; - Documento * &#x60;SISTEMA&#x60; - Sistema | (optional) defaults to undefined|


### Return type

**PaginatedNotificacaoList**

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

# **communicationsNotificacoesMarcarComoLidaCreate**
> ConfiguracaoNotificacao communicationsNotificacoesMarcarComoLidaCreate(notificacaoRequest)

Marca uma notificação como lida.  Define o campo \'lida\' como True e registra a data/hora em \'lida_em\'.  Args:     request: Objeto de requisição     pk: ID da notificação a ser marcada como lida  Returns:     Response: Detalhes da notificação atualizada ou mensagem de status

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    NotificacaoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Notificação. (default to undefined)
let notificacaoRequest: NotificacaoRequest; //

const { status, data } = await apiInstance.communicationsNotificacoesMarcarComoLidaCreate(
    id,
    notificacaoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **notificacaoRequest** | **NotificacaoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Notificação. | defaults to undefined|


### Return type

**ConfiguracaoNotificacao**

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

# **communicationsNotificacoesMarcarTodasComoLidasCreate**
> ConfiguracaoNotificacao communicationsNotificacoesMarcarTodasComoLidasCreate(notificacaoRequest)

Marca todas as notificações não lidas do usuário como lidas.  Atualiza em massa todas as notificações não lidas do usuário atual, definindo \'lida\' como True e \'lida_em\' como a data/hora atual.  Args:     request: Objeto de requisição  Returns:     Response: Mensagem de confirmação com o número de notificações atualizadas

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    NotificacaoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let notificacaoRequest: NotificacaoRequest; //

const { status, data } = await apiInstance.communicationsNotificacoesMarcarTodasComoLidasCreate(
    notificacaoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **notificacaoRequest** | **NotificacaoRequest**|  | |


### Return type

**ConfiguracaoNotificacao**

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

# **communicationsNotificacoesNaoLidasRetrieve**
> ConfiguracaoNotificacao communicationsNotificacoesNaoLidasRetrieve()

Retorna apenas as notificações não lidas do usuário.  Suporta filtros adicionais por tipo e prioridade através de parâmetros na query string.  Args:     request: Objeto de requisição  Returns:     Response: Lista de notificações não lidas filtradas

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

const { status, data } = await apiInstance.communicationsNotificacoesNaoLidasRetrieve();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**ConfiguracaoNotificacao**

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

# **communicationsNotificacoesPartialUpdate**
> Notificacao communicationsNotificacoesPartialUpdate()

Atualiza parcialmente uma notificação existente.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    PatchedNotificacaoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Notificação. (default to undefined)
let patchedNotificacaoRequest: PatchedNotificacaoRequest; // (optional)

const { status, data } = await apiInstance.communicationsNotificacoesPartialUpdate(
    id,
    patchedNotificacaoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedNotificacaoRequest** | **PatchedNotificacaoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Notificação. | defaults to undefined|


### Return type

**Notificacao**

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

# **communicationsNotificacoesRetrieve**
> Notificacao communicationsNotificacoesRetrieve()

Retorna informações detalhadas de uma notificação específica.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Notificação. (default to undefined)

const { status, data } = await apiInstance.communicationsNotificacoesRetrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**number**] | A unique integer value identifying this Notificação. | defaults to undefined|


### Return type

**Notificacao**

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

# **communicationsNotificacoesUpdate**
> Notificacao communicationsNotificacoesUpdate(notificacaoRequest)

Atualiza todos os campos de uma notificação existente.

### Example

```typescript
import {
    ComunicaoApi,
    Configuration,
    NotificacaoRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ComunicaoApi(configuration);

let id: number; //A unique integer value identifying this Notificação. (default to undefined)
let notificacaoRequest: NotificacaoRequest; //

const { status, data } = await apiInstance.communicationsNotificacoesUpdate(
    id,
    notificacaoRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **notificacaoRequest** | **NotificacaoRequest**|  | |
| **id** | [**number**] | A unique integer value identifying this Notificação. | defaults to undefined|


### Return type

**Notificacao**

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

